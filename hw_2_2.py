from typing import List, Dict, Tuple


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію

    Args:
        length: довжина стрижня (>0)
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    if length <= 0:
        raise ValueError("Length must be > 0")
    if len(prices) != length:
        raise ValueError("Prices array length must equal rod length")

    memo_profit: Dict[int, int] = {}
    memo_cut: Dict[int, int] = {}

    def recurse(n: int) -> int:
        if n == 0:
            return 0
        if n in memo_profit:
            return memo_profit[n]
        max_p = 0
        best_cut = n  # за замовчуванням — не різати
        for i in range(1, n + 1):
            current = prices[i - 1] + recurse(n - i)
            if current > max_p:
                max_p = current
                best_cut = i
        memo_profit[n] = max_p
        memo_cut[n] = best_cut
        return max_p

    max_profit = recurse(length)

    # Відновлення розрізів
    cuts: List[int] = []
    n = length
    while n > 0:
        c = memo_cut.get(n, n)
        cuts.append(c)
        n -= c

    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": max(0, len(cuts) - 1)
    }


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію

    Args:
        length: довжина стрижня (>0)
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    if length <= 0:
        raise ValueError("Length must be > 0")
    if len(prices) != length:
        raise ValueError("Prices array length must equal rod length")

    # dp_profit[i] — максимальний прибуток для довжини i
    dp_profit = [0] * (length + 1)
    # first_cut[i] — оптимальна довжина першого шматка при довжині i
    first_cut = [0] * (length + 1)

    for n in range(1, length + 1):
        max_p = 0
        best_cut = n
        for i in range(1, n + 1):
            current = prices[i - 1] + dp_profit[n - i]
            if current > max_p:
                max_p = current
                best_cut = i
        dp_profit[n] = max_p
        first_cut[n] = best_cut

    max_profit = dp_profit[length]

    # Відновлення розрізів
    cuts: List[int] = []
    n = length
    while n > 0:
        c = first_cut[n]
        cuts.append(c)
        n -= c

    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": max(0, len(cuts) - 1)
    }


# Тести
def run_tests():
    test_cases = [
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок"
        },
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати"
        },
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи"
        }
    ]

    for test in test_cases:
        length = test["length"]
        prices = test["prices"]
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {length}")
        print(f"Ціни: {prices}")

        memo_result = rod_cutting_memo(length, prices)
        print("\nРезультат мемоізації:")
        print(f"  Максимальний прибуток: {memo_result['max_profit']}")
        print(f"  Розрізи: {memo_result['cuts']}")
        print(f"  Кількість розрізів: {memo_result['number_of_cuts']}")

        table_result = rod_cutting_table(length, prices)
        print("\nРезультат табуляції:")
        print(f"  Максимальний прибуток: {table_result['max_profit']}")
        print(f"  Розрізи: {table_result['cuts']}")
        print(f"  Кількість розрізів: {table_result['number_of_cuts']}")

        assert memo_result == table_result, "Різні результати між методами!"
        print("Перевірка пройшла успішно!")


if __name__ == "__main__":
    run_tests()
