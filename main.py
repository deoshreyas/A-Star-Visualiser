import pygame 
from pygame.locals import * 

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
start = None
end = None

# CELL CLASS
# There are 3 types of cells - Start, End, Wall
class Cell:
    def __init__(self, grid_x, grid_y):
        global start, end 
        self.x = grid_x*CELL_SIZE
        self.y = grid_y*CELL_SIZE
        if start is None: # START
            self.color = GREEN 
            start = [grid_x, grid_y]
        elif end is None: # END
            self.color = RED
            end = [grid_x, grid_y]
        else: # WALL
            self.color = BLACK
    
    def draw(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))

# DRAW THE GRID 
CELL_SIZE = 25
special_cells = []
def DrawGrid(WIDTH, HEIGHT):
    for i in range(0, HEIGHT, CELL_SIZE):
        row = []
        for j in range(0, WIDTH, CELL_SIZE):
            pygame.draw.rect(window, BLACK, (i, j, CELL_SIZE, CELL_SIZE), 1)
            row.append(0)
        grid.append(row)
    for cell in special_cells:
        cell.draw()

# CLEAR GRID 
def ClearGrid():
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = 0
    special_cells.clear()

# MAIN PROGRAM LOOP
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            grid_x = x // CELL_SIZE
            grid_y = y // CELL_SIZE
            grid[grid_x][grid_y] = 1
            cell = Cell(grid_x, grid_y)
            special_cells.append(cell)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                ClearGrid()
    
    window.fill(WHITE)
    DrawGrid(WIN_WIDTH, WIN_HEIGHT)

    pygame.display.update()