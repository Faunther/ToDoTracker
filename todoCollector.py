# python 3.x

# True  False
callPass1 = False
callPass2 = False
callPass3 = False
callPass4 = False #
callPass5 = False
callPass6 = False

callPass7 = True

# reference guide
# https://realpython.com/working-with-files-in-python/

import os

if (callPass1):
    print('---- 1st pass ----')
    
    entries = os.scandir('../../include/')
    for entry in entries:
        if entry.is_file():
            print('file: {}'.format(entry.name))
        if entry.is_dir():
            print('dir:  {}'.format(entry.name))

import glob

if (callPass2):
    print('---- 2nd pass ----')
    for file in glob.iglob('../../include/**/*.hpp', recursive=True):
        print(file)


if (callPass3):
    print('---- 3rd pass ----')
    for dirpath, dirnames, files in os.walk('../../include'):
        print(f'Found directory: {dirpath}')
        for file_name in files:
            print(file_name)


# GitPython module reference
# https://gitpython.readthedocs.io/en/stable/tutorial.html
# https://gitpython.readthedocs.io/en/stable/reference.html#module-git.diff

# Get changed files using gitpython
# https://stackoverflow.com/questions/33733453/get-changed-files-using-gitpython

# gitpython and git diff
# https://stackoverflow.com/questions/20061898/gitpython-and-git-diff

# How to filter git diff based on file extensions?
# https://stackoverflow.com/questions/8554776/how-to-filter-git-diff-based-on-file-extensions

# pip install GitPython
from git import Repo, DiffIndex, Diff
# Notes:
    # For new files:     a_mode/_blob/_path is None
    # For deleted files: b_mode/_blob/_path is None

import pathlib

def filterHeaders(gitObject):
    if gitObject.change_type == 'M':
        file_extension = pathlib.Path(gitObject.a_path).suffix
        if file_extension == '.hpp':
            return True
        else:
            return False
    else:
        return False
   

def printGitObjectAttributesA(item):
    print('\t-a_blob    {}'.format(item.a_blob))
    print('\t-a_mode    {}'.format(item.a_mode))
    print('\t-a_path    {}'.format(item.a_path)) #
    print('\t-a_rawpath {}'.format(item.a_rawpath))

def printGitObjectAttributesB(item):
    print('\t-b_blob    {}'.format(item.b_blob))
    print('\t-b_mode    {}'.format(item.b_mode))
    print('\t-b_path    {}'.format(item.b_path))
    print('\t-b_rawpath {}'.format(item.b_rawpath))

def printGitObjectChangeAttributes(item):
    print('\t-change_type       {}'.format(item.change_type)) #
    print('\t-copied_file       {}'.format(item.copied_file))
    print('\t-deleted_file      {}'.format(item.deleted_file))
    print('\t-new_file          {}'.format(item.new_file))
    print('\t-renamed_file      {}'.format(item.renamed_file))
    if item.renamed_file:
        print('\t-raw_rename_from   {}'.format(item.raw_rename_from))
        print('\t-raw_rename_to     {}'.format(item.raw_rename_to))
        print('\t-rename_from       {}'.format(item.rename_from))
        print('\t-rename_to         {}'.format(item.rename_to))

def printGitObjectAttributesMisc(item):
    print('\t-re_header {}'.format(item.re_header))
    print('\t-score     {}'.format(item.score))

def printGitObjectAttributesDiff(item):
    print('\t-diff self  {}'.format(item.diff))

def printWholeGitObject(item):
    printGitObjectAttributesA(item)
    printGitObjectAttributesB(item)
    printGitObjectChangeAttributes(item)
    printGitObjectAttributesDiff(item)

def printGitObjectBlobA(item):
    #print("A blob:\n{}\n".format(item.a_blob.data_stream.read().decode('utf-8')))
    print("A blob:")
    # print("- {}\n".format(item.a_blob))
    # print("- {}\n".format(item.a_blob.data_stream))
    # print("- {}\n".format(item.a_blob.data_stream.read()))
    # print("- {}".format(item.a_blob.data_stream.read().decode('utf-8')))
    print(item.a_blob.data_stream.read().decode('utf-8'))


import difflib
def printGitObjectBlobDiff(repo, item):
    if not item.deleted_file and item.a_blob is not None:
        blobContentA_stream  = item.a_blob.data_stream
        blobContentA_read = blobContentA_stream.read()
        blobContentA_decode = blobContentA_read.decode('utf-8')

        #print("stream: \n", blobContentA_stream)
        #print("read: \n", blobContentA_read)
        #print("decode: \n", blobContentA_decode)
        blobAList = str(blobContentA_decode).splitlines()
        #print(blobAList)

        print("# ========================================================================================= #")

        blobContentA = item.a_blob.data_stream.read().decode('utf-8')
        #blobContentA_1 = item.a_blob.data_stream.readLines()
        #print(blobContentA_1)

        #blobContentB = item.b_blob.data_stream.read().decode('utf-8')
        
        realPath = os.path.join(repo.working_dir, item.a_path)
        blobContentB = open(realPath, "r").read()
        #blobContentB = open(realPath, "r").readlines()
        #print(blobContentB)

        blobBList = blobContentB.splitlines()
        #print(blobBList)
        
        #blobContentDelta = difflib.context_diff(blobContentA, blobContentB)
        #print(blobContentDelta)

        diff = difflib.ndiff(blobAList, blobBList)

        for line in diff:
            if line.startswith('+ '):
                print(line[2:])
        
        #diff = difflib.ndiff(blobContentA, blobContentB)
        #for line in list(diff):
        #    print(line)

        #delta = ''.join(x[2:] for x in diff if x.startswith('+ '))
        #print(delta)
        print("# ========================================================================================= #")


if (callPass4):
    print('---- 4th pass ----')
    pk_repo_path = '../../'

    # True  False
    printRepoDirs = False
    printDiffLens = False
    printIndexBlobs = False
    printHeadTreeBlobs = False
    printFirstChanged = False

    repo = Repo(pk_repo_path)
    if printRepoDirs:
        print("repo.working_dir     : ", repo.working_dir)
        print("repo.working_tree_dir: ", repo.working_tree_dir)
        print("repo.git_dir         : ", repo.git_dir)
        print("repo.common_dir      : ", repo.common_dir)

    #changed = [item.a_path for item in repo.index.diff(None)]  # create a list of paths from the items in index.diff(None)
    #changed = repo.index.diff(None, kwargs="-- '*.hpp'") # failed
    changed = repo.index.diff(None)
    #changed = repo.index.diff()
    
    if printDiffLens:
        print("index :")
        print("\t()      : ", len(repo.index.diff()))
        print("\t(None)  : ", len(repo.index.diff(None)))
        print("\t(HEAD)  : ", len(repo.index.diff("HEAD")))
        
        print("HEAD :")
        print("\t()      : ", len(repo.head.commit.diff()))
        print("\t(None)  : ", len(repo.head.commit.diff(None)))
        print("\t(HEAD)  : ", len(repo.head.commit.diff("HEAD")))
        print("\t(HEAD~1): ", len(repo.head.commit.diff("HEAD~1")))
    
    if printIndexBlobs:
        print("index blobs:")
        print(len(list(repo.index.iter_blobs())))
        for _stage, _blob in list(repo.index.iter_blobs())[:5]: # iterate first 5 objects in list
            print(_blob.name)
            #print(_blob.path)
            #print(_blob.size)
    
    hct = repo.head.commit.tree
    if printHeadTreeBlobs:
        print("\n# HCT :")
        print(len(hct.blobs))
        for blob in hct.blobs[:2]:
            print("---------------------------------------------------------------------------------------")
            print(blob.name)
            print(blob.data_stream.read().decode('utf-8'))
        print("---------------------------------------------------------------------------------------")
    
    if printFirstChanged:
        if changed[0].change_type == 'M':
            print(changed[0].a_path)
            if hct[changed[0].a_path]:
                print("exists")
                print(hct[changed[0].a_path].data_stream.read().decode('utf-8'))


    changedHeaders = filter(filterHeaders, changed)
    
    todoTargets = changed
    # todoTargets = changed.iter_change_type('M')
    #todoTargets = changedHeaders

    for item in todoTargets:
        if item.change_type == 'M':
            print(item.a_path)
        elif item.change_type == 'A':   # Seems like this won't happen unless we are comparing against a commit.
            print(item.b_path)
        elif item.change_type == 'D':
            print(item.b_path)

        printGitObjectAttributesA(item)
        #printGitObjectAttributesB(item)
        printGitObjectChangeAttributes(item)
        #printGitObjectBlobA(item)
        printGitObjectBlobDiff(repo, item)

if callPass5:
    pk_repo_path = '../../'
    repo = Repo(pk_repo_path) 
    commits_list = list(repo.iter_commits())
    print("First commit: ", commits_list[0])

    changed_files = []
    
    for x in commits_list[0].diff(commits_list[1]):
        if x.a_blob is not None and x.a_blob.path not in changed_files:
            changed_files.append(x.a_blob.path)
        
        if x.b_blob is not None and x.b_blob.path not in changed_files:
            changed_files.append(x.b_blob.path)
        
    print(changed_files)

if callPass6:
    # https://gitpython.readthedocs.io/en/stable/tutorial.html#obtaining-diff-information

    pk_repo_path = '../../'
    repo = Repo(pk_repo_path) 

    hcommit = repo.head.commit
    index = repo.index
    
    # True  False
    printRawHeadAndIndexDiffs = False
    printHeadDiffs = False
    printIndexDiffs = False
    printUntracked = True
    printHeadTreeBlobs = False
    printHeadTreeTrees = False

    if printRawHeadAndIndexDiffs:
        print(hcommit.diff())           # diff tree against index
        print(hcommit.diff("HEAD~1"))   # diff tree against previous tree
        print(hcommit.diff(None))       # diff tree against working tree

        print(index.diff())             # diff index against itself yielding empty diff
        print(index.diff(None))         # diff index against working copy
        print(index.diff("HEAD"))       # diff index against current HEAD tree

    # "HEAD~1" (previous "commit")
    if printHeadDiffs:
        print("\n# (head.commit) Traverse added Diff objects only ")
        for diff_added in hcommit.diff(None).iter_change_type("A"):
            print(diff_added)
        print("\n# (head.commit) Traverse removed Diff objects only")
        for diff_removed in hcommit.diff(None).iter_change_type("D"):
            print(diff_removed)
        print("\n# (head.commit) Traverse modified Diff objects only")
        for diff_modified in hcommit.diff(None).iter_change_type("M"):
            print(diff_modified)

    if printIndexDiffs:
        print("\n# (index) Traverse added Diff objects only ")
        for diff_added in index.diff(None).iter_change_type("A"):
            print(diff_added)
        print("\n# (index) Traverse removed Diff objects only")
        for diff_removed in index.diff(None).iter_change_type("D"):
            print(diff_removed)
        print("\n# (index) Traverse modified Diff objects only")
        for diff_modified in index.diff(None).iter_change_type("M"):
            print(diff_modified)

    if printUntracked:
        print("\n# Traverse untracked_files")
        for untracked in repo.untracked_files:
            print(untracked)

    if printHeadTreeBlobs:
        print("\n# Traverse Hcommit blobs") # objects in the directory. So all files in root_dir
        for blob in hcommit.tree.blobs:
            print(blob.name)
            print(blob.mode)
            print(blob.data_stream.read())

    if printHeadTreeTrees:
        print("\n# Traverse Hcommit tree") 
            # all known folders with content that we don't ignore in the directory
            # So empty folders, folders mentioned in .gitignore, and uncommited folders do NOT appear.
        for tree in hcommit.tree.trees:
            print(tree.name)
            print(tree.mode)
    
    for (_path, _stage), _entry in index.entries.items():
        #print(_path)
        #print(_stage)
        #print(_entry)
        pass


def filterFile(gitObject):
    if gitObject.change_type == 'M':
        file_extension = pathlib.Path(gitObject.a_path).suffix
        # pathlib.Path(gitObject.a_path).name
        if file_extension == '.hpp':
            return True
        else:
            return False
    else:
        return False

    

from itertools import takewhile
from collections import deque
from typing import NamedTuple, Union
import time

TRACKER_FILE_FORMAT = "tracker{}.txt"
def ExtractTrackerIndex(trackedFileName:str) -> int:
    index = trackedFileName[len("tracker"):-len(".txt")]
    return int(index)

class TrackedFileLUT(NamedTuple):
    trackedFiles:   dict[pathlib.Path, int]         = {}
    itemSlots:      list[Union[pathlib.Path, None]] = list()

    def registerNewEntry(self, trackedFilePath:pathlib.Path) -> str:
        itemIndex:int = 0
        ## Alternative to try-except
        #if None in self.itemSlots:
        #    itemIndex = self.itemSlots.index(None)
        #    self.itemSlots[itemIndex] = trackedFilePath
        #else:
        #    itemIndex = len(self.itemSlots)
        #    self.itemSlots.append(trackedFilePath)
        try:
            itemIndex = self.itemSlots.index(None)
            self.itemSlots[itemIndex] = trackedFilePath
        except:
            itemIndex = len(self.itemSlots)
            self.itemSlots.append(trackedFilePath)

        self.trackedFiles[trackedFilePath] = itemIndex
        trackerFileName = TRACKER_FILE_FORMAT.format(itemIndex)
        return trackerFileName
    
    def hasEntry(self, itemPath:pathlib.Path) -> bool:
        return itemPath in self.trackedFiles

    def getTrackerFile(self, itemPath:pathlib.Path) -> str:
        return TRACKER_FILE_FORMAT.format(self.trackedFiles[itemPath])

    def freeEntry(self, itemPath:pathlib.Path) -> str:
        freedIndex = self.trackedFiles.pop(itemPath)
        self.itemSlots[freedIndex] = None
        if freedIndex == (len(self.itemSlots) - 1):
            self.itemSlots.pop()
        freedTrackerFile = TRACKER_FILE_FORMAT.format(freedIndex)
        return freedTrackerFile


def OpenTrackedFileLUT(lutPath:str) -> TrackedFileLUT:
    trackedLUT: TrackedFileLUT = TrackedFileLUT()

    if os.path.isfile(lutPath):
        with open(lutPath, "r") as fileLUT:
            lutContent = fileLUT.readlines()

        for line in lutContent:
            if line.isspace():
                trackedLUT.itemSlots.append(None)
            else:
                filePath = pathlib.Path(line.rstrip())
                fileIndex = len(trackedLUT.itemSlots)
                trackedLUT.itemSlots.append(filePath)
                trackedLUT.trackedFiles[filePath] = fileIndex
        
    return trackedLUT

def WriteTrackedFileLUT(lutPath:str, oldLUT:TrackedFileLUT) -> None:
    with open(lutPath, "w") as fileLUT:

        def asEntryLine(item:Union[pathlib.Path, None]) -> str:
            if item is not None:
                return item.__str__() + "\n"
            else:
                return "\n"
        
        # newContent = list(map(transformPaths, oldLUT.itemSlots))
        newContent = map(asEntryLine, oldLUT.itemSlots)
        fileLUT.writelines(newContent)


class FileFilter:
    def __init__(self, standardExtensions:list[str] = [], uniqueNames:list[str] = [], uniqueExtension:str = ""):
        self.standardExtensions = standardExtensions
        self.uniqueNames        = uniqueNames
        self.uniqueExtension    = uniqueExtension
    
    def isWhitelisted(self, item:pathlib.Path):
        isStandardFile  = item.suffix in self.standardExtensions
        isUniqueFile    = item.suffix == self.uniqueExtension and item.name in self.uniqueNames
        return isStandardFile or isUniqueFile


def CollectDeletedFiles(gitFiles:DiffIndex, filter:FileFilter) -> list[pathlib.Path]:
    deletedFiles:list[pathlib.Path] = []
    for item in gitFiles.iter_change_type('D'):
        itemPath = pathlib.Path(item.a_path)
        if filter.isWhitelisted(itemPath):
            deletedFiles.append(itemPath)

    return deletedFiles

def CollectModifiedFiles(gitFiles:DiffIndex, filter:FileFilter) -> list[Diff]:
    modifiedFiles:list[Diff] = []
    # Modified files
    for item in gitFiles.iter_change_type('M'):
        itemPath = pathlib.Path(item.a_path)
        if filter.isWhitelisted(itemPath):
            modifiedFiles.append(item)
    
    # renamed files
    for item in gitFiles.iter_change_type('R'):
        itemPath = pathlib.Path(item.a_path)
        if filter.isWhitelisted(itemPath):
            modifiedFiles.append(item)

    return modifiedFiles

def CollectCreatedFiles(gitFiles:list[str], gitDirPath:pathlib.Path, filter:FileFilter) -> list[pathlib.Path]:
    cwd = pathlib.Path.cwd()
    relPath = pathlib.Path(os.path.relpath(cwd, gitDirPath))

    createdFiles:list[pathlib.Path] = []
    for path in gitFiles:
        filePath = pathlib.Path(path)
        # ignore files that we generate and then check the typing
        if filePath.parent is not relPath and filter.isWhitelisted(filePath):
            createdFiles.append(filePath)

    return createdFiles

def CreateNewTrackerFile(trackedFilePath:pathlib.Path, todoComments:list[str], timeStamp, trackedLUT:TrackedFileLUT):
    trackerFileName = trackedLUT.registerNewEntry(trackedFilePath)

    with open(trackerFileName, "w") as trackerFile:
        # Write when the incoming TODOs were found and registered
        trackerFile.write(timeStamp)
        # Formatting will happen later for the complete file.
        content = map(lambda line: line + "\n", todoComments)
        trackerFile.writelines(content)

TIME_SIGNATURE = "@date: "
TIME_SIGNATURE_FORMAT = TIME_SIGNATURE + "{}\n"
def CreateTimeStamp():
    ## time of previous commit
    #pCommitTime = time.gmtime(repo.head.commit.committed_date) 
    
    # time of script execution
    currentTime = time.gmtime(time.time()) 

    timeOfCommit = "{year}-{month:0>2}-{day:0>2} {hour:0>2}:{min:0>2}:{sec:0>2}".format(
        year    = currentTime.tm_year,
        month   = currentTime.tm_mday,
        day     = currentTime.tm_wday,
        hour    = currentTime.tm_hour,
        min     = currentTime.tm_min,
        sec     = currentTime.tm_sec
    )

    return TIME_SIGNATURE_FORMAT.format(timeOfCommit)

class CommitTodos:
    date = ""
    todoLines = [str]

    def __init__(self, date):
        self.date = date
    def empty(self) -> bool:
        return 0 == len(self.todoLines)

## optional?    outPath:pathlib.Path, 
def CreateTodoList(trackerLUT:TrackedFileLUT):
    trackerLUT.trackedFiles
    
    with open("todoList.txt", "w") as todoListFile:
        for fileName, trackerIndex in trackerLUT.trackedFiles.items():
            todoListFile.write(fileName.__str__() + ":\n")
            trackedFileName = TRACKER_FILE_FORMAT.format(trackerIndex)
            with open(trackedFileName, "r") as trackedFile:
                for line in trackedFile:
                    todoListFile.write("\t" + line) # fancy method
                    #todoListFile.write(line)



"""
* output path to the todo-list
* path to git directory
    (option to ignore files the script creates?)
* How shall we whitelist entries?
    select them after a certain file-type   (.h/.hpp)
        each file-type may have a unique "TODO" signifier
        some file-types may share a "TODO" signifier
    select them after a certain name        (CMakeLists.txt)
        each file may have a unique "TODO" signifier
==================================================================
{
    commonFiles:
    [
        {
            types: [ ".h", ".hpp" ]
            keyword: "// TODO"
        },
        {
            types: [ ".py" ]
            keyword: "# TODO"
        }
    ],
    uniqueFiles:
    [
        {
            name: "CMakeLists.txt"
            keyword: "# TODO"
        },
        {
            name: "SomeFile.docx"
            keyword: "@ TODO"
        }
    ]
}
        
"""

import json

# variable names
CFG_K_OUTPUT = "pathOutput"
CFG_K_GITDIR = "pathGitDir"
CFG_K_COMMON = "commonFiles"
CFG_K_UNIQUE = "uniqueFiles"
# sub variable names
CFG_K_TYPES = "types"
CFG_K_NAME = "name"
CFG_K_KEYWORD = "keyword"

def CreateEmptyConfigFile(configPath:pathlib.Path):
    configTemplate = {
        CFG_K_OUTPUT : "./",
        CFG_K_GITDIR : "./",
        CFG_K_COMMON : [ { CFG_K_TYPES : [ "" ], CFG_K_KEYWORD : "" } ],
        CFG_K_UNIQUE : [ { CFG_K_NAME : "", CFG_K_KEYWORD : "" } ]
    }
    configSerialized = json.dumps(configTemplate)
    with open(configPath, "w") as configFile:
        configFile.write(configSerialized)

class TrackerSettings:
    outputPath = ""
    gitDirpath = ""
    todoKeywordsCommon: dict[str, str] = {}
    todoKeywordsUnique: dict[str, str] = {}

    def inWhitelistCommon(self, filename:pathlib.Path) -> bool:
        return filename.suffix in self.todoKeywordsCommon.keys()
    
    def inWhitelistUnique(self, filename:pathlib.Path) -> bool:
        return filename.name in self.todoKeywordsUnique.keys()

    def __getTodoDetector(self, key, todoLUT:dict[str, str]):
        keyword = todoLUT.get(key)
        assert keyword is not None
        def detector(line:str) -> bool:
            return keyword in line
        return detector
        ## OR (haven't decided if assert should be used) 
        '''
        if keyword is not None:
           def detector(line:str) -> bool:
               return keyword in line
           return detector
        def invalidSearch(line:str) -> bool:
           return False
        return invalidSearch
        '''

    def getCommonTodoDetector(self, filename:pathlib.Path):
        return self.__getTodoDetector(filename.suffix, self.todoKeywordsCommon)
    
    def getUniqueTodoDetector(self, filename:pathlib.Path):
        return self.__getTodoDetector(filename.name, self.todoKeywordsUnique)
        
class protoBase(object):
    def __new__(cls, name):
        print("called new")
        if name == "bob":
            instance = super().__new__(cls)
        else:
            instance = None
        return instance
    
    def __init__(self, name):
        print("called init - ", name)
        self.name = name
    
from collections.abc import Callable
from collections import namedtuple

FileFilterSettings = namedtuple("FileFilterSettings", ["whitelist_common", "todoKeywords_common", "whitelist_unique", "todoKeywords_unique"])

def prepareFilterEntry(configPath:pathlib.Path):
    '''
    return a function depening on file's existence.
    function either returns or accepts a new function that takes in the other arguments.

    funcA() -> filterLists
    funcB(arg:workerFunc(filterLists))
    '''
    # https://docs.python.org/3/library/typing.html
    # type callerFunc = Callable[[], str] # only in py 3.12+
    # CallerFunc = Callable[[int], None]  # takes an int, returns nothing
    
    if os.path.exists(configPath):
        whitelist_common:set[str] = set()
        whitelist_unique:set[str] = set()
        todoKeywords_common: dict[str, str] = {}
        todoKeywords_unique: dict[str, str] = {}
        
        # open and read file
        with open(configPath, "r") as configFile:
            configDir = json.load(fp=configFile)

            def typeify(filetype:str):
                return filetype if filetype.startswith('.') else ("." + filetype)
            
            def isNewCommonType(type):
                return type not in todoKeywords_common
            
            # load every allowed filetype and their todo-keyword
            for item in configDir[CFG_K_COMMON]:
                typeIdentifiers = list(map(typeify, item[CFG_K_TYPES]))
                whitelist_common.update(typeIdentifiers)

                newTypeIdentifiers = filter(isNewCommonType, typeIdentifiers)
                todoKeywords_common.update(dict.fromkeys(newTypeIdentifiers, item[CFG_K_KEYWORD]))

            # load every allowed unique file with their todo-keyword        
            for item in configDir[CFG_K_UNIQUE]:
                uniqueName = item[CFG_K_NAME]
                ## optional block - don't allow items whose type is in common.
                # if pathlib.Path(uniqueName).suffix not in whitelist_common:
                whitelist_unique.add(uniqueName)
                if uniqueName not in todoKeywords_unique:
                    todoKeywords_unique[uniqueName] = item[CFG_K_KEYWORD]
        
        def processCaller(process:Callable[[FileFilterSettings], bool]):
            currentFilter = FileFilterSettings(
                whitelist_common    = whitelist_common,
                todoKeywords_common = todoKeywords_common,
                whitelist_unique    = whitelist_unique,
                todoKeywords_unique = todoKeywords_unique
            )
            return process(currentFilter)
        return processCaller
    else:
        CreateEmptyConfigFile(configPath)
        def nullProcess(process:Callable[[FileFilterSettings], bool]) -> bool:
            return False
        return nullProcess

def parseFilter(configPath:pathlib.Path):
    '''
    import statistics as st
    from collections import namedtuple

    def describe(sample):
        Desc = namedtuple("Desc", ["mean", "median", "mode"])
        return Desc(
            st.mean(sample),
            st.median(sample),
            st.mode(sample),
        )
    '''
    if False:
        protoObject1 = protoBase("bob")
        protoObject2 = protoBase("boba")
        print("protoObject1: ", protoObject1)
        print("protoObject2: ", protoObject2)

    if os.path.exists(configPath):
        # config file exists
        with open(configPath, "r") as configFile:
            configDir = json.load(fp=configFile)
            
            if False:
                print("output:", configDir[CFG_K_OUTPUT])
                print("gitdir:", configDir[CFG_K_GITDIR])
                print("common:", configDir[CFG_K_COMMON])
                print("unique:", configDir[CFG_K_UNIQUE])

            #set.add() # single object.
            # these aren't needed anymore
            whitelist_common:set[str] = set()
            whitelist_unique:set[str] = set()

            todoKeywords_common: dict[str, str] = {}
            todoKeywords_unique: dict[str, str] = {}

            def typeify(filetype:str):
                return filetype if filetype.startswith('.') else ("." + filetype)
            
            def isNewCommonType(type):
                return type not in todoKeywords_common
            
            # load every allowed filetype and their todo-keyword
            for item in configDir[CFG_K_COMMON]:
                typeIdentifiers = list(map(typeify, item[CFG_K_TYPES]))
                whitelist_common.update(typeIdentifiers)

                newTypeIdentifiers = filter(isNewCommonType, typeIdentifiers)
                todoKeywords_common.update(dict.fromkeys(newTypeIdentifiers, item[CFG_K_KEYWORD]))

            # load every allowed unique file with their todo-keyword        
            for item in configDir[CFG_K_UNIQUE]:
                uniqueName = item[CFG_K_NAME]
                ## optional block - don't allow items whose type is in common.
                # if pathlib.Path(uniqueName).suffix not in whitelist_common:
                whitelist_unique.add(uniqueName)
                if uniqueName not in todoKeywords_unique:
                    todoKeywords_unique[uniqueName] = item[CFG_K_KEYWORD]
            # -> Similiar solutions:
            '''
            ## These won't work, as any duplicate entries will use the latter value
            todoKeywords_unique = { item[CFG_K_NAME]:item[CFG_K_KEYWORD] for item in configDir[CFG_K_UNIQUE]}
            ## Same as:
            keyvalTransform = lambda item : (item[CFG_K_NAME], item[CFG_K_KEYWORD])
            todoKeywords_unique = dict(map(keyvalTransform, configDir[CFG_K_UNIQUE]))
            '''

            print("whitelist_common: ", whitelist_common)
            print("whitelist_unique: ", whitelist_unique)
            print("todoKeywords_common: ", todoKeywords_common)
            print("todoKeywords_unique: ", todoKeywords_unique)

            ## TODO: Later idea:
            # maybe split "new", "removed" and "modified" into 2 lists (common and unique)

            ## Check whitelist
            # if suffix is in "Common list"
            # OR
            # if name is in unique files
            # 
            ## method:
            # From Common,
                # iterate each case
                # add each type to whitelist_common[] if not already in.
                #! forbid later recurring types.
            # From Unique
                # iterate each case
                # add each name to whitelist_unique[] if not already in.
            #? Forbid unique items if their suffix is in common?
            
            ## Get Todo Checker
            # get name + suffix
            # if suffix is in common
                # Base detector on value
            # if name is in unique
                # Base detector on value
            ## Metod:
            # From Common
                # iterate each case
                # add each NEW type as a key with the current keyword as value.
            # From Unique
                # iterate each case
                # add each NEW name and keyword as key and value respectivly in the list
    else:
        CreateEmptyConfigFile(configPath)

import sys # for sys.exit(0)

def mainProcess(filterSettings:FileFilterSettings):
    print("whitelist_common: ", filterSettings.whitelist_common)
    print("whitelist_unique: ", filterSettings.whitelist_unique)
    print("todoKeywords_common: ", filterSettings.todoKeywords_common)
    print("todoKeywords_unique: ", filterSettings.todoKeywords_unique)
    return True

if callPass7:
    # True  False
    printReferenceTests      = False
    printPathTests           = False
    printUntracked           = False
    printChanges             = False
    printCollectedFiles      = True
    printTrackerEntries      = False
    printTodoCommentAndIndex = False
    printTimeExamples        = False
    
    # prepare the repo.
    pk_repo_path = '../../' # TODO - Fix this to point to the current git dir.

    repo = Repo(pk_repo_path) 
    gitDirPath = pathlib.Path(repo.working_dir)

    currentWorkingDir = pathlib.Path.cwd()
    assert gitDirPath in currentWorkingDir.parents
    print("currentWorkingDir: ", currentWorkingDir)
    
    if printPathTests:
        pathTest = pathlib.Path("something/item.txt")
        print("pathTest : ", pathTest)
        print("pathTest.suffix : ", pathTest.suffix)
        print("pathTest.name : ", pathTest.name)

    entrypoint = prepareFilterEntry("filter.json")
    if entrypoint(mainProcess):
        print("job's done")
    else:
        print("something's amiss")

    #parseFilter("filter.json")

    sys.exit(0)

    if printReferenceTests:
        tmpItems:   list[str]               = ["A", "B", "", "C"]
        tmpPaths:   dict[pathlib.Path, int] = {}
        tmpRows:    list[Union[pathlib.Path, None]]          = list()
        
        for idx, item in enumerate(tmpItems):
            if item == "": # empty slot
                tmpRows.append(None)
            else:
                iPath = pathlib.Path(item)
                tmpPaths[iPath] = idx
                tmpRows.append(iPath)

        print("PRE CHANGE")
        print("tmpPaths {}", tmpPaths)
        print("tmpRows {}", tmpRows)
        print("====================================")
        
        print("POST CHANGE")
        print("tmpPaths {}", tmpPaths)
        print("tmpRows {}", tmpRows)

        print("id(list(tmpPaths.keys())[0]): ", id(list(tmpPaths.keys())[0]))
        print("id(tmpRows[0]):               ", id(tmpRows[0]))
        print("====================================")

    '''
    only look for changed/added *.hpp, *.cpp and CMakeLists.txt(?)

    for every untracked (un-commited) files in the current working tree. (Why? when are we calling this script?)
    for every changed/added file in the last commit.

    for all new files: open and search for TODO keyword
    for all changed files: open the old and current (blob or file) version of it, get changes and open and search for TODO keyword
    '''

    if printUntracked:
        print("\n# Traverse untracked_files")
        for untracked in repo.untracked_files:
            print(untracked)

    hWorkingDiff = repo.head.commit.diff(None)
    hPreviousDiff = repo.head.commit.diff("HEAD~1")

    if printChanges:
        print("\n(None)  : ", len(hWorkingDiff))
        print("================")
        for untracked in hWorkingDiff:
            print(untracked.a_path)

        print("\n(HEAD~1): ", len(hPreviousDiff))
        print("================")
        for untracked in hPreviousDiff:
            print(untracked.a_path)

    
    ## TODO - prepare a list (.yml? .ini?) to let users specify the file types to be searched/
    ## TODO - Unsure how to split the unique case(s) from above
    fileFilter = FileFilter(
        standardExtensions  = ['.hpp', '.cpp', '.h', '.c'], 
        uniqueNames         = ['CMakeLists.txt'], 
        uniqueExtension     = '.txt'
        )

    ## TODO - when writing/loading settings, should the user need to include the dot before the extension
    # This might be the best way to handle this.
    # the problem is when we have unique files with names, such as CMakelist.txt
    TODO_KEYWORDS: dict[str, str] = {}
    TODO_KEYWORDS[".hpp"]   = "// TODO"
    TODO_KEYWORDS[".cpp"]   = "// TODO"
    TODO_KEYWORDS[".h"]     = "// TODO"
    TODO_KEYWORDS[".c"]     = "// TODO"
    TODO_KEYWORDS[".txt"]   = "# TODO"

    # !!! TODO_KEYWORDS and FileFilter NEED to be synced
    assert all(extension in TODO_KEYWORDS for extension in fileFilter.standardExtensions)
    assert fileFilter.uniqueExtension in TODO_KEYWORDS

    def getTodoDetector(fileSuffix:str):
        keyword = TODO_KEYWORDS.get(fileSuffix)
        assert keyword is not None
        def detector(line:str) -> bool:
            return keyword in line
        return detector

    PREFIX_ADD      = "+ "
    PREFIX_REMOVE   = "- "
    PREFIX_OFFSET   = len(PREFIX_ADD)

    # quick pseudo-code
    if False:
        # For all new files
            # Get All TODO comments
        # For all modified files
            # Get the diff
            # Get all TODO comments
        # For all renamed files
            # Get the diff (in case of change in code)
                # file existed previously
                # file might have changed as well as rename
            # Get all TODO comments
        # For all removed files
            # Check if file was tracked
            # TRUE: add file as key for removal

        # ONLY APPEND TODO:
            # created
        # ONLY DESTROY TODO:
            # destroyed
        # APPEND OR REMOVE TODO (including removing file):
            # modified
            # renamed
        bob = 1

    createdFiles = CollectCreatedFiles(repo.untracked_files, gitDirPath, fileFilter)
    removedFiles = CollectDeletedFiles(hWorkingDiff, fileFilter)
    modifiedFiles = CollectModifiedFiles(hWorkingDiff, fileFilter)
    if printCollectedFiles:
        print("createdFiles: \n", createdFiles)
        print("removedFiles: \n", removedFiles)
        print("modifiedFiles: \n", modifiedFiles)

    ## Read all tracked files from the "Lookup table" file
    pathFileLUT = "trackedFileLUT.txt"
    trackedLUT = OpenTrackedFileLUT(pathFileLUT)
    if printTrackerEntries:
        print("# trackedLUT:")
        print("# trackedLUT.itemSlots: ", trackedLUT.itemSlots)
        print("# trackedLUT.trackedFiles: ", trackedLUT.trackedFiles)

    timeStamp = CreateTimeStamp()
    if printTimeExamples:
        print("commit_date: ", repo.head.commit.committed_date)         # seconds since epoch
        print("commit_datetime: ", repo.head.commit.committed_datetime) # 2023-11-12 17:54:44+01:00
        print("time: ", time.time())                                    # seconds since epoch
        print("time asc: ", time.asctime(time.gmtime(time.time())))     # Thu Dec  7 17:09:19 2023
        print("time com: ", time.asctime(time.gmtime(repo.head.commit.committed_date)))
    

    ## Iterate all deleted items
    for itemPath in removedFiles:
        if trackedLUT.hasEntry(itemPath):
            trackedFile = trackedLUT.freeEntry(itemPath)
            truePath = os.path.join(currentWorkingDir, trackedFile)
            if os.path.exists(truePath):
                os.remove(truePath)
                    # we could clean them up at the end instead.
                    # In "WriteTrackedFileLUT()" ?

    ## Iterate all modified items.
    for item in modifiedFiles:
        assert not item.deleted_file
        assert item.a_path is not None
        assert item.a_blob is not None

        itemPath = pathlib.Path(item.a_path)
        todoCondition = getTodoDetector(itemPath.suffix)

        # There might be a better way to do this. 
        # I'm struggling with working with the types.
        oldContent = item.a_blob.data_stream.read().decode('utf-8')
        oldContentAsLines = str(oldContent).splitlines()
        # print('1: \n', oldContent.splitlines())
        # print('2: \n', oldContentAsLines)

        fullFilePath = os.path.join(repo.working_dir, itemPath)
        newContent = open(fullFilePath, "r").read()
        newContentAsLines = newContent.splitlines()

        # Returns an iterator. it remembers each step we move it (loop only happens once.)
        diff = difflib.ndiff(oldContentAsLines, newContentAsLines)
        #diff2 = difflib.unified_diff(oldContentAsLines, newContentAsLines, fromfile='old', tofile='new', lineterm='')

        # Currently covers only the first line of a TODO comment
        # (Current method lacks row index)
        # (Method 3 here might be a better strategy: https://www.geeksforgeeks.org/compare-two-files-line-by-line-in-python/)
        addedTodoComments:list[str] = []
        removedTodoComments:list[str] = []

        for line in diff:
            if line.startswith(PREFIX_ADD) and todoCondition(line):
                addedTodoComments.append(line[PREFIX_OFFSET:])
                
                ## get the index position of '// TODO ' and use that to help check if the next line is a attatched comment.
                #todoStart = line.find(todoKeyword, PREFIX_OFFSET)
                #if todoStart != -1:
                    #if printTodoCommentAndIndex:
                    #    print(line[PREFIX_OFFSET:])
                    #    print(todoStart - PREFIX_OFFSET)

                    # Save the file as a new entry and get:
                        # The row the "TODO" comment starts
                        # The content of the "TODO" comment
                        # The date of when this file was last modified.

                    # ! How do we check the next entry of the iterator, and then use it for the next check.
                    # check if next line:
                        # starts with a comment at the same column as the current "TODO" line
                        # is not another "TODO" line
                    # Then
                        # save the line as a "child" of the "TODO" line and continue with the next
            elif line.startswith(PREFIX_REMOVE) and todoCondition(line):
                # Only check if this first TODO comment line is removed.
                removedTodoComments.append(line[PREFIX_OFFSET:])

        fileHasTodos = len(addedTodoComments) or len(removedTodoComments)
        if fileHasTodos:
            if trackedLUT.hasEntry(itemPath):
                # read the file content, clear any removed todos and append
                trackerFileName = trackedLUT.getTrackerFile(itemPath)
                assert os.path.isfile(trackerFileName)

                remainingCommits = {} # filter[CommitTodos]
                if 0 < len(removedTodoComments):
                    with open(trackerFileName, "r") as trackerFile:
                        oldContent = trackerFile.readlines()
                        assert 0 < len(oldContent)
                        assert TIME_SIGNATURE in oldContent[0]

                        commitCollection = [CommitTodos]
                        for line in oldContent:
                            if TIME_SIGNATURE in line:
                                commitCollection.append(CommitTodos(line))
                            elif line.rstrip() not in removedTodoComments:
                                # get all lines that were not marked as removed (ignoring the newline at the end)
                                commitCollection[-1].todoLines.append(line)
                        keepFilledCommits = lambda commit : not commit.empty()
                        remainingCommits = filter(keepFilledCommits, commitCollection)

                with open(trackerFileName, "w") as trackerFile:
                    for item in remainingCommits:
                        trackerFile.write(item.date)
                        trackerFile.writelines(item.todoLines)

                    # Write when the incoming TODOs were found and registered
                    # Formatting will happen later for the complete file.
                    trackerFile.write(timeStamp)
                    content = map(lambda line: line + "\n", addedTodoComments)
                    trackerFile.writelines(content)
            else:
                CreateNewTrackerFile(itemPath, addedTodoComments, timeStamp, trackedLUT)

    ## Iterate all created items
    # TODO This doesn't check if the item already exists 
    for itemPath in createdFiles:
        fullFilePath = os.path.join(repo.working_dir, itemPath)
        todoCondition = getTodoDetector(itemPath.suffix)

        foundTodoComments = []
        with open(fullFilePath, "r") as file:
            todoLines = filter(todoCondition, file.readlines())
            foundTodoComments = list(todoLines)
            if 0 < len(foundTodoComments):
                CreateNewTrackerFile(itemPath, foundTodoComments, timeStamp, trackedLUT)


    # To flip a map, assuming values are unique
    # inv_map = {v: k for k, v in my_map.items()}

    ## Update the Tracked Files Lookup Table file.
    WriteTrackedFileLUT(pathFileLUT, trackedLUT)

    CreateTodoList(trackedLUT)

    # Regarding the final TODO collection output.
    # We could create individual "Time stamps" for each TODO group
    # We can then create a single overview by reading and combining all the stamps
    # Problem:
        # We don't have a good way of tracking when we have done the TODOs

    # What do we need to track?
    # The TODO comment itself
    # Row ? 
        # it might help to locate the comment and to simplify comparisons, but it will probably change in the file.
            # we could try to detect if lines were added/removed and update the row, but that might be more work than its worth.
    # Time ?
        # To determine how old the Todo comment has been around.
        # Could help make a priority among TODOs
        # If we are going to compare old and new TODOs either way so we can remove them
        # it wouldn't be too hard to also check, we 
    
    # If we create a "watch-file" to track a file's TODOs
    # we can then first check if the TODOs we have are new or already registered.
    # we can then skip those, and just append the new ones at the end of the file under the current timestamp.
    # later when tracking removed TODO changes, we can also remove them from the file.

    # Problem:
    # Names, what if two sub-files have the same name?
    # Comment changes, what if we change a "child line" of a TODO comment, how can we easily detect that?

    
    # If we also want to detect, and remove, any TODOs that have been deleted
    # Then we 


    ## Method 1: simple check
    # Get all files that were modified.
    # Read each line in file for TODO comments and collect them
    # Create a "reflection" of the file and store the todos in it.
        # if file didn't exist before, don't do anything more.
        # if file did exist, ? Read and check if some TODOs has been made.
    # when done
