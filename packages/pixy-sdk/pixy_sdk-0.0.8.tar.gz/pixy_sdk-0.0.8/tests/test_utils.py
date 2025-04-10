from pixy.utils import verify, generate
from core.schemas import ImageGenProperties, SubtitleGenProperties
import pytest
from pydantic import BaseModel
from typing import Literal

import os
from dotenv import load_dotenv

load_dotenv()

valid_api_key = os.getenv("VALID_PIXY_API_KEY")
invalid_api_key = os.getenv("INVALID_PIXY_API_KEY")


class TestVeirify:

    def test_verify_with_valid_api_key(self):
        assert verify(valid_api_key)

    def test_verify_with_invalid_api_key(self):
        assert not verify(invalid_api_key)


class TestGenerate:
    def test_invalid_generation_type(self):
        with pytest.raises(ValueError) as excinfo:
            generate(
                generation_type="human",
                properties=ImageGenProperties(engine="imagen", delineation="test"),
                api_key=valid_api_key,
            )

        assert "is an invalid value for generation_type; valid choices are" in str(
            excinfo
        )

    def test_invalid_properties_type(self):
        class HumanGenProperties(BaseModel):
            name: str
            age: int
            sex: Literal["male", "female"]

        human_properties = HumanGenProperties(name="John Doe", age=25, sex="male")

        with pytest.raises(TypeError) as excinfo:
            generate(
                generation_type="image",
                properties=human_properties,
                api_key=valid_api_key,
            )

        assert "is an invalid properties type; valid choices are:" in str(excinfo)

    def test_generation_type_properties_mismatch(self):
        with pytest.raises(Exception) as excinfo:
            generate(
                generation_type="image",
                properties=SubtitleGenProperties(url="https://example.com/video.mp4"),
                api_key=valid_api_key,
            )

        assert "generation requires property of type" in str(excinfo)
