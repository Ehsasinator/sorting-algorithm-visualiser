import pygame
import random
import math
pygame.init()

class DrawInformation:

    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 128, 128, 128
    BACKGROUND_COLOUR = WHITE
    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)
    SIDE_PAD = 100
    TOP_PAD = 150
    GRADIENTS = [
        GREY,
        [160,160,160],
        [192,192,192]
    ]
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption("sorting visualiser")
        self.set_list(lst)

    def set_list(self,lst):
        self.lst = lst
        self.min_value = min(lst)
        self.max_value = max(lst)

        self.block_width = round((self.width-self.SIDE_PAD)/len(lst))
        self.block_height = math.floor((self.height-self.TOP_PAD)/(self.max_value-self.min_value))
        self.start_x = self.SIDE_PAD//2

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOUR)
    controls = draw_info.FONT.render(f"{algo_name} - {'ascending' if ascending else 'descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(controls, ((draw_info.width - controls.get_width())-draw_info.SIDE_PAD*2, 5))
    controls = draw_info.FONT.render("R - reset | SPACE - sort | A - ascending | D - descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls,((draw_info.width-controls.get_width()), 35))
    sorting = draw_info.FONT.render("I - insertion sort | B - bubble sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting,((draw_info.width - controls.get_width()), 65))
    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, colour_positions={}, clear_bg = False):
    lst = draw_info.lst
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD,draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOUR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i*draw_info.block_width
        y = draw_info.height - (val - draw_info.min_value)*draw_info.block_height

        colour = draw_info.GRADIENTS[i%3]
        if i in colour_positions:
            colour = colour_positions[i]
        pygame.draw.rect(draw_info.window, colour, (x,y,draw_info.block_width,draw_info.height))
    if clear_bg:
        pygame.display.update()
def generate_list(n, min_value, max_value):
    lst = []
    for _ in range(n):
        val = random.randint(min_value, max_value)
        lst.append(val)
    return lst

def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst
    for i in range(len(lst)-1):
        for j in range(len(lst)-i-1):
            num1 = lst[j]
            num2 = lst[j+1]

            if (num1>num2 and ascending) or (num1<num2 and not ascending):
                lst[j] = num2
                lst[j+1] = num1
                draw_list(draw_info, {j:draw_info.GREEN, j+1:draw_info.RED},True)
                yield True
    return lst

def insertion_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(1,len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i-1] > current and ascending
            descending_sort = i > 0 and lst[i-1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break
            lst[i] = lst[i-1]
            i = i-1
            lst[i] = current
            draw_list(draw_info, {i-1:draw_info.GREEN, i:draw_info.RED}, True)
            yield True
    return lst


def main():
    run = True
    n = 50
    min_val = 1
    max_val = 100
    lst = generate_list(n,min_val,max_val)
    draw_info = DrawInformation(800, 600, lst)
    clock = pygame.time.Clock()
    sorting = False
    ascending = True
    sorting_algorithm = insertion_sort
    sorting_algo_name = "insertion sort"
    sorting_algorithm_generator = None
    while run:
        draw(draw_info, sorting_algo_name,ascending)
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info,sorting_algo_name,ascending)




        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_list(n,min_val,max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "insertion sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "bubble sort"

if __name__ == "__main__":
    main()
