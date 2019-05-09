from os import scandir
from os.path import isdir
import argparse
import json
import hashlib

#Gets a list of all files/folders in a path, places all the file names into an
#array with name and path information. Folders recursively call this function
#to get the contents of the folder. The end result is placed into an array called
#contents.
def getFolder(path, excludedExtensions, includedExtensions, recLvl):
    filterList = ['@eaDir', '.DS_Store', '#recycle']

    #Remove the traililng slash if it exists, then re-add it
    path = path.rstrip('/')
    path = path + '/'
    #Create an empty list for return if no contents are included
    files = []
    folders = []
    #Error. Path provided does not exist
    if not isdir(path):
        return {}

    #Get all files and folders from the path
    for i in scandir(path):
        #Filter out nuissance names
        if i.name in filterList:
            pass
        elif i.is_file():

            #Get the file's extension, convert to lowercase
            ext = i.name[i.name.rfind('.')+1:].lower()

            include = False
            #Included extensions has 1 or more elements and the extension is included
            if len(includedExtensions) > 0 and ext in includedExtensions:
                include = True
            #Included extensions is empty and the extension is NOT excluded
            #This is the case that will hit if both lists are empty
            elif len(includedExtensions) < 1 and ext not in excludedExtensions:
                include = True

            if include:
                file = {
                    "id" : hashlib.sha1(bytes(path+i.name, 'utf-8')).hexdigest(),
                    'name':i.name,
                    'size':i.stat().st_size
                }
                files.append(file)
        elif i.is_dir():

            if recLvl != 0:
                folder = getFolder(path+i.name, excludedExtensions, includedExtensions, recLvl-1)
                #Remove later to include recursive functions
                #contents = {}
            else:
                folder = {
                    "id" : hashlib.sha1(bytes(path+i.name, 'utf-8')).hexdigest(),
                    "name": i.name,
                    "path" : path+i.name+"/",
                    "contents" : {
                        "folders" : [],
                        "files" : []
                    }
                }
            folders.append(folder)

    #Sort lists here
    #files = sorted(files, key=lambda k: k["name"].lower())
    dirnameStart = path.rstrip('/').rfind('/')+1
    name = path[dirnameStart:].rstrip('/')
    files = sorted(files, key=lambda k: k['name'].lower())
    folders = sorted(folders, key=lambda k: k["name"].lower())


    folder = {
        "id" : hashlib.sha1(bytes(path, 'utf-8')).hexdigest(),
        "name" : name,
        "path" : path,
        "contents" : {
            "folders" : folders,
            "files" : files
        },
    }

    return folder

def filesOutput(filename, files):

    output = ""
    if files:

        if filename:
            list = open(filename, 'w')
            list.write(json.dumps(files, indent=1))
            list.close()
        else:
            print(json.dumps(files, indent=1))


def main():
    description = "This program makes a list of all files in a directory, filtered by extension."

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-p", "--path", nargs='+', help="Define the path to the directory", required="True")
    parser.add_argument("-r", "--recursion-level", nargs='?', help="Recursively scan all subdirectories")
    parser.add_argument("-f", "--filename", help="Store the output to a file")
    parser.add_argument("-e", "--exclude-extensions", nargs='+', help="A list of extensions that need to be ignored")
    parser.add_argument("-i", "--include-extensions", nargs='+', help="A list of extensions you want to include")
    parser.add_argument("-n", "--id", help="The starting point for ids while iterating through the list")

    args = parser.parse_args()

    #Replacing all provided extensions with lower case variants
    if args.exclude_extensions:
        excludedExtensions = args.exclude_extensions
        for x in range( len(excludedExtensions) ):
            excludedExtensions[x] = excludedExtensions[x].lower()
    else:
        excludedExtensions = {}

    #Replacing all provided extensions with lower case variants
    if args.include_extensions:
        includedExtensions = args.include_extensions
        for x in range( len(includedExtensions) ):
            includedExtensions[x] = includedExtensions[x].lower()
    else:
        includedExtensions = {}

    if args.recursion_level:
        recLvl = int(args.recursion_level)
    else:
        recLvl = 0

    #print(args.recursive)
    files = []
    #If multiple paths are included, iterate through them all
    #for p in args.path:
    #files.append( getFolder(args.path[0], excludedExtensions, includedExtensions, recLvl) )
        #files = getStructure(p, excludedExtensions, includedExtensions, args.recursive)

    #filesOutput(args.filename, files)
    filesOutput( args.filename, getFolder(args.path[0], excludedExtensions, includedExtensions, recLvl) )

main()
