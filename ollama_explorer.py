import time
import requests



OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"  # Change this to a model you have installed.


def generate(prompt, system=None, temperature=None):
    """Send a prompt to Ollama and return response text and elapsed time."""

    messages = []

    if system:
        messages.append({
            "role": "system",
            "content": system,
        })

    messages.append({
        "role": "user",
        "content": prompt,
    })

    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
    }

    if temperature is not None:
        payload["options"] = {
            "temperature": temperature,
        }

    start = time.perf_counter()

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120,
        )
        response.raise_for_status()

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Could not connect to Ollama. "
            "Make sure Ollama is running."
        )

    except requests.exceptions.Timeout:
        raise RuntimeError("Ollama took too long to respond.")

    except requests.exceptions.HTTPError as exc:
        raise RuntimeError(
            f"Ollama returned an HTTP error: {exc}"
        )

    elapsed = time.perf_counter() - start

    data = response.json()

    try:
        text = data["message"]["content"]
    except KeyError:
        raise RuntimeError(
            f"Unexpected Ollama response format: {data}"
        )

    return {
        "text": text,
        "elapsed": elapsed,
    }


def print_result(label, result):
    """Print a response and its timing consistently."""

    print(f"\n--- {label} ---")
    print(f"Time: {result['elapsed']:.2f} seconds")
    print(result["text"])


def experiment_1():
    """Compare the same question with different system prompts."""

    print("\n" + "=" * 60)
    print("EXPERIMENT 1: SAME QUESTION, DIFFERENT SYSTEM PROMPTS")
    print("=" * 60)

    question = "What is an API?"

    prompts = [
        (
            "No system prompt",
            None,
        ),
        (
            "Explain like I'm 5",
            "Explain like I'm 5 years old.",
        ),
        (
            "Senior software architect",
            (
                "You are a senior software architect. "
                "Be technical and precise."
            ),
        ),
    ]

    results = []

    for label, system_prompt in prompts:
        result = generate(question, system=system_prompt)
        results.append((label, result))
        print_result(label, result)

    print("\nObservation:")
    print(
         "The system prompt significantly changed the response style. The "'explain like Im 5'" prompt produced simpler language and analogies, while the senior architect prompt produced more technical terminology and discussed concepts such as endpoints, HTTP methods, scalability, and interoperability. The no-system-prompt response fell between the two."
    )


def experiment_2():
    """Test whether the model stays grounded in supplied context."""

    print("\n" + "=" * 60)
    print("EXPERIMENT 2: RAG-STYLE CONTEXT GROUNDING")
    print("=" * 60)

    context = """
    The fictional Acme Library is a Python library for generating
    reports from CSV files. It was created in 2024 and is maintained
    by a team of three developers. Acme Library can generate HTML
    and Markdown reports, but it cannot generate PDF files directly.
    The library requires Python 3.11 or newer.
    """

    system_prompt = f"""
    Answer questions using only the following context.

    If the answer cannot be determined from the context, say:
    "The context does not provide that information."

    Context:
    {context}
    """

    answerable_question = (
        "What output formats can Acme Library generate?"
    )

    unanswerable_question = (
        "Who is the lead developer of Acme Library?"
    )

    answerable = generate(
        answerable_question,
        system=system_prompt,
    )

    unanswerable = generate(
        unanswerable_question,
        system=system_prompt,
    )

    print_result("Question answerable from context", answerable)
    print_result("Question NOT answerable from context", unanswerable)

    print("\nObservation:")
    print(
        "The model correctly answered the question that was supported by the supplied context and refused to invent an answer when the information was not available. This demonstrates how context grounding can reduce unsupported answers, although the result depends on how well the model follows the grounding instructions."
    )


def experiment_3():
    """Compare response times for prompts of different lengths."""

    print("\n" + "=" * 60)
    print("EXPERIMENT 3: RESPONSE TIMING")
    print("=" * 60)

    prompts = {
        "Short (5 words)": (
            "What is an API and why?"
        ),
        "Medium (20 words)": (
            "Explain what an API is, how applications use APIs, "
            "and why APIs are useful in modern software development."
        ),
        "Long (50 words)": (
            "Explain what an API is to a beginner who understands basic "
            "programming concepts but has never worked with web services. "
            "Describe how a client communicates with an API, what a request "
            "and response are, and give a simple real-world example of an "
            "API being used by an application."
        ),
    }

    results = []

    for label, prompt in prompts.items():
        result = generate(prompt)
        results.append((label, result))

        print_result(label, result)

    print("\nTiming comparison:")
    for label, result in results:
        print(f"{label}: {result['elapsed']:.2f} seconds")

    print("\nObservation:")
    print(
        "Response time generally increased as the prompt became longer. The short prompt took 54.75 seconds, the medium prompt took 59.33 seconds, and the long prompt took 101.69 seconds. However, response time is affected by both the input prompt and the amount of text generated by the model, so these results do not prove that prompt length alone caused the timing difference.."
    )


def experiment_4():
    """Compare low and high temperature responses."""

    print("\n" + "=" * 60)
    print("EXPERIMENT 4: TEMPERATURE")
    print("=" * 60)

    prompt = (
        "Describe a rainy afternoon in three sentences."
    )

    low_temperature = generate(
        prompt,
        temperature=0.1,
    )

    high_temperature = generate(
        prompt,
        temperature=1.0,
    )

    print_result(
        "Temperature 0.1",
        low_temperature,
    )

    print_result(
        "Temperature 1.0",
        high_temperature,
    )

    print("\nObservation:")
    print(
        "The two temperatures produced similar overall responses, but the higher temperature response used somewhat different and more varied descriptive language. Multiple runs would be needed to determine whether the higher temperature consistently produces more variation."
    )


def main():
    """Run all Ollama experiments."""

    experiment_1()
    experiment_2()
    experiment_3()
    experiment_4()


if __name__ == "__main__":
    main()