import sys
import asyncio
from hermes.core.types import Message, MessageRole
from hermes.memory.manager import UnifiedMemoryManager
from hermes.models.mock_provider import MockModelProvider

def main():
    """Interactive CLI REPL for HermesAG agent."""
    print("=" * 60)
    print("  HERMES AGENT — Autonomous Cognitive Engine (v0.1.0)")
    print("  Type 'exit' or 'quit' to terminate session.")
    print("=" * 60)
    
    memory = UnifiedMemoryManager()
    model = MockModelProvider()
    session_id = "cli_session"

    while True:
        try:
            user_input = input("\nOperator > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Session terminated.")
                break

            user_msg = Message(role=MessageRole.USER, content=user_input)
            augmented_context = memory.build_augmented_context(session_id, user_input)
            
            resp = asyncio.run(model.generate([user_msg], system_prompt=augmented_context))
            assistant_msg = Message(role=MessageRole.ASSISTANT, content=resp.content)
            
            memory.record_interaction(session_id, user_msg, assistant_msg)
            
            print(f"\nHermes > {resp.content}")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
