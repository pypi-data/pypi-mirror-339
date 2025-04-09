import os
from dotenv import load_dotenv

load_dotenv()
from .schemas import ImageGenProperties, VideoGenProperties, SubtitleGenProperties


class Settings:

    url_mapping = {
        "api_key_verification": os.getenv("PIXY_API_KEY_VERIFICATION_ENDPOINT"),
        "image": os.getenv("PIXY_IMAGINE_ENDPOINT"),
        "video": os.getenv("PIXY_VIDEOGEN_ENDPOINT"),
        "subtitle": os.getenv("PIXY_SUBTITLE_ENDPOINT"),
    }

    properties_mapping = {
        "image": ImageGenProperties,
        "video": VideoGenProperties,
        "subtitle": SubtitleGenProperties,
    }
