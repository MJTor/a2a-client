import logging
import httpx

from a2a.client import A2AClient
from a2a.types import (
    AgentCard,
    SendMessageRequest,
    SendMessageResponse
)

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class RemoteAgentConnection:
    def __init__(self, agent_card: AgentCard, agent_url: str):
        #print(f'Agent Card initialized: {agent_card.model_dump_json(indent=2)}\n\nWith url: {agent_url}')

        self._httpx_client = httpx.AsyncClient(timeout=None)
        self.agent_client = A2AClient(
            httpx_client=self._httpx_client,
            agent_card=agent_card,
            url=agent_url
        )
        self.agent_card = agent_card
    
    def get_agent(self) -> AgentCard:
        
        return self.agent_card
    
    async def send_message(
        self,
        message_request: SendMessageRequest
    ) -> SendMessageResponse:
    
        return await self.agent_client.send_message(message_request)
        