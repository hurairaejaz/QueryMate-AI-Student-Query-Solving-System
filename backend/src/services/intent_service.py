def detect_intent(query: str) -> str:
    q = query.lower()

    if "course outline" in q or "syllabus" in q:
        return "course_outline"
    if "prerequisite" in q:
        return "prerequisite"
    if "refund" in q:
        return "refund_policy"
    if "fee" in q or "challan" in q:
        return "fee_policy"
    if "transcript" in q:
        return "transcript"
    if "admit card" in q:
        return "admit_card"
    if "semester" in q or "subject" in q:
        return "semester_info"

    return "general"