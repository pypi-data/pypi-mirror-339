import datakund as dk
import networkx as nx
from sqlite_utils import Database


class ScrapeVisualizer:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.db = Database("scraped_data.db")

    def add_node(self, url, content):
        self.graph.add_node(url, **content.metadata)
        self.db["pages"].insert(
            {
                "url": url,
                "content": content.text,
                "links": ",".join(content.links),
                "timestamp": content.metadata["timestamp"],
            }
        )

    def visualize(self):
        return dk.visualize(self.graph)
