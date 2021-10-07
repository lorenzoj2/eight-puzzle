import pygame
import random
import math

from informed_search import InformedSearch

BLACK = (0, 0, 0)
GREY = (200, 200, 200)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)

WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500


class Puzzle:
    def __init__(self, tiles=None):
        if tiles is None:
            tiles = []

        self.tiles = tiles
        self.generate_tiles()
        self.original_state = []

        pygame.init()
        pygame.display.set_caption('Eight Puzzle')
        self.screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.screen.fill(WHITE)
        self.draw_tiles(False)

    def main(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.switch_tiles_click(event)
                    if self.check_win():
                        self.draw_tiles(True)
                    else:
                        self.draw_tiles(False)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        current_seq = [row[1] for row in self.tiles]
                        self.original_state = current_seq
                        solver = InformedSearch(current_seq)
                        path = solver.solve()

                        if path:
                            print("Iterations: ", solver.iter)
                            print("Moves: ", len(path))
                            for move in path:
                                self.draw_tiles(False, move)
                                pygame.display.flip()
                                pygame.time.wait(100)
                                self.switch_tiles(move)

                                if self.check_win():
                                    self.draw_tiles(True)
                                    pygame.display.flip()
                                else:
                                    self.draw_tiles(False)
                                    pygame.display.flip()
                                    pygame.time.wait(40)
                        elif path is None:
                            print("Solution not found.")

                    if event.key == pygame.K_SPACE:
                        self.set_tiles(self.original_state)
                        self.draw_tiles(False)

                    if event.key == pygame.K_r:
                        self.randomize_tiles()
                        self.draw_tiles(False)

            pygame.display.flip()

        pygame.quit()

    def generate_tiles(self):
        grid = []
        block_size = WINDOW_WIDTH / 3

        for y in range(3):
            for x in range(3):
                rect = pygame.Rect(x * (block_size + 1), y * (block_size + 1), block_size, block_size)
                grid.append(rect)

        tiles = []

        numbers = self.tiles if self.tiles else random.sample([1, 2, 3, 4, 5, 6, 7, 8, 0], 9)
        labels = ['(0, 0)', '(1, 0)', '(2, 0)', '(0, 1)', '(1, 1)', '(2, 1)', '(0, 2)', '(1, 2)', '(2, 2)']

        for i in range(len(grid)):
            tiles.append([grid[i], numbers[i], labels[i]])

        self.tiles = tiles

        while not self.is_solvable():
            self.randomize_tiles()

    def draw_tiles(self, win, num=None):
        tile_color = GREY
        if win:
            tile_color = GREEN

        self.screen.fill(WHITE)

        font_name = pygame.font.get_default_font()
        font = pygame.font.Font(font_name, 40)
        small_font = pygame.font.Font(font_name, 11)

        block_size = WINDOW_WIDTH / 3

        for tile in self.tiles:
            if tile[1] == num:
                pygame.draw.rect(self.screen, GREEN, tile[0])
            else:
                pygame.draw.rect(self.screen, tile_color, tile[0])

            text = tile[1]
            text = '' if text == 0 else text
            label = tile[2]
            tile_label = font.render(f'{text}', True, BLACK)
            pos_label = small_font.render(f'{label}', True, BLACK)
            self.screen.blit(tile_label, (tile[0].x + (block_size / 2), tile[0].y + (block_size / 2)))
            self.screen.blit(pos_label, (tile[0].x + (block_size / 2) - 2, tile[0].y + (block_size / 2) + 50))

    def get_empty(self):
        for tile in self.tiles:
            if tile[1] == 0:
                return [math.floor(tile[0].x / (WINDOW_WIDTH/ 3)), math.floor(tile[0].y / (WINDOW_HEIGHT / 3))]

        return None

    def get_clicked(self, event):
        event_pos = [math.floor(event.pos[0] / (WINDOW_WIDTH / 3)), math.floor(event.pos[1] / (WINDOW_HEIGHT / 3))]

        for tile in self.tiles:
            tile_pos = [math.floor(tile[0].x / (WINDOW_WIDTH / 3)), math.floor(tile[0].y / (WINDOW_HEIGHT / 3))]
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

    def randomize_tiles(self):
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        random.shuffle(numbers)

        for i in range(len(numbers)):
            self.tiles[i][1] = numbers[i]

        while not self.is_solvable():
            self.randomize_tiles()

    def set_tiles(self, tiles):
        for i in range(len(tiles)):
            self.tiles[i][1] = tiles[i]

    def check_win(self):
        current_seq = [row[1] for row in self.tiles]
        win = [1, 2, 3, 4, 5, 6, 7, 8, 0]

        if current_seq == win:
            return True

        return False

    def get_inversions(self):
        inversions = 0

        for i in range(0, 9):
            for j in range(i + 1, 9):
                if self.tiles[j][1] != 0 and self.tiles[i][1] != 0 and self.tiles[i][1] > self.tiles[j][1]:
                    inversions += 1

        return inversions

    def is_solvable(self):
        inversions = self.get_inversions()

        return inversions % 2 == 0


custom_state1 = [2, 3, 6, 1, 4, 8, 7, 5, 0]
custom_state2 = [1, 2, 3, 0, 4, 6, 7, 5, 8]
custom_state3 = [5, 7, 2, 6, 0, 4, 1, 8, 3]
custom_state4 = [2, 4, 0, 6, 5, 3, 7, 1, 8]
custom_state5 = [8, 6, 7, 2, 5, 4, 3, 0, 1]
custom_state6 = [6, 4, 7, 8, 5, 0, 3, 2, 1]
Game = Puzzle(custom_state4)
Game.main()
