"""
Elastic Agent Builder A2A Integration

This module provides integration with Elastic's Agent Builder using the A2A protocol
to search for documents containing information about the 12 Days of Christmas gifts.
"""

import asyncio
import os
import threading
from typing import Optional, Dict
from dotenv import load_dotenv
import httpx
from a2a.client import A2ACardResolver
from agent_framework.a2a import A2AAgent


class ElasticSearchAgent:
    """
    Agent to search Elastic for documents related to the 12 Days of Christmas gifts.
    
    This agent connects to an Elastic Agent Builder agent via the A2A protocol
    to retrieve relevant documents containing information about each day's gift.
    """
    
    def __init__(self):
        """Initialize the Elastic search agent."""
        load_dotenv()
        self.es_agent_url = os.getenv("ES_AGENT_URL")
        self.es_api_key = os.getenv("ES_API_KEY")
        self.es_agent_id = os.getenv("ES_AGENT_ID", "christmas_gifts_agent")
        self._agent = None
        self._http_client = None
        self._enabled = bool(self.es_agent_url and self.es_api_key)
    
    def is_enabled(self) -> bool:
        """Check if the Elastic integration is properly configured."""
        return self._enabled
    
    async def _initialize_agent(self) -> Optional[A2AAgent]:
        """Initialize the A2A agent connection to Elastic."""
        if not self.is_enabled():
            return None
        
        if self._agent is not None:
            return self._agent
        
        try:
            custom_headers = {"Authorization": f"ApiKey {self.es_api_key}"}
            
            # Create HTTP client with custom headers
            self._http_client = httpx.AsyncClient(
                timeout=60.0,
                headers=custom_headers
            )
            
            # Resolve the A2A Agent Card
            resolver = A2ACardResolver(
                httpx_client=self._http_client,
                base_url=self.es_agent_url
            )
            agent_card = await resolver.get_agent_card(
                relative_card_path=f"/{self.es_agent_id}.json"
            )
            
            # Create the A2A Agent
            self._agent = A2AAgent(
                name=agent_card.name,
                description=agent_card.description,
                agent_card=agent_card,
                url=self.es_agent_url,
                http_client=self._http_client,
            )
            
            return self._agent
        except Exception as e:
            print(f"Warning: Failed to initialize Elastic agent: {e}")
            self._enabled = False
            return None
    
    async def search_gift(self, gift_name: str, day: int) -> Optional[str]:
        """
        Search Elastic for documents about a specific gift.
        
        Args:
            gift_name: The name of the gift (e.g., "Golden Rings")
            day: The day number (1-12)
        
        Returns:
            The response from Elastic containing relevant documents, or None if not available
        """
        agent = await self._initialize_agent()
        if agent is None:
            return None
        
        try:
            # Create a search query for the gift
            query = f"Find information about {gift_name} from the 12 Days of Christmas, day {day}"
            
            # Run the agent query
            response = await agent.run(query)
            
            # Extract the text from the response messages
            result_text = []
            for message in response.messages:
                if hasattr(message, 'text') and message.text:
                    result_text.append(message.text)
            
            return "\n".join(result_text) if result_text else None
        except Exception as e:
            print(f"Warning: Failed to search for {gift_name}: {e}")
            return None
    
    async def close(self):
        """Close the HTTP client connection."""
        if self._http_client is not None:
            await self._http_client.aclose()
            self._http_client = None
            self._agent = None


# Global instance with thread safety
_elastic_agent = None
_elastic_agent_lock = threading.Lock()


def get_elastic_agent() -> ElasticSearchAgent:
    """Get the global Elastic search agent instance (thread-safe singleton)."""
    global _elastic_agent
    if _elastic_agent is None:
        with _elastic_agent_lock:
            # Double-check locking pattern
            if _elastic_agent is None:
                _elastic_agent = ElasticSearchAgent()
    return _elastic_agent
    return _elastic_agent


async def search_gift_async(gift_name: str, day: int) -> Optional[str]:
    """
    Async function to search for gift information in Elastic.
    
    Args:
        gift_name: The name of the gift
        day: The day number (1-12)
    
    Returns:
        Search results or None
    """
    agent = get_elastic_agent()
    if not agent.is_enabled():
        return None
    return await agent.search_gift(gift_name, day)


def search_gift(gift_name: str, day: int) -> Optional[str]:
    """
    Synchronous wrapper to search for gift information in Elastic.
    
    Args:
        gift_name: The name of the gift
        day: The day number (1-12)
    
    Returns:
        Search results or None
    """
    try:
        # Use asyncio.run() which properly manages the event loop
        return asyncio.run(search_gift_async(gift_name, day))
    except Exception as e:
        print(f"Warning: Failed to search for {gift_name}: {e}")
        return None
