from loguru import logger
from langchain_core.prompts import ChatPromptTemplate

from nl2query.core.base_module import BaseModule
from nl2query.table_selector.schema import TableSelectorSchema
from nl2query.core.llm_models import get_llm
from nl2query.table_selector.prompts import get_table_selector_prompts


class TableSelector(BaseModule):
    """Concrete implementation of BaseModule for intent detection"""

    def __init__(
        self,
        system_prompt: str = None,
        pydantic_class: TableSelectorSchema = TableSelectorSchema,
        prompt: str = None,
        examples: str = None,
        table_info: str = None,
        *args,
        **kwargs,
    ):
        super().__init__(
            system_prompt=system_prompt,
            pydantic_class=pydantic_class,
            examples=examples,
            *args,
            **kwargs,
        )

        self.prompt = prompt
        self.examples = examples
        self.pydantic_class = pydantic_class
        self.table_info = table_info

        logger.info(f"Initialized IntentEngine with prompt: {system_prompt}")

    def run(self, state):
        """Process the state and return intent JSON"""
        try:
            self.model_type = state.get("model_type", "openai")
            self.model_name = state.get("model_name", "gpt-4o")
            self.temperature = state.get("temperature", 0.01)
            self.query = state["query"]

            prompt = get_table_selector_prompts(self.query, self.table_info)

            prompt = ChatPromptTemplate.from_messages(
                [("system", prompt), ("human", "{query}")]
            )

            llm = get_llm(
                model_type=self.model_type,
                model_name=self.model_name,
                temperature=self.temperature,
            )
            structured_llm = llm.with_structured_output(self.pydantic_class)
            few_shot_structured_llm = prompt | structured_llm

            response = few_shot_structured_llm.invoke({"query": self.query})

            selected_table = response.dict()["selected_tables"]

            logger.info(f"Selected tables:{selected_table}")

            state["selected_tables"] = selected_table

            state["raw_messages"].append(
                {"role": "table_selector", "content": response}
            )
            formatted_message = {"role": "user", "content": state["query"]}
            state["messages"].append(formatted_message)
            
            return state, selected_table

        except Exception as e:
            logger.error(f"Error processing intent: {e}")
            raise
