# Лабораторная работа 2
## Мини-макс с альфа-бета отсечением

## Цель работы

Изучить принцип работы алгоритма **Minimax** и его оптимизированной версии с использованием **альфа-бета отсечения**. Сравнить алгоритмы по количеству проверяемых узлов и времени выполнения.

---

## Вариант задания

**Вариант 5**

| Параметр | Значение |
|---|---|
| Глубина дерева | 7 |
| Ширина дерева | 2 |
| Тип игроков | MAX и MIN |
| Количество листьев | 128 |
| Особенность | Часть листовых значений одинаковые |

По условию варианта необходимо построить игровое дерево глубиной `7` и шириной `2`.

Количество листовых узлов:

```text
2^7 = 128
```

Полное количество узлов бинарного дерева:

```text
1 + 2 + 4 + 8 + 16 + 32 + 64 + 128 = 255
```

Часть листьев имеет одинаковые значения, что позволяет проверить работу алгоритмов при наличии равнозначных вариантов развития игры.

---

# Ход работы

## 1. Генерация листовых значений

Для начала были сгенерированы значения для 128 листовых узлов дерева.

Часть значений специально устанавливается равной `20`.

```python
def generate_leaves():
    leaves_count = BRANCHING ** DEPTH

    leaves = []

    for i in range(leaves_count):
        if i % 5 == 0:
            leaves.append(20)
        else:
            leaves.append(random.randint(-100, 100))

    return leaves
```

Условие:

```python
if i % 5 == 0:
    leaves.append(20)
```

означает, что каждый пятый лист получает одинаковое значение `20`.

Остальные значения генерируются случайным образом в диапазоне от `-100` до `100`.

---

## 2. Реализация обычного Minimax

Алгоритм Minimax работает рекурсивно.

Игрок **MAX** пытается выбрать максимальное значение, а игрок **MIN** — минимальное.

```python
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
```

Алгоритм просматривает все возможные состояния дерева.

Для дерева глубиной `7` и шириной `2` обычный Minimax проверяет все:

```text
255 узлов
```

---

## 3. Реализация Alpha-Beta

Для оптимизации алгоритма Minimax было реализовано альфа-бета отсечение.

Используются две дополнительные переменные:

- `alpha` — лучший результат для игрока MAX;
- `beta` — лучший результат для игрока MIN.

```python
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
```

Главное условие отсечения:

```python
if beta <= alpha:
    break
```

Если дальнейшее исследование ветви уже не способно изменить итоговое решение, оставшиеся дочерние узлы не проверяются.

---

# Полный код программы

```python
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
        print("Оба алгоритма получили одинаковый результат.")
    else:
        print("Ошибка: результаты алгоритмов отличаются.")


if __name__ == "__main__":
    main()
```

---

# Результат выполнения программы

После запуска программы выводятся:

- параметры варианта;
- количество листьев;
- сгенерированные листовые значения;
- результат обычного Minimax;
- количество проверенных Minimax узлов;
- время выполнения Minimax;
- результат Alpha-Beta;
- количество проверенных Alpha-Beta узлов;
- время выполнения Alpha-Beta;
- количество сэкономленных узлов;
- процент уменьшения количества проверок.

---

# Скриншоты выполнения программы

## Скриншот 1 — запуск программы и листовые значения

```markdown
![Запуск программы](images/result1.jpg)
```

![Запуск программы](images/result1.jpg)

---

## Скриншот 2 — результаты Minimax и Alpha-Beta

```markdown
![Результаты работы программы](images/result2.jpg)
```

![Результаты работы программы](images/result2.jpg)

---

## Скриншот 3 — сравнение эффективности

```markdown
![Сравнение алгоритмов](images/result3.jpg)
```

![Сравнение алгоритмов](images/result3.jpg)

---

# Сравнение алгоритмов

| Характеристика | Minimax | Alpha-Beta |
|---|---|---|
| Глубина дерева | 7 | 7 |
| Ширина дерева | 2 | 2 |
| Количество листьев | 128 | 128 |
| Максимальное количество узлов | 255 | До 255 |
| Использует отсечения | Нет | Да |
| Результат | Одинаковый | Одинаковый |
| Скорость | Ниже | Обычно выше |

Обычный Minimax полностью исследует игровое дерево, поэтому проверяет все `255` узлов.

Alpha-Beta работает по тому же принципу, но позволяет прекращать исследование тех ветвей, которые уже не способны повлиять на конечное решение.

При этом итоговое значение обоих алгоритмов остается одинаковым.

---

# Анализ эффективности

Эксперимент показывает, что алгоритм Alpha-Beta способен проверять меньше узлов по сравнению с обычным Minimax.

Количество отсечений зависит от порядка расположения листовых значений. При удачном расположении значений значительная часть дерева может быть отброшена.

Одинаковые значения листьев, предусмотренные вариантом 5, позволяют проверить ситуацию, при которой несколько различных путей могут приводить к одинаковому результату.

Несмотря на наличие равных значений, оба алгоритма должны возвращать одинаковый итоговый результат.

Время выполнения измеряется с использованием:

```python
time.perf_counter()
```

Для небольшого дерева разница во времени может быть очень маленькой, поскольку оба алгоритма выполняются быстро. Основным показателем эффективности в данном случае является количество посещённых узлов.

---

# Вывод

В ходе лабораторной работы были реализованы два алгоритма поиска оптимального решения в игровом дереве: классический **Minimax** и оптимизированный **Minimax с альфа-бета отсечением**.

Для варианта 5 было создано бинарное дерево глубиной 7, содержащее 128 листовых вершин и 255 узлов в полном дереве. Часть листовых значений была специально сделана одинаковой.

Обычный Minimax исследует всё игровое дерево, тогда как Alpha-Beta позволяет исключать из рассмотрения ветви, которые уже не могут повлиять на итоговый результат.

В результате оба алгоритма получают одинаковое итоговое значение, однако Alpha-Beta в большинстве случаев анализирует меньшее количество узлов.

Таким образом, альфа-бета отсечение позволяет повысить эффективность алгоритма Minimax без изменения результата его работы.
