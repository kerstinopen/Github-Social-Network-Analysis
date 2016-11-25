# branch-network-mining.py
# Extract branch networks of a repository in a GraphML file
# Version: 0.1 - First draft
# Authors: Kerstin Carola Schmidt, Jérémy Bonvoisin
# Homepage: http://opensourcedesign.cc
# License: GPL v.3
#
# Based on previous work of
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
#
# Requisite: 

# install pyGithub with pip install PyGithub
# install pygithub3 with pip install pygithub3
# install NetworkX with pip install networkx
# install Requests
# install Json
# sub-directory called Results
#
# Parameter :
# Id of the repository to analyse
#
# PyGitHub documentation can be found here: 
# https://github.com/jacquev6/PyGithub
# http://pygithub.readthedocs.io/en/latest/reference.html

from github import Github
from github import Commit

import pygithub3

import networkx as nx
import getpass
import random
import os
import sys
import requests
import json
from lxml import html

# Clear screen
os.system('cls' if os.name=='nt' else 'clear')

# Remove CLS Client from system path
if os.environ['PATH'].find("iCLS Client")>=0:
    os.environ['PATH'] = "".join([it for it in os.environ['PATH'].split(";") if not it.find("iCLS Client")>0])

from lxml import etree
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree


# https://pygithub.readthedocs.io/en/latest/github_objects/Commit.html?

# das Gute: alle commits werden jetzt angezeigt
# das Schlechte: die commits in den forks werden teilweise mehrfach angezeigt
# und: funktioniert nur, wenn json Struktur gleich bleibt

def analyse_repo(repository):
    index = 0;

    # creating graphml header
    graphml = Element('graphml', {
            "xmlns":"http://graphml.graphdrawing.org/xmlns",
            "xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
            "xmlns:y":"http://www.yworks.com/xml/graphml",
            "xmlns:yed":"http://www.yworks.com/xml/yed/3",
            "xsi:schemaLocation":"http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd"})
    SubElement(graphml, 'key', { "for":"node", "id":"nodeStyle", "yfiles.type":"nodegraphics"})
    SubElement(graphml, 'key', { "for":"edge", "id":"edgeStyle", "yfiles.type":"edgegraphics"})
    SubElement(graphml, 'key', { "for":"node", "id":"attrAuthor", "attr.name":"author", "attr.type":"string"})
    SubElement(graphml, 'key', { "for":"node", "id":"attrComment", "attr.name":"comment", "attr.type":"string"})
    SubElement(graphml, 'key', { "for":"node", "id":"attrUrl", "attr.name":"url", "attr.type":"string"})
    SubElement(graphml, 'key', { "for":"node", "id":"attrCommitCommentBody", "attr.name":"commentBody", "attr.type":"string"})
    SubElement(graphml, 'key', { "for":"node", "id":"attrCommitCommentDate", "attr.name":"commentDate", "attr.type":"string"})
    SubElement(graphml, 'key', { "for":"node", "id":"attrCommitCommentCreator", "attr.name":"commentCreator", "attr.type":"string"})
    graph = SubElement(graphml, 'graph', {"edgedefault":"directed"})

    # initialize color dictionary
    # each user is associated with a node color
    colorDictionary = {}
    

    # nur für jetzt:

    for i in repository.get_commits():
        currentCommitSha = i.sha
        currentCommitCommitter = i.author.login
        currentCommitUrl = i.url

        for k in i.get_comments():
            currentCommitCommentBody = k.body
            currentCommitCommentDate = k.created_at.date()
            currentCommitCommentCreator = k.user.login

        index += 1
        print ("commit ", index, " : ", currentCommitSha)



    k = 0
    for i in repository.get_forks():
        k += 1

        r = requests.get("https://api.github.com/repos/{}/{}/branches".format(i.owner.login,i.name))
        j = json.loads(r.text)

        # # k: ktes (Dictionary-)Element der Liste l
        l=0
        # for k, tupel in enumerate((l[0], l[0][1]) for l in j):

        for k, tupel in enumerate((l['name'], l['commit']['sha'] ) for l in j):
            (name,sha) = tupel
            print("")
            # print("branch # ",(k+1),"\n", "name: ", name,"\n", "sha: ", sha)

        t = requests.get("https://api.github.com/repos/{}/{}/branches/{}".format(i.owner.login,i.name,name))
        h = json.loads(t.text)

        sha = h['commit']['sha']
        o = repository.get_commit(sha)
        currentCommitSha_1 = o.sha
        currentCommitCommitter_1 = o.author.login
        currentCommitUrl_1 = o.url
        print("commit", o.sha)
        # die commit sha wird für jede fork, in der der commit auftaucht, angegeben
        # --> wenn 5 Leute das repo geforkt haben, tritt die commit sha 5 mal auf
        print("")

        # index_1=0
        # for b in repository.get_commits():
          
        #     if b.sha != sha:
        #         print("sha: ",currentCommitSha_1)
        #         print("committer:", currentCommitCommitter_1)
        #     # print("url: ",currentCommitUrl_1)

        #     # das sollte eigentlich noch nicht funktionieren:
        #     # index_1=0

        #     for k in o.get_comments():
        #         currentCommitCommentBody_1 = k.body
        #         currentCommitCommentDate_1 = k.created_at.date()
        #         currentCommitCommentCreator_1 = k.user.login

        #     index_1 += 1
        #     print ("commit ", index_1, " : ", currentCommitSha_1)
        #     print("")



    for i in repository.get_commits():


        # update color dictionary
        # if there is no color associated with the user, insert a new random HTML color in the dictionary
        if currentCommitCommitter not in colorDictionary.keys():
            r = lambda: random.randint(0,255) 
            g = lambda: random.randint(0,255)
            b = lambda: random.randint(0,255)
            colorDictionary[currentCommitCommitter]='#%02X%02X%02X' % (r(),g(),b())
     
        # create a new node
        node = SubElement(graph, "node", {"id" : currentCommitSha})
 
        # edit node style
        nodeStyleData = SubElement(node, "data", {"key":"nodeStyle"})
        shapeNode = SubElement(nodeStyleData, "y:ShapeNode")
        NodeLabel = SubElement(shapeNode, "y:NodeLabel")
        Shape= SubElement(shapeNode, "y:Shape", {"type":"retangle"})
        Geometry= SubElement(shapeNode, "y:Geometry", {"height":"15.0", "width":"60"})
        Fill = SubElement(shapeNode, "y:Fill", {"color":colorDictionary[currentCommitCommitter], "transparent":"false"})
        BorderStyle = SubElement(shapeNode, "y:BorderStyle", {"color":"#ffffff", "type":"line", "width":"1.0"})
        NodeLabel.text = str(currentCommitSha[:7])

        # add node attributes
        attributeData = SubElement(node, "data", {"key":"attrAuthor"})
        if i.author.login !=None:
            attributeData.text = str(i.author.login)
        attributeData = SubElement(node, "data", {"key":"attrComment"})
        attributeData.text = str(i.commit.message)
        attributeData = SubElement(node, "data", {"key":"attrUrl"})
        attributeData.text = str(i.url)
        for k in i.get_comments():
            attributeData = SubElement(node, "data", {"key":"attrCommitCommentBody"})
            attributeData.text = str(k.body)
            attributeData = SubElement(node, "data", {"key":"attrCommitCommentDate"})
            attributeData.text = str(k.created_at.date())
            attributeData = SubElement(node, "data", {"key":"attrCommitCommentCreator"})
            attributeData.text = str(k.user.login)




        index2 = 0
        for k in i.parents:
            index2 += 1
            childCommitSha = k.sha
            edge = SubElement(graphml, "edge", {
                "id":str(index)+"_"+str(index2),
                "directed":"true",
                "source":childCommitSha,
                "target":currentCommitSha})

    # write the xml file

    #change because it doesn`t work for me 
    # ElementTree(graphml).write("./Results/"+repository.name + "_commit_structure.graphml")
    ElementTree(graphml).write("commit_structure.graphml")



if __name__ == "__main__":
    # get the repository ID given as parameter to the script
    repoId = sys.argv[1]

    # login
    userlogin = input("Login: Enter your username: ")
    password = getpass.getpass("Login: Enter your password: ")
    g = pygithub3.Github( userlogin, password )
    
    # get the repository object and call analysis function 
    repo = g.get_repo(int(repoId))
    print ("Analysis of repository ",repo.name)
analyse_repo(repo)