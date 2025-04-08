import os

import dotenv
from langchain_groq import ChatGroq
from mcp.server.fastmcp import FastMCP

dotenv.load_dotenv()

mcp = FastMCP("deepthinking")


@mcp.tool()
async def deepthinking(query: str) -> str:
    """
    A tool that helps AI perform deep thinking (reasoning) processes. It can be used for complex problem solving, planning, multi-step reasoning, and more.
    Args:
        query: The input query or prompt for the AI to process.
    """
    allowed_models = [
        "deepseek-r1-distill-llama-70b",
        "deepseek-r1-distill-qwen-32b",
        "qwen-qwq-32b",
    ]
    model_id = os.environ.get("MODEL_ID", "deepseek-r1-distill-llama-70b")
    if model_id not in allowed_models:
        print(
            f"Warning: The specified MODEL_ID '{model_id}' is not allowed, use default model 'deepseek-r1-distill-llama-70b'."
        )
        model_id = "deepseek-r1-distill-llama-70b"

    llm = ChatGroq(
        api_key=os.environ.get("GROQ_API_KEY"),
        model=model_id,
        streaming=False,
        max_tokens=8192,
        max_retries=2,
        temperature=1.0,
        stop="</think>",
    )

    completions = llm.invoke(query)
    return f"{completions.content}</think>"


def serve():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    serve()
