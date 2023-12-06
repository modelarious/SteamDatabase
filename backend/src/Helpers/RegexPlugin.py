from abc import ABC, abstractmethod
from os import replace, walk
import re

"""
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
"""


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
    "Linux",
]
directlyReplaceables = [
    "REPACK2-KaOs",
    "-Razor1911",
    "[FitGirl Repack]",
    "- [DODI Repack]",
    "-[DODI Repack]",
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
    "[Darck Repacks]",
    "plaza-",
    "REPACK",
    "FULL UNLOCKED RePack",
    "-KaOs",
    "INCL.DLC",
    "full",
    "Update",
    "MULTi9",
    "MULTi19" "Vigilancia.y.Seguridad",
    "Animation.Fix",
    "rzr-",
    "codex-",
    "Hotfix",
    "edcarnby",
    "PROPER",
    "- EE",
    "-RUNE",
    "- UE",
    "-TENOKE",
    "- RELOADED by CarlesNeo",
]

regexesToRemove = {
    r"sr-[a-zA-Z]": "sr-",
    r"rld-[a-zA-Z]": "rld-",
}

dotAndVersionReplacables = [
    "REPACK-KaOs",
    "REPACK2-KaOs",
    "-GOG",
    "-CODEX",
    "-SiMPLEX",
    "-THETA",
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
    "Early.Access",
]

underscoreReplacables = ["-DINOByTES", "-FLT", "Razor1911"]

paths = [
    r"C:\Users\micha\Documents\BiglyBT Downloads",
    r"D:\Downloads",
    r"D:\Bigly",
    r"F:\Downloads",
    r"J:\Downloads",
    r"Z:\Downloads",
    r"Z:\Games",
    r"\\TOWER\Big\games",
]

fileTypes = ["rar", "zip", "7z", "gz", "tar.zst", "iso"]

fileNameReplaceables = ["rld-", "-GOG", "-DARKZER0"]


def remove_extra_spaces(name):
    return " ".join(word for word in name.split(" ") if word != "")


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
    def wrapper(*args, **kwargs):
        name = func(*args, **kwargs)
        return name.strip()

    return wrapper


def remove_parenthesis_content(name):
    # Replace content between parentheses, square brackets, or curly braces
    # (including the brackets themselves) with an empty string.
    return re.sub(r"\s?[\[\(\{].*?[\]\)\}]\s?", " ", name).strip()


def too_many_letters(s):
    letter_count = 0
    non_letter_count = 0
    for char in s:
        if char == " ":
            continue
        if char.isalpha():
            letter_count += 1
            # print(f"char='{char}', which is a letter")
        else:
            # print(f"char={char}, which is not a letter")
            non_letter_count += 1
    return letter_count >= non_letter_count


class InputSanitizer(AbstractInputSanitizer):
    @remove_tailing_minus_one_wrapper
    @perform_strip_wrapper
    def perform_directory_name_replacement(
        self, dirName, try_removing_version_number: bool
    ):
        # print(f"starting with {dirName}")

        for skippable in skip:
            if skippable.lower() in dirName.lower():
                return "-" * 100

        # try simple replacement cases first
        for directlyReplaceable in directlyReplaceables:
            if directlyReplaceable in dirName:
                # print(dirName, "-->", "'" + perform_directory_name_replacement(dirName.replace(directlyReplaceable, "")) + "'")
                # print(perform_directory_name_replacement(dirName.replace(directlyReplaceable, "")))
                return self.perform_directory_name_replacement(
                    dirName.replace(directlyReplaceable, ""),
                    try_removing_version_number,
                )

        # check case where it is a KaOs repack
        # AMID.EVIL.v2172c.REPACK-KaOs -> AMID EVIL
        # Red.Faction.Armageddon.v1.01.REPACK-KaOs -> Red Faction Armageddon
        # Transport.Fever.2.v33872-GOG -> Transport Fever 2
        for dotAndVersionReplacable in dotAndVersionReplacables:
            if dotAndVersionReplacable in dirName:
                return self.perform_directory_name_replacement(
                    dirName.replace(dotAndVersionReplacable, "").replace(".", " "),
                    try_removing_version_number,
                )

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
            return self.perform_directory_name_replacement(
                updatedName, try_removing_version_number
            )

        for dotReplacable in dotReplacables:
            if dotReplacable in dirName:
                # print(dirName.replace(dotReplacable, "").replace(".", " "))
                return self.perform_directory_name_replacement(
                    dirName.replace(dotReplacable, "").replace(".", " "),
                    try_removing_version_number,
                )

        for underscoreReplacable in underscoreReplacables:
            if underscoreReplacable in dirName:
                # print(dirName.replace(underscoreReplacable, "").replace("_", " "))
                return self.perform_directory_name_replacement(
                    dirName.replace(underscoreReplacable, "").replace("_", " "),
                    try_removing_version_number,
                )

        for reg_exp, to_replace in regexesToRemove.items():
            if re.search(reg_exp, dirName):
                dirName = dirName.replace(to_replace, "")

        # print(f"I'm about to remove -1 from {dirName}")
        dirName = remove_parenthesis_content(dirName)
        if dirName[-2:] == "-1":
            dirName = dirName[:-2]
        # print(f"after is {dirName}")

        print(f"working on removing version number from {dirName}")
        if try_removing_version_number:
            # if we've already tried to remove the version number, don't try again
            try_removing_version_number = False

            if re.search(r"\b[Bb]uild\b", dirName):
                try:
                    buildIndex = dirName.lower().rindex("build")
                    possibleVersionNumber = dirName[buildIndex + len("build") :]
                    if too_many_letters(possibleVersionNumber):
                        # print(f"there are {count_letters(possibleVersionNumber)} letters, therefore, not doing replacement")
                        return self.perform_directory_name_replacement(
                            dirName, try_removing_version_number
                        )

                    outName = dirName[:buildIndex]
                    return self.perform_directory_name_replacement(
                        outName, try_removing_version_number
                    )
                except ValueError:
                    return self.perform_directory_name_replacement(
                        dirName, try_removing_version_number
                    )
            if "v" in dirName.lower():
                if "VR" in dirName:
                    return self.perform_directory_name_replacement(
                        dirName, try_removing_version_number
                    )
                # print("Found a v in the name")
                # if version number exists in file name......
                try:
                    versionNumberIndex = dirName.lower().rindex("v")
                    possibleVersionNumber = dirName[versionNumberIndex + 1 :]
                    # print(f"possible version number is {possibleVersionNumber}")
                    # if the possible version string contains more than one letter, it's likely not a version string
                    if too_many_letters(possibleVersionNumber):
                        # print(f"there are too many letters therefore, not doing replacement")
                        return self.perform_directory_name_replacement(
                            dirName, try_removing_version_number
                        )

                    outName = dirName[:versionNumberIndex]
                    return self.perform_directory_name_replacement(
                        outName, try_removing_version_number
                    )

                # this is fine - this just means there was no version number in the filename
                except ValueError:
                    return self.perform_directory_name_replacement(
                        dirName, try_removing_version_number
                    )

            # print("TRYING TO REPLACE")
            pattern = r"\d+(\.\d+)+"

            match = re.search(pattern, dirName)
            # print(f"match found? {match}")
            if match:
                return self.perform_directory_name_replacement(
                    dirName.replace(match.group(), ""), try_removing_version_number
                )
            return self.perform_directory_name_replacement(
                dirName, try_removing_version_number
            )

        for sep in [".", "_"]:
            dirName = " ".join(dirName.split(sep))
        return remove_extra_spaces(dirName)

    def possibly_replace(self, pattern: str, filename: str) -> str:
        versionStringPossibleMatch = re.search(pattern, filename)
        if versionStringPossibleMatch:
            versionString = versionStringPossibleMatch.group(0)
            newName = filename.replace(versionString, "")
            return newName
        return filename

    def perform_filename_replacement(self, filename: str) -> str:
        # match a "v" followed by a number - that will match the entire version string and file extension
        # ex: Tales.of.Majeyal.v1.7.2.ALl.DLC.GOG.rar -> matches v1.7.2.ALl.DLC.GOG.rar
        # OR
        # match a series of 2 or more numbers followed by a file extension (rar, zip, 7z, etc) like "Ai.War.2.138962.rar" would match the "138962.rar"
        version_pattern = f"(v|e)\d+.+|\d\d+.({'|'.join(fileTypes)})"
        beta_pattern = r".Beta(.\d+)+"
        build_pattern = r".Build.\d+"
        early_access_pattern = r".Early.Access"

        newName = filename
        newName = self.possibly_replace(build_pattern, newName)
        newName = self.possibly_replace(version_pattern, newName)
        newName = self.possibly_replace(beta_pattern, newName)
        newName = self.possibly_replace(early_access_pattern, newName)

        for replaceable in fileNameReplaceables:
            newName = newName.replace(replaceable, "")

        nameSplit = newName.split(".")
        outName = " ".join(nameSplit[:-1])

        # XXX XXX this is a real problem.  Some things are getting reduced to an empty string
        # assert outName != "", f"{filename} was reduced to nothing"
        if outName == "":
            print(f"{filename} was reduced to nothing")
            return filename
        return outName


def main():
    inputSanitizer = InputSanitizer()
    directories, filenames = [], []
    for path in paths:
        _, currDirectories, currFilenames = next(walk(path), (None, [], []))
        directories.extend(currDirectories)
        filenames.extend(currFilenames)
    outputDirs = [
        f'    ["{dirName}", "{inputSanitizer.perform_directory_name_replacement(dirName, True)}"],'
        for dirName in directories
    ]
    # outputFilenames = [f"    [\"{filename}\", \"{inputSanitizer.perform_filename_replacement(filename)}\"]," for filename in filenames]

    # out = outputDirs + outputFilenames

    print("[")
    for x in outputDirs:
        print(x)
    print("]")


if __name__ == "__main__":
    main()
