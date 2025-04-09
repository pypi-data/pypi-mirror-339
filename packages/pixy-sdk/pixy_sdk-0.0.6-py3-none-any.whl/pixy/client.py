from .schemas import (
    ImageGenProperties,
    VideoGenProperties,
    SubtitleGenProperties,
    GetListParameters,
)
from .utils import verify, generate, get_by_uid, get_list, delete, update
import logging

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)

logger.setLevel(logging.INFO)


class PixyClient:
    def __init__(self, api_key: str):
        """
        Initialize the Pixy client.

        Args:
            api_key (str): API key obtained from the Pixy panel.

        Raises:
            Exception: If the API key is not valid.
        """

        if not verify(api_key):
            raise Exception("API key verification failed.")

        self.api_key = api_key
        logger.info("API key is verified successfully.")

    def generate(
        self,
        generation_type: str,
        properties: ImageGenProperties | VideoGenProperties | SubtitleGenProperties,
    ):
        """
        Generates a resource (image, video, subtitle) using the Pixy API.

        Args:
            generation_type (str): The type of resource to generate.
            properties (ImageGenProperties | VideoGenProperties | SubtitleGenProperties): The properties defining the resource to generate.

        Returns:
            dict: A JSON response containing the generated resource.
        """

        return generate(generation_type, properties, self.api_key)

    def get_by_uid(self, generation_type: str, uid: str):
        """
        Retrieves a resource by its unique identifier using the Pixy API.

        Args:
            generation_type (str): The type of resource to retrieve.
            uid (str): The unique identifier of the resource.

        Returns:
            dict: A JSON response containing the retrieved resource.
        """

        return get_by_uid(generation_type, uid, self.api_key)

    def get_list(self, generation_type: str, params: GetListParameters | None):
        """
        Retrieves a list of resources filtered by the given parameters using the Pixy API.

        Args:
            generation_type (str): The type of resource to retrieve.
            params (GetListParameters | None): The parameters to filter the results by.

        Returns:
            dict: A JSON response containing the retrieved resources.
        """

        return get_list(generation_type, params, self.api_key)

    def delete(self, generation_type: str, uid: str):
        """
        Deletes a resource by its unique identifier using the Pixy API.

        Args:
            generation_type (str): The type of resource to delete.
            uid (str): The unique identifier of the resource.

        Returns:
            dict: A JSON response indicating the result of the deletion.
        """
        return delete(generation_type, uid, self.api_key)

    def update(
        self,
        generation_type: str,
        uid: str,
        properties: dict,
    ):
        """
        Updates a resource by its unique identifier with the given properties using the Pixy API.

        Args:
            generation_type (str): The type of resource to update.
            uid (str): The unique identifier of the resource.
            properties (ImageGenProperties | VideoGenProperties | SubtitleGenProperties):
                The properties to update the resource with. This is supposed to only include
                the key-values to update.

        Returns:
            dict: A JSON response containing the updated resource.
        """
        return update(generation_type, uid, properties, self.api_key)
