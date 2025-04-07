def get_table_selector_prompts(query, tables_info):
    """Function to generate prompts for the pre-filtering engine."""

    if not tables_info:
        tables_info = ["customers", "products", "order", "order_items"]

    prompts = f"""Task: Analyze the provided natural language query to determine which tables in the database it references. List only the relevant tables from the provided list of tables without giving any explanations or reasoning.
    Input:
    1. Natural Language Query: "{query}"
    2. **List of Available Tables:**
    {tables_info}
    Output Requirement: Provide a list of tables from the provided list that are referenced in the natural language query only if you are sure of it.
    **Guidelines:**
    1. Make sure to list the relevent tables from available tables list only.
    2. If no tables are related to given query then return empty list.

    Expected Output Format:
    ["ReferencedTable1","ReferencedTable2",...]
    (Continue listing all relevant tables identified.)"""
    prompts = str(prompts)
    return prompts
