from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="HuggingFaceTB/SmolLM2-1.7B-Instruct",
    max_new_tokens=180,
)

def build_context(candidates: list[dict], top_k: int = 3) -> str:
    context_blocks = []
    for idx, item in enumerate(candidates[:top_k], start=1):
        context_blocks.append(
            f"[Source {idx}]\n"
            f"Title: {item['title']}\n"
            f"Content: {item['content']}\n"
        )
    return "\n".join(context_blocks)


def generate_grounded_answer(user_query: str, candidates: list[dict]) -> str:
    if not candidates:
        return "NOT_ENOUGH_CONTEXT"

    context = build_context(candidates, top_k=3)

    prompt = f"""
You are a university academic assistant.

Answer ONLY from the provided knowledge base context.
If the answer is not clearly present in the context, reply exactly:
NOT_ENOUGH_CONTEXT

Keep the answer short, clear, and student-friendly.
Do not invent rules, dates, policies, or steps.

User Query:
{user_query}

Knowledge Base Context:
{context}

Answer:
""".strip()

    result = generator(prompt, do_sample=False)
    text = result[0]["generated_text"]

    # extract only answer part
    if "Answer:" in text:
        answer = text.split("Answer:", 1)[-1].strip()
    else:
        answer = text.strip()

    return answer