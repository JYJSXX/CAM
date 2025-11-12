import numpy as np
import csv
def pagerank(A, alpha=0.85, max_iter=100, tol=1e-6):

    n = A.shape[0]
    v = np.ones(n) / n
    for i in range(max_iter):
        v_new = alpha * A @ v + (1 - alpha) / n
        if np.linalg.norm(v_new - v) < tol:
            return v_new
        v = v_new
    return v



def pagerank_from_edges(edges, num_nodes=None, damping_factor=0.85, epsilon=1e-8, max_iterations=100):

    nodes = set()
    for src, dst in edges:
        nodes.add(src)
        nodes.add(dst)
    
    if num_nodes is None:
        num_nodes = len(nodes)
    
    node_to_index = {node: idx for idx, node in enumerate(sorted(nodes))}
    
    adjacency_matrix = np.zeros((num_nodes, num_nodes))
    for src, dst in edges:
        adjacency_matrix[node_to_index[src]][node_to_index[dst]] = 1
    
    out_degree = np.sum(adjacency_matrix, axis=1)
    
    for i in range(num_nodes):
        if out_degree[i] == 0:
            adjacency_matrix[i] = np.ones(num_nodes) / num_nodes
    
    pagerank_vector = np.ones(num_nodes) / num_nodes
    
    probability_matrix = adjacency_matrix / np.maximum(out_degree[:, np.newaxis], 1)
    
    for _ in range(max_iterations):
        prev_pagerank = pagerank_vector.copy()
        
        pagerank_vector = (1 - damping_factor) / num_nodes + \
                         damping_factor * probability_matrix.T.dot(prev_pagerank)
        
        if np.sum(np.abs(pagerank_vector - prev_pagerank)) < epsilon:
            break
    index_to_node = {idx: node for node, idx in node_to_index.items()}
    return {index_to_node[i]: score for i, score in enumerate(pagerank_vector)}

if __name__ == "__main__":
    with open("PageRank_Dataset.csv", "r") as f:
        reader = csv.reader(f)
        edges = []
        for row in reader:
            edges.append(row)

    result = pagerank_from_edges(edges)

    sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)

    with open("pagerank_result.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Node", "PageRank"])
        for node, rank in sorted_result:
            writer.writerow([node, rank])

    print(sorted_result[0:20])