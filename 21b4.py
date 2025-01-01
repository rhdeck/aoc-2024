import sys
import datetime


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

small_keypad_transitions_no_A = {
    ('^', '>'): ['>', 'v'],
    ('^', '<'): ['v', '<'],
    ('^', 'v'): ['v'],
    ('^', 'A'): ['>'],
    ('^', '^'): [],
    ('v', '>'): ['>'],
    ('v', '<'): ['<'],
    ('v', 'v'): [],
    ('v', 'A'): ['^', '>'],
    ('v', '^'): ['^'],
    ('<', '>'): ['>', '>'],
    ('<', '<'): [],
    ('<', 'v'): ['>'],
    ('<', 'A'): ['>', '>', '^'],
    ('<', '^'): ['>', '^'],
    ('>', '>'): [],
    ('>', '<'): ['<', '<'],
    ('>', 'v'): ['<'],
    ('>', 'A'): ['^'],
    ('>', '^'): ['<', '^'],
    ('A', '>'): ['v'],
    ('A', '<'): ['v', '<', '<'],
    ('A', 'v'): ['v', '<'],
    ('A', 'A'): [],
    ('A', '^'): ['<']
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
    ('1', 'A'): ['>','>' , 'v'],
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
    ('8', '8'): [],
    ('8', '9'): ['>'],
    ('8', 'A'): ['v', 'v', 'v', '>'],
    ('8', '8'): [],

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

small_pad_controls = ['A', '^', 'v', '<', '>']
large_pad_controls = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A']

def make_controls_for_controls():
    for i in small_pad_controls:
        for j in small_pad_controls:
            print(i,j,small_keypad_transitions[(i, j)])

def make_controls_for_sequence(sequence):
    return [small_keypad_transitions[(c1, c2)] for c1, c2 in zip(sequence[:-1], sequence[1:])]

def test(chain_length=2):

    controls_store = {}
    controls_lists = {}
    # steps = []
    for i in small_pad_controls:
        for j in small_pad_controls:
            controls_store[(i, j)] = 1
            controls_lists[(i, j)] = []
    for i in controls_store:
        print(i, controls_store[i])

    for c in range(chain_length):
        for i in small_pad_controls:
            for j in small_pad_controls:
                transition = small_keypad_transitions[(i, j)]
                new_store = {}
                previous = 'A'
                # current_count = 0
                # counts = []
                for step in transition:
                    print("Step is", step)
                    # counts.append(len())
                    # current_count = current_count + 1
                    print("Adding transition from", previous, "to", step)
                    newSteps = small_keypad_transitions[(previous, step)]
                    # steps.extend(newSteps)
                    controls_store[(previous, step)] = controls_store[(previous, step)] + len(newSteps)
                    controls_lists[(previous, step)].extend(newSteps)
                    previous = step
                # controls_store[(i, j)] = controls_store[(i, j)] * len(small_keypad_transitions[('A', j)])
                # controls_lists[(i, j)].extend(small_keypad_transitions[('A', j)])
    # for i in small_pad_controls:
    #         for j in small_pad_controls:
    #             controls_store[(i, j)] = controls_store[(i, j)] * len(small_keypad_transitions[('A', j)])
    #             controls_lists[(i, j)].extend(small_keypad_transitions[('A', j)])

    sequence = '971A'
    counter = 0
    for i in sequence:

        pattern = large_keypad_transitions[(previous, i)]
        print("Pattern from ", previous, "to", i, "is", pattern)
        previous = 'A'
        for j in pattern:
            print("moving to", j)
            counter = counter + controls_store[(previous, j)]
            print("counter is now", counter, controls_lists[(previous, j)])
            # controls_lists[('A', j)].append(j)
        previous = i
    print(controls_store)
    # for i in controls_lists.keys():
    #         print(i, controls_lists[i])
    print("Final score", counter)

def test2(chain_length=2):
    control_cache = {}
    for j in small_pad_controls:
        for k in small_pad_controls:
            control_cache[(j, k)] = 1
    for c in range(chain_length):
        for j in small_pad_controls:
            for k in small_pad_controls:
                control_cache[(j, k)] = control_cache[(j, k)] * len(small_keypad_transitions[(j, k)])
    for c in control_cache:
        print(c, control_cache[c])

def test3(chain_length):
    """
    Uses dynamic programming to find the minimum number of keypresses needed
    for each possible target key on a chain of keypads. All pads start at 'A'
    position, and we need to navigate from there to execute commands.
    Each pad needs to be positioned correctly to affect the pads below it.
    """
    # Initialize dp table: dp[step][target][curr_pos] represents min keypresses 
    # to achieve target on pad 'step' with current pad at curr_pos
    positions = ['^', 'v', '<', '>', 'A']
    dp = {}
    
    # Base case: step 1 (first pad)
    for target in positions:
        for curr_pos in positions:
            dp[(1, target, curr_pos)] = float('inf')
        # Cost to move from A to target directly
        if ('A', target) in small_keypad_transitions:
            dp[(1, target, target)] = len(small_keypad_transitions[('A', target)])
        elif target == 'A':
            dp[(1, 'A', 'A')] = 0
    
    # For each pad in the chain
    for step in range(2, chain_length + 1):
        for target in positions:
            for curr_pos in positions:
                min_presses = float('inf')
                
                # To reach target on pad 'step':
                # 1. Previous pad (step-1) must be at the target position
                # 2. Current pad must navigate to 'A' to activate previous pad
                
                # First, get cost to position previous pad
                prev_cost = dp[(step-1, target, target)]
                
                if prev_cost != float('inf'):
                    # Now add cost to get current pad to 'A' from its position
                    if curr_pos == 'A':
                        # Already at A, just need to press it
                        total_cost = prev_cost + 1
                    elif ('A', curr_pos) in small_keypad_transitions:
                        # Need to navigate to A first, then press it
                        nav_cost = len(small_keypad_transitions[('A', curr_pos)])
                        total_cost = prev_cost + nav_cost + 1
                    
                    min_presses = min(min_presses, total_cost)
                
                dp[(step, target, curr_pos)] = min_presses
    
    # Print results for the final step
    print(f"\nResults for chain length {chain_length}:")
    for pos in positions:
        min_presses = float('inf')
        for curr_pos in positions:
            min_presses = min(min_presses, dp[(chain_length, pos, curr_pos)])
        print(f"Minimum keypresses to reach '{pos}' on pad {chain_length}: {min_presses}")
        
        # Show example sequence for this position
        if pos == '<':
            print(f"\nExample sequence to reach '<' on pad {chain_length}:")
            print(f"1. Navigate pad {chain_length-1} from A to < (v,<,< = 3 presses)")
            print(f"2. Navigate pad {chain_length-2} to A and press it (1 press)")
            print(f"3. Navigate pad {chain_length-3} to A and press it (1 press)")
            print(f"Total: at least {3 + (chain_length-2)} presses")
    
    return dp

def test4(chain_length=2, test_sequence='971A'):
    print("building command caches...")
    command_caches = {}

    command_chains = {}
    for command in small_pad_controls:
        command_chains[command] = []
    for command in small_pad_controls:
        command_caches[command] = 1
        command_chains[command] = [command]
    print("command caches built", command_caches)
    print("Chain length is:", chain_length)
    previous_chain = None
    for i in range(1, chain_length):
        
        new_command_chains = {}
        for command in small_pad_controls:
            new_command_chains[command] = []
        # for command in small_pad_controls:
        #     new_command_chains[command] = []
        print(f"Looking at keypad {i+1}:")
       
        for command in small_pad_controls:
            print("Working on small pad control", command)
            # look at the cost to go from one command to another
            commands = small_keypad_transitions_no_A[('A', command)]
            print("Commands from", 'A', "to", command, "are", commands)
            command_caches[command] = command_caches[command] * len(commands)
            previous = 'A'
            for subcommand in commands:

                # print("Adding command_chains to new_command_chains", command_chains[command], new_command_chains[subcommand])
                new_command_chains[command] = new_command_chains[command] + command_chains[subcommand]
                previous = command
                # if(previous_chain is not None):
                    # path_to_a = small_keypad_transitions[(new_command_chains[command][-1], 'A')]
                    # new_command_chains[command].extend(path_to_a)
                # else:
                # new_command_chains[command].append('A')
            # a_commands = small_keypad_transitions_no_A[(command, 'A')]
            # for subcommand in a_commands:
            #     # print("Adding command_chains to new_command_chains", command_chains[command], new_command_chains[subcommand])
            #     new_command_chains[command] = new_command_chains[command] + command_chains[subcommand]
            # previous = command
            new_command_chains[command] = new_command_chains[command] + ["A"]
        previous_chain = command_chains
        command_chains = new_command_chains
        previous = 'A'
        print("After keypad", i+1, "command chains look like:")
        for command in command_chains:
            print(f"{command}: {''.join(command_chains[command])} {command_chains[command]}")
    print("Before the last keypad, chains look like:")
    for command in command_chains:
        print(f"{command}: {command_chains[command]}")
    return
    if(chain_length > 0):
        previous = 'A'
        new_command_chains = {}
        for command in small_pad_controls:
            new_command_chains[command] = []
        for command in small_pad_controls:
            print("Working on small pad control", command)
            # look at the cost to go from one command to another
            commands = small_keypad_transitions[(previous, command)]
            print("Commands from", previous, "to", command, "are", commands)
            command_caches[command] = command_caches[command] * len(commands)
            for subcommand in commands:
                print("Adding command_chains to new_command_chains", command_chains[command], new_command_chains[subcommand])
                new_command_chains[command] = new_command_chains[command] + command_chains[subcommand]
            previous = command
            # a_commands = small_keypad_transitions[(command, 'A')]
            # for subcommand in a_commands:
            #     print("Adding command_chains to new_command_chains", command_chains[command], new_command_chains[subcommand])
            #     new_command_chains[command] = new_command_chains[command] + command_chains[subcommand]
            # previous = command
            
        command_chains = new_command_chains
        previous = 'A'


    print("Command chains at the end of the build:")
    for command in command_chains:
        print(f"{command}: {command_chains[command]}")
    previous = 'A'

    # for command in small_pad_controls:
    #     # look at the cost to go from one command to another
    #     commands = small_keypad_transitions_no_A[(previous, command)]
    #     print(f"Commands from {previous} to {command}: {commands}")
    #     command_caches[command] = command_caches[command] * len(commands)
    #     previous = command
    previous_position = 'A'
    total = 0
    command_string = []
    for item in test_sequence:

        print(item)
        needed_commands = large_keypad_transitions[(previous_position, item)]
        # needed_commands.append('A')
        print(f"Commands needed to get from {previous_position} to {item}: {needed_commands}")
        for command in needed_commands:

            print(f"Command: {command}")
            print(f"Cost: {command_caches[command]}")
            command_string.extend(command_chains[command])
            total += command_caches[command]
        back_to_a = small_keypad_transitions_no_A[(needed_commands[-1], 'A')]
        for command in back_to_a:
            print(f"Command: {command}")
            print(f"Cost: {command_caches[command]}")
            command_string.extend(command_chains[command])
            total += command_caches[command]
        # command_string.extend(command_chains['A'])
        total += command_caches['A']
        previous_position = item
    print("Total commands needed:", total)
    print("Command string array:", command_string)
    print("Command string:", ''.join(command_string))
    print("Final command caches:")
    for command in command_chains:
        print(f"{command}: {command_chains[command]}")
    # print("Total commands needed:", sum(command_caches.values()))
    # chain_length = 4
    # total = calculate_sequence_keypresses(test_sequence, chain_length, optimal_paths)
    # print(f"\nTo input sequence {test_sequence} with chain length {chain_length}:")
    # print(f"Total keypresses needed: {total}")




def make_chains_for_level(previous_chains = None, scoreMode = False):
    if previous_chains is None:
        previous_chains = {}
    new_chains = {}
    for source in small_pad_controls:
        for target in small_pad_controls:
            if scoreMode == True:
                new_chains[(source, target)] = 0
            else:
                new_chains[(source, target)] = []
            previous = 'A'
            for step in small_keypad_transitions_no_A[(source, target)]:
                if scoreMode == True:
                    new_chains[(source, target)] = new_chains.get((source, target), 0) + previous_chains.get((previous, step), 1)
                else:
                    new_chains[(source, target)] = new_chains.get((source, target), []) + previous_chains.get((previous, step), [step])
                # print("Analyzed chain from", source, "to", target, "from step", step, ''.join(new_chains[(source, target)]))

                previous = step
            # new_chains[(source, target)] = new_chains.get((source, target), []) + ['A']
    return new_chains

def make_transition_chains(chain_length, scoreMode = False):
    previous_chain = None
    saving_chain = None
    chains = []
    for i in range(chain_length):
        start = datetime.datetime.now()
        print(f"Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
        print(f"Looking at keypad {i+1}:")
        old_chain = saving_chain.copy() if saving_chain != None else None
        previous_chain = make_chains_for_level(saving_chain, scoreMode)
        saving_chain = previous_chain.copy()
        # print("Saving chain", i+1, "is:")
        for command in saving_chain:
            # print(f"{command}: {''.join(saving_chain[command])}")
            saving_chain_value = saving_chain[command]
            og_command = small_keypad_transitions_no_A[command]
            # print("Appending to chain from old_chains", command,"->", saving_chain_value)
            if saving_chain_value == []:
                if scoreMode == True:
                    saving_chain[command] = saving_chain[command]  + 1
                else:
                    saving_chain[command] = saving_chain[command]  + ['A']
                # saving_chain[command] = saving_chain[command]  + (old_chain.get((saving_chain_value[-2], 'A')) if old_chain != None else ['A'])
                pass
            else:
                if old_chain == None:
                    print("old_chain is None, just appending an A", command, saving_chain[command])
                    if scoreMode == True:
                        saving_chain[command] = saving_chain[command]  + 1
                    else:
                        saving_chain[command] = saving_chain[command]  + ['A']
                    print("old_chain is None, just appended an A", command, saving_chain[command])
                else:
                    # print("old_chain is not None, appending back_to_a", ''.join(old_chain.get((saving_chain_value[-2], 'A'))))
                    # if saving_chain_value[-2] == 'A':
                    #     print("position -3")
                    # print("og_command", command, og_command)
                    if len(og_command) > 0:
                        tail_command =  og_command[-1]
                        back_to_a = old_chain.get((tail_command, 'A'))
                    else:
                        print("No tail command found, using A", command, og_command)
                        if scoreMode == True:
                            back_to_a = 1
                        else:
                            back_to_a = ['A']
                        continue
                    
                    # else:
                    #     tail_command =  saving_chain_value[-2]
                    #     print("position -2")
                    #     back_to_a = old_chain.get((tail_command, 'A'))
                    # print("based on tail command of ", tail_command, "adding back_to_a", ''.join(back_to_a),  "to", ''.join(saving_chain_value), "to get", ''.join(saving_chain[command]))
                    saving_chain[command] = saving_chain[command]  + back_to_a
                # else:
                #     saving_chain[command] = saving_chain[command]  + old_chain.get((saving_chain_value[-2], 'A'))
            # print("Updated saving chain", i+1, command, "from:", ''.join(saving_chain_value), "to:", ''.join(saving_chain[command]))
        chains.append(saving_chain)

        end = datetime.datetime.now()
        print(f"Finished keypad {i+1} in {end-start}")
        for i in range(len(chains)):
            print("After keypad", i+1, "command chains look like:")
            for command in chains[i]:
                if(scoreMode == True):
                    print(f"{command}: {chains[i][command]}")
                else:
                    print(f"{command}: {''.join(chains[i][command])} ")
    # print("Before the last keypad, chains look like:")
    # for command in previous_chain:
    #     print(f"{command}: {''.join(previous_chain[command])} ")
    return saving_chain

if __name__ == "__main__":
    if(len(sys.argv) < 4):
        print("Usage: python 21b.py <chain_length> <test_sequence> <scoremode>")    
        print("Example: python 21b.py 4 1 1")
        sys.exit(1)
    chain_length = int(sys.argv[1])
    test_sequence = sys.argv[2]
    scoreMode = True if int(sys.argv[3]) > 0 else False
    # test4(chain_length, test_sequence)
    saving_chain = make_transition_chains(chain_length, scoreMode)
    print("Final command set as of chain ", chain_length, ":")
    for command in saving_chain:
        if(scoreMode == True):
            print(f"{command}: {saving_chain[command]}")
        else:
            print(f"{command}: {len(saving_chain[command])} - {''.join(saving_chain[command])} ")
        # print(f"{command}: {saving_chain[command]} ")
    # previous = 'A'
    # for item in test_sequence:
    #     print(item)
    #     needed_commands = large_keypad_transitions[(previous, item)]
    #     print(f"Commands needed to get from {previous} to {item}: {needed_commands}")
    #     for command in needed_commands:

    #         command_string.extend(command_chains[command])
    #         total += command_caches[command]
    #     back_to_a = small_keypad_transitions_no_A[(needed_commands[-1], 'A')]
    #     for command in back_to_a:
          



    # A>Av<<A>A^>AAvA^<A>A
    # v<<A>^>AvA^Av<A<AA>^>AvA^<A>AAvA^Av<<A>A^>AvA^A<A>Av<<A>A^>AAvA^<A>A