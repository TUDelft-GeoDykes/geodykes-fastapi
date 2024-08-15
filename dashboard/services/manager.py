import os
from dotenv import load_dotenv
from importlib import import_module

# Load environment variables from a .env file
load_dotenv()

class DataFetcher:
    """
    A class responsible for loading environment variables, setting up services, 
    and providing access to different application functionalities.
    
    This class is designed to be flexible and allow for dynamic configuration of
    services by specifying the module that contains the required functions.
    
    Attributes:
        db_host (str): The database host.
        db_port (str): The database port.
        db_username (str): The database username.
        db_password (str): The database password.
        api_host (str): The API host for the OpenAPI client.
        api_key (str): The API key for authenticating with the API (optional).
        api_client: An instance of the API client initialized from the specified module.
    """

    def __init__(self):
        # Load environment variables
        self.load_env_variables()

        # Set up services dependencies
        self.setup_service()

    def load_env_variables(self):
        """
        Load environment variables from the .env file. These include database 
        connection details and API configurations.
        """
        self.db_host = os.getenv('DB_HOST')
        self.db_port = os.getenv('DB_PORT')
        self.db_username = os.getenv('DB_USERNAME')
        self.db_password = os.getenv('DB_PASSWORD')
        self.api_host = os.getenv('API_HOST', 'http://localhost:8000/api')
        self.api_key = os.getenv('API_KEY', None)

    def setup_service(self, module_name='services.openapi'):
        """
        Set up the services dependencies by dynamically importing the specified module.
        The module must implement a `_get_client` function.

        Args:
            module_name (str): The name of the module to import for setting up services.
                               Defaults to 'services.openapi'.
        """
        try:
            # Dynamically import the module specified by module_name
            service_module = import_module(module_name)

            # Check if the module implements the required _get_client function
            if not hasattr(service_module, '_get_client'):
                raise ImportError(f"The module '{module_name}' must implement a '_get_client' function.")

            # Initialize the API client using the _get_client function from the imported module
            self.api_client = service_module._get_client()
            self.fetch_readings = service_module._get_readings

        except ImportError as e:
            raise ImportError(f"Error importing module '{module_name}': {e}")
        
data_fetcher = DataFetcher()
data_fetcher.setup_service(module_name='services.openapi')
