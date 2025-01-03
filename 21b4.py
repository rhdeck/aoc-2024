import sys
import datetime
from sympy.utilities.iterables import multiset_permutations

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

small_keypad_results = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
    "A": (0, 0)
}


def get_value_from_large_keypad(position):
    return large_keypad[position[1]][position[0]]

def test_keypad_path(origin_value, path, destination):
    origin_pos = None
    for y, row in enumerate(large_keypad):
        for x, value in enumerate(row):
            if value == origin_value:
                origin_pos = (x, y)
                break
    print("Origin position:", origin_pos)
    print("Large keypad:", large_keypad)
    for move in path:
        if move == "^":
            origin_pos = (origin_pos[0], origin_pos[1] - 1)
        elif move == "v":
            origin_pos = (origin_pos[0], origin_pos[1] + 1)
        elif move == "<":
            origin_pos = (origin_pos[0] - 1, origin_pos[1])
        elif move == ">":
            origin_pos = (origin_pos[0] + 1, origin_pos[1])
        elif move == "A":
            origin_pos = (origin_pos[0], origin_pos[1])
        if origin_pos[0] < 0 or origin_pos[0] >= len(large_keypad[0]) or origin_pos[1] < 0 or origin_pos[1] >= len(large_keypad):
            return False
        temp_value = get_value_from_large_keypad(origin_pos)
        if temp_value == '#':
            return False
    return True

def test_small_keypad_path(origin_value, path, destination):
    origin_pos = None
    for y, row in enumerate(small_keypad):
        for x, value in enumerate(row):
            if value == origin_value:
                origin_pos = (x, y)
                break
    for move in path:
        if move == "^":
            origin_pos = (origin_pos[0], origin_pos[1] - 1)
        elif move == "v":
            origin_pos = (origin_pos[0], origin_pos[1] + 1)
        elif move == "<":
            origin_pos = (origin_pos[0] - 1, origin_pos[1])
        elif move == ">":
            origin_pos = (origin_pos[0] + 1, origin_pos[1])
        elif move == "A":
            origin_pos = (origin_pos[0], origin_pos[1])
        if origin_pos[0] < 0 or origin_pos[0] >= len(small_keypad[0]) or origin_pos[1] < 0 or origin_pos[1] >= len(small_keypad):
            return False
        temp_value = small_keypad[origin_pos[1]][origin_pos[0]]
        if temp_value == '#':
            return False
    return True

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
    ('2', '9'): ['>', '^', '^'],
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
    ('A', '8'): [ '^', '^', '^', '<'],
    ('A', '9'): ['^', '^', '^']
}

small_pad_controls = ['A', '^', 'v', '<', '>']
large_pad_controls = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A']

def make_chains_for_level(previous_chains = None, scoreMode = False):
    old_chain_is_none = False
    if previous_chains is None:
        old_chain_is_none = True
        previous_chains = {}
    new_chains = {}
    used_combos = {}
    for source in small_pad_controls:
        for target in small_pad_controls:
            if scoreMode == True:
                new_chains[(source, target)] = 0
            else:
                new_chains[(source, target)] = []
           
            # Test all possible sequences of transition ot see which one is the shortest
            shortest_path = None
            combos = multiset_permutations(small_keypad_transitions_no_A[(source, target)])
                # print("Testing transition from", combo[0], "to", combo[1]
            combolist = list(combos)
            print("Testing my combos for", source, "to", target, ":", combolist)

            for combo in combolist:
                print("testing combo", combo, "from",small_keypad_transitions_no_A[(source, target)] )  
                isbadcombo = False
                if not test_small_keypad_path(source, combo, target):
                    print("Bad transition from", source, "to", target, "from",combo)
                    isbadcombo = True 
                    print("Skipping bad transition", combo, "for",small_keypad_transitions_no_A[(source, target)])
                    continue
                else:
                    print("Found good transition", combo, "for",small_keypad_transitions_no_A[(source, target)])
                if(scoreMode == True):
                    temp_path = 0
                else:
                    temp_path = []
                previous = 'A'
                for step in combo:
                    print("Looking at combo step", step)
                    if scoreMode == True:
                        temp_path = temp_path + previous_chains.get((previous, step), 1)
                    else:
                        temp_path = temp_path + previous_chains.get((previous, step), [step])
                    previous = step
                
                if scoreMode == True:
                    if old_chain_is_none == False: temp_path = temp_path + previous_chains.get((previous, "A"), 1)
                    print("SCORE Temp path is", temp_path)
                    if shortest_path == None or temp_path < shortest_path:
                        print("New shortest path is", temp_path)
                        shortest_path = temp_path
                        used_combos[(source, target)] = combo
                else:
                    if old_chain_is_none == False: temp_path = temp_path + previous_chains.get((previous, "A"), ['A'])
                    print("LIST Temp path is", ''.join(temp_path))
                    if shortest_path == None or len(temp_path) < len(shortest_path):
                        print("New shortest path is", ''.join(temp_path))
                        shortest_path = temp_path
                        used_combos[(source, target)] = combo
            if shortest_path != None:
                new_chains[(source, target)] = shortest_path 
            elif scoreMode == True:
                new_chains[(source, target)] = 0
            else:
                new_chains[(source, target)] = new_chains.get((source, target), [])
            if scoreMode == True:
                print("New chain from", source, "to", target, "is", new_chains[(source, target)])
            else:
                print("New chain from", source, "to", target, "is", len(new_chains[(source, target)]))
    return new_chains, used_combos

def make_transition_chains(chain_length, scoreMode = False):
    previous_chain = None
    saving_chain = None
    chains = []
    for i in range(chain_length):
        start = datetime.datetime.now()
        print(f"Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
        print(f"Looking at keypad {i+1}:")
        old_chain = saving_chain.copy() if saving_chain != None else None
        previous_chain, used_combos = make_chains_for_level(saving_chain, scoreMode)
        saving_chain = previous_chain.copy()
        for command in saving_chain:
            if command not in used_combos: print("ERROR Og command is NOT found?", command, command in used_combos)
            og_command = used_combos[command] # if command in used_combos else small_keypad_transitions_no_A[command]
            if saving_chain[command] == [] or saving_chain[command] == 0:
                if scoreMode == True:
                    saving_chain[command] = saving_chain[command]  + 1
                else:
                    saving_chain[command] = saving_chain[command]  + ['A']
                pass
            else:
                if old_chain == None:

                    if scoreMode == True:
                        saving_chain[command] = saving_chain[command]  + 1
                    else:
                        saving_chain[command] = saving_chain[command]  + ['A']

                # else:

                #     if len(og_command) > 0:
                #         tail_command =  og_command[-1]
                #         back_to_a = old_chain.get((tail_command, 'A'))
                #     else:
                #         print("No tail command found - this should never happen, aborting", command, og_command)
                #         exit(1)
                #     saving_chain[command] = saving_chain[command]  + back_to_a
        chains.append(saving_chain)

        end = datetime.datetime.now()
        print(f"Finished keypad {i+1} in {end-start}")
        print("After keypad", i+1, "command chains look like:")
        for command in chains[i]:
            if(scoreMode == True):
                print(f"{command}: {chains[i][command]}")
            else:
                print(f"{command}: {len(chains[i][command])}")
    return saving_chain


def evaluate_sequence(test_sequence, saving_chain, scoreMode = False):
    sequence = test_sequence
    if scoreMode == False:
        counter = []
    else:
        counter = 0
    previous = 'A'
    for i in sequence:
        print("Trying to move from", previous, "to", i)
        og_pattern = large_keypad_transitions[(previous, i)]
        combos = multiset_permutations(og_pattern)
        combolist = list(combos)
       
        mincounter = None
        sub_previous = previous
        # combolist = [og_pattern]
        for pattern in combolist:
            tempcounter = counter
            print("Trying pattern", pattern)
            if not test_keypad_path(previous,pattern, i):
                print("Pattern ", pattern, "from ", previous, "to", i, "is not valid")
                continue

            print("Pattern from ", previous, "to", i, "is", pattern)
            sub_previous = 'A'
            for j in pattern:
                print("moving from", sub_previous, " to", j)
                tempcounter = tempcounter + saving_chain[(sub_previous, j)]
                if scoreMode == False:
                    print("after moving to", j, "counter is now", len(tempcounter), ''.join(tempcounter))
                else:
                    print("after moving to", j, "counter is now", tempcounter)
                sub_previous = j
           
            tempcounter = tempcounter + saving_chain[(sub_previous, 'A')]
            if scoreMode == True:
                if mincounter == None or tempcounter < mincounter:
                    mincounter = tempcounter
            else:
                if mincounter == None or len(tempcounter) < len(mincounter):
                    mincounter = tempcounter
        if(mincounter == None):
            print("No valid patterns found for", previous, "to", i)
            break
        if scoreMode == True:
            counter = mincounter
        else:
            counter = mincounter
       
        previous = i
    print('===============')
    if scoreMode == False:
        print("After all is done, final length is", len(counter) ,":",  ''.join(counter))
    else:
        print("After all is done, final length is", counter)
    
    return counter

def extract_digits(s: str) -> int:
    digits = ''.join(c for c in s if c.isdigit())
    return int(digits) if digits else 0

if __name__ == "__main__":
    if(len(sys.argv) < 4):
        print("Usage: python 21b.py <chain_length> <test_sequence> <scoremode>")    
        print("Example: python 21b.py 4 1 1")
        sys.exit(1)
    chain_length = int(sys.argv[1])
    test_sequence = sys.argv[2] 
    scoreMode = True if int(sys.argv[3]) > 0 else False
    saving_chain = make_transition_chains(chain_length, scoreMode)
    print("Final command set as of chain ", chain_length, ":")
    for command in saving_chain:
        if(scoreMode == True):
            print(f"{command}: {saving_chain[command]}")
        else:
            print(f"{command}: {len(saving_chain[command])}  ")

    print("===============")

    if(test_sequence != "X"):
        print("Evaluating single sequence '", test_sequence, "'")
        l = evaluate_sequence(test_sequence, saving_chain, scoreMode)
        if scoreMode == False:
            print("Sequence:", ''.join(l))
            l = len(l)
        digits = extract_digits(test_sequence)
        print("Score for sequence", test_sequence, "is", l, " * ", digits, " = ", l * digits)
    else:
        total = 0
        with open("21.txt") as f:
            commands = f.read().strip().split('\n')
        for i, seq in enumerate(commands, 1):
            print("Evaluating sequence", seq)
            l = evaluate_sequence(seq, saving_chain, scoreMode)
            if scoreMode == False:
                print("Sequence:", ''.join(l))
                l = len(l)
            digits = extract_digits(seq)
            score = l * digits
            total += score
            print("Score for sequence", seq, "is", l, " * ", digits, " = ", score)
        print("Total score is", total)
