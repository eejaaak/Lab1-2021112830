import networkx as nx
import matplotlib.pyplot as plt
import re
import random
from collections import defaultdict

def create_directed_graph(filepath):
    G = nx.DiGraph()
    with open(filepath, 'r') as file:
        text = file.read().lower()
        # 移除非字母字符并用空格替换
        text = re.sub(r'[^a-z\s]', ' ', text)
        # 替换多个空格为一个空格
        text = re.sub(r'\s+', ' ', text)
        words = text.split()
        for i in range(len(words) - 1):
            if G.has_edge(words[i], words[i+1]):
                G[words[i]][words[i+1]]['weight'] += 1
            else:
                G.add_edge(words[i], words[i+1], weight=1)
    return G

def show_directed_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

def query_bridge_words(G, word1, word2):
    if word1 not in G or word2 not in G:
        return "No word1 or word2 in the graph!"
    bridge_words = [w for w in G if G.has_edge(word1, w) and G.has_edge(w, word2)]
    if not bridge_words:
        return "No bridge words from {} to {}!".format(word1, word2)
    return "The bridge words from {} to {} are: {}.".format(word1, word2, ', '.join(bridge_words))

def generate_new_text(G, input_text):
    words = input_text.lower().split()
    new_text = words[0]
    for i in range(1, len(words)):
        bridge_words = [w for w in G if G.has_edge(words[i-1], w) and G.has_edge(w, words[i])]
        if bridge_words:
            new_word = random.choice(bridge_words)
            new_text += " " + new_word
        new_text += " " + words[i]
    return new_text

def calc_shortest_path(G, word1, word2):
    try:
        path = nx.shortest_path(G, source=word1, target=word2, weight='weight')
        return ' → '.join(path), sum(G[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
    except nx.NetworkXNoPath:
        return "No path found from {} to {}.".format(word1, word2)

def random_walk(G):
    if not G:
        return "Empty graph."
    current_node = random.choice(list(G.nodes))
    visited_edges = set()
    path = [current_node]

    while True:
        neighbors = list(G[current_node])
        if not neighbors or all((current_node, neighbor) in visited_edges for neighbor in neighbors):
            break
        next_node = random.choice(neighbors)
        if (current_node, next_node) in visited_edges:
            break
        visited_edges.add((current_node, next_node))
        path.append(next_node)
        current_node = next_node

    return ' → '.join(path)

def main(args):
    filepath = args[0]  # 假设第一个参数是文件路径
    G = create_directed_graph(filepath)
    show_directed_graph(G)
