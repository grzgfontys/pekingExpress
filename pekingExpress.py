import json

with open('pekingExpressTest1.json') as f:
  board = json.load(f)
print(board)

locationNumber = board["locations"]["number"]
criticalLocation = board["locations"]["critical"]
sources = board["roads"]["source"]
targets = board["roads"]["target"]
prices = board["roads"]["price"]
startLocation = board["startLocation"]
budget = board["budget"]
finishLocation = 88
print(f'{locationNumber=}')
print(f'{criticalLocation=}')
print(f'{sources=}')
print(f'{targets=}')
print(f'{prices=}')
print(f'{startLocation=}')
print(f'{budget=}')
print(f'{finishLocation=}')

# might want to change None to -1 but idk if edges can have minus value
adjMatrix = [[None for j in range(finishLocation+1)] for i in range(finishLocation+1)]

for i in range(len(prices)):
  adjMatrix[sources[i]][targets[i]] = prices[i]
  # is it undirected?
  adjMatrix[targets[i]][sources[i]] = prices[i]

print(adjMatrix)