import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from src.services.docker_service import DockerService
from src.services.system_service import SystemService
from src.services.cleanup_service import CleanupService
from src.services.report_service import ReportService


app = typer.Typer(
    help="Professional Docker cleanup tool.",
    no_args_is_help=True,
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]}
)
console = Console()

def show_banner():
    console.print("==============================================", style="cyan")
    console.print("           DOCKER CLEANUP PRO v1.1 (PY)", style="bold cyan")
    console.print("==============================================", style="cyan")

def format_size(bytes_size: float) -> str:
    """Formats bytes to a human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} PB"


@app.command(name="bc")
def basic_cleanup(
    older_than: Optional[str] = typer.Option(None, "--older-than", help="Filter by age (e.g. 10d, 2w)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be removed")
):
    """[Basic Cleanup] Containers, networks and dangling images."""
    show_banner()
    ds = DockerService()
    cs = CleanupService(ds)
    if dry_run:
        preview = cs.get_preview('basic', older_than)
        console.print("\n[yellow]DRY RUN: Resources to be removed:[/yellow]")
        console.print(preview)
    else:
        with console.status("[bold green]Running basic cleanup..."):
            cs.basic_cleanup(older_than)
        console.print("\n[bold green][OK] Basic cleanup completed.[/bold green]")

@app.command(name="ac")
def advanced_cleanup(
    older_than: Optional[str] = typer.Option(None, "--older-than", help="Filter by age (e.g. 10d, 2w)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be removed")
):
    """[Advanced Cleanup] Basic + Volumes, all unused images and build cache."""
    show_banner()
    ds = DockerService()
    cs = CleanupService(ds)
    if dry_run:
        preview = cs.get_preview('advanced', older_than)
        console.print("\n[yellow]DRY RUN: Resources to be removed:[/yellow]")
        console.print(preview)
    else:
        with console.status("[bold yellow]Running advanced cleanup..."):
            cs.advanced_cleanup(older_than)
        console.print("\n[bold yellow][OK] Advanced cleanup completed.[/bold yellow]")

@app.command(name="tc")
def total_cleanup(
    y: bool = typer.Option(False, "-y", help="Skip confirmation"), 
    older_than: Optional[str] = typer.Option(None, "--older-than", help="Filter by age (e.g. 10d, 2w)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be removed")
):
    """[Total Cleanup] NUCLEAR OPTION: Everything not in use."""
    show_banner()
    if dry_run:
        console.print("\n[bold red]DRY RUN: Total cleanup would remove ALL unused resources.[/bold red]")
        return

    if not y:
        confirm = typer.confirm("Are you sure you want to clean EVERYTHING?")
        if not confirm:
            console.print("[cyan]Aborted.[/cyan]")
            raise typer.Abort()
            
    ds = DockerService()
    cs = CleanupService(ds)
    with console.status("[bold red]Running TOTAL cleanup..."):
        cs.total_cleanup(older_than)
    console.print("\n[bold red][OK] Total cleanup completed.[/bold red]")

@app.command(name="dr")
def disk_report(
    json_path: Optional[str] = typer.Option(None, "--json", help="Path to save JSON report"),
    md_path: Optional[str] = typer.Option(None, "--md", help="Path to save Markdown report"),
    terminal: bool = typer.Option(True, "--terminal/--no-terminal", help="Show report in terminal")
):
    """Show Docker and System disk usage report."""
    if terminal:
        show_banner()
        
    ds = DockerService()
    ss = SystemService()
    
    # Detailed Docker usage
    docker_data = ds.get_detailed_usage()
    
    # Disk usage
    system_usage = ss.get_disk_usage()

    if terminal:
        table = Table(title="Docker Resources Detailed Usage")
        table.add_column("Resource Type", style="magenta")
        table.add_column("Count", style="green", justify="right")
        table.add_column("Size", style="yellow", justify="right")
        
        table.add_row("Containers", str(docker_data['containers']['count']), format_size(docker_data['containers']['size']))
        table.add_row("Images", str(docker_data['images']['count']), format_size(docker_data['images']['size']))
        table.add_row("Volumes", str(docker_data['volumes']['count']), format_size(docker_data['volumes']['size']))
        table.add_row("Build Cache", "-", format_size(docker_data['build_cache']['size']))
        
        console.print(table)

        # Total Docker Size
        docker_total_bytes = (
            docker_data['containers']['size'] + 
            docker_data['images']['size'] + 
            docker_data['volumes']['size'] + 
            docker_data['build_cache']['size']
        )
        docker_total_gb = docker_total_bytes / (1024**3)
        
        console.print(f"\n[bold blue]System Disk Usage:[/bold blue]")
        console.print(f"Used: [white]{system_usage['used_gb']} GB / {system_usage['total_gb']} GB ({system_usage['percent_used']} %)[/white]")
        
        # Relation
        ratio = (docker_total_gb / system_usage['used_gb']) * 100 if system_usage['used_gb'] > 0 else 0
        console.print(f"\n[bold cyan]Docker vs System Relation:[/bold cyan]")
        console.print(f"Docker Total Size: [yellow]{format_size(docker_total_bytes)}[/yellow]")
        console.print(f"Docker represents [bold yellow]{ratio:.2f}%[/bold yellow] of the used disk space.")

    # Export Logic
    if json_path or md_path:
        report_data = {
            "docker_detailed": docker_data,
            "system_disk": system_usage,
            "relation": {
                "docker_total_bytes": docker_total_bytes,
                "docker_ratio_percent": round(ratio, 2)
            }
        }

        
        if json_path:
            ReportService.generate_json(report_data, json_path)
            console.print(f"[green][OK] JSON report saved to: {json_path}[/green]")
            
        if md_path:
            ReportService.generate_markdown(report_data, md_path)
            console.print(f"[green][OK] Markdown report saved to: {md_path}[/green]")


if __name__ == "__main__":
    app()
