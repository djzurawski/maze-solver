"""Depth first search and breadth first search maze solving implementations"""

__author__ = "Daniel Zurawski"
__email__ = "djzurawski@gmail.com"
__license__ = "MIT"
__version__ = "1.0"

"""Python image library required. python-pil package in apt"""
import Image
import os

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

def dfs_search(image, x, y, save_frames):
    """performs iterative depth first search starting at maze entrance (x,y)"""

    pix = image.load()
    (xmax, ymax) = image.size
    frame_number = 0

    #Good number for making DFS animated gifs
    frame_interval = 2000

    stack = []
    stack.append((x, y))

    #parent_map keeps track of what pixel discovered each new pixel for the
    #purpose of coloring the maze solution later. Help from Stack Overflow
    #http://stackoverflow.com/questions/12864004/tracing-and-returning-a-path-in-depth-first-search"""
    parent_map = {}

    while stack:

        (x, y) = stack.pop()

        #If exit found, color solution path red.
        if x == EXIT_X and y in EXIT_Y:
            print "Solution found!"
            color_solution(image, parent_map, x, y)
            return

        #if pixel not discovered or is a wall
        if image.getpixel((x, y))[0] != 0:

            #label as discovered
            pix[x, y] = GREEN

            #if user decided to save frames, save frame at defined interval
            if save_frames and (frame_number % frame_interval == 0):
                save_frame(image, frame_number)

            frame_number = frame_number + 1

            #push undiscovered edges but do bounds checking first.
            #Re-arrange order of if statements to get different DFS paths
            if x - 1 >= 0:
                stack.append((x-1, y))
                if (x-1, y) not in parent_map:
                    parent_map[(x-1, y)] = (x, y)

            if x+1 < xmax:
                stack.append((x+1, y))
                if (x+1, y) not in parent_map:
                    parent_map[(x+1, y)] = (x, y)

            if y-1 >= 0:
                stack.append((x, y-1))
                if (x, y-1) not in parent_map:
                    parent_map[(x, y-1)] = (x, y)

            if y +1 < ymax:
                stack.append((x, y+1))
                if (x, y+1) not in parent_map:
                    parent_map[(x, y+1)] = (x, y)


def bfs_search(image, x, y, save_frames):
    """performs breadth first search starting at maze entrance (x,y)"""

    pix = image.load()
    (xmax, ymax) = image.size
    frame_number = 0

    #Good number for making BFS animated gifs
    frame_interval = 10000

    queue = []
    queue.append((x, y))

    #parent_map keeps track of what pixel discovered each new pixel for the
    #purpose of coloring the maze solution later. Help from Stack Overflow
    #http://stackoverflow.com/questions/12864004/tracing-and-returning-a-path-in-depth-first-search"""
    parent_map = {}

    while queue:

        (x, y) = queue.pop(0)

        #If exit found, color solution path red.
        if x == EXIT_X and y in EXIT_Y:
            print "Solution found!"
            color_solution(image, parent_map, x, y)
            return

        #if pixel not discovered or is a wall
        if image.getpixel((x, y))[0] != 0:

            #label as discovered
            pix[x, y] = GREEN

            #if user decided to save frames, save frame at defined interval
            if save_frames and (frame_number % frame_interval == 0):
                save_frame(image, frame_number)

            frame_number = frame_number + 1

            #push undiscovered edges but do bounds checking first.
            if x - 1 >= 0:
                queue.append((x-1, y))
                if (x-1, y) not in parent_map:
                    parent_map[(x-1, y)] = (x, y)

            if x+1 < xmax:
                queue.append((x+1, y))
                if (x+1, y) not in parent_map:
                    parent_map[(x+1, y)] = (x, y)

            if y-1 >= 0:
                queue.append((x, y-1))
                if (x, y-1) not in parent_map:
                    parent_map[(x, y-1)] = (x, y)

            if y +1 < ymax:
                queue.append((x, y+1))
                if (x, y+1) not in parent_map:
                    parent_map[(x, y+1)] = (x, y)


def normalize_rgb(image):
    """Maze RGB values werent exactly 0 or 255 for black and white respectively.
        Black was in the range ~10-15 and black ~245-255. This ensures black
        and white values are 0 or 255"""

    pix = image.load()

    for x in xrange(image.size[0]):
        for y in xrange(image.size[1]):
            if image.getpixel((x, y))[0] < 200:
                pix[x, y] = BLACK
            else:
                pix[x, y] = WHITE


def color_solution(image, node_dict, x, y):
    """Colors maze solution red"""

    pix = image.load()
    pix[x, y] = RED

    while x != START_X or y != START_Y:
        (x, y) = node_dict[(x, y)]
        pix[x, y] = RED

def save_frame(image, frame_number):
    """Saves current maze image to "images" subdirectory"""

    if not os.path.exists("images"):
        os.mkdir("images")

    filename = "images/frame" + str(frame_number) + ".png"
    image.save(filename)


if __name__ == '__main__':

    #examine maze image to determine start pixels and exit pixels
    START_X = 2
    START_Y = 0
    EXIT_X = 1801
    EXIT_Y = (1794, 1795, 1796, 1798, 1799)

    im = Image.open("maze0.png")
    normalize_rgb(im)

    #change False to True to save progress images
    dfs_search(im, START_X, START_Y, False)
    #bfs_search(im, START_X, START_Y, False)

    im.save("solved_maze.png")
