from task1.task import main as main_task1
import math as m

def entropy(matrix_list: list[list[bool]]) -> float:
    outgoing_count = []

    for matrix in matrix_list:
        outgoing_count.append([sum(row) for row in matrix])

    entropy_list = []
    for count in outgoing_count:
        entropy = 0
        for c in count:
            if c > 0:
                entropy += -(c/6) * m.log2(c/6)
        entropy_list.append(entropy)

    entropy_m_r = sum(entropy_list)
    return entropy_m_r

def get_norm_complexity(entropy: float) -> float:
    c = 1 / (m.e * m.log(2))
    return entropy / (5 * 7 * c)

def main(s: str, e: str) -> tuple[float, float]:
    matrix_list = main_task1(s, e)
    h_m_r = entropy(matrix_list)
    norm_complexity =  get_norm_complexity(h_m_r)
    answer = (round(h_m_r, 1), round(norm_complexity, 1))
    print(answer)


main("1,2\n1,3\n3,4\n3,5\n5,6\n6,7", "1")
