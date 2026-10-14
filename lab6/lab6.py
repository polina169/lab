import time
import itertools
import math
import random

def dist(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5

def is_square(p):
    d = []
    for i in range(4):
        for j in range(i+1,4):
            d.append(dist(p[i],p[j]))
    d.sort()
    if d[0]>0 and d[0]==d[1]==d[2]==d[3] and d[4]==d[5]:
        return True
    return False

K = int(input("Количество точек: "))

points = []

for i in range(K):
    x = random.randint(-5, 5) * 2   
    y = random.randint(-5, 5) * 2   
    points.append((x, y))

points = list(set(points))

print(f"\nСгенерировано {len(points)} уникальных точек:")
print("Ограничение: только чётные координаты (x и y кратны 2)")
print(f"Точек: {len(points)}")
print(points)

print("\n--- 1 способ (циклы) ---")
start = time.time()
s1 = []
n = len(points)
for i in range(n):
    for j in range(i+1,n):
        for k in range(j+1,n):
            for m in range(k+1,n):
                if is_square([points[i],points[j],points[k],points[m]]):
                    s1.append([points[i],points[j],points[k],points[m]])
t1 = (time.time()-start)*1000
print("Найдено квадратов:", len(s1))
print("Время:", t1, "мс")

print("\n--- 2 способ (combinations) ---")
start = time.time()
s2 = []
for combo in itertools.combinations(points,4):
    if is_square(list(combo)):
        s2.append(list(combo))
t2 = (time.time()-start)*1000
print("Найдено квадратов:", len(s2))
print("Время:", t2, "мс")

print("\n--- Сравнение ---")
print("1 способ (циклы):", t1, "мс")
print("2 способ (combinations):", t2, "мс")
if t1 < t2:
    print("Циклы быстрее в", t2/t1, "раз")
else:
    print("Combinations быстрее в", t1/t2, "раз")

print("\n--- Часть 2 (квадрат с максимальной площадью) ---")

if s1:
    max_square = s1[0]
    max_area = 0
    
    for sq in s1:
        dists = []
        for i in range(4):
            for j in range(i+1, 4):
                dists.append(dist(sq[i], sq[j]))
        dists.sort()
        side = dists[0]
        area = side * side
        if area > max_area:
            max_area = area
            max_square = sq
    
    print("\nОПТИМАЛЬНЫЙ КВАДРАТ (с максимальной площадью):")
    print("Вершины:", max_square)
    print("Площадь:", max_area)
    
    if len(s1) > 1:
        print(f"\nВсе найденные квадраты ({len(s1)} шт.):")
        for i, sq in enumerate(s1):
            print(f"  {i+1}: {sq}")
else:
    print("Квадратов не найдено")
