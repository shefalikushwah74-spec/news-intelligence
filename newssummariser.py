from dotenv import load_dotenv
load_dotenv()
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# tools are also runnables
search_tools=TavilySearchResults(max_result=5)
llm_model=ChatGroq(model="openai/gpt-oss-20b")
prompt=ChatPromptTemplate.from_template(
    """
you are a helpful assistant
summarise the following news into clear bullet points
{news}"""
)
parser=StrOutputParser()
chain=prompt | llm_model | parser
news_result=search_tools.run("Latest AI news of 2026")
result=chain.invoke(news_result)
print(result)