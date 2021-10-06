import pygame
import random
import math

from informed_search import InformedSearch

BLACK = (0, 0, 0)
GREY = (200, 200, 200)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLUE = (135, 206, 250)

WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500


def generate_tiles(custom_state):
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    labels = ['(0, 0)', '(1, 0)', '(2, 0)', '(0, 1)', '(1, 1)', '(2, 1)', '(0, 2)', '(1, 2)', '(2, 2)']
    block_size = WINDOW_WIDTH / 3

    grid = []
    for y in range(3):
        for x in range(3):
            rect = pygame.Rect(x * (block_size + 1), y * (block_size + 1), block_size, block_size)
            grid.append(rect)

    if custom_state:
        numbers = custom_state
    else:
        random.shuffle(numbers)

    tiles = []
    for i in range(len(grid)):
        tiles.append([grid[i], numbers[i], labels[i]])

    return tiles


class Puzzle:
    def __init__(self, tiles=None):
        if tiles is None:
            tiles = []

        self.tiles = generate_tiles(tiles)

    def main(self):
        pygame.init()
        pygame.display.set_caption('Eight Puzzle')
        screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        screen.fill(WHITE)

        self.draw_tiles(screen, False)

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.switch_tiles_click(event)
                    if self.check_win():
                        self.draw_tiles(screen, True)
                    else:
                        self.draw_tiles(screen, False)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        current_seq = [row[1] for row in self.tiles]

                        solver = InformedSearch(current_seq)
                        path = solver.solve()

                        print(f'It took {path[0]} iterations to find a path with {path[1]} moves.')

            pygame.display.flip()

        pygame.quit()

    def draw_tiles(self, screen, win):
        tile_color = GREY
        if win:
            tile_color = GREEN

        screen.fill(WHITE)

        font_name = pygame.font.get_default_font()
        font = pygame.font.Font(font_name, 40)
        small_font = pygame.font.Font(font_name, 11)

        block_size = WINDOW_WIDTH / 3

        for tile in self.tiles:
            pygame.draw.rect(screen, tile_color, tile[0])
            text = tile[1]
            text = '' if text == 0 else text
            label = tile[2]
            tile_label = font.render(f'{text}', True, BLACK)
            pos_label = small_font.render(f'{label}', True, BLACK)
            screen.blit(tile_label, (tile[0].x + (block_size / 2), tile[0].y + (block_size / 2)))
            screen.blit(pos_label, (tile[0].x + (block_size / 2) - 2, tile[0].y + (block_size / 2) + 50))

    def get_empty(self):
        for tile in self.tiles:
            if tile[1] == 0:
                return [math.floor(tile[0].x / (WINDOW_HEIGHT / 3)), math.floor(tile[0].y / (WINDOW_HEIGHT / 3))]
        return None

    def get_clicked(self, event):
        event_pos = [math.floor(event.pos[0] / (WINDOW_HEIGHT / 3)), math.floor(event.pos[1] / (WINDOW_HEIGHT / 3))]

        for tile in self.tiles:
            tile_pos = [math.floor(tile[0].x / (WINDOW_HEIGHT / 3)), math.floor(tile[0].y / (WINDOW_HEIGHT / 3))]
            if event_pos == tile_pos:
                return event_pos

        return None

    def switch_tiles_click(self, event):
        empty_rect = self.get_empty()
        empty = 0
        if empty_rect is not None:
            empty = empty_rect[0] + 3 * empty_rect[1]

        clicked_rect = self.get_clicked(event)
        clicked = 0
        if clicked_rect is not None:
            clicked = clicked_rect[0] + 3 * clicked_rect[1]

        is_valid_x = abs(clicked_rect[0] - empty_rect[0])
        is_valid_y = abs(clicked_rect[1] - empty_rect[1])

        if is_valid_x != is_valid_y and is_valid_x <= 1 and is_valid_y <= 1:
            self.tiles[empty][1], self.tiles[clicked][1] = self.tiles[clicked][1], self.tiles[empty][1]
        return self.tiles

    def switch_tiles(self, num):
        empty_rect = self.get_empty()
        empty = 0
        selected = 0

        if empty_rect is not None:
            empty = empty_rect[0] + 3 * empty_rect[1]

        for i in range(len(self.tiles)):
            if self.tiles[i][1] == num:
                selected = i

        self.tiles[empty][1], self.tiles[selected][1] = self.tiles[selected][1], self.tiles[empty][1]

        return self.tiles

    def check_win(self):
        current_seq = [row[1] for row in self.tiles]
        win = [1, 2, 3, 4, 5, 6, 7, 8, 0]

        if current_seq == win:
            return True

        return False


custom_state1 = [2, 3, 6, 1, 4, 8, 7, 5, 0]
custom_state2 = [1, 2, 3, 0, 4, 6, 7, 5, 8]
custom_state3 = [5, 7, 2, 6, 0, 4, 1, 8, 3]

Game = Puzzle(custom_state3)
Game.main()
