class InterestGraph:

    def __init__(self, rl_model):
        self.nodes = []
        self.rl_model = rl_model

def generate_init_nodes():
    url = "direct/retrieval/db/"
    merger = Merger(db_path = url)
    articles = merger.merge()

    


    