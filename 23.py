def load_file(filename):
    with open(filename, 'r') as f:
        edges= set([tuple(line.strip().split('-')) for line in f.readlines()])
    newedges = edges.copy()
    for edge in edges:
        newedges.add((edge[1], edge[0]))
    return newedges

def make_sets_of_threes(edges):
    threes = set()
    for edge in edges:
        start = edge[0]
        middle = edge[1]
        alltails =[edge2[1] for edge2 in edges if edge2[0] == middle and edge2[1] != start]
        for tail in alltails:
            if (tail, start) in edges:
                threes.add(tuple(sorted([start, middle, tail])))
        # tails = [tail for tail in alltails if tail not in connectedtails]
        # for tail in tails:
        #     threes.add(tuple(sorted([start, middle, tail])))
    return threes

def make_threes_with_tees(edges):
    threes = make_sets_of_threes(edges)
    threes_with_tees = [three for three in threes if three[0][0] == 't' or three[1][0] == 't' or three[2][0] == 't']
    return threes_with_tees

def find_largest_connected_set(edges):
    # Get all unique nodes
    nodes = set()
    for edge in edges:
        nodes.add(edge[0])
        nodes.add(edge[1])
    
    def is_fully_connected(node_set):
        # Check if all nodes in the set are connected to each other
        for n1 in node_set:
            for n2 in node_set:
                if n1 != n2 and (n1, n2) not in edges:
                    return False
        return True
    
    def find_max_clique(candidates, current_set):
        if not candidates:
            return current_set if is_fully_connected(current_set) else set()
            
        max_set = current_set if is_fully_connected(current_set) else set()
        
        while candidates:
            v = candidates.pop()
            # Find neighbors of v that are connected to all nodes in current_set
            new_candidates = {u for u in candidates if all((u, n) in edges for n in current_set)}
            new_set = find_max_clique(new_candidates, current_set | {v})
            if len(new_set) > len(max_set):
                max_set = new_set
                
        return max_set
    
    return find_max_clique(nodes, set())

party = load_file('23.txt')
threes = make_sets_of_threes(party) 
threes_with_tees = make_threes_with_tees(party)

    
# print(threes_with_tees)
print("Part 1:", len(threes_with_tees ))

# Test the new function
largest_set = sorted(find_largest_connected_set(party)) #sorted(find_largest_connected_set(party))
print("Largest fully connected set:", ','.join(largest_set)) #largest_set)
print("Part 2: Size of largest set:", len(largest_set))