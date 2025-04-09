import logging
from mcp.server.fastmcp import FastMCP
from langchain_groq import ChatGroq

def serve(api_key: str, model_id: str = "deepseek-r1-distill-llama-70b"):
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    mcp = FastMCP("deepthinking")

    allowed_models = [
        "deepseek-r1-distill-llama-70b",
        "deepseek-r1-distill-qwen-32b",
        "qwen-qwq-32b",
    ]
    if model_id not in allowed_models:
        logging.warning(
            f"The specified MODEL_ID '{model_id}' is not allowed, use default model 'deepseek-r1-distill-llama-70b'."
        )
        model_id = "deepseek-r1-distill-llama-70b"

    llm = ChatGroq(
        api_key=api_key,
        model=model_id,
        streaming=False,
        max_tokens=8192,
        max_retries=2,
        temperature=1.0,
        stop="</think>",
    )

    @mcp.tool()
    async def deepthinking(query: str) -> str:
        """
        A tool that helps AI perform deep thinking (reasoning) processes. It can be used for complex problem solving, planning, multi-step reasoning, and more.
        Args:
            query: The input query or prompt for the AI to process.
        """

        completions = llm.invoke(query)
        return f"{completions.content}</think>"

    mcp.run(transport="stdio")
