from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, web_scrape
from dotenv import load_dotenv

load_dotenv()

# Model setup
llm = ChatMistralAI(model="mistral-small-latest", temperature=0)

# 1st agent: web search agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
    )

# 2nd agent: web scrape agent
def build_scrape_agent():
    return create_agent(
        model=llm,
        tools=[web_scrape],
    )

# Writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a comprehensive report on the following topic:
Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings
- Conclusion
- Sources

Be detailed, factual and professional.""")
])

writer_chain = writer_prompt | llm | StrOutputParser()

# Critic chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a critical reviewer. Review reports for accuracy, clarity, and completeness."),
    ("human", """Review the following report strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas for Improvement:
- ...
- ...

One line verdict: ..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()