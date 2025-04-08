import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

dotenv.load_dotenv()


def deepthinking(query: str) -> str:
    """

    Args:
        query:
    """
    llm = ChatGroq(
        api_key=os.environ.get("GROQ_API_KEY"),
        model=os.environ.get("MODEL_ID", "deepseek-r1-distill-llama-70b"),# deepseek-r1-distill-llama-70b, deepseek-r1-distill-qwen-32b, qwen-qwq-32b
        streaming=False,
        max_tokens=8192,
        max_retries=2,
        temperature=1.0,
        stop="</think>",
    )

    completions = llm.invoke(query)
    print(f"${completions.content}</think>" )


if __name__ == "__main__":
    deepthinking("인생이란?")
