def dfs(graph_dict: dict[int, list[int]], start: int, visited: set[int]) -> set[int]:
    """
    Выполняет обход графа в глубину из вершины start.

    Параметры:
    - graph_dict: ориентированный граф вида {вершина: [смежные вершины]}.
    - start: вершина, из которой начинается обход.
    - visited: множество уже посещённых вершин; будет дополняться.

    Возвращает:
    - Множество посещённых вершин (start может не входить, если не встречается по циклу).
    """

    for neighbor in graph_dict.get(start, []):
        if neighbor not in visited:
            visited.add(neighbor)
            dfs(graph_dict, neighbor, visited)

    return visited

def graph_to_tuple(graph: str) -> list[tuple[int, int]]:
    """
    Преобразует строковое представление рёбер в список пар (u, v).

    Ожидаемый формат строки: "u1,v1\n...\nuk,vk".

    Параметры:
    - graph: многострочная строка, каждая строка — ребро "u,v".

    Возвращает:
    - Список кортежей (u, v), где u и v — целые номера вершин.
    """
    graph_list = graph.split('\n')
    graph_tuple = []

    for i in graph_list:
        graph_tuple.append(tuple(int(j) for j in i.split(',')))

    return graph_tuple

def graph_to_dict(graph_tuple: list[tuple[int, int]]) -> dict[int, list[int]]:
    """
    Строит словарь смежности по списку рёбер.

    Параметры:
    - graph_tuple: список рёбер (u, v).

    Возвращает:
    - d: словарь смежности {u: [v1, v2, ...]} только для u с исходящими рёбрами.
    - n_unique: количество уникальных вершин графа.
    """
    d = {}
    unique = list(set(x for t in graph_tuple for x in t))

    for i in unique:
        connected_edges = []
        for j in graph_tuple:
            if i == j[0]:
                connected_edges.append(j[1])
        if connected_edges != []:
            d[i] = connected_edges
    n_unique = len(unique)
    return d, n_unique

def adjacency_matrix_r1(graph_dict: dict[int, list[int]], dim: int) -> list[list[bool]]:
    """
    Строит матрицу смежности R1: наличие прямого ребра u→v.

    Параметры:
    - graph_dict: словарь смежности {u: [v,...]}.
    - dim: количество вершин (максимальный номер вершины).

    Возвращает:
    - Квадратную матрицу dim×dim из bool: matrix[u-1][v-1] = True, если есть u→v.
    """
    matrix = [[False for _ in range(dim)] for _ in range(dim) ]
 
    for key, values in graph_dict.items():
        for value in values:
            matrix[key - 1][value - 1] = True

    return matrix

def adjacency_matrix_r2(graph_dict: dict[int, list[int]], dim: int) -> list[list[bool]]:
    """
    Строит транспонированную матрицу смежности R2: наличие ребра v→u.

    Параметры:
    - graph_dict: словарь смежности {u: [v,...]}.
    - dim: количество вершин.

    Возвращает:
    - Матрицу dim×dim из bool: matrix[v-1][u-1] = True, если есть u→v.
    """
    matrix = [[False for _ in range(dim)] for _ in range(dim) ]
 
    for key, values in graph_dict.items():
        for value in values:
            matrix[value - 1][key - 1] = True

    return matrix

def adjacency_matrix_r3(graph_dict: dict[int, list[int]], dim: int) -> list[list[bool]]:
    """
    Строит матрицу достижимости R3: существует путь u⇝v длины ≥ 2 (без прямых рёбер).

    Параметры:
    - graph_dict: словарь смежности {u: [v,...]}.
    - dim: количество вершин.

    Возвращает:
    - Матрицу dim×dim из bool: matrix[u-1][v-1] = True, если v достижима из u по пути ≥ 2.
    """
    matrix = [[False for _ in range(dim)] for _ in range(dim) ]

    for key in graph_dict.keys():

        visited = dfs(graph_dict, key, set())
        visited.difference_update(graph_dict.get(key, []))
        print("visited:" + str(list(visited)))

        for neighbor in visited:
            matrix[key - 1][neighbor - 1] = True

    return matrix

def adjacency_matrix_r4(graph_dict: dict[int, list[int]], dim: int) -> list[list[bool]]:
    """
    Строит обратную матрицу достижимости R4: отражение R3 (запись в [v][u]).

    Параметры:
    - graph_dict: словарь смежности {u: [v,...]}.
    - dim: количество вершин.

    Возвращает:
    - Матрицу dim×dim из bool: matrix[v-1][u-1] = True, если v достижима из u по пути ≥ 2.
    """
    matrix = [[False for _ in range(dim)] for _ in range(dim) ]

    for key in graph_dict.keys():

        visited = dfs(graph_dict, key, set())
        visited.difference_update(graph_dict.get(key, []))
        print("visited:" + str(list(visited)))

        for neighbor in visited:
            matrix[neighbor - 1][key - 1] = True

    return matrix
    
def adjacency_matrix_r5(graph_dict: dict[int, list[int]], dim: int) -> list[list[bool]]:
    """
    Строит матрицу R5: соединяет между собой всех «братьев/сестёр» (детей одной вершины).

    Параметры:
    - graph_dict: словарь смежности {u: [v,...]}.
    - dim: количество вершин.

    Возвращает:
    - Матрицу dim×dim из bool: для любых разных детей одного u отмечаются связи в обе стороны.
    """
    matrix = [[False for _ in range(dim)] for _ in range(dim) ]
    for keys in graph_dict.keys():
        children = graph_dict[keys] 
        for child_i in children:
            for child_j in children:
                if child_i != child_j:
                    matrix[child_i - 1][child_j - 1] = True
                    matrix[child_j - 1][child_i - 1] = True
    return matrix
    

def get_matrix_list(graph_dict: dict[int, list[int]], n_unique: int) -> list[list[bool]]:
    """
    Возвращает список из пяти матриц [R1, R2, R3, R4, R5] для графа.

    Параметры:
    - graph_dict: словарь смежности {u: [v,...]}.
    - n_unique: количество уникальных вершин графа.

    Возвращает:
    - Список матриц смежности/достижимости в указанном порядке.
    """
    matrix_list = []
    r1 = adjacency_matrix_r1(graph_dict, n_unique)
    matrix_list.append(r1)
    r2 = adjacency_matrix_r2(graph_dict, n_unique)
    matrix_list.append(r2)
    r3 = adjacency_matrix_r3(graph_dict, n_unique)
    matrix_list.append(r3)
    r4 = adjacency_matrix_r4(graph_dict, n_unique)
    matrix_list.append(r4)
    r5 = adjacency_matrix_r5(graph_dict, n_unique)
    matrix_list.append(r5)
    return matrix_list


from typing import List, Tuple

def main(s: str, e: str) -> Tuple[List[List[bool]], List[List[bool]], List[List[bool]], List[List[bool]], List[List[bool]]]:
    """
    Пример использования: формирует граф, вычисляет матрицы R1–R5 и печатает их.
    """
    graph_tuple = graph_to_tuple(s)
    graph_dict, n_unique = graph_to_dict(graph_tuple)
    matrix_list = get_matrix_list(graph_dict, n_unique)
    return tuple(matrix_list)


main("1,2\n1,3\n3,4\n3,5\n5,6\n6,7", "1")