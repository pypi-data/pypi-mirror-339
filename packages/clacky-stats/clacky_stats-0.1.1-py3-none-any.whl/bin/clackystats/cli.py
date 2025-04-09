#!/usr/bin/env python3

import os
import sys
from datetime import datetime
from typing import Optional

import typer
import yaml
from rich.console import Console
from rich.table import Table

from bin.clackystats.blame import BlameAnalyzer

app = typer.Typer(help="Code Contribution Statistics Tool for Clacky AI")
console = Console()

def validate_date(date_str: str) -> bool:
    """Validate date format"""
    try:
        if len(date_str.split()) == 1:
            datetime.strptime(date_str, "%Y-%m-%d")
        else:
            datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

def print_blame_results(result: dict):
    """Print statistics results"""
    table = Table(title="Code Contribution Statistics")
    table.add_column("Author", style="cyan")
    table.add_column("Lines", justify="right", style="green")
    table.add_column("Percentage", justify="right", style="yellow")

    total_lines = result["total_lines"]
    for author, count in result["grand_total"].items():
        percentage = round((count / total_lines) * 100, 2) if total_lines > 0 else 0
        table.add_row(author, str(count), f"{percentage}%")

    console.print(table)
    # ClackyAI wrote 0%(0/0) code with 0 humans since
    console.print(f"ClackyAI wrote {round(result['clacky_percentage'], 2)}%({result['clacky_total']}/{result['total_lines']}) lines")

@app.command()
def blame(
    start_date: Optional[str] = typer.Option(None, "--start-date", "-s", help="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = typer.Option(None, "--end-date", "-e", help="End date (YYYY-MM-DD)"),
    start_tag: Optional[str] = typer.Option(None, "--start-tag", "-t", help="Start tag"),
    end_tag: Optional[str] = typer.Option(None, "--end-tag", "-T", help="End tag"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    all_since: bool = typer.Option(False, "--all-since", help="Analyze all versions since specified tag"),
) -> None:
    """Analyze code contributions"""
    
    if not os.path.exists(".git"):
        console.print("[red]Error: Current directory is not a git repository[/red]")
        sys.exit(1)

    if start_date and not validate_date(start_date):
        console.print("[red]Error: Invalid start date format, please use YYYY-MM-DD[/red]")
        sys.exit(1)

    if end_date and not validate_date(end_date):
        console.print("[red]Error: Invalid end date format, please use YYYY-MM-DD[/red]")
        sys.exit(1)

    analyzer = BlameAnalyzer()

    if not start_tag and not start_date:
        start_tag = analyzer.get_latest_version_tag()
        if not start_tag:
            console.print("[red]Error: No valid version tag found[/red]")
            sys.exit(1)

    if all_since:
        if start_date or end_date:
            console.print("[red]Error: --all-since cannot be used with date parameters[/red]")
            sys.exit(1)
        results = analyzer.process_all_tags_since(start_tag)
        
        if output:
            # Read and update existing file if it exists
            existing_results = []
            if os.path.exists(output):
                with open(output, "r") as f:
                    existing_results = yaml.safe_load(f) or []

            # Create mapping of existing entries
            existing_map = {(r["start_tag"], r["end_tag"]): i for i, r in enumerate(existing_results)}

            # Update or append new results
            for new_result in results:
                key = (new_result["start_tag"], new_result["end_tag"])
                if key in existing_map:
                    existing_results[existing_map[key]] = new_result
                else:
                    existing_results.append(new_result)

            with open(output, "w") as f:
                yaml.dump(existing_results, f, sort_keys=True)
        else:
            console.print(yaml.dump(results, sort_keys=True))
    else:
        all_file_counts, grand_total, total_lines, clacky_total, clacky_percentage, end_date = analyzer.blame(
            start_date=start_date,
            end_date=end_date,
            start_tag=start_tag,
            end_tag=end_tag
        )

        result = {
            "start_tag": start_tag,
            "end_tag": end_tag or "HEAD",
            "end_date": end_date.strftime("%Y-%m-%d"),
            "file_counts": all_file_counts,
            "grand_total": dict(sorted(grand_total.items(), key=lambda x: x[1], reverse=True)),
            "total_lines": total_lines,
            "clacky_total": clacky_total,
            "clacky_percentage": round(clacky_percentage, 2),
        }

        if output:
            with open(output, "w") as f:
                yaml.dump(result, f, sort_keys=True)
        else:
            print_blame_results(result)

@app.command()
def week():
    """Analyze code contributions for this week (since last Friday)"""
    from datetime import datetime, timedelta
    
    today = datetime.now()
    last_friday = today - timedelta(days=(today.weekday() + 3) % 7)
    start_date = last_friday.strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")
    
    analyzer = BlameAnalyzer()
    all_file_counts, grand_total, total_lines, clacky_total, clacky_percentage, end_date = analyzer.blame(
        start_date=start_date,
        end_date=end_date
    )

    result = {
        "start_date": start_date,
        "end_date": end_date,
        "file_counts": all_file_counts,
        "grand_total": dict(sorted(grand_total.items(), key=lambda x: x[1], reverse=True)),
        "total_lines": total_lines,
        "clacky_total": clacky_total,
        "clacky_percentage": round(clacky_percentage, 2),
    }
    
    print_blame_results(result)

@app.command()
def month():
    """Analyze code contributions for current month"""
    from datetime import datetime
    
    start_date = datetime.now().strftime("%Y-%m-01")
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    analyzer = BlameAnalyzer()
    all_file_counts, grand_total, total_lines, clacky_total, clacky_percentage, end_date = analyzer.blame(
        start_date=start_date,
        end_date=end_date
    )

    result = {
        "start_date": start_date,
        "end_date": end_date,
        "file_counts": all_file_counts,
        "grand_total": dict(sorted(grand_total.items(), key=lambda x: x[1], reverse=True)),
        "total_lines": total_lines,
        "clacky_total": clacky_total,
        "clacky_percentage": round(clacky_percentage, 2),
    }
    
    print_blame_results(result)

def main():
    app() 