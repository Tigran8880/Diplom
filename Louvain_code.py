import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain

df = pd.read_csv(r"C:\Users\tiggr\Downloads\data_dip.csv")

G1 = nx.DiGraph()
G2 = nx.DiGraph()
G3 = nx.Graph()
G4 = nx.Graph()


for index, row in df.iterrows():

    user_id = int(row["id"])

    if not pd.isna(row["friends_ids"]):

        friends = str(row["friends_ids"]).split(",")
        weight = row["weights"]

        for friend in friends:

            friend = friend.strip()
            if friend == "":
                continue

            friend = int(friend)

            G1.add_edge(user_id, friend)
            G2.add_edge(user_id, friend, weight=weight)


    if not pd.isna(row["undirected_friends_ids"]):

        friends = str(row["undirected_friends_ids"]).split(",")
        weights = str(row["undirected_weights"]).split(",")

        for friend, w in zip(friends, weights):

            friend = friend.strip()
            w = w.strip()

            if friend == "":
                continue

            friend = int(friend)
            w = float(w)

            G3.add_edge(user_id, friend)
            G4.add_edge(user_id, friend, weight=w)


partition1 = community_louvain.best_partition(G1.to_undirected())
partition2 = community_louvain.best_partition(G2.to_undirected(), weight="weight")
partition3 = community_louvain.best_partition(G3)
partition4 = community_louvain.best_partition(G4, weight="weight")


def print_communities(partition, title):

    communities = {}

    for node, com in partition.items():
        communities.setdefault(com, []).append(node)

    print(f"\n{title}\n")

    for c, members in communities.items():
        print(f"Համայնք {c} (size={len(members)}): {members}")


print_communities(partition1, "Ուղղորդված")
print_communities(partition2, "Ուղղորդված քաշով")
print_communities(partition3, "Ոչ ուղղորդված")
print_communities(partition4, "Ոչ ուղղորդված քաշով")


def show_graph(G, partition, title):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 8))

    colors = [partition[node] for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=colors, cmap=plt.cm.Set3, node_size=300)

    edges = G.edges()
    weights = [G[u][v].get('weight', 1) for u, v in edges]
    nx.draw_networkx_edges(G, pos, width=weights, alpha=0.6)

    nx.draw_networkx_labels(G, pos, font_size=8)
    plt.title(title)
    plt.axis("off")
    plt.show()


show_graph(G1, partition1, "Ուղղորդված")
show_graph(G2, partition2, "Ուղղորդված քաշով")
show_graph(G3, partition3, "Ոչ ուղղորդված")
show_graph(G4, partition4, "Ոչ ուղղորդված քաշով")