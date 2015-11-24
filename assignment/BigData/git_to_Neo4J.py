from subprocess import Popen, PIPE
from os import listdir, walk, chdir
from git import Repo
from py2neo import Graph
from string import punctuation
import time



def strip_punctuation(string):
    return ''.join(c for c in string if c not in punctuation)

def checkAuthor(name):  #Checks if the author already exists in the database.
    name = strip_punctuation(name) #Should remove all special chars
    query = graph.cypher.execute("MATCH( person{name:'"+str(name)+"'}) RETURN(person)")
    if query.one == None:        #If there are no records with that name value
        print("Author: "+name+" Already exists")
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

def checkProduct(projName):     #Checks if project already exists
    query = graph.cypher.execute("MATCH(Project{name:'"+str(projName)+"'}) RETURN(Project)")
    if query.one == None:
        return False
    else:
        return True

def checkComponant(comName):    #Checks if Conponants already exists
    query = graph.cypher.execute("MATCH(Componant{name:'"+str(comName)+"'}) RETURN(Componant)")
    if query.one == None:
        return False
    else:
        return True

def addCommit(commit, fileName):    #Adds a new commit.
    #First check if we already have authors and dates.
    #If not, create them

    print("Commit: "+commit.hexsha)
    print(dir(commit.author))
    author = strip_punctuation(str(commit.author))
    print(" from author:"+author)
    
    print("Checking Author")
    if checkAuthor(str(commit.author)) == False:     #If the author node doesnt exists already
        addAuthor(str(commit.author))                #Add the author

    print("Checking date...")
    if checkDate != False:
        addDate(commit.authored_date)

    #Then create a new commit node, with relationships to the author and dates
    #XXX Watch out for hidden method use __str__(), possiblity that this could get changed without warning #XXX .
    print("Executing query")
    query = graph.cypher.execute( 
            "MATCH(a:Person),(d:Date),(f:File)\
    WHERE a.name = '"+author+"' AND d.date = '"+str(commit.authored_date)+"' AND f.name = '"+fileName+"'\
    CREATE(c:Commit{hash:'"+commit.hexsha+"'}) \
    CREATE (c)<-[ct:Committed_too]-(a) \
    CREATE (d)<-[cd:Commit_date]-(c) \
    CREATE (c)-[at:Applied_too]->(f) \
    RETURN c ")

#CREATE (c)<-[ct:Committed_too]-(a) 
#CREATE (d)-[cd:Commit_date]->(c) \
#CREATE (c)-[po:Part_of]->(p) \
#CREATE (c)-[at:Applied_too]->(f) \
#RETURN c ")
    print("Query complete")

    if query.one == None:
        print("Something went wrong")
        print(query)
        return False
    else:
        return True

def addAuthor(name):            #Adds a new author..
    print("Adding Author: "+name)
    name = strip_punctuation(name) #Should remove all special chars
    query = graph.cypher.execute("CREATE (p:Person{name: '"+str(name)+"'}) RETURN p")
    return

def  addProduct(projName):      #Adds new Project
    query = graph.cypher.execute("CREATE (p:Product{name:'"+projName+"'}) RETURN p")
    return

def addComponant(comName):      #Adds new conponant and links to the project its part of.
    query = graph.cypher.execute("MATCH (p:Product) WHERE p.name = '"+product+"' CREATE (c:Componant{name:'"+comName+"'}) -[r:Part_of]->(p) RETURN c")
    return

def addFile(filename):
    query = graph.cypher.execute("MATCH (cp:Componant) WHERE cp.name = '"+componant+"' CREATE (f:File{name: '"+filename+"'})-[r:Part_of]->(cp) RETURN f")
    return 

def addDate(date):
    query = graph.cypher.execute("CREATE (d:Date{date: '"+str(date)+"'})RETURN d")
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
    commitData[-1].append(list(repo.iter_commits('master',file[0], max_count=1 )))  #And the next element is  list of commits on that file

print("Making connection to Neo4J....")

graph = Graph("http://neo4j:BigData@localhost:7474/db/data")

if checkProduct(product) == False:
   addProduct(product)

if checkComponant(componant) == False:
   addComponant(componant)





for file in commitData:   #for every commit
    
    if checkFile(file[0]) == True:   #If file node exists
        for commit in file[2]:        #For every commit on this file
            print(commit.hexsha)
            addCommit(commit, file[0])  #Add that commit
    else:
        addFile(file[0])            #Add that file (Since it doesnt exist)
        for commit in file[2]:        #For every commit on this file
            addCommit(commit, file[0])  #Add that commit
