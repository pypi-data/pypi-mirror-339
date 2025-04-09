import httpx
from schemas import (
    ImageGenProperties,
    VideoGenProperties,
    SubtitleGenProperties,
    GetListParameters,
)
from settings import Settings

import logging

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)

logger.setLevel(logging.INFO)
settings = Settings()


def verify(api_key: str) -> bool:
    """
    Verifies the given API key.

    Args:
    api_key (str): The API key to verify.

    Returns:
    bool: True if the API key is valid, False otherwise.
    """
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    json_data = {"api_key": api_key}

    with httpx.Client() as client:
        response = client.post(
            settings.url_mapping.get("api_key_verification"),
            headers=headers,
            json=json_data,
        )
    if response.status_code == 200:
        return True
    else:
        logger.error(
            f"API key verification failed - status code: {response.status_code}"
            + "\n"
            + response.text
        )
        return False


def generate(
    generation_type: str,
    properties: ImageGenProperties | VideoGenProperties | SubtitleGenProperties,
    api_key: str,
) -> dict:
    """
    Generates a resource (image, video, subtitle) based on the given properties.

    Args:
    generation_type (str): The type of resource to generate.
    properties (ImageGenProperties | VideoGenProperties | SubtitleGenProperties): The properties of the resource to generate.
    api_key (str): The API key to use for the request.

    Returns:
    dict: A JSON response containing the generated resource.
    """
    if not generation_type in settings.properties_mapping.keys():
        logger.error(
            f"{generation_type} is an invalid value for generation_type; valid choices are: {settings.properties_mapping.keys()}."
        )
        raise ValueError(
            f"{generation_type} is an invalid value for generation_type; valid choices are: {settings.properties_mapping.keys()}."
        )

    if not isinstance(
        properties, (ImageGenProperties, VideoGenProperties, SubtitleGenProperties)
    ):
        logger.error(
            f"{type(properties).__name__} is an invalid properties type; valid choices are: {[item.__name__ for item in settings.properties_mapping.values()]}"
        )
        raise TypeError(
            f"{type(properties).__name__} is an invalid properties type; valid choices are: {[item.__name__ for item in settings.properties_mapping.values()]}"
        )

    if settings.properties_mapping[generation_type] != properties.__class__:

        logger.exception(
            f"{generation_type} generation requires property of type {settings.properties_mapping[generation_type].__name__}, not {type(properties).__name__}."
        )
        raise Exception(
            f"{generation_type} generation requires property of type {settings.properties_mapping[generation_type].__name__}, not {type(properties).__name__}."
        )

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": api_key,
    }

    json_data = properties.model_dump()

    try:
        with httpx.Client() as client:
            response = client.post(
                settings.url_mapping[generation_type], headers=headers, json=json_data
            )
            response.raise_for_status()
            if response.status_code != 201:
                logger.error(
                    f"{generation_type} generation failed - status code: {response.status_code}"
                )

            logger.info(f"Successful {generation_type} generation.")
            return response.json()

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")


def get_by_uid(generation_type: str, uid: str, api_key: str) -> dict:
    """
    Retrieves a resource by its unique identifier (UID).

    Args:
    generation_type (str): The type of resource to retrieve.
    uid (str): The unique identifier of the resource.
    api_key (str): The API key to use for the request.

    Returns:
    dict: A JSON response containing the retrieved resource.

    Raises:
    Exception: If an error occurs during the request.
    """

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": api_key,
    }

    with httpx.Client() as client:
        response = client.get(
            f"{settings.url_mapping[generation_type]}{uid}", headers=headers
        )

    try:
        return response.json()
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")


def get_list(generation_type: str, params: GetListParameters | None, api_key: str):
    """
    Retrieves a list of resources filtered by the given parameters.

    Args:
    generation_type (str): The type of resource to retrieve.
    params (GetListParameters | None): The parameters to filter the results by.
    api_key (str): The API key to use for the request.

    Returns:
    dict: A JSON response containing the retrieved resources.

    Raises:
    Exception: If an error occurs during the request.
    """
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": api_key,
    }

    with httpx.Client() as client:
        response = client.get(
            settings.url_mapping[generation_type],
            headers=headers,
            params=params.model_dump(exclude_none=True) if params else None,
        )

    try:
        return response.json()
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")


def delete(generation_type: str, uid: str, api_key: str) -> dict:
    """
    Deletes a resource by its unique identifier.

    Args:
    generation_type (str): The type of resource to delete.
    uid (str): The unique identifier of the resource.
    api_key (str): The API key to use for the request.

    Returns:
    dict: A JSON response indicating the result of the deletion.

    Raises:
    Exception: If an error occurs during the request.
    """
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": api_key,
    }

    try:
        with httpx.Client() as client:
            response = client.delete(
                f"{settings.url_mapping[generation_type]}{uid}", headers=headers
            )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")


def update(generation_type: str, uid: str, properties: dict, api_key: str) -> dict:
    """
    Updates a resource by its unique identifier with the given properties.

    Args:
    generation_type (str): The type of resource to update.
    uid (str): The unique identifier of the resource.
    properties (dict): The properties to update the resource with. This is supposed to only include the key-values to update.
    api_key (str): The API key to use for the request.

    Returns:
    dict: A JSON response containing the updated resource.

    Raises:
    Exception: If an error occurs during the request.
    """

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": api_key,
    }

    try:
        with httpx.Client() as client:
            response = client.patch(
                f"{settings.url_mapping[generation_type]}{uid}",
                headers=headers,
                json=properties,
            )

        return response.json()
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
