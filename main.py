#!/usr/bin/env python3
"""
12 Days of Christmas - A2A Protocol Demonstration

This application demonstrates Google's Agent-to-Agent (A2A) protocol
by creating 12 sub-agents (one for each day of Christmas) and a main
orchestrator agent that coordinates all of them.

Usage:
    python main.py                          # Run the full demo (agents + summary + song)
    python main.py --day 5                  # Show only day 5 verse
    python main.py --summary                # Show gift summary only
    python main.py --agents                 # Show individual agent demonstrations
    python main.py --elastic                # Search Elastic for all gifts (requires .env)
    python main.py --elastic --day 5        # Search Elastic for day 5 gift
    python main.py --server                 # Start as A2A server (port 5000)
    python main.py --server --port 8080     # Start server on custom port
"""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.gift_agents import get_gift_agent, GIFTS
from src.orchestrator import ChristmasOrchestratorAgent


def print_header():
    """Print the application header."""
    print("=" * 60)
    print("🎄 12 Days of Christmas - A2A Protocol Demonstration 🎄")
    print("=" * 60)
    print()


def demonstrate_gift_agents():
    """Demonstrate each gift agent individually."""
    print("📦 Demonstrating Individual Gift Agents (A2A Sub-Agents):")
    print("-" * 50)
    print()

    for day in range(1, 13):
        agent = get_gift_agent(day)
        gift = agent.get_gift()
        print(f"  Day {day:2d} Agent → {gift}")

    print()


def demonstrate_orchestrator():
    """Demonstrate the orchestrator agent."""
    orchestrator = ChristmasOrchestratorAgent()

    print("🎼 Orchestrator Agent Calling All 12 Sub-Agents:")
    print("-" * 50)
    print()

    # Show how orchestrator collects from all agents
    print("The orchestrator coordinates with all gift agents to assemble")
    print("the complete '12 Days of Christmas' response.")
    print()

    # Show the full song
    print(orchestrator.get_full_song())
    print()


def show_gift_summary():
    """Display a summary of all gifts."""
    orchestrator = ChristmasOrchestratorAgent()
    print(orchestrator.get_gift_summary(include_elastic=True))
    print()


def show_specific_day(day: int):
    """Show the verse for a specific day."""
    if day < 1 or day > 12:
        print(f"Error: Day must be between 1 and 12, got {day}")
        return

    orchestrator = ChristmasOrchestratorAgent()
    print(orchestrator.get_day_verse(day))
    print()


def search_elastic_for_day(day: int):
    """Search Elastic for information about a specific day's gift."""
    if day < 1 or day > 12:
        print(f"Error: Day must be between 1 and 12, got {day}")
        return

    orchestrator = ChristmasOrchestratorAgent()
    print(orchestrator.search_gift_info(day))
    print()


def start_server(port: int = 5000):
    """Start the orchestrator as an A2A server."""
    try:
        from python_a2a import run_server

        orchestrator = ChristmasOrchestratorAgent()
        print(f"🚀 Starting A2A server on port {port}...")
        print(f"   Send requests to http://localhost:{port}")
        print()
        run_server(orchestrator, port=port)
    except ImportError as e:
        print(f"Error: Could not import python_a2a. Please install it with:")
        print("  pip install python-a2a")
        sys.exit(1)


def main():
    """Main entry point for the demonstration."""
    parser = argparse.ArgumentParser(
        description="12 Days of Christmas - A2A Protocol Demonstration"
    )
    parser.add_argument("--day", "-d", type=int, help="Show only a specific day (1-12)")
    parser.add_argument(
        "--summary", "-s", action="store_true", help="Show only the gift summary"
    )
    parser.add_argument("--server", action="store_true", help="Start as an A2A server")
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=5000,
        help="Port for the A2A server (default: 5000)",
    )
    parser.add_argument(
        "--agents", action="store_true", help="Show individual agent demonstrations"
    )
    parser.add_argument(
        "--elastic",
        "-e",
        action="store_true",
        help="Search Elastic for gift information (requires configuration in .env)",
    )

    args = parser.parse_args()

    print_header()

    if args.server:
        start_server(args.port)
    elif args.elastic:
        # Search Elastic for all days or specific day
        if args.day:
            search_elastic_for_day(args.day)
        else:
            print("🔍 Searching Elastic for information about all 12 gifts:")
            print("-" * 50)
            print()
            for day in range(1, 13):
                search_elastic_for_day(day)
                print()
    elif args.day:
        show_specific_day(args.day)
    elif args.summary:
        show_gift_summary()
    elif args.agents:
        demonstrate_gift_agents()
    else:
        # Default: show everything
        demonstrate_gift_agents()
        print()
        show_gift_summary()
        print()
        print("=" * 60)
        print("📜 THE COMPLETE SONG")
        print("=" * 60)
        print()
        demonstrate_orchestrator()


if __name__ == "__main__":
    main()
