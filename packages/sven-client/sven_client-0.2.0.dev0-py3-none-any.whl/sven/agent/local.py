from textwrap import dedent
from typing import List

from agno.agent import Agent
from agno.embedder.openai import OpenAIEmbedder
from agno.knowledge.combined import CombinedKnowledgeBase
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.models.openai import OpenAIChat
from agno.tools import Toolkit
from agno.tools.knowledge import KnowledgeTools
from agno.vectordb.lancedb import LanceDb, SearchType

from sven.config import settings
from sven.tools.file import FileTools
from sven.tools.git import GitTools
from sven.tools.shell import ShellTools
from sven.tools.user_input import UserInputTools


class LocalAgent(Agent):
    def __init__(
        self,
        model: OpenAIChat = OpenAIChat("gpt-4o"),
        tools: List[Toolkit] = [],
        **kwargs,
    ):
        knowledge_bases = []
        knowledge_base_dir = settings.sven_dir / "knowledge"
        for knowledge in settings.knowledge:
            # If the section contains url and ends with .pdf, use PDFUrlKnowledgeBase
            if knowledge.url and knowledge.url.endswith(".pdf"):
                knowledge_bases.append(
                    PDFUrlKnowledgeBase(
                        urls=[knowledge.url],
                        vector_db=LanceDb(
                            table_name=knowledge.name,
                            uri=knowledge_base_dir,
                            search_type=SearchType.vector,
                            embedder=OpenAIEmbedder(id="text-embedding-3-small"),
                        ),
                    )
                )
            # If the section contains path and ends with .pdf, use PDFKnowledgeBase
            elif knowledge.path and knowledge.path.endswith(".pdf"):
                knowledge_bases.append(
                    PDFKnowledgeBase(
                        path=knowledge_base_dir / knowledge.path,
                        vector_db=LanceDb(
                            table_name=knowledge.name,
                            uri=knowledge_base_dir,
                            search_type=SearchType.vector,
                            embedder=OpenAIEmbedder(id="text-embedding-3-small"),
                        ),
                    )
                )

        knowledge_base = CombinedKnowledgeBase(
            sources=knowledge_bases,
            vector_db=LanceDb(
                table_name="kb",
                uri=knowledge_base_dir,
                search_type=SearchType.vector,
                embedder=OpenAIEmbedder(id="text-embedding-3-small"),
            ),
        )

        super().__init__(
            **kwargs,
            model=model,
            instructions=dedent(
                """
                You are a helpful coding assistant named Sven.

                You use tools extensively and skillfully to execute user's intent.

                When the user requests you to do something, you must do it
                diligently and precisly.

                If you are unable to complete the task, determine what tools you
                would need to complete it and use the request_tool tool to request
                the user to implement the tool for you.

                When you determine that you don't have enough tools to complete the
                task, ask user to provide the tool you need.

                Make at lest five (5) queries to your knowledge base. Use
                generic queries so that you get as much useful information as
                possible.

                Use .sven/scratchpad.txt file to keep track of useful
                infromation. Read this file to retrieve your previous findings
                and use append or edit to modify existing information. This file
                is important so do not overwrite it or delete it.
            """
            ),
            knowledge=knowledge_base,
            search_knowledge=True,
            add_history_to_messages=True,
            tools=[
                KnowledgeTools(
                    knowledge=knowledge_base,
                    think=True,
                    search=True,
                    analyze=True,
                    add_few_shot=True,
                ),
                GitTools(),
                FileTools(),
                ShellTools(),
                UserInputTools(),
            ]
            + tools,
        )
