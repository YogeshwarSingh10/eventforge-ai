from typing import Dict, Any

from langchain_core.prompts import ChatPromptTemplate

from eventforge.agents.base.base_agent import BaseAgent
from eventforge.models.schemas import ConferenceInput, GTMAgentOutput
from eventforge.utils.llm_client import get_llm
from eventforge.tools.web_search import search_communities
from eventforge.utils.logging import get_logger

logger = get_logger(__name__)


class GTMAgent(BaseAgent):

    def __init__(self):
        super().__init__("gtm_agent")

        self.llm = get_llm().with_structured_output(
            GTMAgentOutput,
            method="json_schema",
            strict=True
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are an expert in event marketing and growth strategy."),

            ("user", 
             """
            Conference Details:
            Category: {category}
            Geography: {geography}

            Search Results:
            {search_results}

            TASK:
            - Identify top communities (Discord, LinkedIn, Meetup, etc.)
            - Assign UNIQUE id
            - Provide platform and niche
            - Generate promotion message
            - Assign recommended order (1 = highest priority)

            Also provide a short GTM summary.
            """)
        ])

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info("GTMAgent started")

            input_data = ConferenceInput(**state["input"])

            query = f"{input_data.category} communities in {input_data.geography}"
            search_results = await search_communities.ainvoke(query)

            chain = self.prompt | self.llm

            result = await chain.ainvoke(
                {
                    "category": input_data.category,
                    "geography": input_data.geography,
                    "search_results": search_results,
                }
            )

            return self._success(result)

        except Exception as e:
            logger.exception("GTMAgent failed")
            return self._fail(e)
