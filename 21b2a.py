#Backup of working code that still has exponential complexity

from functools import lru_cache
import heapq
from multiprocessing import Pool
from typing import Tuple, Dict, List
from itertools import product
from collections import deque

@lru_cache(maxsize=None)
def find_path(current_pos, remaining_robots, visited=None):
    if visited is None:
        visited = frozenset()  # Use frozenset instead of list/set for hashability
    # ... rest of your pathfinding logic

def simulate_robot_chain_generalized(target_keys, length = 2):
    robot_positions = [(2,0)] * length  # All robots start at 'A' on small keypad
    large_robot_pos = (2, 3)  # starts at 'A' on large keypad
    pressed_keys = []
    
    # Convert target_keys to list if it's a string
    if isinstance(target_keys, str):
        target_keys = list(target_keys)
    
    # Find path to each target key
    for target in target_keys:
        found = False
        # Try all possible commands
        for cmd in ['^', 'v', '<', '>', 'A']:
            temp_positions = robot_positions.copy()
            temp_large_pos = large_robot_pos
            current_cmd = cmd
            
            # Pass command through robot chain
            for i in range(length):
                if current_cmd is None:
                    break
                temp_positions[i], current_cmd = simulate_single_robot_action(temp_positions[i], current_cmd, temp_large_pos)
            
            if current_cmd == 'A':
                final_key = get_large_key(temp_large_pos)
                if final_key == target:
                    pressed_keys.append(final_key)
                    robot_positions = temp_positions
                    large_robot_pos = temp_large_pos
                    found = True
                    break
            elif current_cmd in ['^', 'v', '<', '>']:
                temp_large_pos = move_on_large_keypad(temp_large_pos, current_cmd)
                large_robot_pos = temp_large_pos
                robot_positions = temp_positions
        
        if not found:
            return []  # Return empty list if we can't find a path to any target
    
    return pressed_keys


def simulate_single_robot_action(robot_pos, command, large_robot_pos):
    if command == 'A':
        # press the current key
        key = get_small_key(robot_pos)
        return robot_pos, key
    else:
        new_robot_pos = move_on_small_keypad(robot_pos, command)
        return new_robot_pos, None

def simulate_large_robot_action(robot_pos, command):
    return move_on_large_keypad(robot_pos, command)

def simulate_robot_chain(start_pos, commands):
    robot1_pos = start_pos  # on small keypad
    robot2_pos = (2, 0)    # starts at 'A' on small keypad
    robot3_pos = (2, 3)    # starts at 'A' on large keypad
    
    pressed_keys = []
    
    for cmd in commands:
        new_robot1_pos = move_on_small_keypad(robot1_pos, cmd)
        key1 = get_small_key(new_robot1_pos)
        
        if cmd == 'A':
            if key1 == 'A':
                key2 = get_small_key(robot2_pos)
                
                if key2 == 'A':
                    final_key = get_large_key(robot3_pos)
                    pressed_keys.append(final_key)
                elif key2 in ['^', 'v', '<', '>']:
                    robot3_pos = move_on_large_keypad(robot3_pos, key2)
            elif key1 in ['^', 'v', '<', '>']:
                new_robot2_pos = move_on_small_keypad(robot2_pos, key1)
                key2 = get_small_key(new_robot2_pos)
                if key2 == 'A':
                    final_key = get_large_key(robot3_pos)
                    pressed_keys.append(final_key)
                elif key2 in ['^', 'v', '<', '>']:
                    robot3_pos = move_on_large_keypad(robot3_pos, key2)
                robot2_pos = new_robot2_pos
        
        robot1_pos = new_robot1_pos
    
    return pressed_keys




def extract_digits(s: str) -> int:
    digits = ''.join(c for c in s if c.isdigit())
    return int(digits) if digits else 0


def test_on_file():
    with open("21.txt") as f:
        commands = f.read().strip().split('\n')
    scores = []
    for cmd in commands:
        length = find_shortest_sequence(cmd)
        numeric_part = extract_digits(cmd)
        score = length *  numeric_part
        print(f"Score for {cmd}: {length} * {numeric_part} = {score}")
        scores.append(score)
    print("Total score: ", sum(scores))


def find_shortest_sequence(target_keys, debug=False):
    from collections import deque
    import time
    
    start_time = time.time()
    
    start_state = ((2, 0), (2, 0), (2, 3), 0)  # (robot1_pos, robot2_pos, robot3_pos, keys_pressed)
    
    queue = deque([(start_state, [])])
    seen = {start_state}
    
    states_checked = 0
    max_states = 1000000  
    
    while queue and states_checked < max_states:
        state, commands = queue.popleft()
        robot1_pos, robot2_pos, robot3_pos, keys_pressed = state
        
        states_checked += 1
        if states_checked % 10000 == 0 and debug:
            print(f"Checked {states_checked} states, current sequence length: {len(commands)}, keys pressed: {keys_pressed}/{len(target_keys)}")
            print(f"Time elapsed: {time.time() - start_time:.2f}s")
            print(f"Queue size: {len(queue)}")
        
        if keys_pressed == len(target_keys):
            if debug:
                print(f"\nFound solution after checking {states_checked} states")
                print(f"Time taken: {time.time() - start_time:.2f}s")
                print("Solution commands:", ''.join(commands))
            return len(commands)
        
        for cmd in ['^', 'v', '<', '>', 'A']:
            new_robot1_pos, new_robot2_pos, new_robot3_pos, key_pressed = simulate_step(
                robot1_pos, robot2_pos, robot3_pos, cmd, debug and len(commands) < 5
            )
            
            if not (is_valid_small_pos(new_robot1_pos) and 
                   is_valid_small_pos(new_robot2_pos) and 
                   is_valid_large_pos(new_robot3_pos)):
                continue
            
            new_keys_pressed = keys_pressed
            if key_pressed is not None:
                if keys_pressed < len(target_keys) and key_pressed == target_keys[keys_pressed]:
                    new_keys_pressed += 1
                else:
                    continue
            
            new_state = (new_robot1_pos, new_robot2_pos, new_robot3_pos, new_keys_pressed)
            if new_state not in seen:
                seen.add(new_state)
                queue.append((new_state, commands + [cmd]))
    
    return -1


def is_valid_small_pos(pos):
    x, y = pos
    keypad = [
        ['#', '^', 'A'],
        ['<', 'v', '>']
    ]
    if x < 0 or x >= len(keypad[0]) or y < 0 or y >= len(keypad):
        return False
    return keypad[y][x] != '#'


def is_valid_large_pos(pos):
    x, y = pos
    keypad = [
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        ['#', '0', 'A']
    ]
    if x < 0 or x >= len(keypad[0]) or y < 0 or y >= len(keypad):
        return False
    return keypad[y][x] != '#'


def simulate_step(robot1_pos, robot2_pos, robot3_pos, cmd, debug=False):
    if debug:
        print(f"\nCommand: {cmd}")
    key_pressed = None
    new_robot1_pos = move_on_small_keypad(robot1_pos, cmd)
    new_robot2_pos = robot2_pos
    new_robot3_pos = robot3_pos
    key1 = get_small_key(new_robot1_pos)
    if cmd == 'A': 
        if key1 == 'A':
            new_robot2_pos = robot2_pos
            key2 = get_small_key(new_robot2_pos)
            if key2 == 'A':
                new_robot3_pos = robot3_pos
                key_pressed = get_large_key(new_robot3_pos)
            else:
                new_robot3_pos = move_on_large_keypad(robot3_pos, key2)
                key_pressed = None
        else:
            new_robot2_pos = move_on_small_keypad(robot2_pos, key1)
            key_pressed = None
            new_robot3_pos = robot3_pos
    
    if debug:
        print(f"Robot1: {robot1_pos} -> {new_robot1_pos} (key: {get_small_key(new_robot1_pos)})")
        print(f"Robot2: {robot2_pos} -> {new_robot2_pos} (key: {get_small_key(new_robot2_pos)})")
        print(f"Robot3: {robot3_pos} -> {new_robot3_pos} (key: {get_large_key(new_robot3_pos)})")
        if key_pressed is not None:
            print(f"Key pressed: {key_pressed}")
    
    return new_robot1_pos, new_robot2_pos, new_robot3_pos, key_pressed

small_keypad =  [
        ['#', '^', 'A'],
        ['<', 'v', '>']
    ]
def move_on_small_keypad(position, command):
    x, y = position
    
    # Define keypad layout
   
    
    # Calculate new position based on command
    new_x, new_y = x, y
    if command == '^':
        new_y = y - 1
    elif command == 'v':
        new_y = y + 1
    elif command == '<':
        new_x = x - 1
    elif command == '>':
        new_x = x + 1
    
    if new_x < 0 or new_x >= len(small_keypad[0]) or new_y < 0 or new_y >= len(small_keypad):
        return (None, None)
    
    # Check if new position is valid (not '#')
    if small_keypad[new_y][new_x] == '#':
        return (None, None)  # Return original position if move is invalid
        # return (x, y)  # Return original position if move is invalid
    
    return (new_x, new_y)

def get_small_key(position):
    return small_keypad[position[1]][position[0]]

large_keypad = [
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        ['#', '0', 'A']
    ]
def move_on_large_keypad(position, command):
    x, y = position
    
    # Calculate new position based on command
    new_x, new_y = x, y
    if command == '^':
        new_y = y - 1
    elif command == 'v':
        new_y = y + 1
    elif command == '<':
        new_x = x - 1
    elif command == '>':
        new_x =  x + 1
    
    if new_x < 0 or new_x >= len(large_keypad[0]) or new_y < 0 or new_y >= len(large_keypad):
        return (None, None)
    
    # Check if new position is valid (not '#')
    if large_keypad[new_y][new_x] == '#':
        return (None, None)
        # return (x, y)  # Return original position if move is invalid
    
    return (new_x, new_y)

def get_large_key(position):
    return large_keypad[position[1]][position[0]]

def test_generalized():
    with open("21.test.txt") as f:
        commands = f.read().strip().split('\n')
    
    scores = []
    for cmd in commands:
        # Try different chain lengths to find the shortest solution
        min_length = float('inf')
        best_chain_length = 0
        
        for chain_length in range(1, 4):  # Test chains of length 1-3
            result = simulate_robot_chain_generalized(cmd, chain_length)
            # Convert result to list of strings for comparison
            result_str = [str(x) for x in result]
            if result_str == list(cmd):  # If we found a valid solution
                min_length = len(cmd)
                best_chain_length = chain_length
                break
        
        if min_length == float('inf'):
            print(f"No solution found for {cmd}")
            continue
            
        numeric_part = extract_digits(cmd)
        score = min_length * numeric_part
        print(f"Score for {cmd}: {min_length} * {numeric_part} = {score} (chain length: {best_chain_length})")
        scores.append(score)
    
    print("Total score: ", sum(scores))

def visualize_keypads(robot_positions, large_robot_pos):
    small_keypad = [
        ['#', '^', 'A'],
        ['<', 'v', '>']
    ]
    large_keypad = [
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        ['#', '0', 'A']
    ]
    
    # Create visualization strings
    output = []
    output.append("Small Keypads (Robots):")
    
    # Show each robot's position on a small keypad
    for i, pos in enumerate(robot_positions):
        pad_str = []
        for y in range(len(small_keypad)):
            row = ""
            for x in range(len(small_keypad[y])):
                if (x, y) == pos:
                    row += f"[{small_keypad[y][x]}]"
                else:
                    row += f" {small_keypad[y][x]} "
            pad_str.append(row)
        output.extend([f"Robot {i+1}:"] + pad_str)
        output.append("")
    
    # Show large keypad
    output.append("Large Keypad:")
    for y in range(len(large_keypad)):
        row = ""
        for x in range(len(large_keypad[y])):
            if (x, y) == large_robot_pos:
                row += f"[{large_keypad[y][x]}]"
            else:
                row += f" {large_keypad[y][x]} "
        output.append(row)
    
    return "\n".join(output)

def interactive_simulator(chain_length=2, instructions=None):
    import curses
    import time
    instruction_length = 0 if instructions is None else len(instructions)
    if instructions is not None : instructions = deque(instructions)
    pressed_commands = []
    def main(stdscr):
        # Set up curses
        curses.curs_set(0)  # Hide cursor
        stdscr.clear()
        
        # Initialize robot positions
        robot_positions = [(2,0)] * chain_length
        large_robot_pos = (2, 3)
        pressed_keys = []
        
        # Key mappings
        key_map = {
            curses.KEY_UP: '^',
            curses.KEY_DOWN: 'v',
            curses.KEY_LEFT: '<',
            curses.KEY_RIGHT: '>',
            ord('a'): 'A'
        }
        
        while True:
            # Clear screen
            stdscr.clear()
            
            # Show current state
            viz = visualize_keypads(robot_positions, large_robot_pos)
            for i, line in enumerate(viz.split('\n')):
                stdscr.addstr(i, 0, line)
            
            # Show pressed keys
            stdscr.addstr(i+2, 0, f"Pressed keys: {' '.join(pressed_keys)}")
            stdscr.addstr(i+3, 0, "Use arrow keys to move, 'a' to press, 'q' to quit")
            stdscr.addstr(i+4, 0, f"Pressed commands: {''.join(pressed_commands[-120:])} ({len(pressed_commands)})")
            interactive_mode = False
            # Get input
            if instructions is not None and len(instructions) > 0:
                # time.sleep(0.2)
                cmd = instructions.popleft()
            else:
                interactive_mode = True
                while True:
                    key = stdscr.getch()
                    if key == ord('q'):
                        return
                    if key in key_map:
                        cmd = key_map[key]
                        break
            current_cmd = cmd
            pressed_commands.append(current_cmd)
            temp_positions = robot_positions.copy()
            temp_large_pos = large_robot_pos
            is_break = False
            # Simulate command through chain
            for i in range(chain_length):
                if current_cmd is None:
                    break
                old_cmd = current_cmd
                temp, current_cmd = simulate_single_robot_action(temp_positions[i], current_cmd, temp_large_pos)
                if temp[0] is None:
                    time.sleep(0.1)
                    stdscr.addstr(i+5, 0, "Invalid move: " + old_cmd + " - aborting")
                    stdscr.refresh()
                    time.sleep(10)
                    is_break = True
                    break
                else:
                    temp_positions[i] = temp
            if is_break:
                break
            if current_cmd == 'A':
                final_key = get_large_key(temp_large_pos)
                pressed_keys.append(final_key)
            elif current_cmd in ['^', 'v', '<', '>']:
                temp = move_on_large_keypad(temp_large_pos, current_cmd)
                if(temp[0] is None):
                    print(i+5, 0, "Invalid move - aborting")
                    time.sleep(0.1)
                    break
                else:
                    temp_large_pos = temp
                    
            
            robot_positions = temp_positions
            large_robot_pos = temp_large_pos
            
            if interactive_mode: time.sleep(0.1)  # Small delay to make visualization smoother
            else: 
                stdscr.refresh()
                time.sleep(max(0.02, 5/instruction_length))
    curses.wrapper(main)

def find_path_to_single_key(start_state, target_key, transition_table):
    """
    BFS to find path to press a single target key, starting from a given state.
    Returns (path, final_state) if found, or (None, None) if no path exists.
    """
    from collections import deque
    
    chain_positions, large_pos = start_state
    initial_state = (chain_positions, large_pos, False)  # False = key not yet pressed
    
    queue = deque([(initial_state, [])])  # (state, path)
    seen = {initial_state}
    
    while queue:
        state, path = queue.popleft()
        chain_positions, large_pos, key_pressed = state
        
        # Success condition: we've pressed the target key
        if key_pressed:
            return path, (chain_positions, large_pos)
        
        # Try each possible command
        for cmd in ['^', 'v', '<', '>', 'A']:
            # Use transition table to get new chain positions and final command
            new_positions, final_cmd = transition_table[(chain_positions, cmd)]
            new_large_pos = large_pos
            new_key_pressed = key_pressed
            
            # Handle the final command's effect
            if final_cmd == 'A':
                # Check if pressing the key matches our target
                pressed_key = get_large_key(large_pos)
                if pressed_key == target_key:
                    new_key_pressed = True
                else:
                    # Wrong key would be pressed - skip this branch
                    continue
            elif final_cmd in ['^', 'v', '<', '>']:
                new_large_pos = move_on_large_keypad(large_pos, final_cmd)
            
            new_state = (new_positions, new_large_pos, new_key_pressed)
            if new_state not in seen:
                seen.add(new_state)
                queue.append((new_state, path + [cmd]))
    
    return None, None  # No solution found

def find_path_to_sequence_incremental(target_sequence, chain_length=2):
    """
    Find path to sequence by solving for each key individually.
    """
    # Build transition table first
    transition_table = build_transition_table(chain_length)
    
    # Initial state
    current_state = (tuple([(2,0)] * chain_length), (2,3))  # (chain_positions, large_pos)
    full_path = []
    
    # Find path to each key in sequence
    for target_key in target_sequence:
        path_segment, new_state = find_path_to_single_key(
            current_state, 
            target_key, 
            transition_table
        )
        
        if path_segment is None:
            return None  # No solution possible
        
        full_path.extend(path_segment)
        current_state = new_state
    
    return full_path

def test_path_finder(chain_length=8):
    import time
    start_time = time.time()
    
    print(f"Building transition table for chain length {chain_length}...")
    table_start = time.time()
    # transition_table = build_transition_table(chain_length)
    # table_time = time.time() - table_start
    # print(f"Transition table built in {table_time:.2f} seconds")
    # print(f"Transition table size: {len(transition_table)} entries")
    
    with open("21.txt") as f:
        commands = f.read().strip().split('\n')

    test_sequences = commands
    scores = []
    
    for i, seq in enumerate(test_sequences, 1):
        sequence_start = time.time()
        print(f"\nFinding path for sequence: {seq} ({i}/{len(test_sequences)})")
        
        path = find_path_to_sequence_incremental(seq, chain_length)
        len_path = len(path) if path else 0
        sequence_time = time.time() - sequence_start
        
        if path:
            print(f"Length: {len_path}")
            score = len_path * extract_digits(seq)
            print(f"Score: {score} from {len_path} * {extract_digits(seq)}")
            print(f"Time taken: {sequence_time:.2f} seconds")
            scores.append(score)
        else:
            print(f"No solution found for command {seq} with chain length {chain_length}")
            print(f"Time taken: {sequence_time:.2f} seconds")

    total_time = time.time() - start_time
    print("\nExecution Summary:")
    print(f"Total score: {sum(scores)}")
    print(f"Total execution time: {total_time:.2f} seconds")
    print(f"Average time per sequence: {total_time/len(test_sequences):.2f} seconds")

# Optional: Add a cache decorator to the transition table builder
@lru_cache(maxsize=1)
def build_transition_table(chain_length: int) -> Dict[Tuple, Tuple]:
    """
    Precompute all possible transitions for a robot chain of given length.
    Returns a dictionary mapping (positions, command) to (new_positions, final_command)
    """
    print(f"Building transition table for chain length {chain_length}...")
    
    transitions = {}
    valid_positions = [
        (x, y) for y in range(2) for x in range(3) 
        if small_keypad[y][x] != '#'
    ]
    
    # For each possible combination of positions and command
    for positions in product(valid_positions, repeat=chain_length):
        positions = tuple(positions)  # Make it hashable
        for cmd in ['^', 'v', '<', '>', 'A']:
            current_cmd = cmd
            new_positions = list(positions)
            
            # Simulate the chain
            for i in range(chain_length):
                if current_cmd is None:
                    break
                new_positions[i], current_cmd = simulate_single_robot_action(
                    new_positions[i], current_cmd, None
                )
            
            # Store the transition
            transitions[(positions, cmd)] = (tuple(new_positions), current_cmd)
    
    print(f"Transition table built with {len(transitions)} entries")
    return transitions

def bidirectional_search(start, end, robots):
    forward_queue = [(start, set([start]))]
    backward_queue = [(end, set([end]))]
    forward_visited = {start: 0}
    backward_visited = {end: 0}
    
    while forward_queue and backward_queue:
        # Expand forward
        current, visited = forward_queue.pop(0)
        # ... process forward
        
        # Expand backward
        current, visited = backward_queue.pop(0)
        # ... process backward
        
        # Check for intersection
        common = set(forward_visited.keys()) & set(backward_visited.keys())
        if common:
            return min(forward_visited[x] + backward_visited[x] for x in common)

def heuristic(pos, remaining_robots):
    # Manhattan distance to nearest robot plus minimum spanning tree estimate
    distances = [manhattan_distance(pos, robot) for robot in remaining_robots]
    return min(distances) if distances else 0

def a_star_search(start, robots):
    open_set = [(0, start, frozenset(robots))]
    g_score = {(start, frozenset(robots)): 0}
    
    while open_set:
        f_score, current, remaining = heapq.heappop(open_set)
        if not remaining:  # All robots visited
            return g_score[(current, remaining)]

def compress_state(pos, remaining_robots):
    # Convert position and robots to a more compact representation
    # For example, using relative positions or bit manipulation
    x, y = pos
    state = (x << 16) | y  # Combine coordinates into single integer
    robot_bits = sum(1 << i for i, robot in enumerate(remaining_robots))
    return (state, robot_bits)

def parallel_search(start, robots, num_processes=4):
    with Pool(num_processes) as pool:
        # Split the search space into chunks
        initial_states = generate_initial_states(start, robots)
        results = pool.map(search_worker, initial_states)
    return min(results)

def find_robot_input_sequence(target_commands, debug=False):
    """
    Find sequence of commands for one robot to make another robot produce target_commands.
    
    Args:
        target_commands: List[str] - sequence of commands to be produced ('^', 'v', '<', '>', 'A')
        debug: bool - whether to print debug information
    
    Returns:
        List[str] - sequence of commands for the first robot, or None if impossible
    """
    from collections import deque
    
    # Initial state: (robot1_pos, robot2_pos, commands_produced)
    initial_state = ((2, 0), (2, 0), ())  # Both robots start at 'A'
    queue = deque([(initial_state, [])])  # (state, path)
    seen = {initial_state}
    
    target_commands = tuple(target_commands)  # Make hashable
    
    while queue:
        state, path = queue.popleft()
        robot1_pos, robot2_pos, commands_produced = state
        
        if debug:
            print(f"\nChecking state:")
            print(f"Robot1: {robot1_pos} ({get_small_key(robot1_pos)})")
            print(f"Robot2: {robot2_pos} ({get_small_key(robot2_pos)})")
            print(f"Commands produced: {commands_produced}")
            print(f"Path so far: {path}")
        
        # Success condition: we've produced all target commands
        if commands_produced == target_commands:
            return path
        
        # Get index of next command we need to produce
        next_cmd_index = len(commands_produced)
        if next_cmd_index >= len(target_commands):
            continue
        
        # Try each possible command for robot1
        for cmd in ['^', 'v', '<', '>', 'A']:
            # Move robot1 according to command
            new_robot1_pos = move_on_small_keypad(robot1_pos, cmd)
            new_commands = list(commands_produced)
            new_robot2_pos = robot2_pos
            
            if cmd == 'A':
                # When robot1 presses 'A', it triggers robot2 with whatever key robot1 is on
                key1 = get_small_key(robot1_pos)
                if key1 in ['^', 'v', '<', '>', 'A']:
                    if key1 == target_commands[next_cmd_index]:
                        new_commands.append(key1)
                    else:
                        # Wrong command would be produced - skip this branch
                        continue
            
            new_state = (new_robot1_pos, new_robot2_pos, tuple(new_commands))
            if new_state not in seen:
                seen.add(new_state)
                queue.append((new_state, path + [cmd]))
    
    return None  # No solution found

def test_robot_input_sequence():
    """Test cases for find_robot_input_sequence"""
    test_cases = [
        ['A'],  # Simple case: just press A
        ['^'],  # Move up
        ['v'],  # Move down
        ['<'],  # Move left
        ['>'],  # Move right
        ['^', 'A'],  # More complex sequences
        ['>', '<'],
        ['A', '>', 'A'],
    ]
    
    for test_case in test_cases:
        print(f"\nFinding sequence for target commands: {test_case}")
        result = find_robot_input_sequence(test_case, debug=False)
        if result:
            print(f"Solution found: {result}")
            # Verify the solution
            print("Verifying solution...")
            robot1_pos = (2, 0)
            robot2_pos = (2, 0)
            commands_produced = []
            
            for cmd in result:
                robot1_pos = move_on_small_keypad(robot1_pos, cmd)
                if cmd == 'A':
                    key1 = get_small_key(robot1_pos)
                    if key1 in ['^', 'v', '<', '>', 'A']:
                        commands_produced.append(key1)
            
            if commands_produced == test_case:
                print("✓ Solution verified correct")
            else:
                print("✗ Solution verification failed!")
                print(f"Expected: {test_case}")
                print(f"Got: {commands_produced}")
        else:
            print("No solution found!")

small_keypad_transitions = {
    ('^', '>'): ['v', '>', 'A'],#
    ('^', '<'): ['v', '<', 'A'],#
    ('^', 'v'): [ 'v', 'A'],#
    ('^', 'A'): ['>', 'A'],
    ('^', '^'): [ 'A'],#
    ('v', '>'): ['>', 'A'],#
    ('v', '<'): ['<', 'A'],#
    ('v', 'v'): [ 'A'],#
    ('v', 'A'): ['^', '>','A'],#
    ('v', '^'): [ '^','A'],#
    ('<', '>'): ['>', '>', 'A'],
    ('<', '<'): [ 'A'],
    ('<', 'v'): ['>', 'A'],
    ('<', 'A'): ['>','>' , '^', 'A'],
    ('<', '^'): [ '>', '^', 'A'],
    ('>', '>'): [ 'A'],#
    ('>', '<'): [ '<', '<', 'A'],
    ('>', 'v'): ['<', 'A'],
    ('>', 'A'): ['^', 'A'],
    ('>', '^'): [ '<', '^', 'A'],
    ('A', '>'): ['v', 'A'],
    ('A', '<'): ['v', '<', '<', 'A'],
    ('A', 'v'): ['v', '<', 'A'],
    ('A', 'A'): [ 'A'],#
    ('A', '^'): ['<', 'A'],#

}

large_keypad_transitions = {
    # From 0
    ('0', '1'): ['^',  '<'],
    ('0', '2'): ['^'],
    ('0', '3'): ['^', '>'],
    ('0', '4'): ['^', '^', '<'],
    ('0', '5'): ['^', '^'],
    ('0', '6'): ['^', '^', '>'],
    ('0', '7'): ['^', '^', '^', '<'],
    ('0', '8'): ['^', '^', '^'],
    ('0', '9'): ['^', '^', '^', '>'],
    ('0', 'A'): ['>'],
    ('0', '0'): [],

    # From 1
    ('1', '0'): ['>', 'v'],
    ('1', '2'): ['>'],
    ('1', '3'): ['>', '>'],
    ('1', '4'): ['^'],
    ('1', '5'): ['^', '>'],
    ('1', '6'): ['^', '>', '>'],
    ('1', '7'): ['^', '^'],
    ('1', '8'): ['^', '^', '>'],
    ('1', '9'): ['^', '^', '>', '>'],
    ('1', 'A'): ['>', '>', 'v'],
    ('1', '1'): [],

    # From 2
    ('2', '0'): ['v'],
    ('2', '1'): ['<'],
    ('2', '3'): ['>'],
    ('2', '4'): ['^', '<'],
    ('2', '5'): ['^'],
    ('2', '6'): ['^', '>'],
    ('2', '7'): ['^', '^', '<'],
    ('2', '8'): ['^', '^'],
    ('2', '9'): ['^', '^', '>'],
    ('2', 'A'): ['v', '>'],
    ('2', '2'): [],
    # From 3
    ('3', '0'): ['v', '<'],
    ('3', '1'): ['<', '<'],
    ('3', '2'): ['<'],
    ('3', '4'): ['^', '<', '<'],
    ('3', '5'): ['^', '<'],
    ('3', '6'): ['^'],
    ('3', '7'): ['^', '^', '<', '<'],
    ('3', '8'): ['^', '^', '<'],
    ('3', '9'): ['^', '^'],
    ('3', 'A'): ['v'],
    ('3', '3'): [],
    # From 4
    ('4', '0'): ['v', '>'],
    ('4', '1'): ['v'],
    ('4', '2'): ['v', '>'],
    ('4', '3'): ['v', '>', '>'],
    ('4', '5'): ['>'],
    ('4', '6'): ['>', '>'],
    ('4', '7'): ['^'],
    ('4', '8'): ['^', '>'],
    ('4', '9'): ['^', '>', '>'],
    ('4', 'A'): [ '>', '>','v', 'v',],
    ('4', '4'): [],

    # From 5
    ('5', '0'): ['v', 'v'],
    ('5', '1'): ['v', '<'],
    ('5', '2'): ['v'],
    ('5', '3'): ['v', '>'],
    ('5', '4'): ['<'],
    ('5', '6'): ['>'],
    ('5', '7'): ['^', '<'],
    ('5', '8'): ['^'],
    ('5', '9'): ['^', '>'],
    ('5', 'A'): ['v', 'v', '>'],
    ('5', '5'): [],

    # From 6
    ('6', '0'): ['v', 'v', '<'],
    ('6', '1'): ['v', '<', '<'],
    ('6', '2'): ['v', '<'],
    ('6', '3'): ['v'],
    ('6', '4'): ['<', '<'],
    ('6', '5'): ['<'],
    ('6', '7'): ['^', '<', '<'],
    ('6', '8'): ['^', '<'],
    ('6', '9'): ['^'],
    ('6', 'A'): ['v', 'v'],
    ('6', '6'): [],

    # From 7
    ('7', '0'): ['>','v', 'v', 'v'],
    ('7', '1'): ['v', 'v'],
    ('7', '2'): ['v', 'v', '>'],
    ('7', '3'): ['v', 'v', '>', '>'],
    ('7', '4'): ['v'],
    ('7', '5'): ['v', '>'],
    ('7', '6'): ['v', '>', '>'],
    ('7', '8'): ['>'],
    ('7', '9'): ['>', '>'],
    ('7', 'A'): [ '>', '>', 'v', 'v', 'v'],
    ('7', '7'): [],

    # From 8
    ('8', '0'): ['v', 'v', 'v'],
    ('8', '1'): ['v', 'v', '<'],
    ('8', '2'): ['v', 'v'],
    ('8', '3'): ['v', 'v', '>'],
    ('8', '4'): ['v', '<'],
    ('8', '5'): ['v'],
    ('8', '6'): ['v', '>'],
    ('8', '7'): ['<'],
    ('8', '9'): ['>'],
    ('8', 'A'): ['v', 'v', 'v', '>'],

    # From 9
    ('9', '0'): ['v', 'v', 'v', '<'],
    ('9', '1'): ['v', 'v', '<', '<'],
    ('9', '2'): ['v', 'v', '<'],
    ('9', '3'): ['v', 'v'],
    ('9', '4'): ['v', '<', '<'],
    ('9', '5'): ['v', '<'],
    ('9', '6'): ['v'],
    ('9', '7'): ['<', '<'],
    ('9', '8'): ['<'],
    ('9', 'A'): ['v', 'v', 'v'],

    # From A
    ('A', '0'): ['<'],
    ('A', '1'): ['^', '<', '<'],
    ('A', '2'): ['^', '<'],
    ('A', '3'): ['^'],
    ('A', '4'): ['^', '^', '<', '<'],
    ('A', '5'): ['^', '^', '<'],
    ('A', '6'): ['^', '^'],
    ('A', '7'): ['^', '^', '^', '<', '<'],
    ('A', '8'): ['^', '^', '^', '<'],
    ('A', '9'): ['^', '^', '^']
}

def build_small_keypad_transitions() -> Dict[Tuple[str, str], List[str]]:
    """
    Builds a dictionary mapping (start_key, end_key) to the shortest sequence of commands
    needed to move from start_key to end_key on the small keypad.
    
    Returns:
        Dict[Tuple[str, str], List[str]]: Dictionary mapping (start_key, end_key) pairs 
        to list of commands ('^', 'v', '<', '>')
    """
    return small_keypad_transitions
    # First, build a mapping of keys to their positions
    key_positions = {}
    for y in range(len(small_keypad)):
        for x in range(len(small_keypad[y])):
            if small_keypad[y][x] != '#':
                key_positions[small_keypad[y][x]] = (x, y)
    
    # Build transitions dictionary using BFS for each start/end pair
    transitions = {}
    valid_keys = ['^', 'v', '<', '>', 'A']
    
    for start_key in valid_keys:
        for end_key in valid_keys:
            if start_key == end_key:
                transitions[(start_key, end_key)] = []
                continue
                
            start_pos = key_positions[start_key]
            end_pos = key_positions[end_key]
            
            # BFS to find shortest path
            queue = deque([(start_pos, [])])
            visited = {start_pos}
            
            while queue:
                pos, path = queue.popleft()
                
                if pos == end_pos:
                    transitions[(start_key, end_key)] = path
                    break
                
                # Try each direction
                for cmd, (dx, dy) in [
                    ('^', (0, -1)),
                    ('v', (0, 1)),
                    ('<', (-1, 0)),
                    ('>', (1, 0))
                ]:
                    new_x = pos[0] + dx
                    new_y = pos[1] + dy
                    new_pos = (new_x, new_y)
                    
                    if (0 <= new_y < len(small_keypad) and 
                        0 <= new_x < len(small_keypad[0]) and
                        small_keypad[new_y][new_x] != '#' and
                        new_pos not in visited):
                        visited.add(new_pos)
                        queue.append((new_pos, path + [cmd]))
    
    return transitions

# Test the function
def test_small_keypad_transitions():
    transitions = build_small_keypad_transitions()
    
    # Test some specific cases
    test_cases = [
        ('^', '>'),
        ('A', '<'),
        ('v', '^'),
        ('>', '<'),
        ('A', 'A'),
    ]
    
    print("Small keypad transitions:")
    for start_key, end_key in test_cases:
        path = transitions[(start_key, end_key)]
        print(f"{start_key} -> {end_key}: {path}")
def simulate_run(commands, chain_length):
    sequence = [] # collect the digits pressed on the large keypad
    positions = [(2,0)] * chain_length
    large_position = (2,3)
    # lastCommand = ''
    for command in commands:
        # print("command", command)
        for i in range(chain_length):
            if(command == 'A'):
                command = get_small_key(positions[i])
            else:
                positions[i] = move_on_small_keypad(positions[i], command)
                # print('.', end='')
                command = ''
                break
            # lastCommand = command
        if command == 'A':
            # print("")
            # print("A pressed")
            # print(large_position)
            # print(get_large_key(large_position))
            sequence.append(get_large_key(large_position))
        elif command != '':
            large_position = move_on_large_keypad(large_position, command)
    return ''.join(sequence)


    previous = 'A'
    for letter in list(commands):
        adders = large_keypad_transitions[previous, letter]
        path.extend(adders)
        path.append('A')
        previous = letter
    return path


if __name__ == "__main__":
    import sys
    # Get chain length from command line argument, default to 8 if not provided
    chain_length = 8
    if len(sys.argv) > 1:
        try:
            chain_length = int(sys.argv[1])
        except ValueError:
            print("Error: Chain length must be an integer")
            sys.exit(1)
    commands = None
    if len(sys.argv) > 2:
        try:
            commands = sys.argv[2]
        except ValueError:
            print("Error: Test sequence must be a string")
            sys.exit(1)
    if True: #commands != None:
        interactive_simulator(chain_length, commands)
    else:
        # Choose which test to run
        test_type = "path_finder"  # or "path_finder"
        
        # if test_type == "fgfg":
        #     test_path_finder(chain_length)
        # else:
        #     # Build transition table first
        #     print("Building transition table...")
        #     transition_table = build_transition_table(2)  # Build for initial chain length of 2
            
        #     seq = "386A"
        #     print(f"Finding path for sequence: {seq}")
        #     path = find_path_to_sequence_incremental(seq, 2)
        #     if path:
        #         print(f"Initial path found, length: {len(path)}")
        #         for i in range(3, chain_length+1,1):
        #             path = find_robot_input_sequence(path)
        #             print(f"Path length at {i} is {len(path) if path else 'No solution'}")
        #         print(f"Final path: {path}")
        #         print(f"Final length: {len(path) if path else 'N/A'}")
        #     else:
        #         print("No initial path found")

        # print("\nTesting small keypad transitions:")
        # test_small_keypad_transitions()
        transitions = build_small_keypad_transitions()
        for key in transitions:
            print(key, transitions[key])
        with open("21.txt", "r") as f:
            sequences = [line.strip() for line in f.readlines()]
        scores = []
        for sequence in sequences:
            # sequence = "386A"

            path = []
            previous = 'A'
            for letter in list(sequence):
                adders = large_keypad_transitions[previous, letter]
                path.extend(adders)
                path.append('A')
                previous = letter
            print("original path for ", sequence)
            print(''.join(path))
            for i in range(1, chain_length+1,1):
                previous = 'A'
                newpath = []
                for j in range(len(path)):
                    adders = transitions[(previous, path[j])]
                    # print("Adding adders for", previous, path[j], ''.join(adders))
                    newpath.extend(adders)
                    # newpath.append('A')
                    previous = path[j]
                path = newpath
                # path = find_robot_input_sequence(path)
                # print(i, end=".")
                # print(''.join(path))
                # print("Path length at ", i, " is ", len(path))
            print("Final path for ", sequence)
            print(''.join(path))
            print("Path length at ", chain_length, " is ", len(path))
            digits = extract_digits(sequence)
            # print(digits)
            # print(len(path))
            score = len(path) * digits
            print("Score at ", chain_length, "for", sequence, " is ", score, " from ", len(path), " * ", digits)
            print("reconstructed command is", simulate_run(path, chain_length))
            scores.append(score)
            print("--------------------------------")
            # break
        print("Total score is ", sum(scores))

