import logging
import os
import warnings

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

warnings.filterwarnings("ignore", category=UserWarning, module="langchain_google_genai")
logging.getLogger("google_genai").setLevel(logging.ERROR)

load_dotenv()


def main():
    print("Hello from langchain course")

    information = """
    Benjamin Todd Shelton (born October 9, 2002) is an American professional tennis player. He has been ranked world No. 4 in men's singles by the Association of Tennis Professionals (ATP), achieved in September 2026. Shelton has won seven ATP Tour singles titles, including two Masters 1000 trophies at the 2025 and 2026 Canadian Opens. His best results at the majors is reaching the final of the 2026 US Open. He is the current American No. 1 player in men's singles.[5]

    Shelton has won one doubles title, at the 2026 U.S. Men's Clay Court Championships with Andrés Andrade, and has a career-high doubles ranking of world No. 68, attained in May 2024.
    """

    summary_template = """
        Given the informatioollaman {information} about a person, I want you to create:
        1. A short summary
        2. Two interesting facts about them       
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    # llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")
    # ollama pull gemma3:270m
    # ollama run gemma3:270m
    # ollama list
    llm = ChatOllama(temperature=0, model="gemma3:270m")

    chain = summary_prompt_template | llm  # | StrOutputParser()
    result = chain.invoke({"information": information})
    print(result.text)


if __name__ == "__main__":
    main()
