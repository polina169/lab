import numpy as np
import matplotlib.pyplot as plt
import os
import random

def print_m(matrix, t):
    print(t)
    for row in matrix:
        for x in row:
            print(x, end=" ")
        print()
    print("-" * 50)

K = int(input("K: "))
N = int(input("N: "))

if N % 2 != 0:
    print("N должно быть четным")
    exit()

if os.path.exists('test.txt'):
    with open('test.txt', 'r') as f:
        A = [[int(x) for x in line.split()] for line in f if line.strip()]
        A = np.array(A)
        N = len(A)
else:
    A = [[random.randint(-10, 10) for _ in range(N)] for _ in range(N)]
    A = np.array(A)

print_m(A, "\nМатрица A:")

half = N // 2

E = A[:half, :half]
B = A[:half, half:]
D = A[half:, :half]
C = A[half:, half:]

print_m(E, "E (левая верхняя):")
print_m(B, "B (правая верхняя):")
print_m(D, "D (левая нижняя):")
print_m(C, "C (правая нижняя):")

F = A.copy()

if E.shape[1] >= 2:
    max_E = np.max(E[:, 1::2])
else:
    max_E = -1000
print_m([[max_E]], f"\nМаксимальный элемент в нечетных столбцах E: {max_E}")

if E.shape[0] >= 2:
    sum_E = np.sum(E[1::2, :])
else:
    sum_E = 0
print_m([[sum_E]], f"Сумма чисел в нечетных строках E: {sum_E}")

if max_E > sum_E:
    print_m([["Условие выполнено: меняем C и B симметрично"]], "\n")
    F[:half, half:], F[half:, half:] = C, B
else:
    print_m([["Условие не выполнено: меняем B и E несимметрично"]], "\n")
    F[:half, :half], F[:half, half:] = B, E

print_m(F, "\nМатрица F после перестановки")

plt.figure(figsize=(15, 4))

plt.subplot(1, 3, 1)
plt.imshow(F, cmap='coolwarm')
plt.colorbar()
plt.title('Тепловая карта F')

plt.subplot(1, 3, 2)
plt.plot(range(N), np.mean(F, axis=1), 'o-', color='blue')
plt.grid(alpha=0.3)
plt.title('Средние по строкам F')

plt.subplot(1, 3, 3)
plt.bar(range(N), np.sum(F, axis=0), color='skyblue')
plt.grid(axis='y', alpha=0.3)
plt.title('Суммы по столбцам F')
plt.tight_layout()
plt.show()

AF = A @ F
print_m(AF, "\nA * F (матричное умножение)")

print_m (A,'---------------')
AT = A.T
print_m (AT,'=================')
print_m(AT, "\nТранспонированная матрица A^T")

K_AF = [[K * AF[i][j] for j in range(N)] for i in range(N)]
print_m(K_AF, f"\nK * (A * F) (K={K})")

K_AT = [[K * AT[i][j] for j in range(N)] for i in range(N)]
print_m(K_AT, f"\nK * A^T (K={K})")

result = [[K_AF[i][j] - K_AT[i][j] for j in range(N)] for i in range(N)]
print_m(result, f"\nРезультат: K*(A*F) - K*A^T")
