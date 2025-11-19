import os

# ------------------ Utilities ------------------

def ensure_sorted_folder():
    folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Sorted")
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

def get_incremented_filename(folder, algorithm):
    count = 1
    while True:
        filename = os.path.join(folder, f"{algorithm} {count}.txt")
        if not os.path.exists(filename):
            return filename
        count += 1

def parse_input(raw):
    if all(x.lstrip("-").isdigit() for x in raw):
        return [int(x) for x in raw]
    return [x.upper() for x in raw]

def write_log(algorithm, log):
    folder = ensure_sorted_folder()
    filename = get_incremented_filename(folder, algorithm)
    with open(filename, "w") as f:
        f.write("\n".join(log))
    return filename

# ------------------ Selection Sort ------------------

class SelectionSorter:
    def __init__(self, items, ascending=True):
        self.items = items
        self.asc = ascending
        self.log = []

    def compare(self, a, b):
        return a < b if self.asc else a > b

    def sort(self):
        arr = self.items
        self.log.append(f"Start: {arr}")
        n = len(arr)

        for i in range(n):
            best = i
            for j in range(i + 1, n):
                if self.compare(arr[j], arr[best]):
                    best = j
            if best != i:
                self.log.append(f"Swap {arr[i]} and {arr[best]}")
                arr[i], arr[best] = arr[best], arr[i]
                self.log.append(f"Array: {arr}")

        self.log.append(f"Finished: {arr}")
        return arr

# ------------------ Heap Sort ------------------

class HeapSorter:
    def __init__(self, items, ascending=True):
        self.items = items
        self.asc = ascending
        self.log = []

    def compare(self, a, b):
        return a > b if self.asc else a < b

    def heapify(self, arr, n, i):
        largest = i
        L = 2 * i + 1
        R = 2 * i + 2

        if L < n and self.compare(arr[L], arr[largest]):
            largest = L
        if R < n and self.compare(arr[R], arr[largest]):
            largest = R

        if largest != i:
            self.log.append(f"Swap {arr[i]} and {arr[largest]}")
            arr[i], arr[largest] = arr[largest], arr[i]
            self.log.append(f"Array: {arr}")
            self.heapify(arr, n, largest)

    def sort(self):
        arr = self.items
        n = len(arr)
        self.log.append(f"Start: {arr}")

        for i in range(n // 2 - 1, -1, -1):
            self.heapify(arr, n, i)

        for i in range(n - 1, 0, -1):
            self.log.append(f"Swap {arr[0]} and {arr[i]}")
            arr[i], arr[0] = arr[0], arr[i]
            self.log.append(f"Array: {arr}")
            self.heapify(arr, i, 0)

        self.log.append(f"Finished: {arr}")
        return arr

# ------------------ Insertion Sort ------------------

class InsertionSorter:
    def __init__(self, items, ascending=True):
        self.items = items
        self.asc = ascending
        self.log = []

    def compare(self, a, b):
        return a < b if self.asc else a > b

    def sort(self):
        arr = self.items
        self.log.append(f"Start: {arr}")

        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and self.compare(key, arr[j]):
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
            self.log.append(f"Insert {key}: {arr}")

        self.log.append(f"Finished: {arr}")
        return arr

# ------------------ Merge Sort ------------------

class MergeSorter:
    def __init__(self, items, ascending=True):
        self.items = items
        self.asc = ascending
        self.log = []

    def compare(self, a, b):
        return a <= b if self.asc else a >= b

    def merge_sort(self, arr):
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        L = self.merge_sort(arr[:mid])
        R = self.merge_sort(arr[mid:])

        merged = []
        i = j = 0

        while i < len(L) and j < len(R):
            if self.compare(L[i], R[j]):
                merged.append(L[i])
                i += 1
            else:
                merged.append(R[j])
                j += 1

        merged.extend(L[i:])
        merged.extend(R[j:])
        self.log.append(f"Merge: {merged}")
        return merged

    def sort(self):
        self.log.append(f"Start: {self.items}")
        sorted_arr = self.merge_sort(self.items)
        self.log.append(f"Finished: {sorted_arr}")
        return sorted_arr

# ------------------ Quick Sort ------------------

class QuickSorter:
    def __init__(self, items, ascending=True):
        self.items = items
        self.asc = ascending
        self.log = []

    def compare(self, a, b):
        return a <= b if self.asc else a >= b

    def quick_sort(self, arr):
        if len(arr) <= 1:
            return arr

        pivot = arr[len(arr) // 2]
        left = [x for x in arr if self.compare(x, pivot) and x != pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if not self.compare(x, pivot)]

        self.log.append(f"Pivot {pivot}: L={left} M={middle} R={right}")

        return self.quick_sort(left) + middle + self.quick_sort(right)

    def sort(self):
        self.log.append(f"Start: {self.items}")
        sorted_arr = self.quick_sort(self.items)
        self.log.append(f"Finished: {sorted_arr}")
        return sorted_arr

# ------------------ Binary Tree Sort ------------------

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class TreeSorter:
    def __init__(self, items):
        self.items = items
        self.log = []

    def insert(self, root, value):
        if root is None:
            self.log.append(f"Insert {value}")
            return TreeNode(value)
        if value < root.value:
            root.left = self.insert(root.left, value)
        else:
            root.right = self.insert(root.right, value)
        return root

    def inorder(self, root, result):
        if root:
            self.inorder(root.left, result)
            result.append(root.value)
            self.inorder(root.right, result)

    def sort(self):
        root = None
        for val in self.items:
            root = self.insert(root, val)

        result = []
        self.inorder(root, result)
        self.log.append(f"Finished: {result}")
        return result

# ------------------ Main Program ------------------

def main():
    print("\nChoose sorting algorithm:")
    print("1) Selection Sort")
    print("2) Heap Sort")
    print("3) Insertion Sort")
    print("4) Merge Sort")
    print("5) Quick Sort")
    print("6) Binary Tree Sort")

    choice = input("Your choice: ")

    raw = input("Enter items separated by spaces: ").split()
    data = parse_input(raw)

    if choice != "6":
        asc = input("Sort ascending? (y/n): ").lower().startswith("y")
    else:
        asc = True

    algorithms = {
        "1": ("Selection Sort", SelectionSorter(data, asc)),
        "2": ("Heap Sort", HeapSorter(data, asc)),
        "3": ("Insertion Sort", InsertionSorter(data, asc)),
        "4": ("Merge Sort", MergeSorter(data, asc)),
        "5": ("Quick Sort", QuickSorter(data, asc)),
        "6": ("Binary Tree Sort", TreeSorter(data))
    }

    if choice not in algorithms:
        print("Invalid choice.")
        return

    name, sorter = algorithms[choice]

    result = sorter.sort()
    filename = write_log(name, sorter.log)

    print("\nSorted:", result)
    print(f"Steps saved to: {filename}")

if __name__ == "__main__":
    main()

