def get_readings(fetch_func, **kwargs):
    """
    Higher-order function to fetch readings using the specified function.
    
    Args:
        fetch_func (callable): The function to fetch readings.
        api_client (DefaultApi): An instance of the API client.
        **kwargs: Additional parameters to pass to the fetch function.
    
    Returns:
        List[dict]: The fetched readings.
    """
    return fetch_func(**kwargs)
