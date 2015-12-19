# Git2Neo
Python script for grabbing all commits from a git repo and adding them to a Neo4J graph database.


## Dependancies:
* [py2neo](http://py2neo.org)
* [GitPython](https://github.com/gitpython-developers/GitPython)


##TODO

- [x] Remove Linux kernel specific stuff (Mostly nodes specific to linux kernel source tree)
- [ ] Add configuration file options to configure what nodes are created for different data in Git repo. (Lamda functions for add/checkNodeName?)
    
- [x] Add option to configure how many commits to retrieve
- [ ] Add threading support
- [ ] Use cypher transactions rather that instant query execution to reduce load on DB.
- [ ] Use better data for nodes: 
    - [ ] Date node contains time stamp and month day year
    - [ ] Commit contains all possible commit data.
    - [ ] Author nodes contain email addresses and all possible data.
- [ ] Write some tests!



