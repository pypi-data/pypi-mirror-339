from pydantic import BaseModel, field_validator, ValidationInfo, model_validator
from enum import Enum
from typing import List, Literal

class ImageGenEngine(str, Enum):
	FLUX_SCHNELL = "flux_schnell"
	FLUX_1_1 = "flux_1.1"
	FLUX_PRO = "flux_pro"
	IMAGEN = "imagen"
	PHOTON_FLASH = "photon_flash"
	PHOTON = "photon"
	DALLE = "dalle"
	IDEOGRAM_TURBO = "ideogram_turbo"
	IDEOGRAM = "ideogram"
	MIDJOURNEY = "midjourney"
	STABILITY = "stability"

# Dictionary mapping engines to aspect ratios
engine_aspect_ratios = {
	ImageGenEngine.FLUX_SCHNELL: ["4:5", "9:16", "3:2", "1:1", "21:9", "16:9", "9:21", "4:3", "3:4", "2:3", "5:4"],
	ImageGenEngine.FLUX_1_1: ["4:5", "9:16", "3:2", "1:1", "21:9", "16:9", "9:21", "4:3", "3:4", "2:3", "5:4"],
	ImageGenEngine.FLUX_PRO: ["4:5", "9:16", "3:2", "1:1", "16:9", "4:3", "3:4", "2:3", "5:4"],
	ImageGenEngine.IMAGEN: ["9:16", "1:1", "16:9", "4:3", "3:4"],
	ImageGenEngine.PHOTON_FLASH: ["9:16", "1:1", "21:9", "9:21", "16:9", "4:3", "3:4"],
	ImageGenEngine.PHOTON: ["9:16", "1:1", "21:9", "9:21", "16:9", "4:3", "3:4"],
	ImageGenEngine.DALLE: ["1:1", "4:7", "7:4"],
	ImageGenEngine.IDEOGRAM_TURBO: ["9:16", "3:2", "16:10", "1:1", "16:9", "3:1", "10:16", "4:3", "3:4", "2:3", "1:3"],
	ImageGenEngine.IDEOGRAM: ["9:16", "3:2", "16:10", "1:1", "16:9", "3:1", "10:16", "4:3", "3:4", "2:3", "1:3"],
	ImageGenEngine.MIDJOURNEY: ["4:5", "9:16", "1:3", "3:2", "16:10", "1:1", "7:4", "4:7", "9:21", "16:9", "21:9", "3:1", "10:16", "4:3", "3:4", "2:3", "5:4"],
	ImageGenEngine.STABILITY: ["4:5", "9:16", "3:2", "1:1", "21:9", "16:9", "9:21", "4:3", "3:4", "2:3", "5:4"],
}

class ImageGenProperties(BaseModel):
	engine: ImageGenEngine
	aspect_ratio: str | None = '1:1'
	delination: str
	context: List[dict] | None = [{},]
	enhance_prompt: bool | None = False

	@field_validator("aspect_ratio")
	def validate_aspect_ratio(cls, v, info: ValidationInfo):
		engine = info.data.get("engine")
		if engine is None:
			raise ValueError(f"Invalid engine; valid choices are {list(ImageGenEngine.__members__.values())}")
		allowed_ratios = engine_aspect_ratios.get(engine)
		if v not in allowed_ratios:
			raise ValueError(f"Invalid aspect ratio '{v}' for engine '{engine.value}'. Allowed ratios are: {allowed_ratios}")
		return v
  

class Language(str, Enum):
    English = "English"
    Persian = "Persian"
    Arabic = "Arabic"
    Turkish = "Turkish"
    French = "French"
    Spanish = "Spanish"
    German = "German"
    Italian = "Italian"
    Portuguese = "Portuguese"
    Dutch = "Dutch"
    Russian = "Russian"
    Polish = "Polish"
    Romanian = "Romanian"
    Bulgarian = "Bulgarian"
    Hungarian = "Hungarian"
    Czech = "Czech"
    Greek = "Greek"
    Hebrew = "Hebrew"
    Japanese = "Japanese"
    Korean = "Korean"
    Mandarin = "Mandarin"
    Vietnamese = "Vietnamese"
    Indonesian = "Indonesian"

class SubtitleGenProperties(BaseModel):
    url: str
    source_language: Literal['auto'] | str = 'auto'
    target_language: str = 'Persian'
    diarization: bool = False
    enhanced: bool = True
    meta_data: dict | None = None
    webhook_url: str| None = None

    @field_validator("source_language")
    def source_language_must_be_valid(cls, v):
        if v != "auto" and v not in Language.__members__.values():
            raise ValueError(f"Invalid source_language: {v}.  Must be 'auto' or one of {list(Language.__members__.values())}")
        return v

    @field_validator("target_language")
    def target_language_must_be_valid(cls, v):
        if v not in Language.__members__.values():
            raise ValueError(f"Invalid target_language: {v}. Must be one of {list(Language.__members__.values())}")
        return v


class VideoGenEngines(str, Enum):
	HAILOU = 'hailou',
	KLING = 'kling',
	HUNYUANIMAGETO= 'hunyuanimageto',
	RUNWAY = 'runway',
	MINIMAX = 'minimax',
	HAILOUTEXT = 'hailoutext',
	KLINGTEXT = 'klingtext',
	KLINGPROTEXT = 'klingprotext',
	KLINGPRO = 'klingpro',
	HUNYUAN = 'hunyuan'
	LUMA = 'luma'

engine_input_types = {
	VideoGenEngines.HAILOU: {"text_to_video": True, "image_to_video": True,},
	VideoGenEngines.KLING: {"text_to_video": True, "image_to_video": True,},
	VideoGenEngines.HUNYUANIMAGETO: {"text_to_video": True, "image_to_video": True,},
	VideoGenEngines.RUNWAY: {"text_to_video": True, "image_to_video": True,},
	VideoGenEngines.MINIMAX: {"text_to_video": True, "image_to_video": True,},
	VideoGenEngines.HAILOUTEXT: {"text_to_video": True, "image_to_video": False,},
	VideoGenEngines.KLINGTEXT: {"text_to_video": True, "image_to_video": False,},
	VideoGenEngines.KLINGPROTEXT: {"text_to_video": True, "image_to_video": False,},
	VideoGenEngines.KLINGPRO: {"text_to_video": True, "image_to_video": False,},
	VideoGenEngines.HUNYUAN: {"text_to_video": True, "image_to_video": False,},
	VideoGenEngines.LUMA: {"text_to_video": True, "image_to_video": False,},
  }

class VideoGenProperties(BaseModel):
	user_prompt: str
	image_url: str | None = None
	meta_data: dict | None = None
	engine: VideoGenEngines
	webhook_url: str | None = None

	@model_validator(mode = 'before')
	def check_engine_supports_image_input(cls, values):
		engine = VideoGenEngines(values['engine'])
		image_url = values.get('image_url', None)
		if image_url is not None and not engine_input_types[engine]['image_to_video']:
			raise ValueError(f"Engine {engine} does not support image input")
		
		if not image_url and engine_input_types[engine]['image_to_video']:
			raise ValueError(f"Image URL is required for engine {engine}")
		return values
	
class GetListParameters(BaseModel):
  offset: int | None = 0
  limit: int | None = 10
  created_at_from: str | (str | None) = None
  created_at_to: str | (str | None) = None