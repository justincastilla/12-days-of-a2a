"""
Main Orchestrator Agent for the 12 Days of Christmas A2A Demonstration

This orchestrator agent coordinates with all 12 gift agents to assemble
the complete "12 Days of Christmas" song response.

Integrates with Elastic Agent Builder to enrich gift information with search results.
"""

import re

from python_a2a import A2AServer, skill, TaskStatus, TaskState, AgentCard
from gift_agents import get_gift_for_day, get_gift_agent, GIFTS
from elastic_search_agent import get_elastic_agent


class ChristmasOrchestratorAgent(A2AServer):
    """
    Main orchestrator that calls each of the 12 gift agents
    and assembles the complete song response.
    """

    def __init__(self, port: int = 5000):
        agent_card = AgentCard(
            name="Christmas Orchestrator Agent",
            description="Coordinates all 12 gift agents to perform the 12 Days of Christmas",
            url=f"http://localhost:{port}",
            version="1.0.0"
        )
        super().__init__(agent_card=agent_card)
        self.total_days = 12

    @skill(
        name="Get Day Verse",
        description="Get the verse for a specific day of Christmas",
        tags=["christmas", "verse", "day"]
    )
    def get_day_verse(self, day: int) -> str:
        """Get the complete verse for a specific day."""
        ordinals = {
            1: "first", 2: "second", 3: "third", 4: "fourth",
            5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth",
            9: "ninth", 10: "tenth", 11: "eleventh", 12: "twelfth"
        }

        verse_lines = [f"On the {ordinals[day]} day of Christmas, my true love gave to me:"]

        # Add gifts in reverse order (from current day down to 1)
        for gift_day in range(day, 0, -1):
            gift = get_gift_for_day(gift_day)
            # Add "and" before the partridge on days > 1
            if gift_day == 1 and day > 1:
                verse_lines.append(f"  And {gift}")
            else:
                verse_lines.append(f"  {gift}")

        return "\n".join(verse_lines)

    @skill(
        name="Get Full Song",
        description="Get the complete 12 Days of Christmas song",
        tags=["christmas", "song", "complete"]
    )
    def get_full_song(self) -> str:
        """Get the complete song with all 12 verses."""
        verses = []
        for day in range(1, self.total_days + 1):
            verses.append(self.get_day_verse(day))
        return "\n\n".join(verses)

    @skill(
        name="Get Gift Summary",
        description="Get a summary of all gifts",
        tags=["christmas", "gifts", "summary"]
    )
    def get_gift_summary(self, include_elastic: bool = False) -> str:
        """Get a summary of all gifts received."""
        lines = ["🎄 Summary of all gifts from the 12 Days of Christmas 🎄", ""]
        total_items = 0

        for day in range(1, self.total_days + 1):
            gift_info = GIFTS[day]
            lines.append(f"Day {day:2d}: {gift_info['quantity']:2d} {gift_info['gift']}")
            total_items += gift_info['quantity']
            
            # Optionally include Elastic search results
            if include_elastic:
                elastic_agent = get_elastic_agent()
                if elastic_agent.is_enabled():
                    # Note: This would be async in production, simplified for demo
                    try:
                        from elastic_search_agent import search_gift
                        info = search_gift(gift_info['gift'], day)
                        if info:
                            lines.append(f"         📝 {info[:100]}...")  # First 100 chars
                    except Exception as e:
                        pass  # Silently skip if Elastic not available

        lines.append("")
        lines.append(f"Total items received: {total_items}")
        return "\n".join(lines)

    @skill(
        name="Search Gift with Elastic",
        description="Search for information about a specific gift using Elastic",
        tags=["christmas", "gift", "elastic", "search"]
    )
    def search_gift_info(self, day: int) -> str:
        """Search for information about a specific day's gift in Elastic."""
        if day < 1 or day > 12:
            return f"Error: Day must be between 1 and 12, got {day}"
        
        gift_info = GIFTS[day]
        gift_name = gift_info['gift']
        
        # Try to get information from Elastic
        elastic_agent = get_elastic_agent()
        if not elastic_agent.is_enabled():
            return f"Day {day}: {gift_info['quantity']} {gift_name}\n\n(Elastic integration not configured - set ES_AGENT_URL and ES_API_KEY in .env file)"
        
        try:
            from elastic_search_agent import search_gift
            elastic_info = search_gift(gift_name, day)
            
            if elastic_info:
                return f"Day {day}: {gift_info['quantity']} {gift_name}\n\nInformation from Elastic:\n{elastic_info}"
            else:
                return f"Day {day}: {gift_info['quantity']} {gift_name}\n\n(No additional information found in Elastic)"
        except Exception as e:
            return f"Day {day}: {gift_info['quantity']} {gift_name}\n\n(Error searching Elastic: {str(e)})"

    def handle_task(self, task):
        """Handle incoming task requests."""
        message_data = task.message or {}
        content = message_data.get("content", {})
        text = content.get("text", "").lower() if isinstance(content, dict) else ""

        # Determine what type of response to generate
        if "search" in text or "elastic" in text:
            # Search for a specific gift
            day_match = re.search(r'day\s*(\d+)', text)
            if day_match:
                day = int(day_match.group(1))
                if 1 <= day <= 12:
                    response_text = self.search_gift_info(day)
                else:
                    response_text = "Please specify a day between 1 and 12."
            else:
                response_text = "Please specify which day you'd like to search for (1-12)."
        elif "summary" in text:
            response_text = self.get_gift_summary()
        elif "day" in text:
            # Try to extract day number
            day_match = re.search(r'day\s*(\d+)', text)
            if day_match:
                day = int(day_match.group(1))
                if 1 <= day <= 12:
                    response_text = self.get_day_verse(day)
                else:
                    response_text = "Please specify a day between 1 and 12."
            else:
                response_text = "Please specify which day you'd like (1-12)."
        else:
            # Default: return the full song
            response_text = self.get_full_song()

        task.artifacts = [{
            "parts": [{"type": "text", "text": response_text}]
        }]
        task.status = TaskStatus(state=TaskState.COMPLETED)
        return task


def create_orchestrator():
    """Create and return the orchestrator agent."""
    return ChristmasOrchestratorAgent()


if __name__ == "__main__":
    # Demonstrate the orchestrator locally
    orchestrator = create_orchestrator()

    print("=" * 60)
    print("🎄 12 Days of Christmas - A2A Protocol Demonstration 🎄")
    print("=" * 60)
    print()

    # Show summary of gifts
    print(orchestrator.get_gift_summary())
    print()
    print("=" * 60)
    print()

    # Show the full song
    print("📜 The Complete Song:")
    print()
    print(orchestrator.get_full_song())
