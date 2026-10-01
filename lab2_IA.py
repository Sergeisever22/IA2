import random
import time

DEPTH = 7
BRANCHING = 2

minimax_nodes = 0
alphabeta_nodes = 0

def generate_leaves():
    leaves_count = BRANCHING ** DEPTH

    leaves = []

    for i in range(leaves_count):
        if i % 5 == 0:
            leaves.append(20)
        else:
            leaves.append(random.randint(-100, 100))

    return leaves



def minimax(depth, index, maximizing_player, leaves):
    global minimax_nodes

    minimax_nodes += 1

    if depth == DEPTH:
        return leaves[index]

    if maximizing_player:

        best_value = float("-inf")

        for child in range(BRANCHING):

            value = minimax(
                depth + 1,
                index * BRANCHING + child,
                False,
                leaves
            )

            best_value = max(best_value, value)

        return best_value

    else:

        best_value = float("inf")

        for child in range(BRANCHING):

            value = minimax(
                depth + 1,
                index * BRANCHING + child,
                True,
                leaves
            )

            best_value = min(best_value, value)

        return best_value


def alpha_beta(
        depth,
        index,
        maximizing_player,
        leaves,
        alpha,
        beta
):
    global alphabeta_nodes

    alphabeta_nodes += 1

    if depth == DEPTH:
        return leaves[index]

    if maximizing_player:

        best_value = float("-inf")

        for child in range(BRANCHING):

            value = alpha_beta(
                depth + 1,
                index * BRANCHING + child,
                False,
                leaves,
                alpha,
                beta
            )

            best_value = max(best_value, value)

            alpha = max(alpha, best_value)

            if beta <= alpha:
                break

        return best_value

    else:

        best_value = float("inf")

        for child in range(BRANCHING):

            value = alpha_beta(
                depth + 1,
                index * BRANCHING + child,
                True,
                leaves,
                alpha,
                beta
            )

            best_value = min(best_value, value)

            beta = min(beta, best_value)

            if beta <= alpha:
                break

        return best_value


def main():

    global minimax_nodes
    global alphabeta_nodes

    random.seed(42)

    leaves = generate_leaves()

    print("Лабораторная работа")
    print("Мини-макс с альфа-бета отсечением")
    print()
    print("Вариант 5")
    print("Глубина дерева:", DEPTH)
    print("Ширина дерева:", BRANCHING)
    print("Количество листьев:", len(leaves))

    print("\nЛистовые значения:")
    print(leaves)

    minimax_nodes = 0

    start_time = time.perf_counter()

    minimax_result = minimax(
        0,
        0,
        True,
        leaves
    )

    minimax_time = time.perf_counter() - start_time


    alphabeta_nodes = 0

    start_time = time.perf_counter()

    alphabeta_result = alpha_beta(
        0,
        0,
        True,
        leaves,
        float("-inf"),
        float("inf")
    )

    alphabeta_time = time.perf_counter() - start_time

    print("\n------------------------------")
    print("Результаты")
    print("------------------------------")

    print("\nОбычный Minimax:")
    print("Результат:", minimax_result)
    print("Проверено узлов:", minimax_nodes)
    print(f"Время: {minimax_time:.8f} секунд")

    print("\nAlpha-Beta:")
    print("Результат:", alphabeta_result)
    print("Проверено узлов:", alphabeta_nodes)
    print(f"Время: {alphabeta_time:.8f} секунд")

    print("\n------------------------------")
    print("Сравнение")
    print("------------------------------")

    print(
        "Сэкономлено узлов:",
        minimax_nodes - alphabeta_nodes
    )

    efficiency = (
        (minimax_nodes - alphabeta_nodes)
        / minimax_nodes
        * 100
    )

    print(f"Уменьшение количества проверок: {efficiency:.2f}%")

    if minimax_result == alphabeta_result:
        print(
            "Оба алгоритма получили одинаковый результат."
        )
    else:
        print("Ошибка: результаты алгоритмов отличаются.")


if __name__ == "__main__":
    main()