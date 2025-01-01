from google.api_core.exceptions import NotFound, BadRequest

def execute_query(client, query: str):
    """Executes a BigQuery query and returns results."""
    try:
        query_job = client.query(query)
        return [dict(row) for row in query_job.result()]  # Return rows as a list of dictionaries
    except NotFound as e:
        raise Exception(f"Resource not found: {e}")
    except BadRequest as e:
        raise Exception(f"Bad Request: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")
