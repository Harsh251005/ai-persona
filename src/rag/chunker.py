from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)


class ContextChunker:
    """
    Chunks documents based on their source type.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 100,
    ):
        self.recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "h1"),
                ("##", "h2"),
                ("###", "h3"),
            ]
        )

    def chunk_documents(
        self,
        documents: List[Document],
    ) -> List[Document]:

        chunks: List[Document] = []

        for document in documents:

            source_type = document.metadata.get("source_type")

            if source_type == "resume":
                chunks.extend(
                    self._chunk_resume(document)
                )

            elif source_type == "readme":
                chunks.extend(
                    self._chunk_readme(document)
                )

            elif source_type == "commits":
                chunks.extend(
                    self._chunk_commits(document)
                )

            else:
                chunks.extend(
                    self.recursive_splitter.split_documents(
                        [document]
                    )
                )

        return chunks

    def _chunk_resume(
        self,
        document: Document,
    ) -> List[Document]:
        return self.recursive_splitter.split_documents(
            [document]
        )

    def _chunk_readme(
        self,
        document: Document,
    ) -> List[Document]:

        markdown_docs = self.markdown_splitter.split_text(
            document.page_content
        )

        chunks: List[Document] = []

        for md_doc in markdown_docs:

            content = md_doc.page_content.strip()

            if not content:
                continue

            temp_doc = Document(
                page_content=content,
                metadata={
                    **document.metadata,
                    **md_doc.metadata,
                },
            )

            chunks.extend(
                self.recursive_splitter.split_documents(
                    [temp_doc]
                )
            )

        return chunks

    def _chunk_commits(
        self,
        document: Document,
    ) -> List[Document]:
        """
        Commit files are already concise and retrieval-friendly.

        No chunking for now.
        """
        return [document]