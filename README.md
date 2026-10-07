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

---
