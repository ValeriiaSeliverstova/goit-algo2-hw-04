import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from collections import deque


G = nx.DiGraph()

nodes = [
    "Термінал 1",
    "Термінал 2",
    "Склад 1",
    "Склад 2",
    "Склад 3",
    "Склад 4",
    "Магазин 1",
    "Магазин 2",
    "Магазин 3",
    "Магазин 4",
    "Магазин 5",
    "Магазин 6",
    "Магазин 7",
    "Магазин 8",
    "Магазин 9",
    "Магазин 10",
    "Магазин 11",
    "Магазин 12",
    "Магазин 13",
    "Магазин 14",
]

# Додаємо ребра з пропускною здатністю
edges = [
    ("Термінал 1", "Склад 1", 25),
    ("Термінал 1", "Склад 2", 20),
    ("Термінал 1", "Склад 3", 15),
    ("Термінал 2", "Склад 3", 15),
    ("Термінал 2", "Склад 4", 30),
    ("Термінал 2", "Склад 2", 10),
    ("Склад 1", "Магазин 1", 15),
    ("Склад 1", "Магазин 2", 10),
    ("Склад 1", "Магазин 3", 20),
    ("Склад 2", "Магазин 4", 15),
    ("Склад 2", "Магазин 5", 10),
    ("Склад 2", "Магазин 6", 25),
    ("Склад 3", "Магазин 7", 20),
    ("Склад 3", "Магазин 8", 15),
    ("Склад 3", "Магазин 9", 10),
    ("Склад 4", "Магазин 10", 20),
    ("Склад 4", "Магазин 11", 10),
    ("Склад 4", "Магазин 12", 15),
    ("Склад 4", "Магазин 13", 5),
    ("Склад 4", "Магазин 14", 10),
]


# Додаємо всі ребра до графа
G.add_weighted_edges_from(edges)

# Позиції для малювання графа
pos = {
    # Термінали
    "Термінал 1": (2, 0),
    "Термінал 2": (10, 0),
    # Склади
    "Склад 1": (4, 2),
    "Склад 2": (8, 2),
    "Склад 3": (4, -2),
    "Склад 4": (8, -2),
    # Верхній ряд — магазини 1–6 (над складами 1–2)
    "Магазин 1": (0, 4),
    "Магазин 2": (2, 4),
    "Магазин 3": (4, 4),
    "Магазин 4": (6, 4),
    "Магазин 5": (8, 4),
    "Магазин 6": (10, 4),
    # Нижній ряд — магазини 7–14 (під складами 3–4)
    "Магазин 7": (0, -4),
    "Магазин 8": (2, -4),
    "Магазин 9": (4, -4),
    "Магазин 10": (6, -4),
    "Магазин 11": (8, -4),
    "Магазин 12": (10, -4),
    "Магазин 13": (12, -4),
    "Магазин 14": (14, -4),
}


# Малюємо граф

plt.figure(figsize=(12, 8))

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=4000,
    node_color="skyblue",
    font_size=12,
    font_weight="bold",
    arrows=True,
)
labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Відображаємо граф
plt.show()


# Створення матриці

n = len(nodes)
capacity = [[0] * n for _ in range(n)]
index = {name: i for i, name in enumerate(nodes)}

for departure, destination, capacity_path in edges:
    capacity[index[departure]][index[destination]] = capacity_path


capacity_matrix_dataFrame = pd.DataFrame(capacity, index=nodes, columns=nodes)
print(capacity_matrix_dataFrame)


# =======================Алгоритм Едмондса-Карпа для знаходження максимального потоку========================

# Функція для пошуку збільшуючого шляху (BFS)


def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()

        for neighbor in range(len(capacity_matrix)):
            # Перевірка, чи є залишкова пропускна здатність у каналі
            if (
                not visited[neighbor]
                and capacity_matrix[current_node][neighbor]
                - flow_matrix[current_node][neighbor]
                > 0
            ):
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)

    return False


# Основна функція для обчислення максимального потоку
def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [
        [0] * num_nodes for _ in range(num_nodes)
    ]  # Ініціалізуємо матрицю потоку нулем
    parent = [-1] * num_nodes
    max_flow = 0

    # Поки є збільшуючий шлях, додаємо потік
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        # Знаходимо мінімальну пропускну здатність уздовж знайденого шляху (вузьке місце)
        path_flow = float("Inf")
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(
                path_flow,
                capacity_matrix[previous_node][current_node]
                - flow_matrix[previous_node][current_node],
            )
            current_node = previous_node

        # Оновлюємо потік уздовж шляху, враховуючи зворотний потік
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node

        max_flow += path_flow

    return max_flow


capacity_matrix = capacity_matrix_dataFrame.values.tolist()

# Звіт по потоках від терміналів до магазинів

terminals = ["Термінал 1", "Термінал 2"]
stores = [node for node in nodes if node.startswith("Магазин")]


results = []
for t in terminals:
    for s in stores:
        src = index[t]
        snk = index[s]
        flow_ts = edmonds_karp(capacity_matrix, src, snk)
        results.append(
            {"Термінал": t, "Магазин": s, "Фактичний потік (од.)": int(flow_ts)}
        )

report_df = (
    pd.DataFrame(results).sort_values(["Термінал", "Магазин"]).reset_index(drop=True)
)


markdown_table = report_df.to_markdown(index=False, tablefmt="github")

with open("task1/table_max_flow.md", "w", encoding="utf-8") as f:
    f.write("# Таблиця потоків (термінал → магазин)\n\n")
    f.write(markdown_table)

print("\nТаблиця збережена у файлі: task1/table_max_flow.md")
