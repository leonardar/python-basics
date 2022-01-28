"""Почтальон выходит из почтового отделения, объезжает всех адресатов один раз для вручения посылки и возвращается
в почтовое отделение. Необходимо найти кратчайший маршрут для почтальона.
Координаты точек:
Почтовое отделение – (0, 2)
Ул. Грибоедова, 104/25 – (2, 5)
Ул. Бейкер стрит, 221б – (5, 2)
Ул. Большая Садовая, 302-бис – (6, 6)
Вечнозелёная Аллея, 742 – (8, 3)
Требования к выходным данным:
Координаты точек, следующие друг за другом, показывают найденный кратчайший путь с указанием промежуточной длины
пути у каждой следующей точки. Полная продолжительность всего маршрута указана после символа равенства.
"""
from itertools import permutations


def delta_spot(point_1, point_2):
    return ((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2) ** 0.5


def short_path_spot(points_list):
    results_dict = {}

    for perm in permutations(points_list[1:]):
        distances = []
        for i in range(len(perm) - 1):
            distances.append(delta_spot(perm[i], perm[i + 1]))
        points_path = [points_list[0]] + list(perm) + [points_list[0]]
        distances = [delta_spot(points_list[0], perm[0])] + distances + [delta_spot(perm[-1], points_list[0])]
        results_dict[sum(distances)] = {'path': points_path, 'distances': distances}

    min_value = sorted(results_dict)[0]
    shortest_path = results_dict[min_value]

    output_data = f"{shortest_path['path'][0]}"
    for i in range(len(shortest_path['path']) - 1):
        output_data += f" -> {shortest_path['path'][i + 1]}[{shortest_path['distances'][i]}]"
    output_data += f" = {min_value}"

    return output_data


if __name__ == '__main__':
    points_list = [(0, 2), (2, 5), (5, 2), (6, 6), (8, 3)]
    print(short_path_spot(points_list))
