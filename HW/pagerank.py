import numpy as np
import csv
def pagerank(A, alpha=0.85, max_iter=100, tol=1e-6):
    """
    A: 邻接矩阵
    alpha: 阻尼因子
    max_iter: 最大迭代次数
    tol: 收敛阈值
    """
    n = A.shape[0]
    v = np.ones(n) / n
    for i in range(max_iter):
        v_new = alpha * A @ v + (1 - alpha) / n
        if np.linalg.norm(v_new - v) < tol:
            return v_new
        v = v_new
    return v



def pagerank_from_edges(edges, num_nodes=None, damping_factor=0.85, epsilon=1e-8, max_iterations=100):
    """
    计算PageRank，接受边的集合作为输入
    
    参数:
    edges: list of tuples, 每个tuple表示一条边 (from_node, to_node)
    num_nodes: 节点总数，如果为None则自动从边集合推断
    
    返回:
    dict: 节点到PageRank值的映射
    """
    # 创建节点映射
    nodes = set()
    for src, dst in edges:
        nodes.add(src)
        nodes.add(dst)
    
    if num_nodes is None:
        num_nodes = len(nodes)
    
    # 创建节点到索引的映射
    node_to_index = {node: idx for idx, node in enumerate(sorted(nodes))}
    
    # 构建邻接矩阵
    adjacency_matrix = np.zeros((num_nodes, num_nodes))
    for src, dst in edges:
        adjacency_matrix[node_to_index[src]][node_to_index[dst]] = 1
    
    # 计算出度
    out_degree = np.sum(adjacency_matrix, axis=1)
    
    # 处理出度为0的节点（悬挂节点）
    for i in range(num_nodes):
        if out_degree[i] == 0:
            adjacency_matrix[i] = np.ones(num_nodes) / num_nodes
    
    # 初始化PageRank值
    pagerank_vector = np.ones(num_nodes) / num_nodes
    
    # 标准化邻接矩阵
    probability_matrix = adjacency_matrix / np.maximum(out_degree[:, np.newaxis], 1)
    
    # 迭代计算PageRank
    for _ in range(max_iterations):
        prev_pagerank = pagerank_vector.copy()
        
        # PageRank计算公式
        pagerank_vector = (1 - damping_factor) / num_nodes + \
                         damping_factor * probability_matrix.T.dot(prev_pagerank)
        
        # 检查是否收敛
        if np.sum(np.abs(pagerank_vector - prev_pagerank)) < epsilon:
            break
    
    # 构建结果字典
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

    print(sorted_result[0:10])