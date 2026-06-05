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

            source_id = self._generate_source_id(file_path)

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

        return documents