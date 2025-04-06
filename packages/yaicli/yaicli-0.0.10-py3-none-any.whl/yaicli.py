import configparser
import json
import platform
import subprocess
from os import getenv
from os.path import basename, pathsep
from pathlib import Path
from typing import Annotated, Optional

import jmespath
import requests
import typer
from distro import name as distro_name
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.keys import Keys
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.prompt import Confirm

SHELL_PROMPT = """Your are a Shell Command Generator.
Generate a command EXCLUSIVELY for {_os} OS with {_shell} shell.
Rules:
1. Use ONLY {_shell}-specific syntax and connectors (&&, ||, |, etc)
2. Output STRICTLY in plain text format
3. NEVER use markdown, code blocks or explanations
4. Chain multi-step commands in SINGLE LINE
5. Return NOTHING except the ready-to-run command"""

DEFAULT_PROMPT = (
    "You are YAICLI, a system management and programing assistant, "
    "You are managing {_os} operating system with {_shell} shell. "
    "Your responses should be concise and use Markdown format, "
    "unless the user explicitly requests more details."
)

CMD_CLEAR = "/clear"
CMD_EXIT = "/exit"

EXEC_MODE = "exec"
CHAT_MODE = "chat"
TEMP_MODE = "temp"

DEFAULT_CONFIG_MAP = {
    "BASE_URL": {"value": "https://api.openai.com/v1", "env_key": "AI_BASE_URL"},
    "API_KEY": {"value": "", "env_key": "AI_API_KEY"},
    "MODEL": {"value": "gpt-4o", "env_key": "AI_MODEL"},
    "SHELL_NAME": {"value": "auto", "env_key": "AI_SHELL_NAME"},
    "OS_NAME": {"value": "auto", "env_key": "AI_OS_NAME"},
    "COMPLETION_PATH": {"value": "chat/completions", "env_key": "AI_COMPLETION_PATH"},
    "ANSWER_PATH": {"value": "choices[0].message.content", "env_key": "AI_ANSWER_PATH"},
    "STREAM": {"value": "true", "env_key": "AI_STREAM"},
}

app = typer.Typer(
    name="yaicli",
    context_settings={"help_option_names": ["-h", "--help"]},
    pretty_exceptions_enable=False,
)


class CasePreservingConfigParser(configparser.RawConfigParser):
    """Case preserving config parser"""

    def optionxform(self, optionstr):
        return optionstr


class CLI:
    CONFIG_PATH = Path("~/.config/yaicli/config.ini").expanduser()
    DEFAULT_CONFIG_INI = """[core]
PROVIDER=openai
BASE_URL=https://api.openai.com/v1
API_KEY=
MODEL=gpt-4o

# auto detect shell and os
SHELL_NAME=auto
OS_NAME=auto

# if you want to use custom completions path, you can set it here
COMPLETION_PATH=/chat/completions
# if you want to use custom answer path, you can set it here
ANSWER_PATH=choices[0].message.content

# true: streaming response
# false: non-streaming response
STREAM=true"""

    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose
        self.console = Console()
        self.bindings = KeyBindings()
        self.session = PromptSession(key_bindings=self.bindings)
        self.config = {}
        self.history = []
        self.max_history_length = 25
        self.current_mode = TEMP_MODE

    def _setup_key_bindings(self) -> None:
        """Setup keyboard shortcuts"""

        @self.bindings.add(Keys.ControlI)  # Bind TAB to switch modes
        def _(event: KeyPressEvent) -> None:
            self.current_mode = EXEC_MODE if self.current_mode == CHAT_MODE else CHAT_MODE

    def load_config(self) -> dict[str, str]:
        """Load LLM API configuration with priority:
        1. Environment variables (highest priority)
        2. Configuration file
        3. Default values (lowest priority)

        Returns:
            dict: merged configuration
        """
        # Start with default configuration (lowest priority)
        merged_config = {k: v["value"] for k, v in DEFAULT_CONFIG_MAP.items()}

        # Create default config file if it doesn't exist
        if not self.CONFIG_PATH.exists():
            self.console.print("[bold yellow]Creating default configuration file.[/bold yellow]")
            self.CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(self.CONFIG_PATH, "w") as f:
                f.write(self.DEFAULT_CONFIG_INI)
        else:
            # Load from configuration file (middle priority)
            config_parser = CasePreservingConfigParser()
            config_parser.read(self.CONFIG_PATH)
            if "core" in config_parser:
                # Update with non-empty values from config file
                merged_config.update({k: v for k, v in config_parser["core"].items() if v.strip()})

        # Override with environment variables (highest priority)
        for key, config in DEFAULT_CONFIG_MAP.items():
            env_value = getenv(config["env_key"])
            if env_value is not None:
                merged_config[key] = env_value

        merged_config["STREAM"] = str(merged_config.get("STREAM", "true")).lower()

        self.config = merged_config
        return merged_config

    def detect_os(self) -> str:
        """Detect operating system + version"""
        if self.config.get("OS_NAME") != "auto":
            return self.config["OS_NAME"]
        current_platform = platform.system()
        if current_platform == "Linux":
            return "Linux/" + distro_name(pretty=True)
        if current_platform == "Windows":
            return "Windows " + platform.release()
        if current_platform == "Darwin":
            return "Darwin/MacOS " + platform.mac_ver()[0]
        return current_platform

    def detect_shell(self) -> str:
        """Detect shell name"""
        if self.config["SHELL_NAME"] != "auto":
            return self.config["SHELL_NAME"]

        current_platform = platform.system()
        if current_platform in ("Windows", "nt"):
            is_powershell = len(getenv("PSModulePath", "").split(pathsep)) >= 3
            return "powershell.exe" if is_powershell else "cmd.exe"
        return basename(getenv("SHELL", "/bin/sh"))

    def _filter_command(self, command: str) -> Optional[str]:
        """Filter out unwanted characters from command

        The LLM may return commands in markdown format with code blocks.
        This method removes markdown formatting from the command.
        It handles various formats including:
        - Commands surrounded by ``` (plain code blocks)
        - Commands with language specifiers like ```bash, ```zsh, etc.
        - Commands with specific examples like ```ls -al```

        example:
        ```bash\nls -la\n``` ==> ls -al
        ```zsh\nls -la\n``` ==> ls -al
        ```ls -al``` ==> ls -al
        ls -al ==> ls -al
        ```\ncd /tmp\nls -la\n``` ==> cd /tmp\nls -la
        ```bash\ncd /tmp\nls -la\n``` ==> cd /tmp\nls -la
        """
        if not command or not command.strip():
            return ""

        # Handle commands that are already without code blocks
        if "```" not in command:
            return command.strip()

        # Handle code blocks with or without language specifiers
        lines = command.strip().split("\n")

        # Check if it's a single-line code block like ```ls -al```
        if len(lines) == 1 and lines[0].startswith("```") and lines[0].endswith("```"):
            return lines[0][3:-3].strip()

        # Handle multi-line code blocks
        if lines[0].startswith("```"):
            # Remove the opening ``` line (with or without language specifier)
            content_lines = lines[1:]

            # If the last line is a closing ```, remove it
            if content_lines and content_lines[-1].strip() == "```":
                content_lines = content_lines[:-1]

            # Join the remaining lines and strip any extra whitespace
            return "\n".join(line.strip() for line in content_lines if line.strip())

    def post(self, message: list[dict[str, str]]) -> requests.Response:
        """Post message to LLM API and return response"""
        url = self.config.get("BASE_URL", "").rstrip("/") + "/" + self.config.get("COMPLETION_PATH", "").lstrip("/")
        body = {
            "messages": message,
            "model": self.config.get("MODEL", "gpt-4o"),
            "stream": self.config.get("STREAM", "true") == "true",
            "temperature": 0.7,
            "top_p": 1,
        }
        response = requests.post(url, json=body, headers={"Authorization": f"Bearer {self.config.get('API_KEY', '')}"})
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.console.print(f"[red]Error calling API: {e}[/red]")
            if self.verbose:
                self.console.print(f"Reason: {e.response.reason}")
                self.console.print(f"Response: {response.text}")
            raise typer.Exit(code=1) from None
        return response

    def get_reasoning_content(self, delta: dict) -> Optional[str]:
        # reasoning: openrouter
        # reasoning_content: infi-ai/deepseek
        for k in ("reasoning_content", "reasoning"):
            if k in delta:
                return delta[k]
        return None

    def _print_stream(self, response: requests.Response) -> str:
        """Print response from LLM in streaming mode"""
        full_completion = ""
        in_reasoning = False

        with Live() as live:
            for line in response.iter_lines():
                if not line:
                    continue

                data = line.decode("utf-8")
                if not data.startswith("data: "):
                    continue

                data = data[6:]
                if data == "[DONE]":
                    break

                try:
                    json_data = json.loads(data)
                    if not json_data.get("choices"):
                        continue

                    delta = json_data["choices"][0]["delta"]
                    reason = self.get_reasoning_content(delta)

                    if reason is not None:
                        # reasoning started
                        if not in_reasoning:
                            in_reasoning = True
                            full_completion = "> Reasoning:\n> "
                        full_completion += reason.replace("\n", "\n> ")
                    else:
                        # reasoning stoped
                        if in_reasoning:
                            in_reasoning = False
                            full_completion += "\n\n"
                        content = delta.get("content", "") or ""
                        full_completion += content
                    live.update(Markdown(markup=full_completion), refresh=True)
                except json.JSONDecodeError:
                    self.console.print("[red]Error decoding response JSON[/red]")
                    if self.verbose:
                        self.console.print(f"[red]Error: {data}[/red]")

        return full_completion

    def _print_non_stream(self, response: requests.Response) -> str:
        """Print response from LLM in non-streaming mode"""
        full_completion = jmespath.search(self.config.get("ANSWER_PATH", "choices[0].message.content"), response.json())
        self.console.print(Markdown(full_completion))
        return full_completion

    def _print(self, response: requests.Response, stream: bool = True) -> str:
        """Print response from LLM and return full completion"""
        if stream:
            # Streaming response
            full_completion = self._print_stream(response)
        else:
            # Non-streaming response
            full_completion = self._print_non_stream(response)
        self.console.print()  # Add a newline after the response to separate from the next input
        return full_completion

    def get_prompt_tokens(self) -> list[tuple[str, str]]:
        """Return prompt tokens for current mode"""
        if self.current_mode == CHAT_MODE:
            qmark = "💬"
        elif self.current_mode == EXEC_MODE:
            qmark = "🚀"
        else:
            qmark = ""
        return [("class:qmark", qmark), ("class:question", " {} ".format(">"))]

    def _check_history_len(self) -> None:
        """Check history length and remove oldest messages if necessary"""
        if len(self.history) > self.max_history_length:
            self.history = self.history[-self.max_history_length :]

    def _run_repl(self) -> None:
        """Run REPL loop, handling user input and generating responses, saving history, and executing commands"""
        # Show REPL instructions
        self._setup_key_bindings()
        self.console.print("""
██    ██  █████  ██  ██████ ██      ██
 ██  ██  ██   ██ ██ ██      ██      ██
  ████   ███████ ██ ██      ██      ██
   ██    ██   ██ ██ ██      ██      ██
   ██    ██   ██ ██  ██████ ███████ ██
""")
        self.console.print("[bold]Press TAB to change in chat and exec mode[/bold]")
        self.console.print("[bold]Type /clear to clear chat history[/bold]")
        self.console.print("[bold]Type /his to see chat history[/bold]")
        self.console.print("[bold]Press Ctrl+C or type /exit to exit[/bold]\n")

        while True:
            # Get user input
            user_input = self.session.prompt(self.get_prompt_tokens).strip()
            if not user_input:
                continue

            # Handle exit commands
            if user_input.lower() == CMD_EXIT:
                break

            # Handle clear command
            if user_input.lower() == CMD_CLEAR and self.current_mode == CHAT_MODE:
                self.history = []
                self.console.print("[bold yellow]Chat history cleared[/bold yellow]\n")
                continue
            elif user_input.lower() == "/his":
                self.console.print(self.history)
                continue
            # Create appropriate system prompt based on mode
            system_prompt = SHELL_PROMPT if self.current_mode == EXEC_MODE else DEFAULT_PROMPT
            system_content = system_prompt.format(_os=self.detect_os(), _shell=self.detect_shell())

            # Create message with system prompt and history
            message = [{"role": "system", "content": system_content}]
            message.extend(self.history)

            # Add current user message
            message.append({"role": "user", "content": user_input})

            # Get response from LLM
            response = self.post(message)
            self.console.print("\n[bold green]Assistant:[/bold green]")
            try:
                content = self._print(response, stream=self.config["STREAM"] == "true")
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
                continue

            # Add user input and assistant response to history
            self.history.append({"role": "user", "content": user_input})
            self.history.append({"role": "assistant", "content": content})

            # Trim history if needed
            self._check_history_len()

            # Handle command execution in exec mode
            if self.current_mode == EXEC_MODE:
                content = self._filter_command(content)
                if not content:
                    self.console.print("[bold red]No command generated[/bold red]")
                    continue
                self.console.print(f"\n[bold magenta]Generated command:[/bold magenta] {content}")
                if Confirm.ask("Execute this command?", default=False):
                    subprocess.call(content, shell=True)

        self.console.print("[bold green]Exiting...[/bold green]")

    def _run_once(self, prompt: str, shell: bool = False) -> None:
        """Run once with given prompt"""
        _os = self.detect_os()
        _shell = self.detect_shell()
        # Create appropriate system prompt based on mode
        system_prompt = SHELL_PROMPT if shell else DEFAULT_PROMPT
        system_content = system_prompt.format(_os=_os, _shell=_shell)

        # Create message with system prompt and user input
        message = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt},
        ]

        # Get response from LLM
        response = self.post(message)
        self.console.print("\n[bold green]Assistant:[/bold green]")
        content = self._print(response, stream=self.config["STREAM"] == "true")

        # Handle shell mode execution
        if shell:
            content = self._filter_command(content)
            if not content:
                self.console.print("[bold red]No command generated[/bold red]")
                return
            self.console.print(f"\n[bold magenta]Generated command:[/bold magenta] {content}")
            if Confirm.ask("Execute this command?", default=False):
                returncode = subprocess.call(content, shell=True)
                if returncode != 0:
                    self.console.print(f"[bold red]Command failed with return code {returncode}[/bold red]")


    def run(self, chat: bool, shell: bool, prompt: str) -> None:
        """Run the CLI"""
        self.load_config()
        if not self.config.get("API_KEY"):
            self.console.print("[bold red]API key not set[/bold red]")
            self.console.print(
                "[bold red]Please set API key in ~/.config/yaicli/config.ini or environment variable[/bold red]"
            )
            raise typer.Exit(code=1)

        # Handle chat mode
        if chat:
            self.current_mode = CHAT_MODE
            self._run_repl()
        else:
            self._run_once(prompt, shell)


@app.command()
def main(
    ctx: typer.Context,
    prompt: Annotated[Optional[str], typer.Argument(show_default=False, help="The prompt send to the LLM")] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-V", help="Show verbose information")] = False,
    chat: Annotated[bool, typer.Option("--chat", "-c", help="Start in chat mode")] = False,
    shell: Annotated[bool, typer.Option("--shell", "-s", help="Generate and execute shell command")] = False,
):
    """yaicli - Your AI interface in cli."""
    if prompt == "":
        typer.echo("Empty prompt, ignored")
        return
    if not prompt and not chat:
        typer.echo(ctx.get_help())
        return

    cli = CLI(verbose=verbose)
    cli.run(chat=chat, shell=shell, prompt=prompt or "")


if __name__ == "__main__":
    app()
