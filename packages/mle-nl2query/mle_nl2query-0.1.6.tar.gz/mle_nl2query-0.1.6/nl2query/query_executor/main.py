from loguru import logger
from nl2query.db.db_connector import execute_sql_query, execute_snowflake_query


class QueryExecutor:
    def run(self, state):
        """Main function to execute the query executor."""
        if state["db_type"] == "postgres":
            query = state["validated_query"]
            result = execute_sql_query(query)
            state["output_response"] = result
        elif state["db_type"] == "snowflake":
            query = state["validated_query"]
            result = execute_snowflake_query(query)
            state["output_response"] = result
        logger.info(f"Output after executing the generated query: {result}")
        return state, result
