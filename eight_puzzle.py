import pygame
import random
import math

BLACK = (0, 0, 0)
GREY = (200, 200, 200)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLUE = (135, 206, 250)

WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500


def main():
    pygame.init()
    pygame.display.set_caption('Eight Puzzle')
    screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
    screen.fill(WHITE)

    tiles = generate_tiles()
    draw_tiles(screen, tiles, False)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                screen.fill(WHITE)
                tiles = switch_tiles(event, tiles)
                if check_win(tiles):
                    draw_tiles(screen, tiles, True)
                else:
                    draw_tiles(screen, tiles, False)

        pygame.display.flip()

    pygame.quit()


def draw_tiles(screen, tiles, win):
    tile_color = GREY
    if win:
        tile_color = GREEN

    screen.fill(WHITE)

    font_name = pygame.font.get_default_font()
    font = pygame.font.Font(font_name, 40)
    small_font = pygame.font.Font(font_name, 11)

    block_size = WINDOW_WIDTH / 3

    for tile in tiles:
        pygame.draw.rect(screen, tile_color, tile[0])
        text = tile[1]
        label = tile[2]
        tile_label = font.render(f"{text}", True, BLACK)
        pos_label = small_font.render(f"{label}", True, BLACK)
        screen.blit(tile_label, (tile[0].x + (block_size / 2), tile[0].y + (block_size / 2)))
        screen.blit(pos_label, (tile[0].x + (block_size / 2) - 2, tile[0].y + (block_size / 2) + 50))


def generate_tiles():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, '']
    labels = ['(0, 0)', '(1, 0)', '(2, 0)', '(0, 1)', '(1, 1)', '(2, 1)', '(0, 2)', '(1, 2)', '(2, 2)']
    block_size = WINDOW_WIDTH / 3

    grid = []
    for y in range(3):
        for x in range(3):
            rect = pygame.Rect(x * (block_size + 1), y * (block_size + 1), block_size, block_size)
            grid.append(rect)

    random.shuffle(numbers)

    tiles = []
    for i in range(len(grid)):
        tiles.append([grid[i], numbers[i], labels[i]])

    return tiles


def get_empty(tiles):
    for tile in tiles:
        if tile[1] == '':
            return [math.floor(tile[0].x / (WINDOW_HEIGHT / 3)), math.floor(tile[0].y / (WINDOW_HEIGHT / 3))]
    return None


def get_clicked(event, tiles):
    event_pos = [math.floor(event.pos[0] / (WINDOW_HEIGHT / 3)), math.floor(event.pos[1] / (WINDOW_HEIGHT / 3))]

    for tile in tiles:
        tile_pos = [math.floor(tile[0].x / (WINDOW_HEIGHT / 3)), math.floor(tile[0].y / (WINDOW_HEIGHT / 3))]
        if event_pos == tile_pos:
            return event_pos

    return None


def switch_tiles(event, tiles):
    empty_rect = get_empty(tiles)
    empty = 0
    if empty_rect is not None:
        empty = empty_rect[0] + 3 * empty_rect[1]

    clicked_rect = get_clicked(event, tiles)
    clicked = 0
    if clicked_rect is not None:
        clicked = clicked_rect[0] + 3 * clicked_rect[1]

    is_valid_x = abs(clicked_rect[0] - empty_rect[0])
    is_valid_y = abs(clicked_rect[1] - empty_rect[1])

    if is_valid_x != is_valid_y and is_valid_x <= 1 and is_valid_y <= 1:
        tiles[empty][1], tiles[clicked][1] = tiles[clicked][1], tiles[empty][1]
    return tiles


def check_win(tiles):
    in_order = [row[1] for row in tiles]
    win = [1, 2, 3, 4, 5, 6, 7, 8, '']

    if in_order == win:
        return True

    return False


main()
