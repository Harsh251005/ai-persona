# src/rag/context_loader.py

from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyMuPDFLoader


class ResumeLoader:
    """Loads a resume PDF into LangChain documents."""

    def __init__(self, pdf_path: Path, source_id: str):
        self.pdf_path = pdf_path
        self.source_id = source_id

    def load(self) -> List[Document]:
        loader = PyMuPDFLoader(str(self.pdf_path))
        documents = loader.load()

        for doc in documents:
            doc.metadata.update(
                {
                    "source_id": self.source_id,
                    "source_type": "resume",
                    "file_name": self.pdf_path.name,
                    "file_path": str(self.pdf_path),
                }
            )

        return documents


class ReadmeLoader:

    def __init__(
        self,
        readme_path: Path,
        source_id: str,
    ):
        self.readme_path = readme_path
        self.source_id = source_id

    def load(self) -> List[Document]:
        project_name = self.readme_path.stem.replace("_README", "")

        content = self.readme_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        return [
            Document(
                page_content=content,
                metadata={
                    "source_id": self.source_id,
                    "source_type": "readme",
                    "project_name": project_name,
                    "file_name": self.readme_path.name,
                    "file_path": str(self.readme_path),
                },
            )
        ]


class CommitLoader:

    def __init__(
        self,
        commit_file_path: Path,
        source_id: str,
    ):
        self.commit_file_path = commit_file_path
        self.source_id = source_id

    def load(self) -> List[Document]:
        project_name = self.commit_file_path.stem.replace("_Commits", "")

        content = self.commit_file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        return [
            Document(
                page_content=content,
                metadata={
                    "source_id": self.source_id,
                    "source_type": "commits",
                    "project_name": project_name,
                    "file_name": self.commit_file_path.name,
                    "file_path": str(self.commit_file_path),
                },
            )
        ]


class ContextLoader:
    """
    Loads all context data from a directory.

    Supported files:
    - *.pdf
    - *_README.md
    - *_Commits.txt
    """

    def __init__(self, context_dir: str):
        self.context_dir = Path(context_dir)

        if not self.context_dir.exists():
            raise FileNotFoundError(
                f"Context directory not found: {self.context_dir}"
            )

    @staticmethod
    def _generate_source_id(file_path: Path) -> str:
        return file_path.stem.lower().replace("-", "_")

    def load_all(self) -> List[Document]:
        documents: List[Document] = []

        for file_path in sorted(self.context_dir.iterdir()):

            source_id = self._generate_source_id(
                file_path
            )

            if file_path.suffix.lower() == ".pdf":
                documents.extend(
                    ResumeLoader(
                        file_path,
                        source_id=source_id,
                    ).load()
                )

            elif file_path.name.endswith("_README.md"):
                documents.extend(
                    ReadmeLoader(
                        file_path,
                        source_id=source_id,
                    ).load()
                )

            elif file_path.name.endswith("_Commits.txt"):
                documents.extend(
                    CommitLoader(
                        file_path,
                        source_id=source_id,
                    ).load()
                )

        documents.append(
            self._create_project_summary_document(
                documents
            )
        )

        return documents

    def _extract_project_descriptions(
            self,
            documents: List[Document],
    ) -> dict[str, str]:
        """
        Extract a concise project description from README documents.
        """

        descriptions = {}

        for doc in documents:

            if doc.metadata.get("source_type") != "readme":
                continue

            project_name = doc.metadata.get("project_name")

            content = doc.page_content.strip()

            lines = [
                line.strip()
                for line in content.splitlines()
                if line.strip()
            ]

            description = ""

            for line in lines:

                if line.startswith("#"):
                    continue

                description = line
                break

            descriptions[project_name] = (
                description[:300]
                if description
                else "Project information available in repository."
            )

        return descriptions

    def _create_project_summary_document(
            self,
            documents: List[Document],
    ) -> Document:
        """
        Creates a portfolio summary document to improve retrieval
        for high-level questions about projects and experience.
        """

        project_descriptions = self._extract_project_descriptions(
            documents
        )

        summary_lines = [
            "Harsh has worked on the following projects:",
            "",
        ]

        for project_name, description in sorted(
                project_descriptions.items()
        ):
            summary_lines.append(
                f"- {project_name}: {description}"
            )

        summary_lines.extend(
            [
                "",
                "These projects demonstrate experience in AI engineering,",
                "LLMs, RAG systems, evaluation frameworks, agentic workflows,",
                "machine learning, and production-grade application development.",
            ]
        )

        return Document(
            page_content="\n".join(summary_lines),
            metadata={
                "source_id": "project_summary",
                "source_type": "project_summary",
                "file_name": "generated_project_summary",
            },
        )