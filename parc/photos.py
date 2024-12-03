from pathlib import Path
from PIL import Image
import logging


logger = logging.getLogger(__name__)

class PhotoCollection:
    def __init__(self):
        self.photos = {}

    def add_photo(self, photo_path):
        self.photos[photo_path] = {}

    # def remove_photo(self, photo_path):
    #     pass

    # def list(self):
    #     return self.photos

    def count(self):
        return len(self.photos)

    def validate_photo_files(self):
        pass

    def analyze_photos(self):
        """Analyze the photos in the collection."""
        for photo_path in self.photos:
            logger.info(f"Analyzing photo: {photo_path}")
            with Image.open(photo_path) as img:
                self.photos[photo_path]["size"] = img.size
                self.photos[photo_path]["format"] = img.format
                exif = img._getexif()
                self.photos[photo_path]["exif"] = exif

    def archive_photos(self, output_session_path: Path):
        pass
