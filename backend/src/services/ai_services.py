from typing import Optional


class AIService:
    @staticmethod
    def decide_tone(query_text: str) -> str:
        """
        Decide response tone roughly from user query style.
        """
        if not query_text:
            return "formal"

        q = query_text.lower()

        informal_markers = ["kya", "hay", "hai", "kr", "pls", "please bata", "kia"]
        if any(marker in q for marker in informal_markers):
            return "natural"

        return "formal"

    @staticmethod
    def build_evidence_text(best_kb: Optional[dict], chunk_results: list[dict]) -> str:
        evidence_parts = []

        if best_kb and best_kb.get("kb"):
            kb = best_kb["kb"]
            evidence_parts.append(f"KB Title: {kb.title}")

        for item in chunk_results[:2]:
            chunk = item["chunk"]
            short_text = chunk.chunk_text[:200].strip()
            evidence_parts.append(f"Chunk {chunk.chunk_index}: {short_text}")

        return "\n".join(evidence_parts)

    @staticmethod
    def build_answer_from_retrieved_data(
        query_text: str,
        best_kb: Optional[dict],
        chunk_results: list[dict],
        tone: str = "formal",
    ) -> dict:
        """
        Build final answer from KB + chunk results.
        This is template-based for now.
        """
        kb_item = best_kb["kb"] if best_kb else None
        kb_score = best_kb["score"] if best_kb else 0.0

        top_chunk = chunk_results[0]["chunk"] if chunk_results else None
        chunk_score = chunk_results[0]["score"] if chunk_results else 0.0

        answer_text = None

        if kb_item and top_chunk:
            if tone == "natural":
                answer_text = (
                    f"According to the available knowledge base, {kb_item.content.strip()} "
                    f"Additional related document content says: {top_chunk.chunk_text[:350].strip()}"
                )
            else:
                answer_text = (
                    f"Based on the available knowledge base, {kb_item.content.strip()} "
                    f"In addition, the related document content states: {top_chunk.chunk_text[:350].strip()}"
                )

        elif kb_item:
            if tone == "natural":
                answer_text = kb_item.content.strip()
            else:
                answer_text = f"Based on the knowledge base, {kb_item.content.strip()}"

        elif top_chunk:
            if tone == "natural":
                answer_text = f"The related document says: {top_chunk.chunk_text[:400].strip()}"
            else:
                answer_text = f"According to the related document, {top_chunk.chunk_text[:400].strip()}"

        evidence = AIService.build_evidence_text(best_kb, chunk_results)

        return {
            "answer_text": answer_text,
            "kb_score": kb_score,
            "chunk_score": chunk_score,
            "evidence": evidence,
        }
        
    @staticmethod          
    def build_answer_from_kb(query_text: str, kb_rows: list):
        """
        Build answer from matched KnowledgeBase rows.
        Used by query_service.py.
        """
        if not kb_rows:
            return None

        kb = kb_rows[0]

        title = getattr(kb, "title", "Relevant Information")
        content = getattr(kb, "content", "")

        if not content or not str(content).strip():
            return None

        q = query_text.lower()

        if "outline" in q or "syllabus" in q:
            return (
                # f"Here is the answer for {title}:\n\n"
                f"{content.strip()}"
            )

        if (
            "process" in q
            or "procedure" in q
            or "how" in q
            or "apply" in q
            or "fee" in q
            or "certificate" in q
            or "card" in q
            or "noc" in q
            or "transcript" in q
        ):
            return (
                f"Here is the process for {title}:\n\n"
                f"{content.strip()}"
            )

        return (
            f"Based on the available knowledge base information:\n\n"
            f"{content.strip()}"
        )
    @staticmethod
    def generate_fallback_message(tone: str = "formal") -> str:
        if tone == "natural":
            return (
                "Unfortunately, we have not been able to find a reliable answer from the current knowledge base related to your query but "
                "your query has been sent for manual review. Thank you for your patience!"
            )

        return (
            "A reliable answer could not be generated from the current knowledge base. "
            "Your query has been forwarded for manual review."
        )