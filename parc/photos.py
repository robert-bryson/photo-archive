from pathlib import Path


class PhotoCollection:
    def __init__(self):
        self.photos = {}

    def add_photo(self, photo_path):
        self.photos.append(photo_path)

    # def remove_photo(self, photo_path):
    #     pass

    def list_photos(self):
        return self.photos

    def count_photos(self):
        return len(self.photos)

    def validate_photo_files(self):
        pass

    def analyze_photos(self):
        pass

    def archive_photos(self, output_session_path: Path):
        pass
