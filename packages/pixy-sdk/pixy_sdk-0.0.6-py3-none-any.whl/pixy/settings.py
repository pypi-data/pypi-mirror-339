from .schemas import ImageGenProperties, VideoGenProperties, SubtitleGenProperties


class Settings:

    url_mapping = {
        "api_key_verification": "https://sso.pixy.ir/api_key/verify",
        "image": "https://media.pixy.ir/v1/apps/imagine/imagination/",
        "video": "https://media.pixy.ir/v1/apps/videogen/videos/",
        "subtitle": "https://media.pixy.ir/v1/apps/subtitle/subtitles/",
    }

    properties_mapping = {
        "image": ImageGenProperties,
        "video": VideoGenProperties,
        "subtitle": SubtitleGenProperties,
    }
