from collections import defaultdict
import heapq
from typing import List, Tuple, Dict, Set
from PIL import Image, ImageDraw

def create_grid_visualization(grid: List[List[str]], positions: Set[Tuple[int, int]], output_file: str):
    # Define colors
    COLORS = {
        '#': (50, 50, 50),      # Dark gray for walls
        '.': (200, 200, 200),   # Light gray for empty spaces
        'S': (0, 255, 0),       # Green for start
        'E': (255, 0, 0),       # Red for end
        '@': (0, 100, 255)      # Blue for path
    }
    
    CELL_SIZE = 20  # Size of each cell in pixels
    PADDING = 2     # Padding within each cell
    
    # Calculate image dimensions
    width = len(grid[0]) * CELL_SIZE
    height = len(grid) * CELL_SIZE
    
    # Create image with white background
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw grid
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            x1 = j * CELL_SIZE + PADDING
            y1 = i * CELL_SIZE + PADDING
            x2 = (j + 1) * CELL_SIZE - PADDING
            y2 = (i + 1) * CELL_SIZE - PADDING
            
            # Determine cell color
            if (i, j) in positions and grid[i][j] != '#':
                color = COLORS['@']
            else:
                color = COLORS[grid[i][j]]
            
            # Draw filled rectangle for cell
            draw.rectangle([x1, y1, x2, y2], fill=color)
    
    # Save image
    image.save(output_file)

def parse_grid(filename):
    with open(filename, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]

# Directions: 0=right, 1=down, 2=left, 3=up
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def find_start_end(grid: List[List[str]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    start = end = None
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'S':
                start = (i, j)
            elif grid[i][j] == 'E':
                end = (i, j)
    return start, end

def find_path(grid: List[List[str]]) -> Tuple[int, int, Set[Tuple[int, int]]]:
    start, end = find_start_end(grid)
    rows, cols = len(grid), len(grid[0])
    
    # Priority queue entries: (cost, (row, col, direction))
    pq = [(0, (start[0], start[1], 0))]  # Start facing right (direction 0)
    
    # Keep track of minimum cost to reach each state
    costs = defaultdict(lambda: float('inf'))
    costs[(start[0], start[1], 0)] = 0
    
    # Keep track of paths to each state
    paths = defaultdict(set)
    paths[(start[0], start[1], 0)].add((start[0], start[1]))
    
    min_cost_to_end = float('inf')
    optimal_paths_count = 0
    optimal_positions = set()
    
    while pq:
        cost, (row, col, direction) = heapq.heappop(pq)
        
        # If we've found a worse path, skip it
        if cost > costs[(row, col, direction)]:
            continue
            
        # If we've reached the end
        if (row, col) == end:
            if cost < min_cost_to_end:
                min_cost_to_end = cost
                optimal_paths_count = 1
                optimal_positions = paths[(row, col, direction)].copy()
            elif cost == min_cost_to_end:
                optimal_paths_count += 1
                optimal_positions.update(paths[(row, col, direction)])
            continue
            
        # If we've exceeded the best cost to end, skip
        if cost > min_cost_to_end:
            continue
            
        # Try all possible directions
        for new_direction in range(4):
            # Calculate turning cost
            turn_cost = 0
            if new_direction != direction:
                # Calculate number of 90-degree turns needed
                turns = min((new_direction - direction) % 4, (direction - new_direction) % 4)
                turn_cost = turns * 1000
            
            # Get new position
            dr, dc = DIRECTIONS[new_direction]
            new_row, new_col = row + dr, col + dc
            
            # Check if the new position is valid
            if (0 <= new_row < rows and 
                0 <= new_col < cols and 
                grid[new_row][new_col] != '#'):
                
                new_cost = cost + turn_cost + 1  # 1 point to move forward
                new_state = (new_row, new_col, new_direction)
                
                if new_cost <= costs[new_state]:
                    # If this is a new best path to this state
                    if new_cost < costs[new_state]:
                        paths[new_state] = set()
                    
                    # Add all positions from current path plus new position
                    new_path = paths[new_state]
                    new_path.update(paths[(row, col, direction)])
                    new_path.add((new_row, new_col))
                    
                    costs[new_state] = new_cost
                    heapq.heappush(pq, (new_cost, (new_row, new_col, new_direction)))
    
    return min_cost_to_end, optimal_paths_count, optimal_positions

# Test the pathfinding
if __name__ == "__main__":
    grid = parse_grid("16.txt")
    cost, paths, positions = find_path(grid)
    print(f"Lowest cost path: {cost} points")
    print(f"Number of optimal paths: {paths}")
    print(f"Number of unique positions covered by optimal paths: {len(positions)}")
    
    # Create visualization
    create_grid_visualization(grid, positions, "16.png")
    print("\nVisualization saved as '16.png'")
