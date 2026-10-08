## promptbuilder

Builds the prompt assembly stage of a RAG system using simulated retrieved document chunks.

Instead of connecting a vector database and LLM, we focus on the smallest possible version of the prompt-building component.

User question
│
▼
Retrieved document chunks
│
▼
Prompt Builder
│
├── system instructions
│
├── retrieved context
│
├── source labels
│
├── user's question
│
└── citation instructions
│
▼
complete RAG prompt
│
▼
LLM

    Takes the user's question.

question

    Takes simulated retrieved document chunks.

retrieved_chunks

    Formats each chunk with its source.

f"[Source: {chunk['source']}]\n{chunk['text']}"

    Combines the system prompt, context, question, and instructions.

prompt = f"""
{system_prompt}

CONTEXT:
{context}

USER QUESTION:
{question}

INSTRUCTIONS:
...
"""

    Estimates the prompt's token count using the assignment's approximation.

estimated_tokens = len(prompt) / 4

    Tests multiple scenarios:
    relevant question + relevant context
    different question + different context
    question that cannot be answered from the supplied context

The prompt instructs the eventual LLM to:

answer from context only

- do not invent information
- cite the provided sources
- admit when the context is insufficient

This represents one stage of a larger RAG system.

Uses:

assembling context for an LLM

grounding LLM responses

source/citation handling

reducing hallucinations

preparing retrieved information for generation

RAG (Retrieval-Augmented Generation)

Architecture:

retrieve → assemble → generate → respond

For this assignment, we implemented and tested:

retrieved chunks
↓
prompt assembly
↓
complete RAG prompt

The next stages would be:

query → embed → retrieve → assemble → generate

______________________________________________________________

## ollama_explorer


Builds a small experimental framework for testing a locally hosted LLM through Ollama.

Instead of building a full RAG pipeline, the code focuses on sending prompts to an Ollama model and measuring how different prompting conditions affect the generated responses.

User prompt 
│ 
▼ 
generate() 
│ 
├── system prompt 
├── user question 
├── model selection 
├── temperature 
└── Ollama API request 
│ 
▼ Local Ollama LLM 
│ 
▼ Generated response + elapsed time

perf_counter()?

- We want to measure how long the request takes.

raise_for_status()?

- Instead of allowing the code to continue with a mysterious JSON error if Ollama returns an HTTP error, this gives us an immediate, meaningful failure for defensive programming.



Experiment 1 — Same Question, Different System Prompts

Tests how different system prompts affect the same question.

Uses:

    no system prompt
    "Explain like I'm 5"
    senior software architect instructions

The system prompt significantly changed the response style. The response without a system prompt provided a general explanation of APIs. The "Explain like I'm 5 years old" prompt produced simpler vocabulary and used a lemonade stand analogy. The senior software architect prompt produced a more technical response using concepts such as endpoints, HTTP methods, scalability

Experiment 2 — RAG-Style Context Grounding

Tests RAG-style context grounding using a fictional Acme Library context.

The model receives instructions to:

    answer using only the supplied context
    avoid inventing information
    explicitly state when the context does not contain an answer

Tests both:

    a question that can be answered from the context
    a question that cannot be answered from the context

The model correctly answered the question that could be answered from the supplied context. When asked who the lead developer was, the model correctly stated that the context did not provide that information. This demonstrated successful context grounding for these tests, although grounding instructions do not guarantee that a model will always refuse unsupported questions.

Experiment 3 — Response Timing

Tests RAG-style context grounding using a fictional Acme Library context.

The model receives instructions to:

    answer using only the supplied context
    avoid inventing information
    explicitly state when the context does not contain an answer

Tests both:

    a question that can be answered from the context
    a question that cannot be answered from the context
    
The short prompt took 54.75 seconds, the medium prompt took 59.33 seconds, and the long prompt took 101.69 seconds. The longer prompt had the longest response time. However, the model also generated different amounts of output for each prompt, so the results measure more than just input prompt length. Multiple trials with controlled output lengths would provide a stronger comparison.

Experiment 4 — Temperature

At temperature 0.1, the model produced a descriptive but relatively predictable response. At temperature 1.0, the response used somewhat different and more varied descriptive language. Multiple runs would be needed to determine whether the higher temperature consistently produces greater variation.

Overall Observation

The experiments demonstrated that system prompts can change response style, supplied context can help ground model responses, prompt and output characteristics affect response time, and temperature can influence response variation.

