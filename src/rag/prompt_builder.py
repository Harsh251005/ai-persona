from typing import List

from langchain_core.documents import Document


class PromptBuilder:
    """
    Responsible for constructing prompts for the AI persona.
    """

    SYSTEM_PROMPT = """
You are Harsh Dharnidharka's AI Persona.

Your job is to answer questions about Harsh's:

- Skills
- Experience
- Projects
- Education
- Technical expertise
- Career background

Use ONLY the provided context.

Rules:
1. If the answer exists in the context, answer clearly and confidently.
2. If the answer cannot be found in the context, say:
   "I don't have enough information to answer that based on the available context."
3. Do not invent projects, skills, achievements, or experiences.
4. Prefer concise and factual responses.
5. When discussing projects, mention relevant technologies whenever available.
"""

    @staticmethod
    def build_context(
        documents: List[Document],
    ) -> str:
        """
        Converts retrieved documents into a context block.
        """

        sections = []

        for idx, doc in enumerate(documents, start=1):

            source_type = doc.metadata.get(
                "source_type",
                "unknown"
            )

            source_id = doc.metadata.get(
                "source_id",
                "unknown"
            )

            sections.append(
                f"""
[DOCUMENT {idx}]
Source Type: {source_type}
Source ID: {source_id}

{doc.page_content}
"""
            )

        return "\n\n".join(sections)

    @classmethod
    def build_prompt(
        cls,
        query: str,
        documents: List[Document],
    ) -> str:
        """
        Creates the final prompt for the LLM.
        """

        context = cls.build_context(
            documents
        )

        return f"""
{cls.SYSTEM_PROMPT}

CONTEXT:

{context}

USER QUESTION:

{query}

ANSWER:
"""