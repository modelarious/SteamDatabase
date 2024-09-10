from os import walk
from Helpers.RegexPlugin import InputSanitizer
from typing import List


class DirListFetcher:
    def get_files_and_dirs(self, pathToGamesFolder: str) -> List[str]:
        dirInfoIterator = walk(pathToGamesFolder)
        try:
            targetDirectoryInfo = next(dirInfoIterator)
        except StopIteration:
            print(f"ERROR: No directories found in the path provided - does '{pathToGamesFolder}' exist?")
            return []

        _, dirs, files = targetDirectoryInfo
        inputSanitizer = InputSanitizer()
        dirs = [
            inputSanitizer.perform_directory_name_replacement(dir, True) for dir in dirs
        ]
        files = [inputSanitizer.perform_filename_replacement(file) for file in files]
        items = [remove_non_approved_characters(item) for item in sorted(dirs + files)]
        return items

approved_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890:!@#$%^&()_+{}|[]:;<>,?-= ")
def remove_non_approved_characters(string: str) -> str:
    return ''.join(e for e in string if e in approved_characters)
