import asyncio
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="/Users/olivier/.local/bin/uv",  # Executable
    args=[
        "--directory",
        "/Users/olivier/Dev/boring-news/boring-news-backend/mcp",
        "run", 
        "boring-news-mcp.py"
    ],  # Server script
    env=None,  # Optional environment variables
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("Available tools:", tools)

            # Get articles by date
            articles = await session.call_tool(
                "get_articles_by_date", 
                arguments={
                    "date": "2024-03-28",
                    "category": "science",
                    "tags": "AI,technology"
                }
            )
            print("\nFiltered articles:")
            print(articles)
            
            # Get articles by person
            person_articles = await session.call_tool(
                "get_articles_by_person",
                arguments={"person": "Emmanuel Macron"}
            )
            print("\nArticles mentioning person:")
            print(person_articles)
            
            # Get similar articles
            similar = await session.call_tool(
                "get_similar_articles",
                arguments={"text": "impact de l'intelligence artificielle sur la société"}
            )
            print("\nSimilar articles:")
            print(similar)

if __name__ == "__main__":
    asyncio.run(run()) 