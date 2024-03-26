# keywords:
    # _BAD - this isn't handled super well, (it could break), but I'm not fixing it now.

# Extra fun stuff:
    # Investigate how to handle Json loading (object_hook).
    # Fix timestamp being an hour behind
        # (It's not due to code!?)
        # https://stackoverflow.com/questions/76413715/time-time-in-python-is-1-hour-behind-from-the-current-unix-epoch

# IMPORTED MODULES
import pathlib
import os
import json
import time
import difflib
from collections.abc import Callable
from git import Repo, DiffIndex, Diff # pip install GitPython
# Notes:
    # For new files:     a_mode/_blob/_path is None
    # For deleted files: b_mode/_blob/_path is None  

# CUSTOM TYPES/TUPLES
# variable names
CFG_K_OUTPUT = "pathOutput"
CFG_K_GITDIR = "pathGitDir"
CFG_K_COMMON = "commonFiles"
CFG_K_UNIQUE = "uniqueFiles"
# sub variable names
CFG_K_TYPES = "types"
CFG_K_NAME = "name"
CFG_K_KEYWORD = "keyword"

class TrackerConfig:
    # Members
    mWorkingDir:pathlib.Path
    mRelativePath:pathlib.Path
    mOutputPath:pathlib.Path            = ""
    mGitPath:pathlib.Path               = ""

    mWhitelist_common:set[str]          = set()
    mWhitelist_unique:set[str]          = set()
    mTodoKeywords_common:dict[str, str] = {}
    mTodoKeywords_unique:dict[str, str] = {}

    def __init__(self, configPath:pathlib.Path):
        self.mWorkingDir = pathlib.Path.cwd()

        # open and read file
        with open(configPath, "r") as configFile:
            configDir = json.load(fp=configFile)
            def typeify(filetype:str):
                return filetype if filetype.startswith('.') else ("." + filetype)
            
            def isNewCommonType(type):
                return type not in self.mTodoKeywords_common
            
            # load output path
            self.mOutputPath = pathlib.Path(configDir[CFG_K_OUTPUT])
            if self.mOutputPath.suffix != ".json":
                print("Warning - Specific output file was not in a json format")
                self.mOutputPath = pathlib.Path("todoRegister.json")

            # load git directory path
            self.mGitPath      = pathlib.Path(configDir[CFG_K_GITDIR]).resolve()
            self.mRelativePath = pathlib.Path(os.path.relpath(self.mWorkingDir, self.mGitPath))
            assert self.mGitPath in self.mWorkingDir.parents # _BAD - we should try to avoid asserts

            # load every allowed filetype and their todo-keyword
            for item in configDir[CFG_K_COMMON]:
                typeIdentifiers = list(map(typeify, item[CFG_K_TYPES]))
                self.mWhitelist_common.update(typeIdentifiers)

                newTypeIdentifiers = filter(isNewCommonType, typeIdentifiers)
                self.mTodoKeywords_common.update(dict.fromkeys(newTypeIdentifiers, item[CFG_K_KEYWORD]))

            # load every allowed unique file with their todo-keyword
            for item in configDir[CFG_K_UNIQUE]:
                uniqueName = item[CFG_K_NAME]
                ## optional block - don't allow items whose type is in common.
                # if pathlib.Path(uniqueName).suffix not in whitelist_common:
                self.mWhitelist_unique.add(uniqueName)
                if uniqueName not in self.mTodoKeywords_unique:
                    self.mTodoKeywords_unique[uniqueName] = item[CFG_K_KEYWORD]
    # End-func __init__
    
    def createConfigTemplateFile(configPath:pathlib.Path):
        configTemplate = {
            CFG_K_OUTPUT : "./",
            CFG_K_GITDIR : "./",
            CFG_K_COMMON : [ { CFG_K_TYPES : [ "" ], CFG_K_KEYWORD : "" } ],
            CFG_K_UNIQUE : [ { CFG_K_NAME : "", CFG_K_KEYWORD : "" } ]
        }
        configSerialized = json.dumps(configTemplate)
        with open(configPath, "w") as configFile:
            configFile.write(configSerialized)
    # End-func createConfigTemplateFile

    def createGitRepoObject(self):
        return Repo(self.mGitPath)
    # End-func createGitRepoObject

    def getStorageFilePath(self):
        return self.mOutputPath
    # End-func getStorageFilePath

    def whitelistFilter(self):
        def whitelistFunc(filePath:pathlib):
            # ignore files that we generate
            if filePath.parent == self.mRelativePath:
                return False

            # check the typing
            isStandardFile  = filePath.suffix in self.mWhitelist_common
            isUniqueFile    = filePath.suffix in self.mWhitelist_unique
            return isStandardFile or isUniqueFile
        return whitelistFunc
    # End-func whitelistFilter

    def todoDetector(self, file:pathlib.Path):
        # default with an "ignore" func when we try to investigate an invalid file.
        chosenDetector:Callable[[str], bool] = lambda line : False

        if file.suffix in self.mTodoKeywords_common:
            keyword = self.mTodoKeywords_common[file.suffix]
            chosenDetector = lambda line : keyword in line
        elif file.name in self.mTodoKeywords_unique:
            keyword = self.mTodoKeywords_unique[file.name]
            chosenDetector = lambda line : keyword in line
        
        return chosenDetector    
    # End-func todoDetector

    def getExtendedPath(self, filePath:pathlib.Path):
        return pathlib.Path.joinpath(self.mGitPath, filePath)
    # End-func getExtendedPath

    # debug function
    def printStats(self):
        print("==== Config stats: ====")
        print("Git path: ", self.mGitPath)
        print("Output path: ", self.mOutputPath)
        print("whitelist_common: ", self.mWhitelist_common)
        print("whitelist_unique: ", self.mWhitelist_unique)
        print("todoKeywords_common: ", self.mTodoKeywords_common)
        print("todoKeywords_unique: ", self.mTodoKeywords_unique)
        print("==== X ====")
    # End-func printStats
# End - TrackerConfig

class CommitTodos:
    # Members
    mDate = ""
    mTodoLines = [str]

    def __init__(self, date:str, todoComments:list[str]):
        self.mDate = date
        self.mTodoLines = todoComments
    # End-func __init__
        
    def commitDate(self) -> str:
        return self.mDate
    # End-func commitDate
    
    def tryRemoveComment(self, line:str):
        if line in self.mTodoLines:
            self.mTodoLines.remove(line)
            return True
        return False
    # End-func tryRemoveComment

    def empty(self) -> bool:
        return 0 == len(self.mTodoLines)
    # End-func empty
# End-class CommitTodos

class TodoRegister:
    # Literals
    KEY_ENTRY       = "trackedFiles"# list of files with todo comments
    KEY_FILE_NAME   = "File"        # name of the file, including filetype
    KEY_COMMITS     = "Commits"     # list of the file's "todo commits"
    KEY_DATE        = "Date"        # when the commit was made
    KEY_COMMENTS    = "Comments"    # The first line of the todo comment (including the todo-keyword)
    # Members
    mLUT:dict[pathlib.Path, list[CommitTodos]]   = {}
    mTimeStamp:str                               = "Unknown"

    def __init__(self, filePath:pathlib.Path, timeStamp:str):
        # Members
        self.mTimeStamp = timeStamp
        
        # open and read file if it exists
        if filePath.exists():
            with open(filePath, "r") as jsonFile:
                jsonLUT = json.load(fp=jsonFile)
                
                # _BAD - maybe make a function that checks validity and then returns an object on success.
                assert self.KEY_ENTRY in jsonLUT 

                for trackedFile in jsonLUT[self.KEY_ENTRY]:
                    filePath = pathlib.Path(trackedFile[self.KEY_FILE_NAME])
                    
                    commits:list[CommitTodos] = []
                    for commit in trackedFile[self.KEY_COMMITS]:
                        date     = commit[self.KEY_DATE]
                        comments = commit[self.KEY_COMMENTS]
                        commits.append(CommitTodos(date, comments))
                    
                    # _BAD - we don't check if filename (filePath) or date is in a good format
                        # Comments could also be in a bad format
                    self.mLUT[filePath] = commits
    # End-func __init__


    def removeOldComments(self, fileEntry:pathlib.Path, removedComments:list[str]):
        if fileEntry in self.mLUT:
            commits = self.mLUT[fileEntry]
            for line in removedComments:
                for commit in commits:
                    if commit.tryRemoveComment(line):
                        if commit.empty():
                            commits.remove(commit)
                        break
    # End-func removeOldCommentsInEntry

    def appendNewComments(self, fileEntry:pathlib.Path, appendedComments:list[str]):
        if fileEntry in self.mLUT:
            # update old entry with todo comments
            commits = self.mLUT[fileEntry]
            lastObject = commits[-1]
            # _BAD - This check to prevent copies of commits is not good.
            #        It would be better to compare against a commit hash or similar
            if (lastObject.commitDate() is not self.mTimeStamp) and (lastObject.mTodoLines != appendedComments):
                commits.append(CommitTodos(self.mTimeStamp, appendedComments))
        else:
            # create new entry with todo comments
            self.mLUT[fileEntry] = [ CommitTodos(self.mTimeStamp, appendedComments) ]
    # End-func updateRegistry


    def removeOldFileEntries(self, removedFiles:list[pathlib.Path]):
        # Unlike in previous code, we don't need to delete any "tracker files"
        
        # iterate each item and remove them from the LUT if they were there.
        for filePath in removedFiles:
            if filePath in self.mLUT:
                self.mLUT.pop(filePath)
    # End-func removeOldFileEntries

    def updateOldFileEntries(self, modifiedFiles:list[Diff], config:TrackerConfig):
        PREFIX_ADD      = "+ "
        PREFIX_REMOVE   = "- "
        PREFIX_OFFSET   = len(PREFIX_ADD)

        # Get differences and then sort found todo comments into "new" or "removed" 
        for item in modifiedFiles:
            # _BAD - It's good to verify, but we shouldn't need to do it here.
            assert not item.deleted_file
            assert item.a_path is not None
            assert item.a_blob is not None

            itemPath = pathlib.Path(item.a_path)
            todoCondition = config.todoDetector(itemPath)

            # There might be a better way to do this. 
            # I'm struggling with working with the types.
            oldContent = item.a_blob.data_stream.read().decode('utf-8')
            oldContentAsLines = str(oldContent).splitlines()

            fullFilePath = config.getExtendedPath(itemPath)
            newContent = open(fullFilePath, "r").read()
            newContentAsLines = newContent.splitlines()

            # Returns an iterator. it remembers each step we move it (loop only happens once.)
            diff = difflib.ndiff(oldContentAsLines, newContentAsLines)

            # Currently covers only the first line of a todo-comment
            # (Current method lacks row index)
            # (Method 3 here might be a better strategy: https://www.geeksforgeeks.org/compare-two-files-line-by-line-in-python/)
            createdTodoComments:list[str] = []
            removedTodoComments:list[str] = []
            for line in diff:
                # Will only check and "mark" the first line of a todo-comment
                if line.startswith(PREFIX_REMOVE) and todoCondition(line): 
                    removedTodoComments.append(line[PREFIX_OFFSET:])
                elif line.startswith(PREFIX_ADD) and todoCondition(line):
                    createdTodoComments.append(line[PREFIX_OFFSET:])        
            
            if 0 < len(removedTodoComments):
                self.removeOldComments(itemPath, removedTodoComments)
            if 0 < len(createdTodoComments):
                self.appendNewComments(itemPath, createdTodoComments)
    # func-end updateOldFileEntries

    def appendNewFileEntries(self, createdFiles:list[pathlib.Path], config:TrackerConfig):
        for itemPath in createdFiles:
            if itemPath in self.mLUT:
                print("Warning - Overwriting entry \"{}\" with new data".format(itemPath))
            
            # Open "new" file
            extendedPath = config.getExtendedPath(itemPath)
            with open(extendedPath, "r") as file:
                # Gather all the todo comments
                todoCondition = config.todoDetector(itemPath)
                foundTodoComments = list(filter(todoCondition, file.readlines()))

                # Create new entry if file had todo comments.
                if 0 < len(foundTodoComments):
                    self.mLUT[itemPath] = [ CommitTodos(self.mTimeStamp, foundTodoComments) ]
    # func-end appendNewFileEntries


    def saveRegisterToFile(self, outputPath:pathlib.Path):
        # Data to be written
        dictFormat = {
            self.KEY_ENTRY : [
                {
                    self.KEY_FILE_NAME: file.as_posix(),
                    self.KEY_COMMITS: [
                        {
                            self.KEY_DATE:      commit.commitDate(),
                            self.KEY_COMMENTS : commit.mTodoLines
                        }
                        for commit in commits 
                    ]
                }
                for file, commits in self.mLUT.items()
            ] 
        }
        
        # Serializing json
        json_object = json.dumps(dictFormat, indent=4)
        
        # Write to file
        with open(outputPath, "w") as outfile:
            outfile.write(json_object)
    # End-func updateRegistry


    # debug function
    def printRegister(self, detailed=False):
        print("==== TodoRegister stats: ====")
        for key, items in self.mLUT.items():
            print(key)
            if detailed:
                for item in items:
                    print("date: ", item.commitDate())
                    print("lines: ", item.mTodoLines)
            else:
                print("\t", items)
        print("==== X ====")
    # End-func printRegister
# End - TodoRegister


# HANDLE SETTINGS
def prepareFilterEntry(configPath:pathlib.Path, process:Callable[[TrackerConfig], bool]):
    '''
    Tries to load the TrackerConfig if the file exists, and calls the sent in process with it.
    Otherwise, it creates an empty TrackerConfig file.
    '''
    # https://docs.python.org/3/library/typing.html
    # type callerFunc = Callable[[], str] # only in py 3.12+
    # CallerFunc = Callable[[int], None]  # takes an int, returns nothing

    # annoying case where a string input isn't transformed into a pathlib.Path despite type hinting
    configPath = pathlib.Path(configPath) 
    if configPath.exists():
       currentConfig = TrackerConfig(configPath)
       process(currentConfig)
    else:
       TrackerConfig.createConfigTemplateFile(configPath)
# func-End - prepareFilterEntry

def createTimeStamp() -> str:
    ## time of previous commit
    #pCommitTime = time.gmtime(repo.head.commit.committed_date) 

    currentTime = time.gmtime(time.time()) 
    timeStamp = "{year}-{month:0>2}-{day:0>2} {hour:0>2}:{min:0>2}:{sec:0>2}".format(
        year    = currentTime.tm_year,
        month   = currentTime.tm_mon,
        day     = currentTime.tm_mday,
        hour    = currentTime.tm_hour,
        min     = currentTime.tm_min,
        sec     = currentTime.tm_sec
    )
    return timeStamp
# End-func 

## MAIN PROCESS
# DATA COLLECTION
def CollectCreatedFiles(gitFiles:list[str], whitelistFunc:Callable[[pathlib.Path], bool]) -> list[pathlib.Path]:
    createdFiles:list[pathlib.Path] = []
    for path in gitFiles:
        filePath = pathlib.Path(path)
        if whitelistFunc(filePath):
            createdFiles.append(filePath)

    return createdFiles
# func-end CollectCreatedFiles
def CollectDeletedFiles(gitFiles:DiffIndex, whitelistFunc:Callable[[pathlib.Path], bool]) -> list[pathlib.Path]:
    deletedFiles:list[pathlib.Path] = []
    for item in gitFiles.iter_change_type('D'):
        itemPath = pathlib.Path(item.a_path)
        if whitelistFunc(itemPath):
            deletedFiles.append(itemPath)

    return deletedFiles
# func-end CollectDeletedFiles
def CollectModifiedFiles(gitFiles:DiffIndex, whitelistFunc:Callable[[pathlib.Path], bool]) -> list[Diff]:
    modifiedFiles:list[Diff] = []
    # Modified files
    for item in gitFiles.iter_change_type('M'):
        itemPath = pathlib.Path(item.a_path)
        if whitelistFunc(itemPath):
            modifiedFiles.append(item)
    
    # renamed files
    for item in gitFiles.iter_change_type('R'):
        itemPath = pathlib.Path(item.a_path)
        if whitelistFunc(itemPath):
            modifiedFiles.append(item)

    return modifiedFiles
# func-end CollectModifiedFiles

def mainProcess(config:TrackerConfig):
    # [x] Read config settings
    # [x] Gather lists of new, modified and deleted files.
    # [x] Read saved files with todos
    # [x] get the current date (time stamp)
    # [x] remove saved files if their file has been deleted
    # [x] remove saved todos if they've been deleted in modified file
        # [x] sort out the created and removed todos in the modified files
        # [x] handle the removed todos in a modified file
        # [x] handle the created todos in a modified file
            # [x] In a registered "todo" file
            # [x] In a "discovered" "todo" file
    # [x] add line to saved[] if modified file got a todo line.
    # [x] add file to saved[] if created file has todo line
    # [x] Write over saved file with new data.
    # -- EXTRA --
    # [x] Fix the bug with allowing "autogenerated files" 
    # [x] (MAYBE) - don't add new comments if they're already registered under a entry # START WORKING HERE!!!

    # Print variables
    mPrintSettings       = False
    mPrintCollectedFiles = False
    mPrintTimeStamp      = False
    mPrintRegister       = False

    if mPrintSettings:
        config.printStats()
    
    if mPrintTimeStamp:
        print("Time Stamp: {}".format(createTimeStamp()))

    ## Prepare git repo
    repo = config.createGitRepoObject()
    
    # Prepare git difference
    hWorkingDiff = repo.head.commit.diff(None)

    fileFilterFunc = config.whitelistFilter()
    createdFiles = CollectCreatedFiles(repo.untracked_files, fileFilterFunc)
    removedFiles = CollectDeletedFiles(hWorkingDiff, fileFilterFunc)
    modifiedFiles = CollectModifiedFiles(hWorkingDiff, fileFilterFunc)
    if mPrintCollectedFiles:
        print("createdFiles: \n\t", createdFiles)
        print("removedFiles: \n\t", removedFiles)
        print("modifiedFiles: \n\t", modifiedFiles)
        
    registerFilePath = config.getStorageFilePath()

    ## Read all tracked files from the "Lookup table" file
    mRegister = TodoRegister(registerFilePath, createTimeStamp())

    ## Iterate all deleted items
    mRegister.removeOldFileEntries(removedFiles)

    ## Iterate all modified items.
    mRegister.updateOldFileEntries(modifiedFiles, config)
    
    ## Iterate all created items
    mRegister.appendNewFileEntries(createdFiles, config)

    if mPrintRegister:
        mRegister.printRegister()

    ## Save the current register to file.
    mRegister.saveRegisterToFile(registerFilePath)

    return True
# func-end mainProcess

if __name__ == "__main__":
    execute = True
    if execute:
        print("Started script")
        prepareFilterEntry("filter.json", mainProcess)