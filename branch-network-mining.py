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
# sub-directory called Results
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

# Clear screen
os.system('cls' if os.name=='nt' else 'clear')

# Remove CLS Client from system path
if os.environ['PATH'].find("iCLS Client")>=0:
    os.environ['PATH'] = "".join([it for it in os.environ['PATH'].split(";") if not it.find("iCLS Client")>0])

from lxml import etree
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree

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
    graph = SubElement(graphml, 'graph', {"edgedefault":"directed"})

    # initialize color dictionary
    # each user is associated with a node color
    colorDictionary = {}
    
    # generate network
    for i in repository.get_commits():
        currentCommitSha = i.sha
        currentCommitCommitter = i.author.login
        index += 1
        print ("commit ", index, " : ", currentCommitSha)
 
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
        BorderStyle = SubElement(shapeNode, "y:BoderStyle", {"hasColor":"false", "type":"line", "width":"1.0"}) # does not work and i don't know why :-(
        NodeLabel.text = str(currentCommitSha[:7])

        # add node attributes
        attributeData = SubElement(node, "data", {"key":"attrAuthor"})
        attributeData.text = str(i.author.login)
        attributeData = SubElement(node, "data", {"key":"attrComment"})
        attributeData.text = str(i.commit.message)

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
    ElementTree(graphml).write("./Results/"+chosenRepo.name + "_commit_structure.graphml")





if __name__ == "__main__":
    # login
    userlogin = input("Login: Enter your username: ")
    password = getpass.getpass("Login: Enter your password: ")
    g = pygithub3.Github( userlogin, password )
    
    # ask user to repository to analyse
    reponame = input("Enter the name of the repository you want to analyse: ")
    queryResult = g.search_repositories(reponame+ " in:name")
    index = 0
    for i in queryResult:
        print ("type ",index," for ",i.owner.login,"/",i.name)
        index += 1
    chosenIndex = input("type a number and press enter: ");
    chosenRepo = queryResult.get_page(0)[int(chosenIndex)]
    print ("Analysis of repository ",chosenRepo.name)
    analyse_repo(chosenRepo)