def build_rag_prompt(question, retrieved_chunks):
    """Build a RAG prompt from a question and retrieved document chunks."""

    system_prompt = """You are a helpful assistant.
Answer the user's question using only the provided context.
If the context does not contain enough information to answer,
say that you do not have enough information.

Cite the source of information in your answer using the source labels
provided in the context.
"""

    context = "\n\n".join(
        f"[Source: {chunk['source']}]\n{chunk['text']}"
        for chunk in retrieved_chunks
        )

    prompt = f"""{system_prompt}

CONTEXT:
{context}

USER QUESTION:
{question}

INSTRUCTIONS:
- Answer using only the provided context.
- Do not invent information.
- Cite the relevant source labels in your answer.
"""

    return prompt


def print_prompt(question, retrieved_chunks):
    """Build and print a RAG prompt with an estimated token count."""

    prompt = build_rag_prompt(question, retrieved_chunks)

    character_count = len(prompt)
    estimated_tokens = character_count / 4

    print("=" * 70)
    print("RAG PROMPT")
    print("=" * 70)
    print(prompt)

    print("-" * 70)
    print(f"Character count: {character_count}")
    print(f"Estimated token count: {estimated_tokens:.0f}")
    print("=" * 70)
    print()



# TEST 1: Employee Vacation Question
# ==============================================

chunks_1 = [
    {
        "source": "employee_handbook.pdf",
        "text": "Employees receive 15 days of paid vacation each year.",
    },
    {
        "source": "benefits_guide.pdf",
        "text": "Vacation requests should be submitted at least two weeks in advance.",
    },
]

print_prompt(
    "How many vacation days do employees receive?",
    chunks_1,
    )



# TEST 2: Product Battery Question
# ===============================================

chunks_2 = [
    {
        "source": "product_manual.pdf",
        "text": "The device battery takes approximately two hours to fully charge.",
    },
    {
        "source": "product_manual.pdf",
        "text": "A fully charged battery provides approximately eight hours of normal use.",
    },
]

print_prompt(
    "How long does the battery take to charge?",
    chunks_2,
    )

# Test 3: Question not answered by the retrieved context
#================================================
print_prompt(
    "What is the company's parental leave policy?",
    chunks_1,
    )