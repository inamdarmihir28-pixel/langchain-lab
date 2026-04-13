import os
from dotenv import load_dotenv

load_dotenv()

print("DEBUG API KEY:", os.getenv("OPENAI_API_KEY"))

# Setup (LLM + Imports)

import os, re, ast, operator as op, requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field, HttpUrl, ValidationError
from bs4 import BeautifulSoup


from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_community.vectorstores import FAISS
from langchain.agents import Tool, AgentType, initialize_agent
from langchain.callbacks.base import BaseCallbackHandler

load_dotenv()
import os
print("DEBUG API KEY:", os.getenv("OPENAI_API_KEY"))

import os  # (only if not already imported)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)
emb = OpenAIEmbeddings(model="text-embedding-3-small")

#Debug Logger

class PrintTrace(BaseCallbackHandler):
    def on_tool_start(self, *args, **kwargs):
        print("\n[Tool start]", kwargs.get("tool", "unknown"), kwargs.get("tool_input"))

    def on_tool_end(self, output, **kwargs):
        print("[Tool end]", str(output)[:200])

trace = [PrintTrace()]

# Knowledge Tool (RAG)
docs = [
    "LangChain helps orchestrate LLM prompts, tools, and retrieval for agents.",
    "LangGraph supports stateful, branching workflows for complex agents.",
    "RAG grounds LLM answers by retrieving relevant documents before generation.",
    "Agentic AI uses tools, memory, and goals for autonomous actions."
]

vs = FAISS.from_texts(docs, emb)
retriever = vs.as_retriever(search_kwargs={"k": 2})

def rag_answer(query: str) -> str:
    hits = retriever.get_relevant_documents(query)
    ctx = "\n".join([h.page_content for h in hits])
    prompt = f"Use only this context to answer.\n\nContext:\n{ctx}\n\nQuestion: {query}"
    return llm.invoke(prompt).content

knowledge_tool = Tool(
    name="Knowledge",
    description="Answer questions from notes using retrieval.",
    func=rag_answer
)


OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.Mod: op.mod
}

# Calculator Tool
def _eval(node):
    if isinstance(node, ast.Num): return node.n
    if isinstance(node, ast.UnaryOp): return OPS[type(node.op)](_eval(node.operand))
    if isinstance(node, ast.BinOp): return OPS[type(node.op)](_eval(node.left), _eval(node.right))
    raise ValueError("Invalid")

def safe_calc(expr: str) -> str:
    node = ast.parse(expr, mode="eval").body
    return str(_eval(node))

calculator_tool = Tool(
    name="Calculator",
    description="Do math calculations",
    func=safe_calc
)


# URL Summarizer

ALLOWLIST = {"openai.com", "python.org"}

class UrlIn(BaseModel):
    url: HttpUrl
    max_words: int = Field(120, ge=40, le=300)

def fetch_and_summarize(payload: str) -> str:
    try:
        m = re.search(r'(https?://\S+)', payload)
        url = m.group(1) if m else payload.strip()
        args = UrlIn(url=url, max_words=120)
    except ValidationError as e:
        return str(e)

    r = requests.get(str(args.url))
    soup = BeautifulSoup(r.text, "html.parser")
    text = " ".join(p.get_text() for p in soup.find_all("p"))

    prompt = f"Summarize in {args.max_words} words:\n{text[:3000]}"
    return llm.invoke(prompt).content

url_tool = Tool(
    name="URLSummarizer",
    description="Summarizes a webpage",
    func=fetch_and_summarize
)




# Create Agent

tools = [calculator_tool, knowledge_tool, url_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    callbacks=trace
)

# Test Query

print("\n--- Calc ---")
print(agent.run("What is (25*8) + 90/2?"))

print("\n--- RAG ---")
print(agent.run("Explain trigonometry simply"))

print("\n--- URL ---")
print(agent.run("Summarize https://python.org"))

