from os import walk


class DirListFetcher:
    def get_dirs(self, pathToGamesFolder: str):
        dirInfoIterator = walk(pathToGamesFolder)
        try:
            directoryInfo = next(dirInfoIterator)
        except StopIteration:
            return False
        dirs = directoryInfo[1]
        return sorted(dirs)


x = DirListFetcher()

# returns an array with values
print(x.get_dirs("/usr"))

# returns False
print(x.get_dirs("/ussr"))
