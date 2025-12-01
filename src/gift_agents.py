"""
Gift Agents for the 12 Days of Christmas A2A Demonstration

Each agent represents one day's gift from the classic song "The Twelve Days of Christmas".
These agents implement the A2A protocol using python-a2a library.
"""

from python_a2a import A2AServer, skill, agent, TaskStatus, TaskState, AgentCard

# Gift data for each day
GIFTS = {
    1: {"gift": "a Partridge in a Pear Tree", "quantity": 1},
    2: {"gift": "Turtle Doves", "quantity": 2},
    3: {"gift": "French Hens", "quantity": 3},
    4: {"gift": "Calling Birds", "quantity": 4},
    5: {"gift": "Golden Rings", "quantity": 5},
    6: {"gift": "Geese a-Laying", "quantity": 6},
    7: {"gift": "Swans a-Swimming", "quantity": 7},
    8: {"gift": "Maids a-Milking", "quantity": 8},
    9: {"gift": "Ladies Dancing", "quantity": 9},
    10: {"gift": "Lords a-Leaping", "quantity": 10},
    11: {"gift": "Pipers Piping", "quantity": 11},
    12: {"gift": "Drummers Drumming", "quantity": 12},
}


def create_gift_agent(day: int, base_port: int = 5001):
    """Factory function to create a gift agent for a specific day."""
    gift_info = GIFTS[day]
    gift_name = gift_info["gift"]
    quantity = gift_info["quantity"]
    port = base_port + day - 1

    class GiftAgent(A2AServer):
        """Agent that returns the gift for a specific day of Christmas."""

        def __init__(self):
            agent_card = AgentCard(
                name=f"Day {day} Gift Agent",
                description=f"Provides the gift for day {day} of Christmas: {quantity} {gift_name}",
                url=f"http://localhost:{port}",
                version="1.0.0"
            )
            super().__init__(agent_card=agent_card)
            self.day = day
            self.gift = gift_name
            self.quantity = quantity

        @skill(
            name="Get Gift",
            description=f"Get the gift for day {day} of Christmas",
            tags=["christmas", "gift", f"day{day}"]
        )
        def get_gift(self):
            """Return the gift for this day."""
            return f"{self.quantity} {self.gift}"

        def handle_task(self, task):
            """Handle incoming task requests."""
            # Return the gift for this day
            gift_text = self.get_gift()
            task.artifacts = [{
                "parts": [{"type": "text", "text": gift_text}]
            }]
            task.status = TaskStatus(state=TaskState.COMPLETED)
            return task

    return GiftAgent()


# Create all 12 gift agents
gift_agents = {day: create_gift_agent(day) for day in range(1, 13)}


def get_gift_agent(day: int) -> A2AServer:
    """Get the gift agent for a specific day (1-12)."""
    if day < 1 or day > 12:
        raise ValueError(f"Day must be between 1 and 12, got {day}")
    return gift_agents[day]


def get_gift_for_day(day: int) -> str:
    """Directly get the gift string for a specific day."""
    if day < 1 or day > 12:
        raise ValueError(f"Day must be between 1 and 12, got {day}")
    gift_info = GIFTS[day]
    return f"{gift_info['quantity']} {gift_info['gift']}"


def get_all_gifts() -> list:
    """Get all gifts in order."""
    return [get_gift_for_day(day) for day in range(1, 13)]
