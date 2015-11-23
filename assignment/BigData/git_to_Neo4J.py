from subprocess import Popen, PIPE
from os import listdir, walk, chdir
from git import Repo





def checkAuthor(name):  #Checks if the author already exists in the database.
    return

def checkFile(file):    #Checks if the file already exists in the database.
    return

def addCommit(commit, file):    #Adds a new commit.
    if checkAuthor(commit.author) == False:     #If the author node doesnt exists already
        addAuthor(commit.author)                #Add the author
    return

def addAuthor(name):            #Adds a new author..
    return

def checkProject(projName):     #Checks if project already exists
    return

def checkComponant(comName):    #Checks if Conponants already exists
    return

def  addProject(projName):      #Adds new Project
    return

def addConponant(conName, project):      #Adds new conponant and links to the project its part of.
    return


print("Input the location of the Git repo\n")
#repoPath = input()
repoPath = "/home/samathy/LINUX/linux/"

num = 0
tree = []
fileList = []

chdir(repoPath)

for root, dirs, files in walk(repoPath):
    num = num + 1
    files = [f for f in files if not f[0] == '.']
    dirs[:] = [d for d in dirs if not d[0] == '.']
    tree.append((root,dirs,files))


for items in tree:
    for files in items[2]:
        fileList.append((str(items[0])+"/"+str(files),items[0]))
print("Please input the subdirectory. Use a \" . \" for this directory")
print("[DIR]/[DIR]/[DIR]\n")
#subdir = input()
subdir = 'fs/ext4'
print("Please enter the product.")
product = input()
print("Please enter the componant.")
componant = input()
repo = Repo(repoPath)

commitData = list() #   store the commit data.
for file in fileList:   #for everyfile in the files we want to analyse
    if subdir not in file[1]:   #If the file is not in the directory we want to look at
        continue                #Skip it
    print("Adding commits from file: "+file[0])
    commitData.append(list(file))     #Append a list with the first elemet the file tuple (name)
    commitData[-1].append(list(repo.iter_commits('master',file[0],max_count=100)))  #And the next element is  list of commits on that file


for file in commitData:   #for every commit
    
    if checkFile(file[0]) == True:   #If file node exists
        for commit in file[2]:        #For every commit on this file
            addCommit(commit, file[0])  #Add that commit
    else:
        addFile(file[0])            #Add that file (Since it doesnt exist)
        for commit in file[2]:        #For every commit on this file
            addCommit(commit, file[0])  #Add that commit

