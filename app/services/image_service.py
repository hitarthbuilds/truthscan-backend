from PIL import Image
from PIL.ExifTags import TAGS
from typing import Dict, List
import io


class ImageVerificationService:
    def __init__(self):
        pass

    def _extract_exif(self, image: Image.Image) -> Dict:
        exif_data = {}
        raw_exif = image._getexif()

        if raw_exif:
            for tag_id, value in raw_exif.items():
                tag = TAGS.get(tag_id, tag_id)
                exif_data[tag] = value

        return exif_data

    def _detect_screenshot_like(self, image: Image.Image) -> bool:
        width, height = image.size
        aspect_ratio = round(width / height, 2)

        common_ratios = {
            16 / 9,
            9 / 16,
            4 / 3,
            3 / 4,
        }

        return any(abs(aspect_ratio - r) < 0.05 for r in common_ratios)

    def _compression_artifact_check(self, image: Image.Image) -> bool:
        return image.format in {"PNG", "WEBP"}

    def verify(self, file_bytes: bytes) -> Dict:
        image = Image.open(io.BytesIO(file_bytes))
        flags: List[str] = []

        exif = self._extract_exif(image)
        if not exif:
            flags.append("missing_metadata")

        if self._detect_screenshot_like(image):
            flags.append("screenshot_like")

        if self._compression_artifact_check(image):
            flags.append("compression_artifacts")

        confidence = max(0.0, 1.0 - (0.2 * len(flags)))

        return {
            "authenticity_score": round(confidence, 3),
            "confidence": round(confidence, 3),
            "details": {
                "exif_present": bool(exif),
                "exif_keys": list(exif.keys()),
                "image_flags": flags,
                "image_flag_count": len(flags),
            },
        }
