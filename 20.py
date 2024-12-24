from collections import deque

def load_grid(filename):
    """
    Load the maze grid from a file and identify start (S) and end (E) positions.
    Returns:
        tuple: (grid, start_pos, end_pos) where grid is a list of strings and positions are (row, col) tuples
    """
    with open(filename, 'r') as f:
        grid = [line.strip() for line in f]
    
    start_pos = None
    end_pos = None
    
    # Find S and E positions
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 'S':
                start_pos = (row, col)
            elif grid[row][col] == 'E':
                end_pos = (row, col)
    
    return grid, start_pos, end_pos

def walk_grid(grid, start_pos):
    """
    Walk the grid using BFS and count steps to each position.
    Returns a dictionary where key is (row,col) and value is steps from start.
    """
    steps = {start_pos: 0}  # Dictionary to store steps to each position
    queue = deque([(start_pos, 0)])  # Queue stores (position, steps)
    rows, cols = len(grid), len(grid[0])
    
    while queue:
        (row, col), current_steps = queue.popleft()
        
        # Check all four directions
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # right, down, left, up
            new_row, new_col = row + dr, col + dc
            
            # Check if the new position is valid and not visited
            if (0 <= new_row < rows and 
                0 <= new_col < cols and 
                grid[new_row][new_col] != '#' and 
                (new_row, new_col) not in steps):
                
                steps[(new_row, new_col)] = current_steps + 1
                queue.append(((new_row, new_col), current_steps + 1))
    
    return steps

def find_all_shortcuts(grid, steps_dict, position):
    """
    Evaluates positions around walls for potential shortcuts.
    Returns a list of tuples (direction, beyond_pos, difference) for all possible shortcuts.
    """
    row, col = position
    current_steps = steps_dict.get(position)
    if current_steps is None:
        return []
    
    rows, cols = len(grid), len(grid[0])
    shortcuts = []
    
    directions = {
        (0, 1): "right",
        (1, 0): "down",
        (0, -1): "left",
        (-1, 0): "up"
    }
    
    # Check all four directions
    for (dr, dc), direction in directions.items():
        # Position of adjacent cell
        wall_row, wall_col = row + dr, col + dc
        # Position on other side of wall
        beyond_row, beyond_col = row + 2*dr, col + 2*dc
        
        # Check if wall exists and the position beyond is valid
        if (0 <= wall_row < rows and 0 <= wall_col < cols and
            0 <= beyond_row < rows and 0 <= beyond_col < cols and
            grid[wall_row][wall_col] == '#'):  # Is there a wall?
            
            beyond_pos = (beyond_row, beyond_col)
            beyond_steps = steps_dict.get(beyond_pos)
            
            # If position beyond wall exists in steps_dict and has higher value
            if beyond_steps is not None and beyond_steps > current_steps:
                diff = beyond_steps - current_steps - 2
                shortcuts.append((direction, beyond_pos, diff))
    
    return shortcuts

def evaluate_wall_shortcuts(grid, steps_dict, position):
    """
    Evaluates positions around walls for potential shortcuts.
    Returns the maximum difference (minus 1) between current position's steps
    and any higher value position on the other side of adjacent walls.
    """
    row, col = position
    current_steps = steps_dict.get(position)
    if current_steps is None:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    max_diff = 0
    
    # Check all four directions
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # right, down, left, up
        # Position of adjacent cell
        wall_row, wall_col = row + dr, col + dc
        # Position on other side of wall
        beyond_row, beyond_col = row + 2*dr, col + 2*dc
        
        # Check if wall exists and the position beyond is valid
        if (0 <= wall_row < rows and 0 <= wall_col < cols and
            0 <= beyond_row < rows and 0 <= beyond_col < cols and
            grid[wall_row][wall_col] == '#'):  # Is there a wall?
            
            beyond_pos = (beyond_row, beyond_col)
            beyond_steps = steps_dict.get(beyond_pos)
            
            # If position beyond wall exists in steps_dict and has higher value
            if beyond_steps is not None and beyond_steps > current_steps:
                diff = beyond_steps - current_steps - 1
                max_diff = max(max_diff, diff)
    
    return max_diff

def find_potential_long_shortcuts(steps, max_length=20):
    """
    Find pairs of positions that could potentially be connected with a significant shortcut.
    Criteria:
    - Step difference must be at least 102
    - Manhattan distance must be no more than 20
    - Step difference must exceed Manhattan distance + 102
    Returns count of such pairs.
    """
    counter = 0
    positions = list(steps.items())
    
    for i, (pos1, steps1) in enumerate(positions):
        for pos2, steps2 in positions[i+1:]:
            if steps2 - steps1 >= 100:  # Only check if step difference is at least 102
                manhattan_dist = abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])
                if manhattan_dist <= max_length and steps2 - steps1 >= manhattan_dist + 100:
                    counter += 1
    
    return counter

def find_potential_shortcuts_alt(steps, max_length=20):
    """
    Alternative approach to finding potential shortcuts using list comprehensions.
    For each position i, look at all positions j where:
    - j's score is higher than i's
    - manhattan distance <= max_length
    - difference in scores >= 100 + manhattan distance
    Returns count of such pairs.
    """
    positions = list(steps.items())
    
    return sum(
        1
        for pos_i, score_i in positions
        for pos_j, score_j in positions
        if score_j > score_i
        and (manhattan_dist := abs(pos_j[0] - pos_i[0]) + abs(pos_j[1] - pos_i[1])) <= max_length
        and score_j - score_i >= manhattan_dist + 100
    )

# Test the functions
if __name__ == "__main__":
    import time

    grid, start, end = load_grid("20.txt")
    steps = walk_grid(grid, start)
    print("Steps from start to end:", steps[end])
    
    # Collect all shortcuts
    all_shortcuts = []
    for pos in steps.keys():
        shortcuts = find_all_shortcuts(grid, steps, pos)
        all_shortcuts.extend(shortcuts)
    
    # Count shortcuts by steps saved
    shortcut_counts = {}
    for _, _, diff in all_shortcuts:
        shortcut_counts[diff] = shortcut_counts.get(diff, 0) + 1
    
    # Print summary
    print("\nShortcut Summary:")
    print(f"Total number of possible shortcuts: {len(all_shortcuts)}")
    print("\nBreakdown by steps saved:")
    for steps_saved in sorted(shortcut_counts.keys()):
        print(f"Saves {steps_saved:2d} steps: {shortcut_counts[steps_saved]:2d} shortcuts")

    print("\nTotal number of shortcuts that save at least 100 steps:", 
          sum([shortcut_counts[pos] for pos in shortcut_counts.keys() if pos >= 100]))
    
    # Test short shortcuts
    print("\nTesting short shortcuts (max_length=2):")
    start_time = time.time()
    long_shortcuts = find_potential_long_shortcuts(steps, 2)
    end_time = time.time()
    print(f"Original method: {long_shortcuts} shortcuts found in {end_time - start_time:.4f} seconds")

    start_time = time.time()
    alt_shortcuts = find_potential_shortcuts_alt(steps, 2)
    end_time = time.time()
    print(f"Alternative method: {alt_shortcuts} shortcuts found in {end_time - start_time:.4f} seconds")

    # Test long shortcuts
    print("\nTesting long shortcuts (max_length=20):")
    start_time = time.time()
    long_shortcuts = find_potential_long_shortcuts(steps, 20)
    end_time = time.time()
    print(f"Original method: {long_shortcuts} shortcuts found in {end_time - start_time:.4f} seconds")

    start_time = time.time()
    alt_shortcuts = find_potential_shortcuts_alt(steps, 20)
    end_time = time.time()
    print(f"Alternative method: {alt_shortcuts} shortcuts found in {end_time - start_time:.4f} seconds")
