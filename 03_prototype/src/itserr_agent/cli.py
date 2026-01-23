"""
CLI interface for the ITSERR Agent.

Provides a command-line interface for interacting with the agent,
useful for testing and demonstration.
"""

import asyncio

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from itserr_agent import __version__

app = typer.Typer(
    name="itserr-agent",
    help="Ethically-grounded AI agent for religious studies research",
    add_completion=False,
)
console = Console()


@app.command()
def version() -> None:
    """Show the version."""
    console.print(f"ITSERR Agent v{__version__}")


@app.command()
def chat(
    session_id: str = typer.Option(
        "default",
        "--session",
        "-s",
        help="Session identifier for memory isolation",
    ),
    model: str = typer.Option(
        None,
        "--model",
        "-m",
        help="Override the LLM model",
    ),
) -> None:
    """
    Start an interactive chat session with the agent.

    The agent maintains context across the session and uses
    epistemic indicators to differentiate response types.
    """
    console.print(
        Panel(
            "[bold blue]ITSERR Agent[/bold blue]\n"
            "An ethically-grounded AI assistant for religious studies research.\n\n"
            "Epistemic indicators:\n"
            "  [green][FACTUAL][/green] - Verifiable information\n"
            "  [yellow][INTERPRETIVE][/yellow] - AI analysis (verify)\n"
            "  [red][DEFERRED][/red] - Human judgment required\n\n"
            "Type 'quit' or 'exit' to end the session.",
            title="Welcome",
        )
    )

    asyncio.run(_chat_loop(session_id, model))


async def _chat_loop(session_id: str, model: str | None) -> None:
    """Run the interactive chat loop."""
    from itserr_agent import AgentConfig, ITSERRAgent

    # Load configuration
    config = AgentConfig()
    if model:
        config.llm_model = model

    # Initialize agent to None for proper cleanup in finally block
    agent: ITSERRAgent | None = None

    try:
        agent = ITSERRAgent(config)
        console.print(f"\n[dim]Session: {session_id}[/dim]\n")

        while True:
            try:
                user_input = Prompt.ask("[bold]You[/bold]")

                if user_input.lower() in ("quit", "exit", "q"):
                    break

                if not user_input.strip():
                    continue

                # Process the input
                with console.status("[dim]Thinking...[/dim]"):
                    response = await agent.process(user_input, session_id=session_id)

                # Display the response with markdown formatting
                console.print()
                console.print(Panel(Markdown(response.content), title="[bold]Agent[/bold]"))
                console.print()

            except KeyboardInterrupt:
                break

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)

    finally:
        if agent is not None:
            await agent.close()

    console.print("\n[dim]Session ended. Memory has been preserved.[/dim]")


@app.command()
def config() -> None:
    """Show current configuration."""
    from itserr_agent import AgentConfig

    cfg = AgentConfig()

    console.print(Panel("[bold]Current Configuration[/bold]"))
    console.print(f"  LLM Provider: {cfg.llm_provider.value}")
    console.print(f"  LLM Model: {cfg.llm_model}")
    console.print(f"  Embedding Provider: {cfg.embedding_provider.value}")
    console.print(f"  Memory Path: {cfg.memory_persist_path}")
    console.print(f"  GNORM URL: {cfg.gnorm_api_url or 'Not configured'}")


@app.command()
def demo(
    live: bool = typer.Option(
        False,
        "--live",
        "-l",
        help="Use live API calls (requires configured API key)",
    ),
) -> None:
    """
    Run an interactive demonstration of the ITSERR Agent.

    The demo showcases the three core innovations:
    - Narrative Memory System
    - Epistemic Modesty Indicators
    - Human-Centered Tool Patterns

    By default, runs in mock mode (no API key needed).
    Use --live to enable actual LLM calls.
    """
    from itserr_agent.demo import run_demo

    asyncio.run(run_demo(live_mode=live))


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
