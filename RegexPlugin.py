from abc import ABC, abstractmethod
from os import walk
import re

'''
dirs snuck through:


#Devil Slayer Raksasi v1 2 2
#Wuppo Definitive Edition v1 0 37
#Fort Triumph v1 1 6
#Timelie v.1.1.0  (2020)
#The Beginners Guide (2015)
SYNTHETIK Legion Rising ULTIMATE v39-
Strategic Command WWII War in Europe v1.21.01-
Star Wars - Republic Commando 2.0.0.6
Moonlighter Between Dimensions v1.14.29
Element TD 2 Update v1 1
Element TD 2 Update v1 1
Valheim v0 148 7
The Dungeon Of Naheulbeuk The Amulet Of Chaos v1.2.47.38606-
SpellForce 3 Fallen God v1.6-
Creeper World 4 v2.0.1-
Wuppo Definitive Edition v1 0 37
There Is No Game Wrong Dimension v1.0.29-
Shantae And The Seven Sirens v731089-
'''

class AbstractInputSanitizer(ABC):
    @abstractmethod
    def perform_directory_name_replacement(self, directoryName: str) -> str:
        return ""
    
    @abstractmethod
    def perform_filename_replacement(self, fileName: str) -> str:
        return ""

# XXX temporary
skip = [
    "Toontrack",
    "spectrasonics",
    "steinberg",
    "getgood",
    "FL Studio",
    "CCleaner",
    "Matt Halpern",
    "Linux"
]
directlyReplaceables = [
    "[FitGirl Repack]",
    "- [DODI Repack]",
    "[R2VP01]",
    "[GOG]",
    "[Masquerade Repack]",
    "{TJ}",
    "- ELAMIGOS",
    "- CorePack",
    "- [Tiny Repack]",
    "by xatab",
    "[ELECTRO-TORRENT.PL]",
    "- [EMPRESS DODI Repack]",
    "[Darck Repacks]"
]

dotAndVersionReplacables = [
    "REPACK-KaOs",
    "REPACK2-KaOs",
    "-GOG",
    "-CODEX",
    "-SiMPLEX",
    "-THETA"
]

dotReplacables = [
    "-PLAZA",
    "-DARKSiDERS",
    "-DOGE",
    "-DARKZER0",
    "-Unleashed",
    "-PiNDASAUS",
    "-RELOADED",
    "-TiNYiSO",
    "-SKIDROW",
    "-PROPHET",
    "-EMPRESS",
    "-VREX",
    "Early.Access"
]

underscoreReplacables = [
    "-DINOByTES",
    "-FLT",
    "Razor1911"
]

paths = [
    r"C:\Users\micha\Documents\BiglyBT Downloads",
    r"D:\Downloads",
    r"D:\Bigly",
    r"F:\Downloads",
    r"J:\Downloads",
    r"Z:\Downloads",
    r"Z:\Games"
]

fileTypes = [
    "rar",
    "zip",
    "7z",
    "gz",
    "tar.zst"
]

# on windows - when a folder is a copy of another folder, windows adds a -1 to the end of the file, the next copy is -2, etc
# this wrapper removes a -1 (but not any other copy indicator like -2)
def remove_tailing_minus_one_wrapper(func):
    def wrapper(*args, **kwargs):
        name = func(*args, **kwargs)
        if name[-2:] == "-1":
            return name[:-2]
        return name
    return wrapper

def perform_strip_wrapper(func):
    def wrapper( *args, **kwargs):
        name = func(*args, **kwargs)
        return name.strip()
    return wrapper

class InputSanitizer(AbstractInputSanitizer):

    @remove_tailing_minus_one_wrapper
    @perform_strip_wrapper
    def perform_directory_name_replacement(self, dirName):
        for skippable in skip:
            if skippable.lower() in dirName.lower():
                return "-" * 100
        
        # try simple replacement cases first
        for directlyReplaceable in directlyReplaceables:
            if directlyReplaceable in dirName:
                # print(dirName, "-->", "'" + perform_directory_name_replacement(dirName.replace(directlyReplaceable, "")) + "'") 
                # print(perform_directory_name_replacement(dirName.replace(directlyReplaceable, "")))
                return self.perform_directory_name_replacement(dirName.replace(directlyReplaceable, ""))

        # check case where it is a KaOs repack
        # AMID.EVIL.v2172c.REPACK-KaOs -> AMID EVIL 
        # Red.Faction.Armageddon.v1.01.REPACK-KaOs -> Red Faction Armageddon
        # Transport.Fever.2.v33872-GOG -> Transport Fever 2
        for dotAndVersionReplacable in dotAndVersionReplacables:
            if dotAndVersionReplacable in dirName:
                newName = dirName.replace(dotAndVersionReplacable, "").replace(".", " ")

                # if version number exists in file name...... 
                # XXX oh lol, if version doesn't exist in the filename and the file has a "v" in it then this will break
                # XXX the way to fix this would be to go backwards through the string making sure you hit numbers, spaces and periods, and stop when you hit the v.
                # XXX and if you don't hit a v but run into another character that isnt a number, space or period, then you claim there is no version string
                try:
                    versionNumberIndex = newName.lower().rindex("v")
                    outName = newName[:versionNumberIndex]
                    # print(outName)
                    return self.perform_directory_name_replacement(outName)
                
                # this is fine - this just means there was no version number in the filename
                except ValueError:
                    # print(newName)
                    return self.perform_directory_name_replacement(newName)
        
        # Just_Cause_2_1.0.0.2_(50335)_win_gog
        # Steel_Division_2_51957_(47364)_win_gog-1
        # Streets_of_Rogue_95_(48531)_win_gog
        if ")_win_gog" in dirName or ")_win_dev_gog" in dirName:
            # if this doesn't exist, I want an exception to be triggered because the format is invalid
            openBracketIndex = dirName.rindex("(")
            updatedName = dirName[:openBracketIndex]

            # remove version and split something like
            # Streets_of_Rogue_95_
            updatedName = " ".join(updatedName.split("_")[:-2])
            # print(updatedName)
            return self.perform_directory_name_replacement(updatedName)
        
        for dotReplacable in dotReplacables:
            if dotReplacable in dirName:
                # print(dirName.replace(dotReplacable, "").replace(".", " "))
                return self.perform_directory_name_replacement(dirName.replace(dotReplacable, "").replace(".", " "))
        
        for underscoreReplacable in underscoreReplacables:
            if underscoreReplacable in dirName:
                # print(dirName.replace(underscoreReplacable, "").replace("_", " "))
                return self.perform_directory_name_replacement(dirName.replace(underscoreReplacable, "").replace("_", " "))
        # print(dirName)
        return dirName
    
    def possibly_replace(self, pattern: str, filename: str) -> str:
        versionStringPossibleMatch = re.search(pattern, filename)
        if versionStringPossibleMatch:
            versionString = versionStringPossibleMatch.group(0)
            newName = filename.replace(versionString, "")
            return newName
        return filename

    def perform_filename_replacement(self, filename: str) -> str:
        #match a "v" followed by a number - that will match the entire version string and file extension
        # ex: Tales.of.Majeyal.v1.7.2.ALl.DLC.GOG.rar -> matches v1.7.2.ALl.DLC.GOG.rar
        # OR
        # match a series of 2 or more numbers followed by a file extension (rar, zip, 7z, etc) like "Ai.War.2.138962.rar" would match the "138962.rar"
        version_pattern = f"(v\d+.+|\d\d+.({'|'.join(fileTypes)}))"
        build_pattern = r"(.Build.\d+)"
        newName = filename
        newName = self.possibly_replace(build_pattern, newName)
        newName = self.possibly_replace(version_pattern, newName)

        nameSplit = newName.split(".")
        outName = " ".join(nameSplit[:-1])
        assert outName != ""
        return outName

        updatedName = filename
        for fileType in fileTypes:
            updatedName = updatedName.replace(f".{fileType}", "")
        updatedName = self.perform_directory_name_replacement(updatedName) # XXX why only here?
        updatedName = " ".join(updatedName.split("."))
        return updatedName

class DebugInputSanitizer(AbstractInputSanitizer):

    @remove_tailing_minus_one_wrapper
    @perform_strip_wrapper
    def perform_directory_name_replacement(self, dirName):
        for skippable in skip:
            if skippable.lower() in dirName.lower():
                return "-" * 100
        
        # try simple replacement cases first
        for directlyReplaceable in directlyReplaceables:
            if directlyReplaceable in dirName:
                # print(dirName, "-->", "'" + perform_directory_name_replacement(dirName.replace(directlyReplaceable, "")) + "'") 
                # print(perform_directory_name_replacement(dirName.replace(directlyReplaceable, "")))
                return self.perform_directory_name_replacement(dirName.replace(directlyReplaceable, ""))

        # check case where it is a KaOs repack
        # AMID.EVIL.v2172c.REPACK-KaOs -> AMID EVIL 
        # Red.Faction.Armageddon.v1.01.REPACK-KaOs -> Red Faction Armageddon
        # Transport.Fever.2.v33872-GOG -> Transport Fever 2
        for dotAndVersionReplacable in dotAndVersionReplacables:
            if dotAndVersionReplacable in dirName:
                newName = dirName.replace(dotAndVersionReplacable, "").replace(".", " ")

                # if version number exists in file name...... 
                # XXX oh lol, if version doesn't exist in the filename and the file has a "v" in it then this will break
                # XXX the way to fix this would be to go backwards through the string making sure you hit numbers, spaces and periods, and stop when you hit the v.
                # XXX and if you don't hit a v but run into another character that isnt a number, space or period, then you claim there is no version string
                try:
                    versionNumberIndex = newName.lower().rindex("v")
                    outName = newName[:versionNumberIndex]
                    # print(outName)
                    return self.perform_directory_name_replacement(outName)
                
                # this is fine - this just means there was no version number in the filename
                except ValueError:
                    # print(newName)
                    return self.perform_directory_name_replacement(newName)
        
        # Just_Cause_2_1.0.0.2_(50335)_win_gog
        # Steel_Division_2_51957_(47364)_win_gog-1
        # Streets_of_Rogue_95_(48531)_win_gog
        if ")_win_gog" in dirName or ")_win_dev_gog" in dirName:
            # if this doesn't exist, I want an exception to be triggered because the format is invalid
            openBracketIndex = dirName.rindex("(")
            updatedName = dirName[:openBracketIndex]

            # remove version and split something like
            # Streets_of_Rogue_95_
            updatedName = " ".join(updatedName.split("_")[:-2])
            # print(updatedName)
            return self.perform_directory_name_replacement(updatedName)
        
        for dotReplacable in dotReplacables:
            if dotReplacable in dirName:
                # print(dirName.replace(dotReplacable, "").replace(".", " "))
                return self.perform_directory_name_replacement(dirName.replace(dotReplacable, "").replace(".", " "))
        
        for underscoreReplacable in underscoreReplacables:
            if underscoreReplacable in dirName:
                # print(dirName.replace(underscoreReplacable, "").replace("_", " "))
                return self.perform_directory_name_replacement(dirName.replace(underscoreReplacable, "").replace("_", " "))
        # print(dirName)
        return dirName
    
    def possibly_replace(self, pattern: str, filename: str) -> str:
        versionStringPossibleMatch = re.search(pattern, filename)
        if versionStringPossibleMatch:
            versionString = versionStringPossibleMatch.group(0)
            newName = filename.replace(versionString, "")
            return f"{filename} -> {newName}"
        return filename

    def perform_filename_replacement(self, filename: str) -> str:
        #match a "v" followed by a number - that will match the entire version string and file extension
        # ex: Tales.of.Majeyal.v1.7.2.ALl.DLC.GOG.rar -> matches v1.7.2.ALl.DLC.GOG.rar
        # OR
        # match a series of 2 or more numbers followed by a file extension (rar, zip, 7z, etc) like "Ai.War.2.138962.rar" would match the "138962.rar"
        version_pattern = f"(v\d+.+|\d\d+.({'|'.join(fileTypes)}))"
        build_pattern = f"(.Build.\d+)"
        newName = filename
        newName = self.possibly_replace(build_pattern, newName)
        newName = self.possibly_replace(version_pattern, newName)

        nameSplit = newName.split(".")
        outName = " ".join(nameSplit[:-1])
        assert outName != ""
        return f"{filename} -> {outName}", outName

        updatedName = filename
        for fileType in fileTypes:
            updatedName = updatedName.replace(f".{fileType}", "")
        updatedName = self.perform_directory_name_replacement(updatedName) # XXX why only here?
        updatedName = " ".join(updatedName.split("."))
        return updatedName

def main():
    inputSanitizer = InputSanitizer()
    directories, filenames = [], []
    for path in paths:
        _, currDirectories, currFilenames = next(walk(path), (None, [], []))
        directories.extend(currDirectories)
        filenames.extend(currFilenames)
    # outputDirs = [inputSanitizer.perform_directory_name_replacement(dirName) for dirName in directories]
    outputFilenames = [f"    [\"{filename}\", \"{inputSanitizer.perform_filename_replacement(filename)}\"]," for filename in filenames]
    
    # out = outputDirs + outputFilenames

    print("[")
    for x in outputFilenames:
        print(x)
    print("]")
    


if __name__ == "__main__":
    main()