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
#
# PyGitHub documentation can be found here: 
# https://github.com/jacquev6/PyGithub
# http://pygithub.readthedocs.io/en/latest/reference.html

from github import Github
from github import Commit

import pygithub3

import networkx as nx
import getpass

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
    graphml = Element('graphml', {
            "xmlns":"http://graphml.graphdrawing.org/xmlns",
            "xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
            "xmlns:y":"http://www.yworks.com/xml/graphml",
            "xmlns:yed":"http://www.yworks.com/xml/yed/3",
            "xsi:schemaLocation":"http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd"})
    SubElement(graphml, 'key', { "for":"node", "id":"d1", "yfiles.type":"nodegraphics"})
    SubElement(graphml, 'key', { "for":"edge", "id":"d2", "yfiles.type":"edgegraphics"})
    graph = SubElement(graphml, 'graph', {"edgedefault":"directed"})
    for i in repository.get_commits():
        source = i.sha
        index += 1
        print ("commit ", index, " : ", source)
        node = SubElement(graph, "node", {"id" : source})
        data = SubElement(node, "data", {"key":"d1"})
        shapeNode = SubElement(data, "y:ShapeNode")
        NodeLabel = SubElement(shapeNode, "y:NodeLabel")

        #node shape
        Shape= SubElement(shapeNode, "y:Shape", {"type":"retangle"})

        # Geometry= SubElement(shapeNode, "y:Geometry", {"height":"30.0"}, {"width":"30.0"}, {"x":"0.0"}, {"y":"0.0"})

        # Erklärung:
        # def SubElement(parent, tag, attrib={}, **extra):
        # **extra Additional attributes, given as keyword arguments.

        Geometry= SubElement(shapeNode, "y:Geometry", {"height":"30.0"}, width="%s" %"30.0", x="%s" %"0.0", y="%s" %"0.0")
        Fill = SubElement(shapeNode, "y:Fill", {"color":"#FFCC00"}, transparent="%s" %"false")
        BorderStyle = SubElement(shapeNode, "y:BoderStyle", {"color":"#000000"}, type="%s" %"line", width="%s" %"1.0")

        NodeLabel.text = str(index)
        index2 = 0
        for k in i.parents:
            index2 += 1
            target = k.sha
            edge = SubElement(graphml, "edge", {
                "id":str(index)+"_"+str(index2),
                "directed":"true",
                "source":i.sha,
                "target":k.sha})
#           commit = etree.SubElement(root, "commit")
#
#            nodes = etree.SubElement(commit, "nodes")
#            edges = etree.SubElement(commit, "edges")
#
#            node = etree.SubElement(nodes, "node", id="%s" %C_sha)
#            edge = etree.SubElement(edges, "edge", source = "%s" %source, target = "%s" %target)


#        newfile = (etree.tostring(root, pretty_print=True, xml_declaration = True, encoding="UTF-8"))
 #       newfile = (etree.tostring(root, pretty_print=True))
    ElementTree(graphml).write(chosenRepo.name + "_commit_structure.graphml")
#    print (ElementTree.tostring(graphml))











if __name__ == "__main__":
    # login
    userlogin = input("Login: Enter your username: ")
    password = getpass.getpass("Login: Enter your password: ")
    g = pygithub3.Github( userlogin, password )
	
    # ask user to repository to analyse
    reponame = input("Enter the name of the repository you want to analyse: ")
    queryResult = g.search_repositories(reponame)
    index = 0
    for i in queryResult:
	    print ("type ",index," for ",i.name)
	    index += 1
    chosenIndex = input("type a number and press enter: ");
    chosenRepo = queryResult.get_page(0)[int(chosenIndex)]
    print ("Analysis of repository ",chosenRepo.name)
    analyse_repo(chosenRepo)