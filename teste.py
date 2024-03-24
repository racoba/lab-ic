import random
maze_size = 20
NUM_TREASURES = 10
m=[['.' for a in range(maze_size)] for x in range(maze_size)]
start_row = 0
start_col = 0
end_row = 0
end_col = 0
player_pos = [random.randint(0, maze_size-1), random.randint(0, maze_size-1)]
treasures = []
for _ in range(NUM_TREASURES):  # Number of treasures
    while True:
        treasure = [random.randint(0, maze_size-1), random.randint(0, maze_size-1)]
        if treasure not in treasures and treasure != player_pos:
            treasures.append(treasure)
            break

# Generating walls and obstacles dynamically
def generate_walls():
    walls = []
    for i in range(1, maze_size-1):  # Avoid placing walls on the border
        for j in range(1, maze_size-1):
            if [i,j] != player_pos \
               and [i,j] not in treasures \
               and random.choice([True, False, False]):  
                walls.append([i, j])

    return walls

def fullfillMap():
    for treasure in treasures:
        
        m[treasure[0]][treasure[1]] = 'T'
    for wall in walls:
        m[wall[0]][wall[1]] = '#'
    for w in water:
        m[w[0]][w[1]] = '~'
    m[player_pos[0]][player_pos[1]] = 'P'
    pass
    


def generate_water(slope):
    water = []
    
    water_size = min(maze_size, maze_size) // 4

    start_x = random.randint(0, maze_size - water_size)
    start_y = random.randint(0, maze_size - water_size)

    # Fill the square with water
    for i in range(start_x, start_x + water_size):
        for j in range(start_y, start_y + water_size):
            water.append([i, j])

    return water





def solve(start_row, start_col):
    q = []
    q.append((start_row, start_col))
    visited = [[False for i in range(maze_size)] for j in range(maze_size)]
    visited[start_row][start_col] = True
    prev = [[None for i in range(maze_size)] for j in range(maze_size)]
    while len(q) > 0:
        row, col = q.pop(0)
        
        if [row, col] in treasures:
            return prev, row, col

        # Check adjacent cells
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_row = row + dr
            next_col = col + dc
            if (
                next_row >= 0 and next_row < maze_size and
                next_col >= 0 and next_col < maze_size and
                not visited[next_row][next_col] and
                (next_row,next_col) not in walls
            ):
                q.append((next_row, next_col))
                visited[next_row][next_col] = True
                prev[next_row][next_col] = (row, col)

    return None

def reconstructPath(start_row, start_col, end_row, end_col, prev):
    path = []
    row, col = end_row, end_col
    while (row, col) != (start_row, start_col):
        path.append((row, col))
        row, col = prev[row][col]
    path.append((start_row, start_col))
    path.reverse()
    return path

def bfs(start_row, start_col):
    prev, row, col = solve(start_row, start_col)
    if prev is None:
        print("Caminho não encontrado.")
        return []
    return reconstructPath(start_row, start_col, row, col, prev)


def getPLayerMovmentByList(path):
    tempPlayerPos = player_pos.copy()
    movements = []
    for p in path:
        if p == (tempPlayerPos[0] + 1, tempPlayerPos[1]):
            movements.append("DOWN")
            tempPlayerPos = p
        elif p == (tempPlayerPos[0] - 1, tempPlayerPos[1]):
            movements.append("UP")
            tempPlayerPos = p
        elif p == (tempPlayerPos[0], tempPlayerPos[1] + 1):
            movements.append("RIGHT")
            tempPlayerPos = p
        elif p == (tempPlayerPos[0], tempPlayerPos[1] - 1):
            movements.append("LEFT")
            tempPlayerPos = p
        else: print("Caminho está errado")

    return movements
    


if __name__ == '__main__':
    slope = 0.5  # This is a placeholder; adjust your slope logic as needed
    water = generate_water(slope)
    walls = generate_walls()
    fullfillMap()
    for n in m:
        print(f"""{n}""")
    print(getPLayerMovmentByList(bfs(player_pos[0], player_pos[1])))