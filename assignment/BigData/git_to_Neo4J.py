from subprocess import Popen, PIPE
from os import listdir, walk, chdir
from git import Repo
from py2neo import Graph
import time





def checkAuthor(name):  #Checks if the author already exists in the database.
    query = graph.cypher.execute("MATCH( person{name:'"+str(name)+"'}) RETURN(person)")
    if query.one == None:        #If there are no records with that name value
        return False            #Return falsch
    else:
        return True
    return

def checkFile(fileName):    #Checks if the file already exists in the database.
    query = graph.cypher.execute("MATCH (File{filename:'"+str(fileName)+"'}) RETURN (File)")
    if query.one == None:        #If there are no records with that filename value
        return False            #Return falsch
    else:
        return True
    return

def checkDate(date):
    query = graph.cypher.execute("MATCH(Date{date:'"+str(date)+"'}) RETURN(date)")
    if query.one == None:
        return False
    else:
        return True

def checkProject(projName):     #Checks if project already exists
    query = graph.cypher.execute("MATCH(Project{name:'"+str(projName)+"'}) RETURN(Project)")
    if query.one == None:
        return False
    else:
        return True

def checkComponant(comName):    #Checks if Conponants already exists
    query = graph.cypher.execute("MATCH(Componant{name:'"+str(projName)+"'}) RETURN(Componant)")
    if query.one == None:
        return False
    else:
        return True

def addCommit(commit, fileName):    #Adds a new commit.
    #First check if we already have authors and dates.
    #If not, create them

    if checkAuthor(commit.author) == False:     #If the author node doesnt exists already
        addAuthor(commit.author)                #Add the author

    if checkDate != False:
        addDate(commit.authored_date)

    #Then create a new commit node, with relationships to the author and dates

    #XXX Watch out for hidden method use __str__(), possiblity that this could get changed without warning #XXX .
    query = graph.cypher.execute("MATCH(a:Person),(d:Date),(p:Componant), (f:File) \
WHERE p.name = '"+commit.author.__str__()+"' AND d.date = '"+str(commit.authored_date)+"' AND p.name = '"+componant+"' AND f.filename = '"+fileName+"' \
CREATE(c:Commit{hash:'"+commit.hexsha+"'}) <-[ct:Committed to]-(a)  \
CREATE (d)-[cd:Commit date]->(c) \
CREATE (c)-[po:Part of]->(p) \
CREATE (c)-[at:Applied too]->(f) \
RETURN c ")

    if query.one == None:
        print("Something went wrong")
        print(query)
        return False
    else:
        return True

def addAuthor(name):            #Adds a new author..
    query = graph.cypher.execute("CREATE (:Person{name: '"+str(name)+"'})")
    return

def  addProject(projName):      #Adds new Project
    query = graph.cypher.execute("CREATE (:Project{name:'"+projName+"'])")
    return

def addConponant(comName, project):      #Adds new conponant and links to the project its part of.
    query = graph.cypher.execute("CREATE (:Componant{name:'"+comName+"'])")
    return

def addFile(filename):
    query = graph.cypher.execute("CREATE (:File{name: '"+filename+"'})")
    return 

def addDate(date):
    query = graph.cypher.execute("CREATE (:Date{date: '"+str(date)+"'})")
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
    print("Gathering commits from file: "+file[0])
    commitData.append(list(file))     #Append a list with the first elemet the file tuple (name)
    commitData[-1].append(list(repo.iter_commits('master',file[0],max_count=1)))  #And the next element is  list of commits on that file

print("Making connection to Neo4J....")

graph = Graph("http://neo4j:BigData@localhost:7474/db/data")

for file in commitData:   #for every commit
    
    if checkFile(file[0]) == True:   #If file node exists
        for commit in file[2]:        #For every commit on this file
            print(commit.hexsha)
            addCommit(commit, file[0])  #Add that commit
    else:
        addFile(file[0])            #Add that file (Since it doesnt exist)
        for commit in file[2]:        #For every commit on this file
            addCommit(commit, file[0])  #Add that commit

