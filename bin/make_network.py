#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Library to write graph data into JSON or GEXF (Gephi Network files)
"""

import json
import networkx as nx
from networkx.readwrite import json_graph

def write_graph_in_format(graph, filename, fileformat='gexf') :
    if fileformat.lower() == 'json' or filename.endswith('.json'):
        return json.dump(json_graph.node_link_data(graph), open(filename,'w'))
    return nx.write_gexf(graph, filename)

def add_node(graph, node, **args):
    if not graph.has_node(node):
        graph.add_node(node, label=node, **args)

def add_edge(graph, node1, node2, weight=1):
    if graph.has_edge(node1, node2) and weight:
        graph[node1][node2]['weight'] += weight
    else:
        graph.add_edge(node1, node2, weight=weight)

def record_links(dic, line, val):
    line = line.lower().strip()
    if line and line != "undefined":
        if not line in dic:
            dic[line] = []
        if not val in dic[line]:
            dic[line].append(val)

def add_links(G, dic):
    for f in dic:
        print f
        past = []
        for a in f:
            for b in past:
                add_edge(G, a, b)
            past.append(a)

with open('data/data.json') as f:
    data = json.loads(f.read())

G = nx.Graph()
cats = {}
fams = {}
for line in data:
    add_node(G, line['name'], desc=line["description"], category=line["category"], status=line["status"])
    record_links(cats, line["category"], line['name'])
    record_links(fams, line["family"], line['name'])

for line in data:
    for link in line["relatedItems"]:
        link = link.strip('[],: ')
        if link and link != 'undefined' and link != "see" and link != "also":
            add_edge(G, line['name'], link, weight=5)
add_links(G, cats)
add_links(G, fams)

write_graph_in_format(G, 'public/graph/network.gexf')
write_graph_in_format(G, 'public/graph/network.json')
