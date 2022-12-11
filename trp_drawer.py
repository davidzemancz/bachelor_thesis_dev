import random
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from trp import TRP, Request, Vehicle
from networkx.drawing.nx_agraph import graphviz_layout
import utils

def draw(trp : TRP):
    # Grid graph
    G = nx.Graph()
    plt.figure(figsize=(12,8))

    # Add nodes
    for vehicle in trp.vehicles:
        G.add_node(vehicle.node)
    for request in trp.requests:
        G.add_node(request.nodeFrom)
        G.add_node(request.nodeTo)

    # Add routes edges
    for route in trp.routes:
        for i in range(len(route)-1):
            u = route[i]
            v = route[i+1]
            G.add_edge(u, v)
    pos = nx.spring_layout(G)
    #pos = nx.kamada_kawai_layout(G)
    #pos = nx.planar_layout(G)
    #pos = nx.fruchterman_reingold_layout(G)
    #pos = graphviz_layout(G, prog='sfdp')
    #pos = graphviz_layout(G, prog='dot')

    # Draw nodes
    node_size = 100
    nx.draw_networkx_nodes(     # vehicles
        G, 
        pos, 
        node_size = node_size, 
        nodelist=[vehicle.node for vehicle in trp.vehicles],
        node_color="green",
    )
    nx.draw_networkx_nodes(     # requests
        G, 
        pos,
        node_size = node_size,
        nodelist=[request.nodeFrom for request in trp.requests] + [request.nodeTo for request in trp.requests],
        node_color="blue",
    )
   
    # labels = {order.node: f'{order.id}' for order in vrp.orders}
    # nx.draw_networkx_labels(G, pos, labels)

    # Draw requests edges
    for request in trp.requests:
         nx.draw_networkx_edges(
            G,
            pos,
            edgelist=[(request.nodeFrom, request.nodeTo)],
            width=4,
            edge_color='blue',
            alpha=0.5,
        )

    # Draw routes
    for route in trp.routes:
        route_color = utils.rnd_color(f='hex')
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=[(route[i], route[i+1]) for i in range(len(route)-1)],
            width=2,
            edge_color=route_color,
            alpha=1,
        )
    # edge_labels = nx.get_edge_attributes(G, 'len')
    # nx.draw_networkx_edge_labels(G, pos=pos, label_pos=0.5, edge_labels=edge_labels)

    # Plot graph
    plt.show()

