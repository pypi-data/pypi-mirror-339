from core.schemas import ImageGenEngine, ImageGenProperties, SubtitleGenProperties, VideoGenProperties, VideoGenEngines, GetListParameters
from pydantic import ValidationError
import pytest

# Starting by tests for ImageGenProperties

class TestImageGenProperties:
    def test_imagegenproperties_default_values(self):
        """Test default values for aspect_ratio, context, and enhance_prompt."""
        props = ImageGenProperties(engine=ImageGenEngine.IMAGEN, delination="test")
        assert props.aspect_ratio == '1:1'
        assert props.context == [{}]
        assert props.enhance_prompt is False

    def test_imagegenproperties_valid_aspect_ratio(self):
        """Test that a valid aspect ratio is accepted."""
        props = ImageGenProperties(engine=ImageGenEngine.IMAGEN, aspect_ratio="16:9", delination="test")
        assert props.aspect_ratio == "16:9"

    def test_imagegenproperties_invalid_aspect_ratio(self):
        """Test that an invalid aspect ratio raises a ValueError."""
        with pytest.raises(ValidationError) as excinfo:
            ImageGenProperties(engine=ImageGenEngine.IMAGEN, aspect_ratio="2:1", delination="test")
        assert "Invalid aspect ratio '2:1' for engine 'imagen'. Allowed ratios are: ['9:16', '1:1', '16:9', '4:3', '3:4']" in str(excinfo.value)

    def test_imagegenproperties_different_engine_aspect_ratio(self):
        """Test aspect ratio validation with a different engine."""
        props = ImageGenProperties(engine=ImageGenEngine.DALLE, aspect_ratio="4:7", delination="test")
        assert props.aspect_ratio == "4:7"

    def test_imagegenproperties_invalid_aspect_ratio_different_engine(self):
        """Test that an invalid aspect ratio raises a ValueError with a different engine."""
        with pytest.raises(ValidationError) as excinfo:
            ImageGenProperties(engine=ImageGenEngine.DALLE, aspect_ratio="16:9", delination="test")
        assert "Invalid aspect ratio '16:9' for engine 'dalle'. Allowed ratios are: ['1:1', '4:7', '7:4']" in str(excinfo.value)

    def test_imagegenproperties_valid_context(self):
        """Test that a valid context is accepted."""
        context_data = [{"key1": "value1"}, {"key2": "value2"}]
        props = ImageGenProperties(engine=ImageGenEngine.IMAGEN, aspect_ratio="1:1", delination="test", context=context_data)
        assert props.context == context_data

    def test_imagegenproperties_enhance_prompt_true(self):
        """Test when enhance_prompt is set to True."""
        props = ImageGenProperties(engine=ImageGenEngine.IMAGEN, delination="test", enhance_prompt=True)
        assert props.enhance_prompt is True

    def test_imagegenproperties_all_fields(self):
        """Test creating an instance with all fields specified."""
        context_data = [{"key1": "value1"}]
        props = ImageGenProperties(
            engine=ImageGenEngine.FLUX_SCHNELL,
            aspect_ratio="4:5",
            delination="a photo",
            context=context_data,
            enhance_prompt=True
        )
        assert props.engine == ImageGenEngine.FLUX_SCHNELL
        assert props.aspect_ratio == "4:5"
        assert props.delination == "a photo"
        assert props.context == context_data
        assert props.enhance_prompt is True

    def test_imagegenproperties_engine_only(self):
        """Test creating an instance with only the engine and delination specified."""
        props = ImageGenProperties(engine=ImageGenEngine.IMAGEN, delination="test")
        assert props.engine == ImageGenEngine.IMAGEN
        assert props.delination == "test"
        assert props.aspect_ratio == "1:1"  # Default value
        assert props.context == [{}]  # Default value
        assert props.enhance_prompt is False  # Default value

    def test_imagegenproperties_invalid_engine(self):
        """Test that an invalid engine raises a ValueError."""
        with pytest.raises(ValueError) as excinfo:
            ImageGenProperties(engine="invalid_engine", aspect_ratio="1:1", delination="test")
        assert "Invalid engine; valid choices are" in str(excinfo.value)

class TestSubtitleGenProperties:
    def test_default_values(self):
        """Test default values for source_language, target_language, diarization, enhanced, meta_data, and webhook_url."""
        props = SubtitleGenProperties(url="https://example.com/video.mp4")
        assert props.source_language == "auto"
        assert props.target_language == "Persian"
        assert props.diarization is False
        assert props.enhanced is True
        assert props.meta_data is None
        assert props.webhook_url is None

    def test_valid_source_language_auto(self):
        """Test that 'auto' is a valid source_language."""
        props = SubtitleGenProperties(url="https://example.com/video.mp4", source_language="auto")
        assert props.source_language == "auto"

    def test_valid_source_language_enum(self):
        """Test that a valid Language enum value is accepted as source_language."""
        props = SubtitleGenProperties(url="https://example.com/video.mp4", source_language="English")
        assert props.source_language == "English"

    def test_invalid_source_language(self):
        """Test that an invalid source_language raises a ValueError."""
        with pytest.raises(ValueError) as excinfo:
            SubtitleGenProperties(url="https://example.com/video.mp4", source_language="InvalidLanguage")
        assert "Invalid source_language: InvalidLanguage.  Must be 'auto' or one of" in str(excinfo.value)

    def test_valid_target_language(self):
        """Test that a valid Language enum value is accepted as target_language."""
        props = SubtitleGenProperties(url="https://example.com/video.mp4", target_language="German")
        assert props.target_language == "German"

    def test_invalid_target_language(self):
        """Test that an invalid target_language raises a ValueError."""
        with pytest.raises(ValueError) as excinfo:
            SubtitleGenProperties(url="https://example.com/video.mp4", target_language="InvalidLanguage")
        assert "Invalid target_language: InvalidLanguage. Must be one of" in str(excinfo.value)

    def test_all_fields(self):
        """Test creating an instance with all fields specified."""
        meta = {"key1": "value1"}
        props = SubtitleGenProperties(
            url="https://example.com/video.mp4",
            source_language="English",
            target_language="French",
            diarization=True,
            enhanced=False,
            meta_data=meta,
            webhook_url="https://example.com/webhook"
        )
        assert props.url == "https://example.com/video.mp4"
        assert props.source_language == "English"
        assert props.target_language == "French"
        assert props.diarization is True
        assert props.enhanced is False
        assert props.meta_data == meta
        assert props.webhook_url == "https://example.com/webhook"

class TestVideoGenProperties:
    def test_valid_text_to_video_engine_no_image(self):
        """Test a valid engine that only supports text-to-video with no image_url."""
        props = VideoGenProperties(user_prompt="A cat", engine=VideoGenEngines.HAILOUTEXT)
        assert props.user_prompt == "A cat"
        assert props.engine == VideoGenEngines.HAILOUTEXT
        assert props.image_url is None

    def test_valid_image_to_video_engine_with_image(self):
        """Test a valid engine that supports image-to-video with an image_url."""
        props = VideoGenProperties(user_prompt="A cat", engine=VideoGenEngines.HAILOU, image_url="https://example.com/image.jpg")
        assert props.user_prompt == "A cat"
        assert props.engine == VideoGenEngines.HAILOU
        assert props.image_url == "https://example.com/image.jpg"

    def test_image_to_video_engine_requires_image_url(self):
        """Test that an engine supporting image-to-video requires an image_url."""
        with pytest.raises(ValueError) as excinfo:
            VideoGenProperties(user_prompt="A cat", engine=VideoGenEngines.HAILOU)
        assert f"Image URL is required for engine {VideoGenEngines.HAILOU}" in str(excinfo.value)

    def test_text_to_video_engine_does_not_allow_image_url(self):
        """Test that an engine that doesn't support image-to-video raises an error when image_url is provided."""
        with pytest.raises(ValueError) as excinfo:
            VideoGenProperties(user_prompt="A cat", engine=VideoGenEngines.HAILOUTEXT, image_url="https://example.com/image.jpg")
        assert f"Engine {VideoGenEngines.HAILOUTEXT} does not support image input" in str(excinfo.value)

    def test_all_fields(self):
        """Test creating an instance with all fields specified."""
        meta = {"key1": "value1"}
        props = VideoGenProperties(
            user_prompt="A cat",
            image_url="https://example.com/image.jpg",
            meta_data=meta,
            engine=VideoGenEngines.HAILOU,
            webhook_url="https://example.com/webhook"
        )
        assert props.user_prompt == "A cat"
        assert props.image_url == "https://example.com/image.jpg"
        assert props.meta_data == meta
        assert props.engine == VideoGenEngines.HAILOU
        assert props.webhook_url == "https://example.com/webhook"

    def test_enum_value_assignment(self):
        """Test that the engine enum is assigned correctly."""
        props = VideoGenProperties(user_prompt="A cat", engine='luma')
        assert props.engine == VideoGenEngines.LUMA

    
    def test_invalid_engine_value(self):
        """Test that an invalid engine value raises an error."""
        with pytest.raises(ValueError) as excinfo:
            VideoGenProperties(user_prompt="A cat", engine="invalid_engine")
        assert "is not a valid" in str(excinfo.value)

    def test_valid_engine_no_image_required(self):
        """Test a valid engine that supports only text input and no image is provided."""
        props = VideoGenProperties(user_prompt="A cat", engine=VideoGenEngines.KLINGTEXT)
        assert props.user_prompt == "A cat"
        assert props.engine == VideoGenEngines.KLINGTEXT
        assert props.image_url is None

class TestGetListParams:
    def test_default_values(self):
        """Test that default values are set correctly."""
        params = GetListParameters()
        assert params.offset == 0
        assert params.limit == 10
        assert params.created_at_from is None
        assert params.created_at_to is None