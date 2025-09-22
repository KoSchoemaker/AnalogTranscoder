from General import *
import os
import json


class ScanCache:
    def __init__(self, cache_directory: str):
        self.cache_directory = cache_directory
        os.makedirs(self.cache_directory, exist_ok=True)

    def get_pts_from_external_cache(self, filename):
        cache_filepath = self.__get_external_cache_filepath(filename)

        if os.path.isfile(cache_filepath):
            print(
                f'INFO: cache file exists for {filename}, using that ({cache_filepath})')

            with open(os.path.join(self.cache_directory, filename) + '.json', 'r') as file:
                return json.load(file)

        print(f'INFO: no cache file exists for {filename}')
        return False

    def add_pts_to_external_cache(self, filename, pts) -> bool:
        cache_filepath = self.__get_external_cache_filepath(filename)
        if os.path.isfile(cache_filepath):
            print(
                f'INFO: cache file already exists for {filename}, overwriting')
        with open(cache_filepath, 'w') as file:
            json.dump(pts, file)

    def __get_external_cache_filepath(self, filename) -> str:
        print(f"{self.cache_directory}, {filename}")
        return os.path.join(self.cache_directory, filename) + '.json'
