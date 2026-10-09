import os
import random

K = int(input("K: "))
N = int(input("N: "))

if os.path.exists('test1.txt'):
    with open('test1.txt', 'r') as f:
        A = [[int(x) for x in line.split()] for line in f if line.strip()]
        N = len(A)
else:
    A = [[random.randint(-10, 10) for _ in range(N)] for _ in range(N)]
print("\nМатрица А")
def print_m(A):
    for r in A:
        for x in r:
            print(x, end=" ")
        print()
    print('---------------------------------------------------')
print_m(A)

def is_area1(i, j, n): return i < j and i + j < n - 1
def is_area2(i, j, n): return i < j and i + j > n - 1
def is_area3(i, j, n): return i > j and i + j > n - 1
def is_area4(i, j, n): return i > j and i + j < n - 1

F = [row[:] for row in A]

zeros_area4 = 0
for i in range(N):
    for j in range(N):
        if is_area4(i, j, N) and j % 2 == 0: 
            if A[i][j] == 0:
                zeros_area4 += 1

sum_area1 = 0
for i in range(N):
    for j in range(N):
        if is_area1(i, j, N) and i % 2 == 0: 
            sum_area1 += A[i][j]

print("\nКоличество нулей в нечётных столбцах области 4: " + str(zeros_area4))
print("Сумма чисел в нечётных строках области 1: " + str(sum_area1))

if zeros_area4 > sum_area1:
    print("\nУсловие выполнено: меняем области 1 и 2 симметрично")
    for i in range(N):
        for j in range(N):
            if is_area1(i, j, N):
                i2 = j
                j2 = N - 1 - i
                F[i][j], F[i2][j2] = A[i2][j2], A[i][j]
else:
    print("\nУсловие не выполнено: меняем области 2 и 3 несимметрично")
    area2_elems = []
    area3_elems = []
    for i in range(N):
        for j in range(N):
            if is_area2(i, j, N):
                area2_elems.append((i, j))
            if is_area3(i, j, N):
                area3_elems.append((i, j))
    for (i2, j2), (i3, j3) in zip(area2_elems, area3_elems):
        F[i2][j2], F[i3][j3] = A[i3][j3], A[i2][j2]

print("\nМатрица F после перестановки")

AF = [[sum(A[i][k] * F[k][j] for k in range(N)) for j in range(N)] for i in range(N)]
print("\nA * F (матричное умножение)")
print_m(AF)

AT = [[A[j][i] for j in range(N)] for i in range(N)]
print("\nТранспонированная матрица A^T")
print_m(AT)

K_AF = [[K * AF[i][j] for j in range(N)] for i in range(N)]
print("\nK * (A * F)")
print_m(K_AF)

K_AT = [[K * AT[i][j] for j in range(N)] for i in range(N)]
print("\nK * A^T")
print_m(K_AT)

result = [[K_AF[i][j] - K_AT[i][j] for j in range(N)] for i in range(N)]
print("\nРезультат: K*(A*F) - K*A^T")
print_m(result)

