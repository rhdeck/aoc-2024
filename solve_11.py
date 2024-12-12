from collections import defaultdict, Counter

def handle_number(num, cache):
    if num in cache:
        return cache[num]
    
    if num == 0:
        return [1]
        
    s = str(num)
    l = len(s)
    if l % 2 == 0:
        result = [int(s[0:l//2]), int(s[l//2:])]
    else:
        result = [num * 2024]
    
    cache[num] = result
    return result

def solve(numbers, turns):
    cache = {}
    current_counts = Counter(numbers)
    
    for turn in range(turns):
        next_counts = Counter()
        for num, count in current_counts.items():
            for new_num in handle_number(num, cache):
                next_counts[new_num] += count
        current_counts = next_counts
        
    return sum(current_counts.values())

# Read input
with open('11.txt', 'r') as f:
    numbers = [int(x) for x in f.read().strip().split()]

result = solve(numbers, 75)
print(f"After 75 turns, there are {result} numbers")
