from itertools import permutations


def delta(point_1: tuple, point_2: tuple) -> float:
    """
    Вычисление расстояния между двумя точками (адресами)
    :param point_1:первый адрес
    :param point_2:второй адрес
    :return:результат вычисления
    """
    return ((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2) ** 0.5


def shortest_path_spot(points_list: list) -> float and dict:
    """
    Перебор всех возможных маршрутов, сравнение расстояний маршрутов и нахождение кратчайшего пути
    :param points_list:координаты точек
    :return:наименьшее расстояние, все промежуточные точки кратчайшего пути и расстояния между ними
    """
    results = {}

    for perm in permutations(points_list[1:]):
        distances = []
        for i in range(len(perm) - 1):
            distances.append(delta(perm[i], perm[i + 1]))
        points_path = [points_list[0]] + list(perm) + [points_list[0]]
        distances = [delta(points_list[0], perm[0])] + distances + [delta(perm[-1], points_list[0])]
        results[sum(distances)] = {'path': points_path, 'distances': distances}

    min_value = sorted(results)[0]
    shortest_path = results[min_value]
    return min_value, shortest_path


def output(min_value: float, shortest_path: dict) -> str:
    """
    Формирование выходных данных: последовательность точек кратчайшего пути с выводом промежуточных
    расстояний для каждой точки и общая длина маршрута
    :param min_value:наименьшее расстояние
    :param shortest_path:все промежуточные точки кратчайшего пути и расстояния между ними
    :return: выходные данные
    """
    output_data = f"{shortest_path['path'][0]}"
    for i in range(len(shortest_path['path']) - 1):
        output_data += f" -> {shortest_path['path'][i + 1]}[{shortest_path['distances'][i]}]"
    output_data += f" = {min_value}"
    return output_data


if __name__ == '__main__':

    points_list = [
        (0, 2),
        (2, 5),
        (5, 2),
        (6, 6),
        (8, 3)]

    min_value, shortest_path = shortest_path_spot(points_list)
    output(min_value, shortest_path)
