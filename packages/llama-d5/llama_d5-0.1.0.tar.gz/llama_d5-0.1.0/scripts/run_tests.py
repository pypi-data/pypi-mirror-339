#!/usr/bin/env python
"""Automated test runner with progress bar."""
import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)
from rich.syntax import Syntax

console = Console()


def discover_tests():
    """Discover all test files in the tests directory."""
    tests_dir = Path("tests")
    if not tests_dir.exists():
        console.print("[bold red]Error:[/bold red] Tests directory not found.")
        sys.exit(1)

    test_files = list(tests_dir.glob("test_*.py"))
    return test_files


def run_test(test_file):
    """Run a specific test file and return success/failure."""
    result = subprocess.run(
        ["python", "-m", "pytest", str(test_file), "-v"], capture_output=True, text=True
    )
    return result.returncode == 0, result.stdout, result.stderr


def print_error_details(stdout, stderr):
    """Print detailed error information in a readable format."""
    if stdout.strip():
        console.print("\n[bold]Test Output:[/bold]")
        for line in stdout.strip().split("\n"):
            if "FAILED" in line:
                console.print(f"[red]{line}[/red]")
            elif "PASSED" in line:
                console.print(f"[green]{line}[/green]")
            else:
                console.print(line)

    if stderr.strip():
        console.print("\n[bold red]Error Output:[/bold red]")
        console.print(
            Syntax(
                stderr.strip(),
                "python",
                theme="monokai",
                line_numbers=True,
                word_wrap=True,
            )
        )


def run_all_tests():
    """Run all tests with a progress bar."""
    console.print(
        Panel.fit(
            "[bold blue]LlamaDoc2PDF[/bold blue] [bold green]Automated Test Runner[/bold green]",
            border_style="green",
        )
    )

    test_files = discover_tests()

    if not test_files:
        console.print("[yellow]Warning:[/yellow] No test files found.")
        return

    console.print(f"Found [bold]{len(test_files)}[/bold] test files.")

    passed_tests = 0
    failed_tests = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[green]Running tests...", total=len(test_files))

        for test_file in test_files:
            progress.update(task, description=f"[green]Testing[/green] {test_file.name}")
            success, stdout, stderr = run_test(test_file)

            if success:
                passed_tests += 1
                progress.update(task, advance=1)
            else:
                failed_tests.append((test_file, stdout, stderr))
                progress.update(task, description=f"[red]Failed[/red] {test_file.name}")
                progress.advance(task)

    # Show summary
    console.print("\n[bold]Test Results:[/bold]")
    console.print(f"✅ [green]{passed_tests} tests passed[/green]")

    if failed_tests:
        console.print(f"❌ [red]{len(failed_tests)} tests failed[/red]\n")

        console.print("[bold]Failed Tests:[/bold]")
        for test_file, stdout, stderr in failed_tests:
            console.print(f"[red]{test_file}[/red]")
            print_error_details(stdout, stderr)
    else:
        console.print("🎉 [bold green]All tests passed![/bold green]")


if __name__ == "__main__":
    run_all_tests()
