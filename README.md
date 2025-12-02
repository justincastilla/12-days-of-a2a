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

# Search Elastic for information about all gifts (requires .env configuration)
python main.py --elastic

# Search Elastic for a specific day's gift
python main.py --elastic --day 5

# Start as an A2A server (default port: 5000)
python main.py --server

# Start server on a custom port
python main.py --server --port 8080
```

## 🔍 Elastic Agent Builder Integration

This project includes integration with [Elastic Agent Builder](https://www.elastic.co/elasticsearch/agent-builder) to search for documents containing information about each day's gift using the A2A protocol.

### Prerequisites for Elastic Integration

1. An Elasticsearch project/deployment running in [Elastic Cloud](https://cloud.elastic.co/registration)
   * Requires Elasticsearch serverless project (or hosted deployments with Elasticsearch version 9.2.0+)
2. Documents indexed in Elasticsearch related to the 12 Days of Christmas gifts
3. An Agent Builder agent configured to search your documents

### Setting up Elastic Integration

1. **Configure your Elasticsearch project:**
   
   Create an index for your Christmas gift documents (or use an existing index):
   ```
   PUT /christmas-gifts
   {
       "mappings": {
           "properties": {
               "title": { "type": "text" },
               "content": { "type": "semantic_text" },
               "gift_name": { "type": "keyword" },
               "day": { "type": "integer" }
           }
       }
   }
   ```

2. **Create an Agent Builder tool:**
   
   In Elastic Agent Builder, create a tool to search your documents:
   * **Type**: `ES|QL`
   * **Tool ID**: `search_christmas_gifts`
   * **Description**: `Search for documents about 12 Days of Christmas gifts`
   * **ES|QL**: Create a query to search your index

3. **Create an Agent Builder agent:**
   
   * **Agent ID**: `christmas_gifts_agent` (or customize in `.env`)
   * **Custom Instructions**: Configure how the agent should respond to queries about Christmas gifts
   * **Display Name**: `Christmas Gifts Search Agent`

4. **Configure environment variables:**
   
   Copy `.env.example` to `.env` and fill in your values:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set:
   * `ES_AGENT_URL`: Your Elastic Agent Builder A2A URL
     * Get from Agent Builder Tools page → MCP Server → Copy MCP Server URL
     * Replace `mcp` at the end with `a2a`
     * Example: `https://example.kb.region.azure.elastic.cloud/api/agent_builder/a2a`
   * `ES_API_KEY`: Your Elastic API key
     * Create in Elasticsearch navigation → Create API key
   * `ES_AGENT_ID`: Your agent ID (default: `christmas_gifts_agent`)

5. **Test the integration:**
   ```bash
   python main.py --elastic --day 5
   ```

### How It Works

The integration uses the A2A (Agent-to-Agent) protocol to communicate with Elastic Agent Builder:

1. **Gift agents** can optionally query Elastic for additional information about each gift
2. **The orchestrator** provides a `search_gift_info()` skill to search for specific gifts
3. The `--elastic` flag triggers Elastic searches when running the demo
4. If Elastic is not configured, the application continues to work with the base gift data

This demonstrates how multiple specialized agents can work together:
* 12 gift sub-agents (local)
* 1 orchestrator agent (local)
* 1 Elastic search agent (remote via A2A)


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
5. **Remote Agent Integration**: Connect to external agents via A2A protocol (Elastic Agent Builder)

## 📚 Learn More

- [Python A2A Library](https://github.com/themanojdesai/python-a2a)
- [Google A2A Protocol](https://google.github.io/A2A/)
- [A2A Documentation](https://python-a2a.readthedocs.io/)
- [Elastic Agent Builder](https://www.elastic.co/elasticsearch/agent-builder)
- [Elastic Agent Builder A2A Example](https://github.com/elastic/elasticsearch-labs/tree/main/supporting-blog-content/agent-builder-a2a-agent-framework)

## 📄 License

This project is open source and available under the MIT License.
