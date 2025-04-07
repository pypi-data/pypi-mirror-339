class SDKClient:
    """Main client class for the SDK."""

    def __init__(self, api_key=None, config=None):
        """Initialize the SDK client.

        Args:
            api_key (str): API key for authentication
            config (dict): Configuration dictionary
        """
        self.api_key = api_key
        self.config = config or {}

    def do_something(self, param1, param2):
        """Example method that does something.

        Args:
            param1: First parameter
            param2: Second parameter

        Returns:
            Result of the operation

        Raises:
            SDKError: If something goes wrong
        """
        # Implementation here
        return f"Result with {param1} and {param2}"