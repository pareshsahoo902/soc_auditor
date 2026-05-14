import typer
import json
from rich import print
from typing import Optional

from mock_simulation.scenarios.registry import ScenarioRegistry
from mock_simulation.scenarios.replay import DeterministicReplay

app = typer.Typer(help="CLI for the Mock Governance Simulation Framework")

@app.command()
def list_scenarios():
    """List all available governance scenarios."""
    scenarios = ScenarioRegistry.list_scenarios().keys()
    print("[bold green]Available Scenarios:[/bold green]")
    for s in scenarios:
        print(f"- {s}")

@app.command()
def simulate(scenario: str, org_id: str = "ORG-123", seed: int = 42, output_file: Optional[str] = None):
    """Run a scenario and generate events deterministically."""
    if scenario not in ScenarioRegistry.list_scenarios():
        print(f"[bold red]Error:[/bold red] Scenario '{scenario}' not found.")
        raise typer.Exit(code=1)

    print(f"[bold blue]Running scenario '{scenario}' for {org_id} (Seed: {seed})...[/bold blue]")
    result = DeterministicReplay.run_scenario(scenario, org_id, seed=seed)

    if output_file:
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"[bold green]Success![/bold green] Results written to {output_file}")
    else:
        # Avoid printing massive JSON outputs completely to terminal, just print summary
        print(f"[bold green]Simulation Complete![/bold green]")
        print(f"Events generated: {len(result['events'])}")
        print(f"Scores: {result['scores']}")
        print(f"Graph Valid: {result['graph_validation']['is_valid']}")

if __name__ == "__main__":
    app()
