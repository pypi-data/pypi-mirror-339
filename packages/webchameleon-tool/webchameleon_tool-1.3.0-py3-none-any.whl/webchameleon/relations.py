import networkx as nx
from typing import List, Dict
import matplotlib.pyplot as plt
from community import best_partition  # Impor dari python-louvain
import numpy as np
import uuid


class RelationMapper:
    def build_enhanced_graph(
        self, data: List[Dict], weight_threshold: float = 0.5
    ) -> nx.DiGraph:
        G = nx.DiGraph()
        for item in data:
            node_id = item.get("url") or str(uuid.uuid4())
            G.add_node(node_id, type="post", attrs=item.get("metadata", {}))
            if "author" in item.get("metadata", {}):
                G.add_node(item["metadata"]["author"], type="author")
                G.add_edge(
                    node_id,
                    item["metadata"]["author"],
                    relationship="authored_by",
                    weight=1.0,
                )
            if "links" in item:
                for link in item["links"]:
                    G.add_node(link, type="link")
                    G.add_edge(node_id, link, relationship="links_to", weight=0.7)
        # Analisis komunitas
        partition = best_partition(G.to_undirected())
        nx.set_node_attributes(G, partition, "community")
        return G

    def save_graph(
        self,
        graph: nx.DiGraph,
        filename: str,
        include_visualization: bool = True,
        layout: str = "spring",
    ):
        nx.write_graphml(graph, filename)
        if include_visualization:
            plt.figure(figsize=(12, 8))
            pos = getattr(nx, f"{layout}_layout")(graph)
            communities = nx.get_node_attributes(graph, "community")
            unique_communities = set(communities.values())
            colors = {
                comm: np.random.rand(
                    3,
                )
                for comm in unique_communities
            }
            node_colors = [colors[communities[node]] for node in graph.nodes()]
            nx.draw_networkx_nodes(graph, pos, node_color=node_colors, alpha=0.7)
            nx.draw_networkx_edges(graph, pos, alpha=0.3)
            nx.draw_networkx_labels(graph, pos, font_size=8)
            plt.title(f"Graph Visualization with {len(unique_communities)} Communities")
            plt.savefig(f"{filename}.png", dpi=300)
            plt.close()
