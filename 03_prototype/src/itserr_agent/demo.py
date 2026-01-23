"""
Demonstration script for the ITSERR Agent.

This module provides interactive demonstrations of the three core innovations:
1. Narrative Memory System - Preserves research journey across sessions
2. Epistemic Modesty Indicators - Differentiates response types
3. Human-Centered Tool Patterns - Maintains researcher agency

Run with: python -m itserr_agent.demo
Or via CLI: itserr-agent demo
"""

import asyncio
from dataclasses import dataclass
from typing import Any

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text

console = Console()


@dataclass
class DemoScenario:
    """A demonstration scenario with queries and expected behaviors."""

    name: str
    description: str
    queries: list[str]
    expected_features: list[str]


# Predefined demonstration scenarios
DEMO_SCENARIOS = [
    DemoScenario(
        name="Theological Research Session",
        description="Explore Paul's concept of justification in Romans",
        queries=[
            "I'm researching Paul's concept of justification in Romans. What are the key Greek terms?",
            "How does the New Perspective on Paul differ from traditional Protestant readings?",
            "What should I believe about justification?",
        ],
        expected_features=[
            "[FACTUAL] for Greek terms and publication dates",
            "[INTERPRETIVE] for scholarly comparisons",
            "[DEFERRED] for theological truth claims",
        ],
    ),
    DemoScenario(
        name="Hermeneutical Exploration",
        description="Investigate Gadamer's philosophical hermeneutics",
        queries=[
            "When did Gadamer publish Truth and Method?",
            "How does Gadamer's concept of the hermeneutical circle relate to Heidegger?",
            "Is Gadamer's approach compatible with objective textual meaning?",
        ],
        expected_features=[
            "[FACTUAL] for publication date (1960)",
            "[INTERPRETIVE] for philosophical connections",
            "[DEFERRED] for evaluative questions",
        ],
    ),
    DemoScenario(
        name="Memory Continuity Demo",
        description="Demonstrate narrative memory across exchanges",
        queries=[
            "I'm interested in Emmanuel Mounier's personalist philosophy.",
            "How does this connect to my research interests?",
            "Can you summarize what we've discussed?",
        ],
        expected_features=[
            "Memory retrieval from previous exchanges",
            "Context-aware responses referencing earlier discussion",
            "Session summary generation",
        ],
    ),
]


def display_welcome() -> None:
    """Display the welcome banner and introduction."""
    console.print()
    console.print(
        Panel(
            Text.from_markup(
                "[bold blue]ITSERR Agent Demonstration[/bold blue]\n\n"
                "This demonstration showcases the three core innovations of the\n"
                "Ethically-Grounded AI Agent for Religious Studies Research:\n\n"
                "[bold cyan]1. Narrative Memory System[/bold cyan]\n"
                "   Preserves your hermeneutical journey across sessions through\n"
                "   three memory streams: Conversation, Research, and Decision.\n\n"
                "[bold cyan]2. Epistemic Modesty Indicators[/bold cyan]\n"
                "   Clearly differentiates response types:\n"
                "   [green][FACTUAL][/green] - Verifiable information with citations\n"
                "   [yellow][INTERPRETIVE][/yellow] - AI analysis requiring verification\n"
                "   [red][DEFERRED][/red] - Matters requiring human judgment\n\n"
                "[bold cyan]3. Human-Centered Tool Patterns[/bold cyan]\n"
                "   Maintains researcher agency through transparent, confirmable\n"
                "   tool invocations with appropriate confirmation gates."
            ),
            title="[bold]Welcome to the ITSERR Agent Demo[/bold]",
            border_style="blue",
        )
    )
    console.print()


def display_scenario_menu() -> int:
    """Display the scenario selection menu."""
    table = Table(title="Available Demo Scenarios", show_header=True)
    table.add_column("#", style="cyan", width=3)
    table.add_column("Scenario", style="bold")
    table.add_column("Description")

    for i, scenario in enumerate(DEMO_SCENARIOS, 1):
        table.add_row(str(i), scenario.name, scenario.description)

    table.add_row("4", "Custom Session", "Start your own interactive session")
    table.add_row("0", "Exit", "Exit the demonstration")

    console.print(table)
    console.print()

    choice = Prompt.ask(
        "Select a scenario",
        choices=["0", "1", "2", "3", "4"],
        default="1",
    )
    return int(choice)


def display_expected_features(scenario: DemoScenario) -> None:
    """Display the expected features for a scenario."""
    console.print()
    console.print(
        Panel(
            "\n".join(f"  • {feature}" for feature in scenario.expected_features),
            title=f"[bold]Expected Features: {scenario.name}[/bold]",
            border_style="dim",
        )
    )
    console.print()


async def run_scenario(scenario: DemoScenario, mock_mode: bool = True) -> None:
    """Run a demonstration scenario."""
    display_expected_features(scenario)

    if mock_mode:
        await run_mock_scenario(scenario)
    else:
        await run_live_scenario(scenario)


async def run_mock_scenario(scenario: DemoScenario) -> None:
    """Run a scenario with mock responses (no API needed)."""
    console.print(
        "[dim]Running in demonstration mode (mock responses)[/dim]\n"
    )

    mock_responses = get_mock_responses(scenario.name)

    for i, query in enumerate(scenario.queries):
        # Display user query
        console.print(f"[bold cyan]You:[/bold cyan] {query}")
        console.print()

        # Simulate processing
        with Progress(
            SpinnerColumn(),
            TextColumn("[dim]Processing...[/dim]"),
            transient=True,
        ) as progress:
            progress.add_task("", total=None)
            await asyncio.sleep(1.5)  # Simulate thinking time

        # Display response
        response = mock_responses[i] if i < len(mock_responses) else "[INTERPRETIVE] Response not available."
        console.print(
            Panel(
                Markdown(response),
                title="[bold blue]Agent[/bold blue]",
                border_style="blue",
            )
        )
        console.print()

        # Pause between queries
        if i < len(scenario.queries) - 1:
            if not Confirm.ask("Continue to next query?", default=True):
                break
            console.print()


async def run_live_scenario(scenario: DemoScenario) -> None:
    """Run a scenario with the actual agent (requires API key)."""
    from itserr_agent import AgentConfig, ITSERRAgent

    config = AgentConfig()
    session_id = f"demo-{scenario.name.lower().replace(' ', '-')}"

    try:
        config.validate_api_keys()
    except ValueError as e:
        console.print(f"[red]Configuration Error: {e}[/red]")
        console.print("[dim]Running in mock mode instead.[/dim]")
        await run_mock_scenario(scenario)
        return

    agent = ITSERRAgent(config)

    try:
        console.print(f"[dim]Session: {session_id}[/dim]\n")

        for i, query in enumerate(scenario.queries):
            console.print(f"[bold cyan]You:[/bold cyan] {query}")
            console.print()

            with Progress(
                SpinnerColumn(),
                TextColumn("[dim]Processing...[/dim]"),
                transient=True,
            ) as progress:
                progress.add_task("", total=None)
                response = await agent.process(query, session_id=session_id)

            console.print(
                Panel(
                    Markdown(response.content),
                    title="[bold blue]Agent[/bold blue]",
                    border_style="blue",
                )
            )
            console.print()

            if i < len(scenario.queries) - 1:
                if not Confirm.ask("Continue to next query?", default=True):
                    break
                console.print()

        # Show session summary
        console.print("\n[bold]Session Summary:[/bold]")
        summary = await agent._memory.get_session_summary(session_id)
        if summary:
            console.print(Panel(Markdown(summary), border_style="dim"))

    finally:
        await agent.close()


async def run_custom_session(mock_mode: bool = True) -> None:
    """Run a custom interactive session."""
    console.print(
        Panel(
            "You can now interact freely with the agent.\n"
            "Type 'quit' to exit, 'summary' to see session summary.",
            title="[bold]Custom Session[/bold]",
        )
    )
    console.print()

    if mock_mode:
        await run_mock_custom_session()
    else:
        await run_live_custom_session()


async def run_mock_custom_session() -> None:
    """Run a mock custom session for demonstration."""
    console.print("[dim]Running in demonstration mode (mock responses)[/dim]\n")

    exchange_count = 0
    while True:
        user_input = Prompt.ask("[bold cyan]You[/bold cyan]")

        if user_input.lower() in ("quit", "exit", "q"):
            break

        if user_input.lower() == "summary":
            console.print(
                Panel(
                    f"## Session Summary\n\n"
                    f"**Exchanges:** {exchange_count}\n\n"
                    f"This mock session demonstrates the ITSERR Agent interface.\n"
                    f"In a live session, the summary would include:\n"
                    f"- Memory statistics by stream type\n"
                    f"- Research questions explored\n"
                    f"- Reflection summaries",
                    title="[bold]Session Summary[/bold]",
                    border_style="dim",
                )
            )
            continue

        if not user_input.strip():
            continue

        exchange_count += 1

        with Progress(
            SpinnerColumn(),
            TextColumn("[dim]Processing...[/dim]"),
            transient=True,
        ) as progress:
            progress.add_task("", total=None)
            await asyncio.sleep(1.0)

        # Generate contextual mock response
        response = generate_contextual_mock_response(user_input)
        console.print()
        console.print(
            Panel(
                Markdown(response),
                title="[bold blue]Agent[/bold blue]",
                border_style="blue",
            )
        )
        console.print()


async def run_live_custom_session() -> None:
    """Run a live custom session with the actual agent."""
    from itserr_agent import AgentConfig, ITSERRAgent

    config = AgentConfig()
    session_id = "demo-custom"

    try:
        config.validate_api_keys()
    except ValueError as e:
        console.print(f"[red]Configuration Error: {e}[/red]")
        console.print("[dim]Running in mock mode instead.[/dim]")
        await run_mock_custom_session()
        return

    agent = ITSERRAgent(config)

    try:
        console.print(f"[dim]Session: {session_id}[/dim]\n")

        while True:
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]")

            if user_input.lower() in ("quit", "exit", "q"):
                break

            if user_input.lower() == "summary":
                summary = await agent._memory.get_session_summary(session_id)
                if summary:
                    console.print(Panel(Markdown(summary), title="[bold]Session Summary[/bold]"))
                else:
                    console.print("[dim]No session data yet.[/dim]")
                continue

            if not user_input.strip():
                continue

            with Progress(
                SpinnerColumn(),
                TextColumn("[dim]Processing...[/dim]"),
                transient=True,
            ) as progress:
                progress.add_task("", total=None)
                response = await agent.process(user_input, session_id=session_id)

            console.print()
            console.print(
                Panel(
                    Markdown(response.content),
                    title="[bold blue]Agent[/bold blue]",
                    border_style="blue",
                )
            )
            console.print()

    finally:
        await agent.close()

    console.print("\n[dim]Session ended. Memory has been preserved.[/dim]")


def generate_contextual_mock_response(user_input: str) -> str:
    """Generate a contextually appropriate mock response."""
    lower_input = user_input.lower()

    # Check for theological/philosophical keywords
    if any(word in lower_input for word in ["justify", "justification", "paul", "romans"]):
        return (
            "[FACTUAL] The Greek term *δικαιοσύνη* (dikaiosyne) appears 58 times in "
            "Paul's letters, with the highest concentration in Romans.\n\n"
            "[INTERPRETIVE] Your question touches on a central debate in Pauline studies. "
            "The traditional Protestant reading emphasizes forensic justification, while "
            "the 'New Perspective' (Sanders, Dunn, Wright) emphasizes covenant membership.\n\n"
            "[DEFERRED] Which reading more faithfully represents Paul's intention is a "
            "matter requiring your own engagement with the texts and scholarly literature."
        )

    if any(word in lower_input for word in ["gadamer", "hermeneutic", "interpretation"]):
        return (
            "[FACTUAL] Hans-Georg Gadamer published *Truth and Method* (Wahrheit und Methode) "
            "in 1960. The work is considered foundational to philosophical hermeneutics.\n\n"
            "[INTERPRETIVE] Gadamer's concept of the 'hermeneutical circle' builds on "
            "Heidegger's earlier work but shifts focus to the productive role of tradition "
            "and prejudice (Vorurteil) in understanding.\n\n"
            "[DEFERRED] Whether Gadamer's approach is compatible with claims of objective "
            "textual meaning remains a contested philosophical question."
        )

    if any(word in lower_input for word in ["mounier", "personalist", "person"]):
        return (
            "[FACTUAL] Emmanuel Mounier (1905-1950) founded the personalist movement "
            "and the journal *Esprit* in 1932.\n\n"
            "[INTERPRETIVE] Personalist philosophy emphasizes the irreducible dignity "
            "of the human person, distinguishing 'person' from 'individual.' This framework "
            "is particularly relevant to AI ethics, as it grounds human agency in "
            "ontological rather than merely functional terms.\n\n"
            "[DEFERRED] How personalist principles should be applied to AI design "
            "involves value judgments that require human deliberation."
        )

    # Default response
    return (
        "[INTERPRETIVE] Thank you for your question. In a live session, the agent would:\n\n"
        "1. Retrieve relevant context from your research history\n"
        "2. Generate a response using the configured LLM\n"
        "3. Apply epistemic classification to differentiate claim types\n"
        "4. Store this exchange in the narrative memory system\n\n"
        "[DEFERRED] For interpretive or evaluative aspects of your question, "
        "the agent would defer to your judgment as the researcher."
    )


def get_mock_responses(scenario_name: str) -> list[str]:
    """Get predefined mock responses for a scenario."""
    responses: dict[str, list[str]] = {
        "Theological Research Session": [
            # Response to Greek terms question
            (
                "[FACTUAL] The key Greek terms in Paul's discussion of justification include:\n\n"
                "- **δικαιοσύνη** (dikaiosyne) - 'righteousness/justification' - appears 58 times in Paul\n"
                "- **δικαιόω** (dikaioō) - 'to justify/declare righteous' - 27 times in Paul\n"
                "- **πίστις** (pistis) - 'faith/faithfulness' - 142 times in Paul\n"
                "- **χάρις** (charis) - 'grace' - 100 times in Paul\n\n"
                "[INTERPRETIVE] The semantic range of these terms is contested among scholars. "
                "For instance, *dikaiosyne theou* ('righteousness of God') in Romans 1:17 has been "
                "interpreted as both a divine attribute and a gift to believers."
            ),
            # Response to New Perspective question
            (
                "[FACTUAL] The 'New Perspective on Paul' emerged from E.P. Sanders' 1977 work "
                "*Paul and Palestinian Judaism*, followed by James D.G. Dunn's coining of the term "
                "in 1983, and N.T. Wright's extensive contributions.\n\n"
                "[INTERPRETIVE] Key differences include:\n\n"
                "| Aspect | Traditional View | New Perspective |\n"
                "|--------|------------------|------------------|\n"
                "| 'Works of law' | Moral achievement | Ethnic boundary markers |\n"
                "| Justification | Individual salvation | Covenant membership |\n"
                "| Judaism | Legalistic religion | Covenantal nomism |\n\n"
                "The debate continues, with scholars like John Piper defending traditional readings."
            ),
            # Response to belief question
            (
                "[DEFERRED] What you should believe about justification is fundamentally a matter "
                "for your own theological reflection, informed by:\n\n"
                "- Your engagement with the primary texts (Romans, Galatians)\n"
                "- Your interpretive tradition and community\n"
                "- Your broader theological commitments\n"
                "- Prayer and spiritual discernment\n\n"
                "[INTERPRETIVE] I can help you explore the evidence and arguments on various sides, "
                "but the AI cannot and should not determine theological truth claims for you. "
                "This represents an appropriate boundary for AI assistance in religious studies."
            ),
        ],
        "Hermeneutical Exploration": [
            # Publication date
            (
                "[FACTUAL] Hans-Georg Gadamer published *Wahrheit und Methode* (Truth and Method) "
                "in 1960, in Tübingen, Germany. The first English translation appeared in 1975, "
                "with a revised edition in 1989 translated by Joel Weinsheimer and Donald G. Marshall.\n\n"
                "[FACTUAL] Gadamer (1900-2002) was a student of Heidegger and succeeded him at Freiburg."
            ),
            # Relation to Heidegger
            (
                "[FACTUAL] Gadamer studied with Heidegger in Marburg in the 1920s and was deeply "
                "influenced by Heidegger's analysis of understanding in *Being and Time* (1927).\n\n"
                "[INTERPRETIVE] Key connections include:\n\n"
                "- **Fore-structure of understanding**: Gadamer develops Heidegger's notion that "
                "interpretation always proceeds from prior understanding (Vorverständnis)\n"
                "- **Hermeneutical circle**: Both emphasize the part-whole dialectic, but Gadamer "
                "focuses on the productive role of tradition rather than existential disclosure\n"
                "- **Critique of method**: Both resist the dominance of natural-scientific method, "
                "but Gadamer specifically targets the human sciences (Geisteswissenschaften)\n\n"
                "[INTERPRETIVE] Gadamer's departure from Heidegger centers on rehabilitation of "
                "tradition and authority, which Heidegger's more radical approach tended to bracket."
            ),
            # Compatibility with objective meaning
            (
                "[DEFERRED] Whether Gadamer's hermeneutics is compatible with objective textual "
                "meaning is a contested philosophical question that requires your own judgment.\n\n"
                "[INTERPRETIVE] Key considerations include:\n\n"
                "- Gadamer rejects the ideal of 'presuppositionless' interpretation\n"
                "- He argues all understanding is historically conditioned (wirkungsgeschichtliches Bewußtsein)\n"
                "- Critics (like E.D. Hirsch) argue this leads to relativism\n"
                "- Defenders argue Gadamer seeks truth *through* rather than *despite* tradition\n\n"
                "[DEFERRED] How you resolve this tension may depend on your broader epistemological "
                "commitments and the interpretive purposes of your research."
            ),
        ],
        "Memory Continuity Demo": [
            # Interest in Mounier
            (
                "[FACTUAL] Emmanuel Mounier (1905-1950) was a French philosopher who founded "
                "the personalist movement and the influential journal *Esprit* in 1932.\n\n"
                "[INTERPRETIVE] Key themes in Mounier's personalism include:\n\n"
                "- The distinction between 'person' and 'individual'\n"
                "- Engagement (*engagement*) as essential to personal existence\n"
                "- Community as constitutive of personhood\n"
                "- Critique of both capitalism and collectivism\n\n"
                "I've noted your interest in personalist philosophy for future reference."
            ),
            # Connection to research interests
            (
                "[INTERPRETIVE] Based on our conversation, I can identify several connections:\n\n"
                "**Your stated interest:** Mounier's personalist philosophy\n\n"
                "**Potential connections:**\n"
                "1. Personalist anthropology → grounds for AI ethics (human dignity)\n"
                "2. 'Person' vs 'individual' → distinction relevant to AI agency questions\n"
                "3. Community and dialogue → I-Thou vs I-It in human-AI interaction\n\n"
                "[DEFERRED] How you integrate personalist insights with your specific research "
                "questions requires your own creative synthesis."
            ),
            # Summary request
            (
                "## Session Summary\n\n"
                "**This session explored:**\n\n"
                "1. Emmanuel Mounier's personalist philosophy (1905-1950)\n"
                "2. Key themes: person vs. individual, engagement, community\n"
                "3. Potential connections to your broader research interests\n\n"
                "**Memory Statistics:**\n"
                "- Conversation exchanges: 3\n"
                "- Research notes: 0\n"
                "- Decisions recorded: 0\n\n"
                "[INTERPRETIVE] This demonstrates the narrative memory system's ability to "
                "maintain context across exchanges and generate session summaries."
            ),
        ],
    }

    return responses.get(scenario_name, [])


async def run_demo(live_mode: bool = False) -> None:
    """Main demo entry point."""
    display_welcome()

    while True:
        choice = display_scenario_menu()

        if choice == 0:
            console.print("\n[dim]Thank you for exploring the ITSERR Agent![/dim]\n")
            break

        elif choice in (1, 2, 3):
            scenario = DEMO_SCENARIOS[choice - 1]
            console.print(f"\n[bold]Starting: {scenario.name}[/bold]\n")
            await run_scenario(scenario, mock_mode=not live_mode)

        elif choice == 4:
            await run_custom_session(mock_mode=not live_mode)

        console.print()
        if not Confirm.ask("Return to scenario menu?", default=True):
            console.print("\n[dim]Thank you for exploring the ITSERR Agent![/dim]\n")
            break
        console.print()


def main() -> None:
    """CLI entry point for the demo."""
    import typer

    app = typer.Typer()

    @app.command()
    def demo(
        live: bool = typer.Option(
            False,
            "--live",
            "-l",
            help="Use live API calls (requires API key)",
        ),
    ) -> None:
        """Run the ITSERR Agent demonstration."""
        asyncio.run(run_demo(live_mode=live))

    app()


if __name__ == "__main__":
    main()
