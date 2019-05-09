# python-file-list

This script recursively generates a list of files & subdirectories plus the files & subdirectories within each subdirectory.

## Usage:

python3 getFileList.py -p /path/

This will generate a list of all files, directories and all files and directories within each subdirectory at /path/. The JSON will display in the command line. This can be piped into a PHP script.

## Saving to a file

python3 getFileList.py -p /path/ -f filelist.json

This does the same as above, but saves the output to a json file.

## Scraping only a few layers deep

python3 getFileList.py -p /path/ -r 2

This only goes 2 layers deep into the directory structure before outputing the end result. This is good if you only want to show a few files without having to traverse the entire file system.

## Including extensions

python3 getFileList.py -p /path/ -i mp4 mpg avi

This only lists all files that have those extensions.

## Excluding extensions

python3 getFileList.py -p /path/ -e js php py

This lists all files with the exception of those extensions
