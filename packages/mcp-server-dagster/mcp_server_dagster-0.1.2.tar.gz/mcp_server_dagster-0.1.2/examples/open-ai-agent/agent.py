import asyncio

from agents import Agent, ModelSettings, Runner
from agents.mcp import MCPServerSse


async def main():
    conversation_history = []

    async with MCPServerSse(
        name="Dagster MCP Server",
        params={
            "url": "http://0.0.0.0:8000/sse",
        },
    ) as server:
        tools = await server.list_tools()
        print(f"Available tools: {[x.name for x in tools]}")

        agent = Agent(
            name="Dagster Explorer",
            instructions="""You are a Data Engineering Assistant specializing in Dagster workflows.
You help users explore their Dagster instance, monitor pipelines, and troubleshoot issues.
When interacting with the Dagster instance:
1. Start by exploring available repositories, jobs, and assets
2. Provide clear, concise explanations of pipeline components
3. Help users materialize assets and monitor runs
4. Summarize complex Dagster information in a user-friendly way
Always confirm actions before materializing assets or launching jobs.""",
            mcp_servers=[server],
            model_settings=ModelSettings(tool_choice="auto", parallel_tool_calls=True),
        )

        while True:
            user_input = input("\nEnter your question (or 'exit' to quit): ")
            if user_input.lower() == "exit":
                break

            if conversation_history:
                context = "\n".join(conversation_history)
                full_input = (
                    f"Previous conversation:\n{context}\n\nNew question: {user_input}"
                )
            else:
                full_input = user_input

            print("\nProcessing your request...")
            result = await Runner.run(starting_agent=agent, input=full_input)
            print(f"\nResponse: {result.final_output}")

            conversation_history.append(f"User: {user_input}")
            conversation_history.append(f"Assistant: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
