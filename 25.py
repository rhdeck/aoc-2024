def load_specs(filename):
    """
    Load lock and key specifications from a file.
    Each spec is separated by double newlines.
    Returns a list of tuples (spec_type, counts) where:
    - spec_type is 'key' if first row is all metal (#), 'lock' if first row is all empty (.)
    - counts is a tuple of 5 numbers indicating metal count in each column
    """
    with open(filename) as f:
        content = f.read().strip()
    
    specs = []
    for spec in content.split('\n\n'):
        lines = spec.strip().split('\n')
        # Determine if it's a key (all . in first row) or lock (all # in first row)
        spec_type = 'lock' if all(c == '#' for c in lines[0]) else 'key'
        
        # Count metal pieces in each column
        counts = []
        for col in range(len(lines[0])):  # Assuming all rows have same length
            metal_count = sum(1 for row in lines if row[col] == '#')
            counts.append(metal_count)
        
        specs.append((spec_type, tuple(counts)))
    
    return specs

def find_matches(specs):
    """
    Compare all locks to all keys to find valid combinations.
    A combination is valid if the sum of values in each column is <= 7.
    Returns a list of tuples (lock_counts, key_counts) for valid combinations.
    """
    locks = [counts for spec_type, counts in specs if spec_type == 'lock']
    keys = [counts for spec_type, counts in specs if spec_type == 'key']
    
    matches = []
    for lock in locks:
        for key in keys:
            # Check if all columns satisfy the condition
            if all(lock[i] + key[i] <= 7 for i in range(5)):
                matches.append((lock, key))
    
    return matches

if __name__ == '__main__':
    import sys
    # Test the functions
    if(len(sys.argv) > 1):
        filename = sys.argv[1]
    else:
        filename = '25.txt'
    specs = load_specs(filename)
    print("Specifications:")
    for spec_type, counts in specs:
        print(f"{spec_type}: {counts}")
    
    print("\nMatching combinations:")
    matches = find_matches(specs)
    for lock, key in matches:
        print(f"Lock {lock} + Key {key}")
        print(f"Column sums: {tuple(l + k for l, k in zip(lock, key))}")
    print("Part 1:", len(matches))

