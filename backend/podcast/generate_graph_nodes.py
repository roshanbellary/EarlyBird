from sklearn.manifold import TSNE
from podcast.ml.retrieval.merger import Merger
from podcast.ml.inference.rl_bandit import HybridLinUCBModel
import numpy as np

class InterestGraph:

    def __init__(self, rl_model):
        self.nodes = rl_model.articles
        self.rl_model = rl_model

    def generate_init_nodes(self):
        embeddings = []
        for node in self.nodes:
            embeddings.append(node.embedding)
        tsne = TSNE(n_components=3, perplexity=30, learning_rate=200, n_iter=1000)
        embeddings_3d = tsne.fit_transform(np.array(embeddings))

        for embedding in embeddings_3d:
            node.embedding_3d = embedding

    def interest_score_function(x, n, alpha=0.5):
        numerator = math.exp(-alpha * (x - 1)) - math.exp(-alpha * (n - 1))
        denominator = 1 - math.exp(-alpha * (n - 1))
        return numerator / denominator

    def update_interest_scores(self):
        n = self.rl_model.num_articles
        top_articles = self.rl_model.return_next_articles(n, update_state=False)
        
        for x in range(1, n + 1):
            fx = decaying_function(x, n)
            top_articles[x - 1].interest_score = fx
    
    def update_rl_model(self, x, y, z):
        closest_article = self.nodes[0]
        dist = float('inf')
        for node in self.nodes:
            e = node.embedding_3d
            d = (e[0] - x) ** 2 + (e[1] - y) ** 2 + (e[2] - z) ** 2
            if d < dist:
                dist = d
                closest_article = node
        
        category = closest_article.section
        delta = 75
        for node in self.nodes:
            if node.section == category:
                self.rl_model.feedback(node, delta)

# if __name__ == "__main__":  
#     url = "backend/podcast/ml/retrieval/db/"
#     merger = Merger(db_path = url)
#     articles = merger.merge()

#     rl_model = HybridLinUCBModel(articles)
#     graph = InterestGraph(rl_model)
#     embeddings = []
#     for node in graph.nodes:
#         embeddings.append(node.embedding)
#     tsne = TSNE(n_components=3, perplexity=30, learning_rate=200, n_iter=1000)
#     # print(len(embeddings), len(embeddings[0]))
#     embeddings_3d = tsne.fit_transform(np.array(embeddings))
#     print(embeddings_3d.shape)
    








    