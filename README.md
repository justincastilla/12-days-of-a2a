# 12 Days of Christmas - A2A Protocol Demonstration

A Python application demonstrating Google's Agent-to-Agent (A2A) protocol using the classic "12 Days of Christmas" song. This project showcases how multiple specialized agents can coordinate through a main orchestrator agent.

## 🎄 Overview

This project implements a multi-agent system using the [python-a2a](https://github.com/themanojdesai/python-a2a) library, where:

- **12 Gift Agents**: Each agent represents one day's gift from the song (e.g., "5 Golden Rings", "2 Turtle Doves")
- **1 Orchestrator Agent**: Coordinates all gift agents to assemble the complete song

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/justincastilla/12-days-of-a2a.git
cd 12-days-of-a2a
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Demo

Run the full demonstration:
```bash
python main.py
```

### Command Line Options

```bash
# Show the complete demo (gift agents + summary + full song)
python main.py

# Show only a specific day's verse
python main.py --day 5

# Show only the gift summary
python main.py --summary

# Show individual agent demonstrations
python main.py --agents

# Start as an A2A server (default port: 5000)
python main.py --server

# Start server on a custom port
python main.py --server --port 8080
```

## 📁 Project Structure

```
12-days-of-a2a/
├── main.py              # Main entry point
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── src/
    ├── __init__.py      # Package init
    ├── gift_agents.py   # 12 gift sub-agents
    └── orchestrator.py  # Main orchestrator agent
```

## 🎁 The 12 Gifts

| Day | Gift | Quantity |
|-----|------|----------|
| 1 | Partridge in a Pear Tree | 1 |
| 2 | Turtle Doves | 2 |
| 3 | French Hens | 3 |
| 4 | Calling Birds | 4 |
| 5 | Golden Rings | 5 |
| 6 | Geese a-Laying | 6 |
| 7 | Swans a-Swimming | 7 |
| 8 | Maids a-Milking | 8 |
| 9 | Ladies Dancing | 9 |
| 10 | Lords a-Leaping | 10 |
| 11 | Pipers Piping | 11 |
| 12 | Drummers Drumming | 12 |

**Total items received: 78**

## 🔧 A2A Protocol Concepts Demonstrated

1. **Agent Cards**: Each agent has metadata describing its capabilities
2. **Skills**: Agents expose specific skills (e.g., `get_gift`, `get_day_verse`)
3. **Tasks**: Agents handle tasks and return responses with artifacts
4. **Orchestration**: The main agent coordinates multiple sub-agents

## 📚 Learn More

- [Python A2A Library](https://github.com/themanojdesai/python-a2a)
- [Google A2A Protocol](https://google.github.io/A2A/)
- [A2A Documentation](https://python-a2a.readthedocs.io/)

## 📄 License

This project is open source and available under the MIT License.
