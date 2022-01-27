'''Почтальон выходит из почтового отделения, объезжает всех адресатов один раз для вручения посылки и возвращается
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
'''
from itertools import permutations


def delta(point_1, point_2):
    return ((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2) ** 0.5


points_list = [(0, 2), (2, 5), (5, 2), (6, 6), (8, 3)]
results = {}

for perm in permutations(points_list[1:]):
    distances = []
    for i in range(len(perm)-1):
        distances.append(delta(perm[i], perm[i+1]))
    path = [points_list[0]] + list(perm) + [points_list[0]]
    distances = [delta(points_list[0], perm[0])] + distances + [delta(perm[-1], points_list[0])]
    results[sum(distances)] = {'path': path, 'distances': distances}

min = sorted(results)[0]
min_result = results[min]

answer = f"{min_result['path'][0]}"
for i in range(len(min_result['path'])-1):
    answer += f" -> {min_result['path'][i+1]}[{min_result['distances'][i]}]"
answer += f" = {min}"

print(answer)
