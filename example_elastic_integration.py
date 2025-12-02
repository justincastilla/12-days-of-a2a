#!/usr/bin/env python3
"""
Example script demonstrating the Elastic Agent Builder integration

This script shows how the integration works when properly configured.
To use this with a real Elastic instance:

1. Copy .env.example to .env
2. Fill in your Elastic Agent Builder credentials
3. Run this script
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.elastic_search_agent import get_elastic_agent
from src.orchestrator import ChristmasOrchestratorAgent


def main():
    print("=" * 60)
    print("🔍 Elastic Agent Builder Integration Example")
    print("=" * 60)
    print()
    
    # Check if Elastic is configured
    elastic_agent = get_elastic_agent()
    
    if not elastic_agent.is_enabled():
        print("⚠️  Elastic integration is not configured.")
        print()
        print("To enable it:")
        print("1. Copy .env.example to .env")
        print("2. Set ES_AGENT_URL to your Elastic Agent Builder A2A URL")
        print("3. Set ES_API_KEY to your Elastic API key")
        print("4. Set ES_AGENT_ID to your agent ID (default: christmas_gifts_agent)")
        print()
        print("Example .env file:")
        print("-" * 60)
        print("ES_AGENT_URL=https://example.kb.region.azure.elastic.cloud/api/agent_builder/a2a")
        print("ES_API_KEY=your-api-key-here")
        print("ES_AGENT_ID=christmas_gifts_agent")
        print("-" * 60)
        print()
        return
    
    print("✅ Elastic integration is configured!")
    print()
    
    # Create the orchestrator
    orchestrator = ChristmasOrchestratorAgent()
    
    # Test searching for Day 5 (Golden Rings)
    print("Searching Elastic for information about Day 5 (Golden Rings)...")
    print("-" * 60)
    result = orchestrator.search_gift_info(5)
    print(result)
    print()


if __name__ == "__main__":
    main()
