def load_data(filename):
    """
    Load and parse the component data from the input file.
    Returns a tuple of (components, sequences) where:
    - components is a list of component strings
    - sequences is a list of sequence strings
    """
    with open(filename, 'r') as f:
        # Split the file into two parts based on double newline
        parts = f.read().strip().split('\n\n')
        
        # Parse the components (first part)
        components = [comp.strip() for comp in parts[0].split(',')]
        
        # Parse the sequences (second part)
        sequences = [seq.strip() for seq in parts[1].splitlines()]
        
        return components, sequences

def can_make_sequence(components, sequence):
    """
    Determine if the given sequence can be made from the list of components.
    Uses list comprehension and dynamic programming for improved performance.
    
    Args:
        components: List of available component strings
        sequence: Target sequence to construct
        
    Returns:
        bool: True if sequence can be constructed, False otherwise
    """
    n = len(sequence)
    dp = [False] * (n + 1)
    dp[0] = True  # Empty sequence can always be made
    
    [dp.__setitem__(i + len(component), True)
     for i in range(n + 1) if dp[i]
     for component in components if sequence[i:].startswith(component)]
    
    return dp[n]

def count_combinations(components, sequence):
    """
    Count how many different combinations of components can make the given sequence.
    Uses list comprehension and dynamic programming for improved performance.
    
    Args:
        components: List of available component strings
        sequence: Target sequence to construct
        
    Returns:
        int: Number of different ways to construct the sequence
    """
    n = len(sequence)
    dp = [0] * (n + 1)
    dp[0] = 1  # Empty sequence can be made in one way
    
    [dp.__setitem__(i + len(component), dp[i + len(component)] + dp[i])
     for i in range(n + 1) if dp[i] > 0
     for component in components if sequence[i:].startswith(component)]
    
    return dp[n]

def count_possible_sequences(components, sequences):
    """
    Count how many sequences can be made from the given components.
    
    Args:
        components: List of available component strings
        sequences: List of sequences to check
        
    Returns:
        int: Number of sequences that can be made
    """
    return sum(1 for seq in sequences if can_make_sequence(components, seq))

def sum_all_combinations(components, sequences):
    """
    Calculate the sum of all possible combinations for all sequences.
    Uses list comprehension for improved performance.
    
    Args:
        components: List of available component strings
        sequences: List of sequences to analyze
        
    Returns:
        int: Sum of all possible combinations across all sequences
    """
    return sum(count_combinations(components, seq) for seq in sequences)

if __name__ == '__main__':
    # Test the function with the input file
    components, sequences = load_data('19.txt')
    print("Components:", components)
    print(f"Total number of components: {len(components)}")
    print(f"Total number of sequences: {len(sequences)}")
    
    # Count possible sequences
    possible_count = count_possible_sequences(components, sequences)
    print(f"\nNumber of possible sequences: {possible_count}")
    
    # Calculate total combinations
    print("\nCalculating total combinations for all sequences...")
    total_combinations = sum_all_combinations(components, sequences)
    print(f"\nTotal combinations across all sequences: {total_combinations}")
