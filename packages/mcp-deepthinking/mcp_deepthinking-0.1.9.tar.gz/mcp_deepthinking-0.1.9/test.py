import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

dotenv.load_dotenv()


# def deepthinking(query: str) -> str:
#     """

#     Args:
#         query:
#     """
#     llm = ChatGroq(
#         api_key=os.environ.get("GROQ_API_KEY"),
#         model=os.environ.get("MODEL_ID", "deepseek-r1-distill-llama-70b"),# deepseek-r1-distill-llama-70b, deepseek-r1-distill-qwen-32b, qwen-qwq-32b
#         streaming=False,
#         max_tokens=8192,
#         max_retries=2,
#         temperature=1.0,
#         stop="</think>",
#     )

#     completions = llm.invoke(query)
#     print(f"${completions.content}</think>" )


# if __name__ == "__main__":
#     deepthinking("인생이란?")


from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0.0, api_key="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")

async def main():
    async with MultiServerMCPClient(
        {
            "mcp-deepthinking": {
                "command": "uvx",
                # Make sure to update to the full absolute path to your math_server.py file
                "args": ["mcp-deepthinking@latest"],
                "env": {
                    "GROQ_API_KEY": "matgsk_XiStwY4z4REYaKrdhl5oWGdyb3FYFHR7GW7WLSnfEumHh5LudIFE"
                },
                "transport": "stdio",
            }
        }
    ) as client:
        agent = create_react_agent(model, client.get_tools())
        response = await agent.ainvoke({"messages": "샐리(여자)는 형제가 3명 있습니다. 각 형제는 자매가 2명 있습니다. 샐리는 자매가 몇 명입니까? mcp-deepthinking 도구를 사용하세요."})
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())