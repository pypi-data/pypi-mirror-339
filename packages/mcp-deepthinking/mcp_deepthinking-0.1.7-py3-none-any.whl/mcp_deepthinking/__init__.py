from .server import serve


def main():
    """MCP Deepthinking main entry point."""
    import asyncio
    import os

    api_key = os.environ.get("GROQ_API_KEY")
    if api_key is None:
        raise ValueError("GROQ_API_KEY environment variable is not set.")
    
    model_id = os.environ.get("MODEL_ID", "deepseek-r1-distill-llama-70b")

    asyncio.run(serve(model_id))


if __name__ == "__main__":
    main()
