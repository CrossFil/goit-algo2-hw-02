# Greedy Algorithms and Dynamic Programming

## Task 1. 3D‑Printer Job Queue Optimization in a University Lab

### Description
Develop a program to optimize the queue of 3D‑printing jobs by taking into account job priorities and the printer’s technical constraints. Use a greedy algorithm to group models into batches and minimize total print time.

---

### Input Data

1. **Print Jobs List** (`print_jobs`), where each job is represented as a dictionary:
   - `id` (string) — unique model identifier  
   - `volume` (float) — model volume in cm³ (> 0)  
   - `priority` (int) — job priority (1, 2, or 3; 1 is highest)  
   - `print_time` (int) — print time in minutes (> 0)  

2. **Printer Constraints** (`printer_constraints`):
   - `max_volume` (float) — maximum total volume per batch  
   - `max_items` (int) — maximum number of models per batch  

---

### Priorities

1. **1** — course and diploma projects (highest)  
2. **2** — laboratory assignments  
3. **3** — personal projects (lowest)  

---

### Task Requirements

1. Sort all jobs in ascending order of priority.  
2. Assemble jobs into **greedy batches** such that:
   - The sum of volumes in each batch does not exceed `max_volume`.  
   - The number of models in each batch does not exceed `max_items`.  
3. For each batch, calculate the batch print time as the **maximum** `print_time` among its models.  
4. Sum the batch times to compute the **total print time**.  
5. Return the result in the following format:
   ```json
   {
     "print_order": [ /* sequence of job IDs in print order */ ],
     "total_time": /* total time in minutes */
   }

## Task 2. Rod Cutting for Maximum Profit

### Description
Implement a program to determine the optimal way to cut a rod of given length to maximize profit. You must provide two dynamic‑programming solutions:  
1. **Memoized recursion**  
2. **Bottom‑up tabulation**

---

### Input
- `length` (int) — length of the rod (> 0)  
- `prices` (List[int]) — array of prices where `prices[i]` is the price of a rod of length `i+1`  
  - all prices > 0  
  - `len(prices) == length`

---

### Output
Return a dictionary with:
```json
{
  "max_profit": int,       // maximum achievable profit
  "cuts": List[int],       // list of piece lengths in the optimal solution
  "number_of_cuts": int    // total number of cuts made
}
