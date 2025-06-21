from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк у вигляді словників:
            {
                "id": str,
                "volume": float,
                "priority": int,
                "print_time": int
            }
        constraints: Обмеження принтера у вигляді словника:
            {
                "max_volume": float,
                "max_items": int
            }

    Returns:
        Dict з порядком друку та загальним часом:
        {
            "print_order": List[str],
            "total_time": int
        }
    """
    # Перетворюємо словники у об’єкти для зручності
    jobs = [PrintJob(**job) for job in print_jobs]
    cons = PrinterConstraints(**constraints)

    # Сортуємо за пріоритетом (1 — найвищий)
    jobs.sort(key=lambda j: j.priority)

    print_order: List[str] = []
    total_time = 0

    # Поточна група для одночасного друку
    current_batch: List[PrintJob] = []
    current_volume = 0.0

    def flush_batch():
        nonlocal total_time, current_batch, current_volume, print_order
        if not current_batch:
            return
        # Час друку групи = максимальний час серед моделей у групі
        batch_time = max(job.print_time for job in current_batch)
        total_time += batch_time
        # Додаємо ідентифікатори моделей до порядку
        print_order.extend(job.id for job in current_batch)
        # Очистка для нової групи
        current_batch = []
        current_volume = 0.0
        return current_batch, current_volume

    # Формуємо групи жадібно
    for job in jobs:
        can_add_by_volume = (current_volume + job.volume) <= cons.max_volume
        can_add_by_count = len(current_batch) < cons.max_items

        if can_add_by_volume and can_add_by_count:
            current_batch.append(job)
            current_volume += job.volume
        else:
            # Немає місця — друкуємо поточну групу та починаємо нову
            current_batch, current_volume = flush_batch() or ([], 0.0)
            current_batch.append(job)
            current_volume = job.volume

    # Друкуємо останню групу
    flush_batch()

    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Тестування
def test_printing_optimization():
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}
    ]
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]
    constraints = {"max_volume": 300, "max_items": 2}

    print("Тест 1 (однаковий пріоритет):")
    res1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {res1['print_order']}")
    print(f"Загальний час: {res1['total_time']} хвилин\n")

    print("Тест 2 (різні пріоритети):")
    res2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {res2['print_order']}")
    print(f"Загальний час: {res2['total_time']} хвилин\n")

    print("Тест 3 (перевищення обмежень):")
    res3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {res3['print_order']}")
    print(f"Загальний час: {res3['total_time']} хвилин")

if __name__ == "__main__":
    test_printing_optimization()
