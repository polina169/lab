import time
import sys
import math
import matplotlib.pyplot as plt

sys.setrecursionlimit(10000)

def fact(n):
    f = 1
    for i in range(2, n + 1):
        f = f * i
    return f

def F_rec(n):
    """Рекурсия"""
    if n == 1:
        return 1.0
    else:
        s = 1 if n % 2 == 0 else -1
        if n % 2 == 0:
            return s * (F_rec(n - 1) / math.factorial(2 * n))
        else:
            return math.factorial(n)

def F_iter(n):
    """Итерация"""
    if n == 1:
        return 1.0

    prev_f = 1.0
    fact_n = 1
    fact_2n = 2

    for k in range(2, n + 1):
        fact_n *= k
        fact_2n *= (2*k - 1) * (2*k)
        
        s = 1 if k % 2 == 0 else -1

        if k % 2 == 0:
            r = s * (prev_f / fact_2n)
        else:
            r = fact_n

        prev_f = r

    return prev_f

def measure_time(func, n, repeat=3):
    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        result = func(n)
        end = time.perf_counter()
        times.append(end - start)
    return min(times), result

def run_investigation():

    n_values = list(range(1, 16))
    n_values.extend([20, 25, 30, 35, 40, 45, 50])

    rec_times = []
    iter_times = []
    rec_values = []
    iter_values = []

    print(f"{'n':<5} | {'Значение F(n) (итер)':<25} | {'Значение F(n) (рек)':<25} | {'Время Iter(мс)':<15} | {'Время Rec(мс)':<15}")
    print("-" * 120)

    max_rec_n = 0

    for n in n_values:
        iter_time, iter_val = measure_time(F_iter, n)
        iter_times.append(iter_time * 1000)
        iter_values.append(iter_val)

        try:
            rec_time, rec_val = measure_time(F_rec, n)
            rec_times.append(rec_time * 1000)
            rec_values.append(rec_val)
            max_rec_n = n
        except RecursionError:
            rec_times.append(None)
            rec_values.append(None)
        except Exception:
            rec_times.append(None)
            rec_values.append(None)

        iter_val_str = f"{iter_val:.10e}"
        rec_val_str = f"{rec_val:.10e}" if rec_values[-1] is not None else "N/A"
        iter_time_str = f"{iter_time * 1000:.6f}"
        rec_time_str = f"{rec_time * 1000:.6f}" if rec_times[-1] is not None else "N/A"

        print(f"{n:<5} | {iter_val_str:<25} | {rec_val_str:<25} | {iter_time_str:<15} | {rec_time_str:<15}")

    # ========== ГРАФИК ==========
    plt.figure(figsize=(10, 6))
    
    plt.plot(n_values, iter_times, 'o-', color='blue', label='Итеративный метод')
    
    rec_valid_n = [n_values[i] for i in range(len(rec_times)) if rec_times[i] is not None]
    rec_valid_t = [t for t in rec_times if t is not None]
    if rec_valid_t:
        plt.plot(rec_valid_n, rec_valid_t, 's-', color='red', label='Рекурсивный метод')
    
    plt.xlabel('n')
    plt.ylabel('Время (мс)')
    plt.title('Сравнение времени выполнения')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Вывод статистики
    print("\n" + "=" * 120)
    print("СТАТИСТИЧЕСКИЙ АНАЛИЗ:")
    print("-" * 120)

    rec_valid_t = [t for t in rec_times if t is not None]
    if len(rec_valid_t) > 0:
        avg_rec_time = sum(rec_valid_t) / len(rec_valid_t)
        avg_iter_time = sum(iter_times[:len(rec_valid_t)]) / len(rec_valid_t)
        print(f"  • Среднее время рекурсии (n ≤ {max_rec_n}): {avg_rec_time:.6f} мс")
        print(f"  • Среднее время итерации (n ≤ {max_rec_n}): {avg_iter_time:.6f} мс")

if __name__ == "__main__":
    run_investigation()
