import pygame 
from pygame.locals import * 
import math, heapq

# WINDOW
WIN_WIDTH, WIN_HEIGHT = 500, 500 
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("A* Algorithm Visualiser")

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# GRID 
grid = []
solution = []
start = None
end = None

# CELL CLASS
# There are 3 types of cells - Start, End, Wall
class Cell:
    def __init__(self, grid_x, grid_y):
        global start, end, grid  
        self.x = grid_x*CELL_SIZE
        self.y = grid_y*CELL_SIZE
        if start is None: # START
            self.color = GREEN 
            start = [grid_x, grid_y]
            special_cells.append(self)
        elif end is None and [grid_x, grid_y]!=start: # END
            self.color = RED
            end = [grid_x, grid_y]
            special_cells.append(self)
        else: # WALL
            if [grid_x, grid_y] != start and [grid_x, grid_y] != end:
                grid[grid_y][grid_x] = 1
                self.color = BLACK
                special_cells.append(self)
    
    def draw(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))

# INITIALIZE GRID 
CELL_SIZE = 25
for i in range(WIN_WIDTH//CELL_SIZE):
    grid.append([0 for _ in range(WIN_HEIGHT//CELL_SIZE)])

# DRAW THE GRID
special_cells = []
def DrawGrid(WIDTH, HEIGHT):
    for i in range(0, HEIGHT, CELL_SIZE):
        for j in range(0, WIDTH, CELL_SIZE):
            pygame.draw.rect(window, BLACK, (i, j, CELL_SIZE, CELL_SIZE), 1)
    for cell in special_cells:
        cell.draw()
    for square in solution:
        pygame.draw.rect(window, BLUE, (square[0]*CELL_SIZE, square[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

# CLEAR GRID 
def ClearGrid():
    global start, end
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = 0
    special_cells.clear()
    solution.clear()
    start = None
    end = None

# A* ALGORITHM

# SQUARE CLASS
class Square:
    def __init__(self):
        self.parent_i = 0  # Parent cell's row index
        self.parent_j = 0  # Parent cell's column index
        self.f = float('inf')  # Total cost of the cell (g + h)
        self.g = float('inf')  # Cost from start to this cell
        self.h = 0  # Heuristic cost from this cell to destination

# Check if a cell is valid (within the grid)
def is_valid(row, col):
    return (row >= 0) and (row < len(grid)) and (col >= 0) and (col < len(grid[0]))
 
# Check if a cell is unblocked
def is_unblocked(grid, row, col):
    return grid[row][col] == 0
 
# Check if a cell is the destination
def is_destination(row, col, dest):
    return row == dest[1] and col == dest[0]
 
# Calculate the heuristic value of a cell (Euclidean distance to destination)
def calculate_h_value(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

# Add the solution of the maze to the solution list for displaying
def trace_path(cell_details, dest):
    row = dest[0]
    col = dest[1]
 
    # Trace the path from destination to source using parent cells
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col
        solution.append((row, col))
 
    # Reverse the path to get the path from source to destination
    solution.reverse()

def a_star(grid, start, end):
    # Initialize the closed list for visited cells 
    closed_list = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    # Initialize the details of each cell 
    squares = [[Square() for _ in range(len(grid[0]))] for _ in range(len(grid))]

    # Initialize the start cell details
    i = start[0]
    j = start[1]
    squares[i][j].f = 0
    squares[i][j].g = 0
    squares[i][j].h = 0
    squares[i][j].parent_i = i
    squares[i][j].parent_j = j

    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    # Initialize the flag for whether destination is found
    found_dest = False

    # Main loop of A* Search algorithm
    while len(open_list) > 0:
        # Pop the cell with the smallest f value from the open list
        p = heapq.heappop(open_list)

        # Mark the cell as visited
        i = p[1]
        j = p[2]
        closed_list[i][j] = True

        # For each direction, check the successors
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]
        
            # If the successor is valid, unblocked, and not visited
            if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                # If the successor is the destination
                if is_destination(new_i, new_j, end):
                    # Set the parent of the destination cell
                    squares[new_i][new_j].parent_i = i
                    squares[new_i][new_j].parent_j = j
                    print("The destination cell is found")
                    # Trace and print the path from source to destination
                    trace_path(squares, end)
                    found_dest = True
                    return
                else:
                    # Calculate the new f, g, and h values
                    g_new = squares[i][j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, end)
                    f_new = g_new + h_new
 
                    # If the cell is not in the open list or the new f value is smaller
                    if squares[new_i][new_j].f == float('inf') or squares[new_i][new_j].f > f_new:
                        # Add the cell to the open list
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        # Update the cell details
                        squares[new_i][new_j].f = f_new
                        squares[new_i][new_j].g = g_new
                        squares[new_i][new_j].h = h_new
                        squares[new_i][new_j].parent_i = i
                        squares[new_i][new_j].parent_j = j
 
    # If the destination is not found after visiting all cells
    if not found_dest:
        print("Failed to find the destination cell")

# MAIN PROGRAM LOOP
running = True
clock = pygame.time.Clock()
solving = False
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                ClearGrid()
            if event.key == pygame.K_SPACE:
                solving = True
                a_star(grid, start, end)
                solving = False
    
    # check if mouse is down and moving to make the walls
    if pygame.mouse.get_pressed()[0] and not solving:
        x, y = pygame.mouse.get_pos()
        grid_x = x // CELL_SIZE
        grid_y = y // CELL_SIZE
        # check to ensure they are not out of bounds
        if grid_x < len(grid) and grid_y < len(grid[0]):
            cell = Cell(grid_x, grid_y)
    
    window.fill(WHITE)
    DrawGrid(WIN_WIDTH, WIN_HEIGHT)

    pygame.display.update()