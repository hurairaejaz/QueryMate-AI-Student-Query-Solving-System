def clamp_score(value: float, min_value: float = 0.0, max_value: float = 1.0) -> float:
    return max(min_value, min(value, max_value))


def calculate_confidence(kb_score: float = 0.0, chunk_score: float = 0.0, has_answer_text: bool = False) -> float:
    """
    Create a simple confidence score from retrieval signals.

    Args:
        kb_score: Score from KB match
        chunk_score: Score from chunk match
        has_answer_text: Whether answer text was successfully generated

    Returns:
        Confidence score between 0 and 1
    """
    score = (kb_score * 0.5) + (chunk_score * 0.4)

    if has_answer_text:
        score += 0.1

    return clamp_score(score)


def should_escalate(confidence_score: float, has_evidence: bool) -> bool:
    """
    Decide whether query should go to escalation.

    Escalate if:
    - no evidence found
    - confidence too low
    """
    if not has_evidence:
        return True

    return confidence_score < 0.45