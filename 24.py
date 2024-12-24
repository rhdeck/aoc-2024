import graphviz

def load_file(filename):
    with open(filename) as f:
        contents = f.read()
    
    # Split into registers and rules sections
    registers_text, rules_text = contents.strip().split('\n\n')
    
    # Parse registers
    registers = {}
    for line in registers_text.split('\n'):
        reg, val = line.split(': ')
        registers[reg] = val == '1'
    
    # Parse rules
    rules = []
    for line in rules_text.split('\n'):
        # Format: "a OP b -> c"
        expr, output = line.split(' -> ')
        parts = expr.split()
        if len(parts) == 3:  # binary operation
            operand1, operator, operand2 = parts
            rules.append((operand1, operand2, operator, output))
    
    return registers, rules

def run_rule(rule, registers):
    operand1, operand2, operator, output = rule
    if(operand1 not in registers or operand2 not in registers):
        pass
    elif operator == 'AND':
        registers[output] = registers[operand1] and registers[operand2]
    elif operator == 'OR':
        registers[output] = registers[operand1] or registers[operand2]
    elif operator == 'XOR':
        registers[output] = registers[operand1] ^ registers[operand2]
    else:
        pass
        # raise ValueError(f"Unknown operator: {operator}")

    return registers

def run_rules(rules, registers, runs=100):
    for _ in range(runs):
        for rule in rules:
            registers = run_rule(rule, registers)
    return registers

def registerHash(registers):
    return tuple(sorted([registers[reg] for reg in registers]))

def getRegisters(prefix, limit = None):
    r = sorted([(reg, registers[reg]) for reg in registers if reg[0] == (prefix)])
    if limit is not None:
        r = r[:limit]
    return r

def getScore(prefix, limit = None):
    prefixed_registers= getRegisters(prefix, limit)
    return sum(val * (2 ** i) for i, (_, val) in enumerate(prefixed_registers))

def getPart1(registers):
    return getScore("z")

def add_x_y_registers(registers, limit = None):
    return getScore("x", limit) + getScore("y", limit)


def test_x_y_registers(registers, limit = None):
    return getScore("x", limit) + getScore("y", limit) == getScore("z", limit)

def get_upstream_nodes(target_node, rules):
    upstream = set()
    
    def find_dependencies(node):
        # Find all rules where this node is the output
        for operand1, operand2, operator, output in rules:
            if output == node:
                # Add both operands to upstream set
                upstream.add(operand1)
                upstream.add(operand2)
                # Recursively find dependencies of operands
                find_dependencies(operand1)
                find_dependencies(operand2)
    
    find_dependencies(target_node)
    return upstream

def visualize_rules(rules, limit = None):
    dot = graphviz.Digraph(comment='Circuit Dependencies')
    dot.attr(rankdir='LR')  # Left to right layout
    dot.attr(ranksep='1 equally')
    # Add all nodes and edges
    for operand1, operand2, operator, output in rules:
        # Add nodes with different colors based on register type
        for reg in [operand1, operand2, output]:
            if reg[0] == 'x':
                dot.node(reg, reg, color='blue')
            elif reg[0] == 'y':
                dot.node(reg, reg, color='green')
            elif reg[0] == 'z':
                dot.node(reg, reg, color='red')
            else:
                dot.node(reg, reg)
        
        # Add edges with operator as label
        dot.edge(operand1, output, label=operator)
        dot.edge(operand2, output, label=operator)
    
    # Save the graph
    dot.render('circuit_dependencies', format='png', cleanup=True)

def swap_rule_outputs(node1, node2, rules):
    # Find the rules that have these nodes as outputs
    rule1 = next(rule for rule in rules if rule[3] == node1)
    rule2 = next(rule for rule in rules if rule[3] == node2)
    print(rule1)
    print(rule2)
    # Swap their outputs
    rule1_idx = rules.index(rule1)
    rule2_idx = rules.index(rule2)
    print(rule1_idx, rule2_idx)
    rules[rule1_idx] = (rule1[0], rule1[1], rule1[2], node2)
    rules[rule2_idx] = (rule2[0], rule2[1], rule2[2], node1)
    print(rules[rule1_idx])
    print(rules[rule2_idx])
    return rules

if __name__ == "__main__":
    registers, rules = load_file("24.txt")
    print(registers)
    # print(rules)
    # registers, rules = load_file("24.txt")
    # Swap z30 and rvp outputs
    # theory of answer: btb,cmv,mwp,rdg,rmj,z17,z23,z30
    rules = swap_rule_outputs('z30', 'rdg', rules)
    rules = swap_rule_outputs('z17', 'cmv', rules)
    rules = swap_rule_outputs('z23', 'rmj', rules)
    rules = swap_rule_outputs('btb', 'mwp', rules)
    oldHash = None
    while oldHash != registerHash(registers):
        # print("hash", registerHash(registers))
        oldHash = registerHash(registers)
        registers = run_rules(rules, registers)
    print(registerHash(registers))

    print(getPart1(registers))
    print(   "{0:b}".format(add_x_y_registers(registers, 46)), add_x_y_registers(registers, 46))
    print("{0:b}".format(getScore("z", 46)), getScore("z", 46))    
    print("---------------")
    # Visualize the dependency graph
    visualize_rules(rules)
    # for i in range(46):
    #     for x in [True, False]:
    #         registers["x" + str(i).rjust(2, '0')] = x
    #         for y in [True, False]:
    #             registers["y" + str(i).rjust(2, '0')] = y
    #             print(i, x,y,"---",test_x_y_registers(registers, i), add_x_y_registers(registers, i), getScore("z", i))

    # Find all nodes that contribute to z00
    lastScore = 0
    rankedNodes = {'x00': 0, 'y00': 0}
    for i in range(1,3):
        indexStr = str(i).rjust(2, '0')
        upstream_nodes = get_upstream_nodes("z" + indexStr, rules)
        for node in upstream_nodes:
            if node not in rankedNodes:
                rankedNodes[node] = i
        previousIndexStr = str(i-1).rjust(2, '0')
        if i > 1:
            # set everything to false except for previous and this one
            for j in range(46):
                registers["x" + str(j).rjust(2, '0')] = False
                registers["y" + str(j).rjust(2, '0')] = False
        for previousX in [True, False]:
            registers["x" + previousIndexStr] = previousX
            for previousY in [True, False]:
                registers["y" + previousIndexStr] = previousY
                for x in [True, False]:
                    registers["x" + indexStr] = x
                    for y in [True, False]:

                        registers["y" + indexStr] = y
                        # print(f"Registers as of now ({i})", x,y, "x", getScore("x", i), "y", getScore("y", i), "z", getScore("z", i), "x+y", add_x_y_registers(registers, i), )
                        total = add_x_y_registers(registers, i)
                        # print("sum at index ", i, "is", total, "inputs",previousX, previousY, x, y)



                        # upstream_z00 = get_upstream_nodes("z" + indexStr, rules)
        # do any future nodes also feed in
        # for node in upstream_z00:
        #     if((node[0] == 'x' or node[0] == 'y' ) and  int(node[1:])> i):
        #         print("Bad node found in set for z" + indexStr, node)
        # print(f"Nodes that feed into {indexStr} {len(upstream_z00)} (difference: {len(upstream_z00) - lastScore})")
        # lastScore = len(upstream_z00)
        # print(rankedNodes)
