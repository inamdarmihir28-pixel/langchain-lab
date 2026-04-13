# LangChain Agent Lab

## 🚀 Agent Goal

The goal of this project is to build a simple **AI agent using LangChain** that can intelligently choose between multiple tools to solve user queries.

Instead of responding directly, the agent:

* Understands the user’s intent
* Selects the appropriate tool
* Uses reasoning to generate accurate responses

This demonstrates the core idea of **Agentic AI**, where an AI system can take actions using tools rather than just generating text.
---
## 🏗️ Agent Architecture

This agent follows a modular architecture using LangChain components:

### 1. LLM (Language Model)

* Uses OpenAI (`gpt-4o-mini`)
* Responsible for reasoning and decision-making

### 2. Tools

The agent is equipped with multiple tools:

* **Calculator Tool**
  Performs safe mathematical computations

* **Knowledge Tool (RAG)**
  Retrieves information from local documents using a vector database (FAISS)

* **URL Summarizer Tool**
  Fetches and summarizes content from allowed web pages

### 3. Vector Store & Retriever

* Uses **FAISS** for storing embeddings
* Retrieves relevant context for answering questions (RAG)

### 4. Agent Executor

* Uses `ZERO_SHOT_REACT_DESCRIPTION`
* Enables the agent to:

  * Think step-by-step
  * Choose tools dynamically
  * Execute actions

### 5. Callbacks (Tracing)

* Custom callback prints tool usage and outputs
* Helps visualize internal execution
---

✅ Capabilities

* Performs **multi-step reasoning**
* Dynamically selects the correct tool
* Answers questions using **retrieval (RAG)**
* Executes **mathematical calculations safely**
* Summarizes content from selected websites
* Provides transparent reasoning via verbose mode
---

 ❌ Limitations
* Limited to **predefined tools only**
* URL summarization works only for **allowlisted domains**
* Knowledge tool depends on **local static documents**
* Not suitable for real-time or large-scale data retrieval
* Performance depends on the underlying LLM
---

## ⭐ Key Feature: Verbose Mode 
One of the most important features of this agent is **Verbose Mode**, which enables full visibility into the agent’s reasoning process.

### 🔍 What is Verbose Mode?
Verbose Mode prints the internal decision-making steps of the agent, including:

* Thought process
* Tool selection
* Tool inputs
* Tool outputs
* Final answer
---

### 🧠 Why it matters
Verbose Mode implements **reasoning frameworks** that help the agent:

* Perform **intelligent tool selection**
* Clearly show **decision paths**
* Handle **complex, multi-step problem solving**
* Support **conversational reasoning across steps**
---

### 🧪 Example Behavior
When given a query like:

```text
What is (25*4) + 90/3?
```

The agent will:

1. Recognize this as a math problem
2. Select the **Calculator tool**
3. Execute the calculation
4. Return the final answer

All intermediate steps are visible in verbose mode.
---
### 💡 Why this is powerful

* Makes AI behavior **transparent and explainable**
* Helps developers **debug and improve agents**
* Enables better understanding of **how decisions are made**
* Essential for building **trustworthy AI systems**
---
## 🔐 API Key Setup

This project requires an OpenAI API key.
1. Copy `.env.example` → `.env`
2. Add your key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

* Uses tools
* Reasons step-by-step
* Solves real problems
* Exposes its thinking via verbose mode

It is a strong foundation for building more advanced **Agentic AI systems**.
