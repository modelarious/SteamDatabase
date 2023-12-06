from os import walk
from RegexPlugin import InputSanitizer
from typing import List


class DirListFetcher:
    def get_files_and_dirs(self, pathToGamesFolder: str) -> List[str]:
        dirInfoIterator = walk(pathToGamesFolder)
        try:
            targetDirectoryInfo = next(dirInfoIterator)
        except StopIteration:
            return False
        _, dirs, files = targetDirectoryInfo
        inputSanitizer = InputSanitizer()
        dirs = [
            inputSanitizer.perform_directory_name_replacement(dir, True) for dir in dirs
        ]
        files = [inputSanitizer.perform_filename_replacement(file) for file in files]
        return sorted(dirs + files)
