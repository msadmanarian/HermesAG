import asyncio
from hermes.memory.manager import UnifiedMemoryManager
from hermes.models.mock_provider import MockModelProvider
from hermes.core.types import Message, MessageRole

async def main():
    print("=== HermesAG Quickstart Demo ===")
    memory = UnifiedMemoryManager()
    model = MockModelProvider(default_reply="Hermes cognitive pipeline initialized. All 4 memory tiers are synchronized.")
    
    query = "Analyze my Obsidian Second Brain and summarize today's goals."
    context = memory.build_augmented_context("quickstart_sess", query)
    
    resp = await model.generate([Message(role=MessageRole.USER, content=query)], system_prompt=context)
    print(f"Agent Reply:\n{resp.content}")

if __name__ == "__main__":
    asyncio.run(main())
