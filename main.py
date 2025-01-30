import os
import random
import pygame
from pygame.locals import *

from objects import World, Player, Player2, Button, draw_lines, load_level, draw_text, sounds

SIZE = WIDTH , HEIGHT= 1000, 650
tile_size = 50

pygame.init()
win = pygame.display.set_mode(SIZE)
pygame.display.set_caption('DASH')
clock = pygame.time.Clock()
FPS = 30
bg1 = pygame.image.load('assets/BG1.png')
bg2 = pygame.image.load('assets/BG2.png')
bg4 = pygame.image.load('assets/BG4.png')
bg5 = pygame.image.load('assets/BG5.png')
bg = bg4
sun = pygame.image.load('assets/sun.png')
jungle_dash = pygame.image.load('assets/jungle dash.png')
you_won = pygame.image.load('assets/won.png')
level = 1
max_level = len(os.listdir('levels/'))
data = load_level(level)

player_pos_1 = (10, 340)
player_pos_2 = (20, 340)

water_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
forest_group = pygame.sprite.Group()
diamond_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
bridge_group = pygame.sprite.Group()
groups = [water_group, lava_group, forest_group, diamond_group, enemies_group, exit_group, platform_group,
			bridge_group]
world = World(win, data, groups)
player1 = Player(win, player_pos_1, world, groups)
player2 = Player2(win, player_pos_2, world, groups)

play= pygame.image.load('assets/play.png')
replay = pygame.image.load('assets/replay.png')
home = pygame.image.load('assets/home.png')
exit = pygame.image.load('assets/exit.png')
setting = pygame.image.load('assets/setting.png')

play_btn = Button(play, (128, 64), WIDTH//2 - WIDTH // 16, HEIGHT//2)
replay_btn  = Button(replay, (45,42), WIDTH//2 - 110, HEIGHT//2 + 20)
home_btn  = Button(home, (45,42), WIDTH//2 - 20, HEIGHT//2 + 20)
exit_btn  = Button(exit, (45,42), WIDTH//2 + 70, HEIGHT//2 + 20)

def reset_level(level):
	global world, cur_score_1, cur_score_2

	data = load_level(level)
	if data:
		for group in groups:
			group.empty()
		world = World(win, data, groups)
		player1.reset(win, player_pos_1, world, groups)
		player2.reset(win, player_pos_2, world, groups)
	return world

score_1, score_2 = 0, 0
cur_score_1, cur_score_2 = 0, 0
lives_1, lives_2 = 3, 3

main_menu = True
game_over = False
level_won_1 = False
level_won_2 = False
game_won = False
running = True
game_over_player = None

while running:
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False

	pressed_keys = pygame.key.get_pressed()

	win.blit(bg, (0,0))
	win.blit(sun, (40,40))
	world.draw()
	for group in groups:
		group.draw(win)

	if main_menu:
		win.blit(jungle_dash, (WIDTH//2 - WIDTH//8, HEIGHT//4))

		play_game = play_btn.draw(win)
		if play_game:
			main_menu = False
			game_over = False
			game_won = False
			score_1, score_2 = 0, 0
			lives_1, lives_2 = 3, 3

	else:
		if not game_over and not game_won:
			enemies_group.update(player1)
			enemies_group.update(player2)
			platform_group.update()
			exit_group.update(player1)
			exit_group.update(player2)

			if pygame.sprite.spritecollide(player1, diamond_group, True):
				sounds[0].play()
				cur_score_1 += 1
				score_1 += 1
			if pygame.sprite.spritecollide(player2, diamond_group, True):
				sounds[0].play()
				cur_score_2 += 1
				score_2 += 1

			draw_text(win, f"P1: {score_1} | Lives: {lives_1}", ((WIDTH // 4), tile_size // 2 + 10))
			draw_text(win, f"P2: {score_2} | Lives: {lives_2}", ((WIDTH // 4) * 3, tile_size // 2 + 10))
			
		game_over1, level_won_1 = player1.update(pressed_keys, game_over, level_won_1, game_won)
		game_over2, level_won_2 = player2.update(pressed_keys, game_over, level_won_2, game_won)

		if game_over1:
			if lives_1 > 0:
				lives_1 = max(lives_1 - 1, 0)
			if lives_1 == 0:
				game_over_player = "Player 1"
			else:
				world = reset_level(level)
				game_over = False

		if game_over2:
			if lives_2 > 0:
				lives_2 = max(lives_2 - 1, 0)
			if lives_2 == 0:
				game_over_player = "Player 2"
			else:
				world = reset_level(level)
				game_over = False

		if lives_1 == 0 or lives_2 == 0:
			game_over = True
			winner = "Player 1" if lives_1 > lives_2 else "Player 2" if lives_2 > lives_1 else "Tie"
			draw_text(win, f"Game Over! {game_over_player} lost!", (WIDTH // 2 - 80, HEIGHT // 2 - 35))
			draw_text(win, f"Player 1: {score_1} Player 2: {score_2}", (440, 400))

			if replay_btn.draw(win):
				level = 1
				world = reset_level(level)
				lives_1, lives_2 = 3, 3
				game_over = False
			if home_btn.draw(win):
				main_menu = True
				level = 1
				world = reset_level(level)
			if exit_btn.draw(win):
				running = False

		if level_won_1 or level_won_2:
			if level <= max_level:
				level += 1
				if level % 3 == 0:
					lives_1 += 1
					lives_2 += 1
				game_level = f'levels/level{level}_data'
				if os.path.exists(game_level):
					data = []
					world = reset_level(level)
					level_won_1 = False
					level_won_2 = False

				bg = random.choice([bg4, bg5, bg2, bg1])
			else:
				game_won = True
				bg = bg4
				win.blit(you_won, (WIDTH//4, HEIGHT // 4))

				winner_text = "P1 Wins!" if score_1 > score_2 else "P2 Wins!" if score_2 > score_1 else "It's a Tie!"
				draw_text(win, winner_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

				home = home_btn.draw(win)

				if home:
					game_over = True
					main_menu = True
					level_won_1 = False
					level_won_2 = False
					level = 1
					world = reset_level(level)

	pygame.display.flip()
	clock.tick(FPS)

pygame.quit()