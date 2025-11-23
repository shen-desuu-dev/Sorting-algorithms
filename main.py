import os
import math

def log_and_print(log_list, message):
    log_list.append(message)
    print(message)

def table_array(arr, explanation):
    rows = []
    rows.append("| Position | Value | Explanation |")
    rows.append("|---------|--------|-------------|")
    for i, v in enumerate(arr):
        rows.append(f"| {i:<7} | {str(v):<6} | {explanation} |")
    return "\n".join(rows) + "\n"

def table_tree(arr):
    if not arr:
        return "Tree is empty.\n"
    n = len(arr)
    display = [("[ ]" if v is None else str(v)) for v in arr]
    depth = math.floor(math.log2(n)) + 1
    out = []
    out.append("### Tree Structure (Markdown Table)\n")
    out.append("| Level | Nodes | Explanation |")
    out.append("|-------|--------|-------------|")
    index = 0
    for level in range(depth):
        level_count = 2 ** level
        row = display[index:index + level_count]
        index += level_count
        explanation = "Root level." if level == 0 else "Children of previous level. Missing children shown as [ ]."
        out.append(f"| {level} | {', '.join(row)} | {explanation} |")
    return "\n".join(out) + "\n"

def parse_input(raw):
    if all(x.lstrip("-").isdigit() for x in raw):
        return [int(x) for x in raw]
    return [s.upper() for s in raw]

def write_log(algorithm, log):
    folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Sorted")
    os.makedirs(folder, exist_ok=True)
    count = 1
    while True:
        file = os.path.join(folder, f"{algorithm} {count}.txt")
        if not os.path.exists(file):
            with open(file, "w") as f:
                f.write("\n".join(log))
            return file
        count += 1

class SelectionSorter:
    def __init__(self, items, asc=True):
        self.items = items
        self.asc = asc
        self.log = []
    def compare(self, a, b):
        return a < b if self.asc else a > b
    def sort(self):
        arr = self.items
        log_and_print(self.log, f"--- SELECTION SORT START ---\nInitial array:\n{table_array(arr,'Initial')}")

        n = len(arr)
        for i in range(n):
            best = i
            for j in range(i+1, n):
                log_and_print(self.log, f"Compare {arr[j]} and {arr[best]}")
            for j in range(i+1, n):
                if self.compare(arr[j], arr[best]):
                    best = j
            if best != i:
                arr[i], arr[best] = arr[best], arr[i]
                log_and_print(self.log, table_array(arr, f"Swapped positions {i} and {best}"))
        log_and_print(self.log, f"--- COMPLETED ---\nFinal:\n{table_array(arr,'Final state')}")
        return arr

class HeapSorter:
    def __init__(self, items, asc=True):
        self.items = items
        self.asc = asc
        self.log = []
    def compare(self, a, b):
        return a > b if self.asc else a < b
    def heapify(self, arr, n, i):
        left = 2*i + 1
        right = 2*i + 2
        largest = i

        if left < n:
            log_and_print(self.log, f"Compare {arr[largest]} with {arr[left]}")
            if self.compare(arr[left], arr[largest]):
                largest = left
        if right < n:
            log_and_print(self.log, f"Compare {arr[largest]} with {arr[right]}")
            if self.compare(arr[right], arr[largest]):
                largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            log_and_print(self.log, table_array(arr, f"Swap {i} <-> {largest}"))
            log_and_print(self.log, table_tree(arr))
            self.heapify(arr, n, largest)

    def sort(self):
        arr = self.items
        n = len(arr)

        log_and_print(self.log, f"--- HEAP SORT START ---\nInitial:\n{table_array(arr,'Initial')}")

        for i in range(n//2 - 1, -1, -1):
            self.heapify(arr, n, i)

        for i in range(n-1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            log_and_print(self.log, table_array(arr, f"Extract root to position {i}"))
            log_and_print(self.log, table_tree(arr))
            self.heapify(arr, i, 0)

        log_and_print(self.log, f"--- COMPLETED ---\nFinal:\n{table_array(arr,'Final state')}")
        return arr

class InsertionSorter:
    def __init__(self, items, asc=True):
        self.items = items
        self.asc = asc
        self.log = []
    def compare(self, a, b):
        return a < b if self.asc else a > b
    def sort(self):
        arr = self.items
        log_and_print(self.log, f"--- INSERTION SORT START ---\nInitial:\n{table_array(arr,'Initial')}")

        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and self.compare(key, arr[j]):
                arr[j+1] = arr[j]
                j -= 1
            arr[j+1] = key
            log_and_print(self.log, table_array(arr, f"Inserted {key} at {j+1}"))

        log_and_print(self.log, f"--- COMPLETED ---\nFinal:\n{table_array(arr,'Final state')}")
        return arr

class MergeSorter:
    def __init__(self, items, asc=True):
        self.items = items
        self.asc = asc
        self.log = []
    def compare(self, a, b):
        return a <= b if self.asc else a >= b
    def merge_sort(self, arr):
        if len(arr) <= 1:
            return arr

        mid = len(arr)//2
        left = self.merge_sort(arr[:mid])
        right = self.merge_sort(arr[mid:])

        merged = []
        i = j = 0

        while i < len(left) and j < len(right):
            if self.compare(left[i], right[j]):
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])

        log_and_print(self.log, table_array(merged, "After merge"))
        log_and_print(self.log, table_tree(merged))
        return merged
    def sort(self):
        log_and_print(self.log, f"--- MERGE SORT START ---\nInitial:\n{table_array(self.items,'Initial')}")
        result = self.merge_sort(self.items)
        log_and_print(self.log, f"--- COMPLETED ---\nFinal:\n{table_array(result,'Final state')}")
        return result

class QuickSorter:
    def __init__(self, items, asc=True):
        self.items = items
        self.asc = asc
        self.log = []
    def compare(self, a, b):
        return a <= b if self.asc else a >= b
    def quick(self, arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr)//2]
        left = [x for x in arr if self.compare(x, pivot) and x != pivot]
        mid = [x for x in arr if x == pivot]
        right = [x for x in arr if not self.compare(x, pivot)]

        combined = left + mid + right
        log_and_print(self.log, table_array(combined, f"Pivot {pivot}"))
        log_and_print(self.log, table_tree(combined))

        return self.quick(left) + mid + self.quick(right)
    def sort(self):
        log_and_print(self.log, f"--- QUICK SORT START ---\nInitial:\n{table_array(self.items,'Initial')}")
        result = self.quick(self.items)
        log_and_print(self.log, f"--- COMPLETED ---\nFinal:\n{table_array(result,'Final state')}")
        return result

class Node:
    def __init__(self, v):
        self.v = v
        self.left = None
        self.right = None

class TreeSorter:
    def __init__(self, items):
        self.items = items
        self.log = []
    def insert(self, root, v):
        if not root:
            return Node(v)
        if v < root.v:
            root.left = self.insert(root.left, v)
        else:
            root.right = self.insert(root.right, v)
        return root
    def inorder(self, r, out):
        if r:
            self.inorder(r.left, out)
            out.append(r.v)
            self.inorder(r.right, out)
    def to_list(self, root):
        q = [root]
        arr = []
        while q:
            n = q.pop(0)
            if n:
                arr.append(n.v)
                q.append(n.left)
                q.append(n.right)
            else:
                arr.append(None)
        return arr
    def sort(self):
        root = None
        for v in self.items:
            root = self.insert(root, v)
            arr = self.to_list(root)
            log_and_print(self.log, table_array(arr, f"Inserted {v}"))
            log_and_print(self.log, table_tree(arr))
        result = []
        self.inorder(root, result)
        log_and_print(self.log, f"--- COMPLETED ---\nFinal:\n{table_array(result,'Final state')}")
        return result

def main():
    while True:
        print("\nSORTING ALGORITHMS")
        print("1) Selection Sort")
        print("2) Heap Sort")
        print("3) Insertion Sort")
        print("4) Merge Sort")
        print("5) Quick Sort")
        print("6) Binary Tree Sort")
        print("again) Run again")
        print("exit) Quit")

        choice = input("Choose algorithm: ").strip().lower()
        if choice == "exit":
            print("Goodbye.")
            return
        if choice == "again":
            continue
        if choice not in {"1","2","3","4","5","6"}:
            print("Invalid choice.")
            continue

        raw = input("Enter values separated by spaces: ").split()
        data = parse_input(raw)

        asc = True
        if choice != "6":
            asc = input("Ascending? (y/n): ").lower().startswith("y")

        alg = {
            "1": ("Selection Sort", SelectionSorter(data, asc)),
            "2": ("Heap Sort", HeapSorter(data, asc)),
            "3": ("Insertion Sort", InsertionSorter(data, asc)),
            "4": ("Merge Sort", MergeSorter(data, asc)),
            "5": ("Quick Sort", QuickSorter(data, asc)),
            "6": ("Binary Tree Sort", TreeSorter(data)),
        }

        name, sorter = alg[choice]
        sorter.sort()
        saved = write_log(name, sorter.log)
        print("\nSaved to:", saved)
        print("\nType 'again' to sort another list, or 'exit' to quit.")

if __name__ == "__main__":
    main()
