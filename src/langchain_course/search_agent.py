from typing import List

import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field
from tavily import TavilyClient

load_dotenv()

tavily_client = TavilyClient()


@tool
def search(query: str):
    """
    Tool that searches over internet
    Args:
        query: string to search over internet
    Returns:
        dict: result of the search
    """
    print(f"using search function for {query}")
    return tavily_client.search(query)


@tool
def verify_job_url(url: str) -> str:
    """Checks if a LinkedIn or career page job posting is still active."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        text = resp.text.lower()
        if "no longer accepting applications" in text or "job is closed" in text:
            return f"CLOSED: {url}"
        return f"ACTIVE: {url}"
    except Exception as e:
        return f"ERROR checking {url}: {e}"


class Source(BaseModel):
    """
    Schema for source used by the agent
    """

    url: str = Field(description="The URL of the source")


class AgentResponse(BaseModel):
    """
    Schema for agent response with answer and sources
    """

    answer: str = Field(description="Agent answer to the user query")
    sources: List[Source] = Field(
        default_factory=list, description="List of sources used to generate the answer"
    )


if __name__ == "__main__":
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        # model="gemini-3.7-flash",
        temperature=0,
    )
    # tools = [search,verify_job_url]
    tools = [
        TavilySearch(max_results=7, days=7, search_depth="advanced"),
        verify_job_url,
    ]
    agent = create_agent(
        model=llm,
        tools=tools,
        response_format=AgentResponse,
        system_prompt=(
            "You are an expert technical recruiter and job search assistant.\n"
            "Guidelines:\n"
            "1. Only return actively open, full-time positions. Strictly exclude closed roles, 'no longer accepting applications', and contract/temporary positions.\n"
            "2. If search results show expired or closed postings, run additional targeted searches with date filters (e.g. 'posted past week') until you find 3 confirmed active listings.\n"
            "3. Check the snippet text carefully for application status before including it in the final response."
        ),
    )
    # result = agent.invoke({"messages": [HumanMessage(content="What is the weather in Charlotte")]})
    result = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content=(
                        "Search for 3 currently active job postings (posted within the last 14 days) "
                        "for an AI Engineer using LangChain in the Charlotte, NC area on LinkedIn. "
                        "List their details with direct LinkedIn URLs. "
                        "Do NOT include roles that are expired, 'no longer accepting applications', or contracting."
                    )
                )
            ]
        }
    )
    print(result)
