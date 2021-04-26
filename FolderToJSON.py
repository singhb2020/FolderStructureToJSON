import json
from os import path, chdir, getcwd, walk, scandir, listdir

abspath = path.abspath(__file__)
dname = path.dirname(abspath)
chdir(dname)

def getDirectoryCount(rootPath):
    totalCount = 0

    try:
        for entry in scandir(rootPath):
            if entry.is_file():
                totalCount += 1
            elif entry.is_dir():
                totalCount += getDirectoryCount(entry.path)
    except NotADirectoryError:
        return totalCount
    except PermissionError:
        return 0
    except OSError:
        return 0
    return totalCount

def getDirectorySize(rootPath):
    totalSize = 0

    try:
        for entry in scandir(rootPath):
            if entry.is_file():
                totalSize += entry.stat().st_size
            elif entry.is_dir():
                totalSize += getDirectorySize(entry.path)
    except NotADirectoryError:
        return path.getsize(rootPath)
    except PermissionError:
        return 0
    except OSError:
        return 0
    return totalSize

def readableSize(filePath):
    rawSize = 0
    if path.isfile(filePath): 
        rawSize = path.getsize(filePath)
    elif path.isdir(filePath):
        rawSize = getDirectorySize(filePath)

    readSize = 0
    readAbbrev = ''
    precision = 1

    abbrevList = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    for x in range(5):
        if rawSize < (1024**(x+1)):
            readSize = round((rawSize / (1024**x)), precision)
            readAbbrev = abbrevList[x]
            break

    return readSize, readAbbrev

def fileDict(filePath):
    print(filePath)
    size, abbrev = readableSize(filePath)
    return {
        'name' : path.basename(filePath),
        'type' : 'file',
        'extension' : path.splitext(path.basename(filePath))[-1],
        'size' : size,
        'unit' : abbrev,
        'path' : filePath,
        }

def folderDict(rootPath):
    print(rootPath)
    totalSize, abbrev = readableSize(rootPath)
    totalCount = getDirectoryCount(rootPath)
    return {
        'name' : path.basename(rootPath),
        'type' : 'folder',
        'size' : totalSize,
        'unit' : abbrev,
        'files' : totalCount,
        'path' : rootPath,
        'children' : [],
        }

def treeDict(rootPath):
    rootDict = folderDict(rootPath)
    for root, folders, files in walk(rootPath):
        for fpath in sorted(files):
            rootDict['children'] += [fileDict(path.sep.join([root, fpath]))]
        for folder in sorted(folders):
            rootDict['children'] += [treeDict(path.sep.join([root, folder]))]

        return rootDict

def treeToJson(rootDir):
    for root, folders, files in walk(rootDir):
        for fpath in sorted(files):
            rootDict = [fileDict(path.sep.join([root, fpath]))]
        for folder in sorted(folders):
            rootDict += [treeDict(path.sep.join([root, folder]))]

        return rootDict


print(getcwd())

outputFileName = 'Structure'
inputFolderPath = "C:\\"

with open(str(outputFileName + '.json'), 'w') as jsonFile:
    json.dump(treeToJson(inputFolderPath), jsonFile, indent=4)
