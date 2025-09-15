
import uuid

import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    AgentCard,
    AgentCapabilities,
    AgentSkill,
    Message,
    MessageSendParams,
    Part,
    Role,
    SendMessageRequest,
    TextPart
)

from remote_agent_connection import RemoteAgentConnection

PUBLIC_AGENT_CARD_PATH = "/.well-known/agent.json"
BASE_URL = "http://localhost:8080"

async def main():
    async with httpx.AsyncClient(timeout=None) as httpx_client:
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=BASE_URL
        )

        final_agent_card_to_use: AgentCard | None = None

        try:
            print(f"Getting Agent card from {BASE_URL}{PUBLIC_AGENT_CARD_PATH}...")
            _public_card = await resolver.get_agent_card()

             
            final_agent_card_to_use = _public_card
        except Exception as e:
            print(f"Error fetching agent card: {e}")
            raise RuntimeError("Failed to fetch agent card")

        agent_connection = RemoteAgentConnection(final_agent_card_to_use, BASE_URL)

        print("A2A client initialized")

        task_id = None
        context_id = str(uuid.uuid4())
        while True:
            user_input = input("Enter prompt or type 'quit to quit: ")
            print("\n")

            if user_input == 'quit':
                break
            
            message_payload = Message(
                role=Role.user,
                message_id=str(uuid.uuid4()),
                task_id=task_id,
                context_id=context_id,
                parts=[Part(root=TextPart(text=user_input))]
            )

            request = SendMessageRequest(
                id=str(uuid.uuid4()),
                params=MessageSendParams(
                    message=message_payload
                )
            )

            response = await agent_connection.send_message(request)

            if context_id == None:
                context_id = response.root.result.context_id
                task_id = response.root.result.id

            is_complete = response.root.result.status.state == 'completed'

            if is_complete:
                print(response.root.result.artifacts[0].parts[0].root.text)
                task_id = None

            else:
                print(response.root.result.status.message.parts[0].root.text)

if __name__ == "__main__":
    import asyncio
    
    asyncio.run(main())