# getRepoId.py
# Get the Id a 
# Version: 0.1 - First draft
# Authors: Kerstin Carola Schmidt, Jérémy Bonvoisin
# Homepage: http://opensourcedesign.cc
# License: GPL v.3
#
# Requisite: 
# install pyGithub with pip install PyGithub
# install pygithub3 with pip install pygithub3
#
# PyGitHub documentation can be found here: 
# https://github.com/jacquev6/PyGithub
# http://pygithub.readthedocs.io/en/latest/reference.html

from github import Github
import pygithub3
import getpass

# get credentials
userlogin = input("Enter your GitHub login: ")
password = getpass.getpass("Enter your GitHub password: ")
g = pygithub3.Github( userlogin, password )

# get the owner of the targeted repository
username = input("Who is the owner of the repository you are looking for: ")
targetedUser = g.get_user(username)

# list all repositories of the given user
index = 0
repoIds = []
repoNames = []
print ("repositories of ",targetedUser.login)
for i in targetedUser.get_repos():
    print ("type ",index," for ",i.owner.login,"/",i.name)
    repoIds.append(i.id)
    repoNames.append(i.name)
    index += 1

# choose the targeted repository
chosenIndex = input("type a number and press enter: ");
print ("The id of ",repoNames[int(chosenIndex)], " is ", repoIds[int(chosenIndex)])
