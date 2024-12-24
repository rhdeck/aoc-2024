cache = {}
def evolve(current):
    if current in cache:
        # print("Found", current, "in cache")
        return cache[current]
    uppermask = current * 64
    output = uppermask ^ current
    output = output % 8**8
    lowermask = output // 32
    output = output ^ lowermask
    output = output % 8**8
    bigmask = output * 2048
    output = output ^ bigmask
    output = output % 8**8
    cache[current] = output
    return output

def get_score(current, iterations):
    for i in range(iterations):
        current = evolve(current)
    return current


def get_prices(current, iterations):
    priceSets = {}
    prices = []
    previousPrice = current % 10
    for i in range(iterations):
        current = evolve(current)
        currentPrice = current % 10
        change = currentPrice - previousPrice
        previousPrice = currentPrice
        prices.append(change)
        # print("prices", prices)
        if(len(prices) == 4):
            priceSet = tuple(prices)
            if not priceSet in priceSets:
                priceSets[priceSet] = currentPrice
            prices = prices[1:]
    return priceSets

def test_part_1():
    with open("22.txt") as f:
        lines = f.readlines()
    scores = []
    for line in lines:
        start = int(line.strip())
        score = get_score(start, 2000)
        # print("Score for", start, "is", score)
        scores.append(score)
    sumscores = sum(scores)
    print("Total score is", sumscores)

def test_part_2():
    with open("22.txt") as f:
        lines = f.readlines()
    setCache = {}
    for line in lines:
        start = int(line.strip())
        
        priceSets = get_prices(start, 2000)
        # print("Price sets for", start, "is")
        for key in priceSets:
            # print(key, priceSets[key])
            if(key in setCache):
                setCache[key] += priceSets[key]
            else:
                setCache[key] = priceSets[key]
    # find maximum value in priceSets
    maxValue = max(setCache.values())
    print("Part 2: Max value is", maxValue)
    # get the key with the maximum value
    maxKey = max(setCache, key=setCache.get)
    # print("Part 2: Max key is", maxKey)
    # print(setCache[(-2,1,-1,3)])
    # for key in setCache:
    #     print(key, setCache[key])
if __name__ == "__main__":

    test_part_1()
    test_part_2()
   
