import pygame_menu
import pygame, sys, random
from pygame import mixer
import sqlite3, os

global _music_config
global _sfx_config
global _firstrun_cfg
global _epilepsy_mode


def first_run_cek():
    global _firstrun_cfg
    con = sqlite3.connect("config.db")
    cursor = con.cursor()
    cursor.execute("SELECT firstrun from config")
    firstrun_list = cursor.fetchall()


def create_cfg():
    if (os.path.exists("config.db") == False):
        con = sqlite3.connect("config.db")
        cursor = con.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS config(firstrun INT, player_name TEXT,install_date TEXT,music INT,sfx INT,passed_ep INT,_epilepsy_mode INT)")
        con.commit()
        cursor.execute("INSERT INTO config VALUES(1,'player','22.07.2022',1,1,0,'0')")
        con.commit()
    else:
        con = sqlite3.connect("config.db")
        cursor = con.cursor()
        cursor.execute("Update config set firstrun = 0")
        con.commit()
        first_run_cek()


def music_db_update(state):
    con = sqlite3.connect("config.db")
    cursor = con.cursor()
    global _music_config
    if state == 1:
        cursor.execute("Update config set music = 1 ")
        con.commit()
        _music_config = 1
    else:
        cursor.execute("Update config set music = 0 ")
        con.commit()
        _music_config = 0


def take_music_config():
    global _music_config
    con = sqlite3.connect("config.db")
    cursor = con.cursor()
    cursor.execute("SELECT music from config")
    music_cfg_list = cursor.fetchall()
    _music_config = music_cfg_list[0][0]


def music_config(value=bool) -> None:
    if (value == 0):
        music_db_update(0)
        menu_sfx_music("main_menu_bg_music", "pause", 1)
    else:
        music_db_update(1)
        menu_sfx_music("main_menu_bg_music", "start", 1)


def epilepsy_mode_change(value=int) -> None:
    global _epilepsy_mode
    con = sqlite3.connect("config.db")
    cursor = con.cursor()
    if (value == 1):
        cursor.execute("Update config set _epilepsy_mode = 1 ")
        con.commit()
        _epilepsy_mode = value
    else:
        cursor.execute("Update config set _epilepsy_mode = 0 ")
        con.commit()
        _epilepsy_mode = value


def sfx_db_update(state):
    con = sqlite3.connect("config.db")
    cursor = con.cursor()
    global _sfx_config
    if state == 1:
        cursor.execute("Update config set sfx = 1 ")
        con.commit()
        _sfx_config = 1
    else:
        cursor.execute("Update config set sfx = 0 ")
        con.commit()
        _sfx_config = 0


def take_sfx_config():
    global _sfx_config
    con = sqlite3.connect("config.db")
    cursor = con.cursor()
    cursor.execute("SELECT sfx from config")
    _sfx_cfg_list = cursor.fetchall()
    _sfx_config = _sfx_cfg_list[0][0]


def sfx_config(value=bool) -> None:
    if (value == 0):
        sfx_db_update(0)
    else:
        sfx_db_update(1)


def take_epilepsy_mode_config():
    global _epilepsy_mode
    con = sqlite3.connect("config.db")
    cursor = con.cursor()
    cursor.execute("SELECT _epilepsy_mode from config")
    epilepsy_mode_list = cursor.fetchall()
    _epilepsy_mode = epilepsy_mode_list[0][0]


create_cfg()
first_run_cek()
take_music_config()
take_sfx_config()
take_epilepsy_mode_config()

pygame.init()
pygame.font.init()
pygame.joystick.init()
mixer.init()

screen_width = 600
screen_height = 600

gridsize = 20
grid_width = screen_width / gridsize
grid_hight = screen_height / gridsize

siyah = (0, 0, 0)
acik_siyah = (28, 28, 28)
food_color_list = [(224, 4, 36), (0, 255, 0), (0, 13, 255), (255, 230, 22)]
self_color = (255, 255, 255)

up = (0, -1)
down = (0, 1)
right = (1, 0)
left = (-1, 0)

ABOUT_TEXT = "PySnake\nV1.0 RELEASE \n by Mdd"
CHOICE_EP_TEXT = "CHOICE EPISODE"

main_menu_bg_music = pygame.mixer.Sound("./resources/music_bg_main_menu.mp3")
free_mode_bg_music = pygame.mixer.Sound("./resources/music_bg_free_mode.mp3")
pause_menu_bg_music = pygame.mixer.Sound(".//resources/music_bg_pause_menu.mp3")
ep1_bg_music = pygame.mixer.Sound("./resources/music_bg_ep1.mp3")
crash_sfx = pygame.mixer.Sound("./resources/sfx_crash.wav")
eat_sfx = pygame.mixer.Sound("./resources/sfx_eat.mp3")
passing_ep_sfx = pygame.mixer.Sound("./resources/sfx_ep_pass.mp3")


pygame.init()
clock = pygame.time.Clock()
pygame.joystick.init()
can_back_main_menu = False

pygame.display.set_caption("PySnake V1.0 RELEASE ")
screen = pygame.display.set_mode((screen_width, screen_height))

main_menu_surface = pygame.display.set_mode((600, 600))
settings_surface = pygame.display.set_mode((600, 600))
pause_menu_surface = pygame.display.set_mode((600, 600))
about_menu_surface = pygame.display.set_mode((600, 600))
player_menu_surface = pygame.display.set_mode((600, 600))

game_surface = pygame.Surface(screen.get_size())
game_surface = game_surface.convert()

score_font = pygame.font.SysFont("SegoeUI Variable Display", 20)
version_font = pygame.font.SysFont("SegoeUI Variable Display", 20)

main_menu_theme = pygame_menu.Theme(background_color=(0, 0, 0),
                                    title_background_color=(28, 28, 28),
                                    title_font_shadow=False,
                                    widget_padding=25,
                                    widget_font=pygame_menu.font.FONT_BEBAS,
                                    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE)

settings_theme = pygame_menu.Theme(background_color=(0, 0, 0),
                                   title_background_color=(28, 28, 28),
                                   title_font_shadow=False,
                                   widget_padding=25,
                                   widget_alignment=pygame_menu.locals.ALIGN_CENTER,
                                   widget_font=pygame_menu.font.FONT_BEBAS,
                                   title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE,
                                  )

pause_menu_theme = pygame_menu.Theme(background_color=(0, 0, 0, 0),
                                     title_background_color=(28, 28, 28),
                                     title_font_shadow=False,
                                     widget_padding=25,
                                     widget_font=pygame_menu.font.FONT_BEBAS,
                                     title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE)
pause_menu_theme.set_background_color_opacity(0.2)

about_menu = pygame_menu.Menu("ABOUT GAME", 600, 600, theme=main_menu_theme)

about_menu.add.label(ABOUT_TEXT, max_char=10)

episode_choice_menu = pygame_menu.Menu("CHOOSE EPISODE", 600, 600, theme=main_menu_theme)

episode_choice_menu.add.button("EPISODE 2")

game_mode_menu = pygame_menu.Menu("CHOOSE GAME MODE", 600, 600, theme=main_menu_theme)
game_mode_menu.add.button("EPISODES", episode_choice_menu)
game_mode_menu.add.button("FREE MODE")

ayarlar_menu = pygame_menu.Menu('SETTINGS', 600, 600, theme=settings_theme)

ayarlar_menu.add.toggle_switch("MUSIC", _music_config, state_text=("Passive", "Active"), onchange=music_config)
ayarlar_menu.add.toggle_switch("SFX", _sfx_config, state_text=("Passive", "Active"), onchange=sfx_config)
ayarlar_menu.add.toggle_switch("EPILEPSY MODE", _epilepsy_mode, state_text=("Passive", "Active"),
                               onchange=epilepsy_mode_change)


def menu_sfx_music(sound_name, action, music_state):
    if (music_state != 0):
        if (sound_name == "main_menu_bg_music"):
            if (action == "start"):
                pygame.mixer.Channel(0).play(main_menu_bg_music, 64)
            elif (action == "pause"):
                pygame.mixer.Channel(0).pause()
            elif (action == "continue"):
                pygame.mixer.Channel(0).unpause()

how_to_menu = pygame_menu.Menu("HOW TO PLAY",600,600,theme=settings_theme)
how_to_menu.add.label("HOW   TO   PLAY\nWASD   or   AXIS: Control Snake\nSPACE: Pause Game")
main_menu = pygame_menu.Menu("PYSNAKE V1.0 RELEASE", 600, 600, theme=main_menu_theme)

main_menu.add.button("SETTINGS", ayarlar_menu)
main_menu.add.button("ABOUT GAME", about_menu)
main_menu.add.button("HOW TO PLAY",how_to_menu)
main_menu.add.button('EXIT GAME', pygame_menu.events.EXIT)


class ep1():
    def __init__(self):
        pause_menu = pygame_menu.Menu('PAUSED', 600, 600, theme=pause_menu_theme)
        pause_menu.add.button("CONTINUE GAME", self.continue_game)
        pause_menu.add.button("RESTART", self.restart_game)
        pause_menu.add.button("MAIN MENU", self.back_to_main_menu)

        self.pause_menu = pause_menu
        self.episode_name_text = pygame.font.SysFont("SegoeUI Variable Display", 20)
        self.anamenu = main_menu
        self.episode_choose_menu = episode_choice_menu
        self.passed_episode_font = pygame.font.SysFont("Arial Bold", 75)
        self.snake_positions = [(0, 580)]
        self.snake_start_position = (0, 580)
        self.snake_lenght = 5
        self.snake_direction = up
        self.snake_color = (5, 249, 1)
        self.snake_score = 0
        self.yemek_pozisyon = (280, 320)
        self.duvar_pozisyon = (0, 0)
        self.duvar_renk = (255, 255, 255)
        self._music_config = _music_config

    def restart_game(self):
        self.reset()
        self.play_music("pause_menu_music", "pause", _music_config)
        self.start_game()


    def finish_ep_save(self):
        con = sqlite3.connect("config.db")
        cursor = con.cursor()
        cursor.execute("Update config set passed_ep = 1")
        con.commit()

    def play_music(self, music_name, action, state):
        if (state != 0):
            if (music_name == "game_bg_music"):
                if (action == "start"):
                    pygame.mixer.Channel(1).play(ep1_bg_music, 64)
                elif (action == "pause"):
                    pygame.mixer.Channel(1).pause()
                elif (action == "continue"):
                    pygame.mixer.Channel(1).unpause()

            elif (music_name == "pause_menu_music"):
                if (action == "start"):
                    pygame.mixer.Channel(2).play(pause_menu_bg_music, 64)
                elif (action == "pause"):
                    pygame.mixer.Channel(2).pause()
                elif (action == "continue"):
                    pygame.mixer.Channel(2).unpause()

    def play_sfx(self, sfx_name, action, state):
        if (state != 0):
            if (sfx_name == "eat"):
                if (action == "start"):
                    pygame.mixer.Channel(3).play(eat_sfx)
                elif (action == "pause"):
                    pygame.mixer.Channel(3).pause()
                elif (action == "continue"):
                    pygame.mixer.Channel(3).unpause()
            elif (sfx_name == "crash"):
                if (action == "start"):
                    pygame.mixer.Channel(4).play(crash_sfx)
                elif (action == "pause"):
                    pygame.mixer.Channel(4).pause()
                elif (action == "continue"):
                    pygame.mixer.Channel(4).unpause()
            elif (sfx_name == "gecme"):
                if (action == "start"):
                    pygame.mixer.Channel(5).play(passing_ep_sfx)
                elif (action == "pause"):
                    pygame.mixer.Channel(5).pause()
                elif (action == "continue"):
                    pygame.mixer.Channel(5).unpause()

    def draw_wall(self, surface):
        for y in range(581):
            if (y % 20 == 0):
                if (y != 0 and y % 20 == 0):
                    duvar_rectangle = pygame.Rect((20, y), (20, 20))
                    pygame.draw.rect(surface, self.duvar_renk, duvar_rectangle)
                    if (self.snake_positions[0] == (20, y)):
                        self.reset()
        for y in range(581):
            if (y != 580 and y % 20 == 0 and y != 0):
                duvar_rectangle = pygame.Rect((y, 20), (20, 20))
                pygame.draw.rect(surface, self.duvar_renk, duvar_rectangle)
                if (self.snake_positions[0] == (y, 20)):
                    self.reset()
        for y in range(581):
            if (y % 20 == 0):
                if (y != 0 and y != 580 and y != 560):
                    duvar_rectangle = pygame.Rect((560, y), (20, 20))
                    pygame.draw.rect(surface, self.duvar_renk, duvar_rectangle)
                    if (self.snake_positions[0] == (560, y)):
                        self.reset()
        for y in range(581):
            if (y % 20 == 0):
                if (y != 0 and y != 580 and y != 40):
                    duvar_rectangle = pygame.Rect((y, 560), (20, 20))
                    pygame.draw.rect(surface, self.duvar_renk, duvar_rectangle)
                    if (self.snake_positions[0] == (y, 560)):
                        self.reset()
        for y in range(581):
            if (y % 20 == 0):
                if (y != 0 and y != 580 and y != 40):
                    duvar_rectangle = pygame.Rect((60, y), (20, 20))
                    pygame.draw.rect(surface, self.duvar_renk, duvar_rectangle)
                    if (self.snake_positions[0] == (60, y)):
                        self.reset()
        for y in range(581):
            if (y != 0 and y % 20 == 0):
                if (y != 580 and y != 60 and y != 540 and y != 40):
                    duvar_rectangle = pygame.Rect((y, 60), (20, 20))
                    pygame.draw.rect(surface, self.duvar_renk, duvar_rectangle)
                    if (self.snake_positions[0] == (y, 60)):
                        self.reset()

        for y in range(581):
            if (y % 20 == 0):
                if (y != 0 and y != 580 and y != 560 and y != 20 and y != 40 and y != 540 and y != 520):
                    duvar_rectangle = pygame.Rect((520, y), (20, 20))
                    pygame.draw.rect(surface, self.duvar_renk, duvar_rectangle)
                    if (self.snake_positions[0] == (520, y)):
                        self.reset()
        for y in range(581):
            if (y % 20 == 0):
                if (y != 0 and y != 580 and y != 40 and y != 60 and y != 540 and y != 560 and y != 80):
                    duvar_rectangle = pygame.Rect((y, 520), (20, 20))
                    pygame.draw.rect(surface, self.duvar_renk, duvar_rectangle)
                    if (self.snake_positions[0] == (y, 520)):
                        self.reset()
        for y in range(581):
            if (y % 20 == 0):
                if (y != 0 and y != 580 and y != 40 and y != 60 and y != 80 and y != 540):
                    duvar_rectangle = pygame.Rect((100, y), (20, 20))
                    pygame.draw.rect(surface, self.duvar_renk, duvar_rectangle)
                    if (self.snake_positions[0] == (100, y)):
                        self.reset()
        for y in range(581):
            if (y % 20 == 0):
                if (
                        y != 0 and y != 580 and y != 560 and y != 20 and y != 40 and y != 540 and y != 520 and y != 60 and y != 80 and y != 500 and y != 480):
                    duvar_rectangle = pygame.Rect((480, y), (20, 20))
                    pygame.draw.rect(surface, self.duvar_renk, duvar_rectangle)
                    if (self.snake_positions[0] == (480, y)):
                        self.reset()
        for y in range(581):
            if (y % 20 == 0):
                if (
                        y != 0 and y != 580 and y != 40 and y != 60 and y != 540 and y != 560 and y != 80 and y != 100 and y != 520 and y != 500 and y != 120):
                    duvar_rectangle = pygame.Rect((y, 480), (20, 20))
                    pygame.draw.rect(surface, self.duvar_renk, duvar_rectangle)
                    if (self.snake_positions[0] == (y, 480)):
                        self.reset()
        for y in range(581):
            if (y != 0 and y % 20 == 0):
                if (y != 580 and y != 60 and y != 540 and y != 40 and y != 80 and y != 520 and y != 100 and y != 500):
                    duvar_rectangle = pygame.Rect((y, 100), (20, 20))
                    pygame.draw.rect(surface, self.duvar_renk, duvar_rectangle)
                    if (self.snake_positions[0] == (y, 100)):
                        self.reset()
        for y in range(581):
            if (y % 20 == 0):
                if (
                        y != 0 and y != 580 and y != 40 and y != 60 and y != 80 and y != 540 and y != 500 and y != 520 and y != 100 and y != 120):
                    duvar_rectangle = pygame.Rect((140, y), (20, 20))
                    pygame.draw.rect(surface, self.duvar_renk, duvar_rectangle)
                    if (self.snake_positions[0] == (140, y)):
                        self.reset()
        for y in range(581):
            if (y % 20 == 0):
                if (
                        y != 0 and y != 580 and y != 560 and y != 20 and y != 40 and y != 540 and y != 520 and y != 60 and y != 460 and y != 80 and y != 500 and y != 480 and y != 60 and y != 120):
                    duvar_rectangle = pygame.Rect((y, 140), (20, 20))
                    pygame.draw.rect(surface, self.duvar_renk, duvar_rectangle)
                    if (self.snake_positions[0] == (y, 140)):
                        self.reset()
        for y in range(581):
            if (y % 20 == 0):
                if (
                        y != 0 and y != 580 and y != 40 and y != 60 and y != 540 and y != 560 and y != 80 and y != 100 and y != 520 and y != 500 and y != 460 and y != 120 and y != 500):
                    duvar_rectangle = pygame.Rect((440, y), (20, 20))
                    pygame.draw.rect(surface, self.duvar_renk, duvar_rectangle)
                    if self.snake_positions[0] == (440, y):
                        self.reset()
        for y in range(581):
            if y != 0 and y % 20 == 0:
                if (
                        y != 580 and y != 60 and y != 180 and y != 160 and y != 480 and y != 460 and y != 440 and y != 100 and y != 120 and y != 540 and y != 40 and y != 80 and y != 520 and y != 100 and y != 500):
                    duvar_rectangle = pygame.Rect((y, 440), (20, 20))
                    pygame.draw.rect(surface, self.duvar_renk, duvar_rectangle)
                    if self.snake_positions[0] == (y, 440):
                        self.reset()
        for y in range(581):
            if (y % 20 == 0):
                if (y != 580 and y != 60 and y != 180 and y != 160 and y != 480 and y != 460
                        and y != 100 and y != 120 and y != 540 and y != 40 and y != 80 and
                        y != 520 and y != 100 and y != 500 and y != 0 and y != 580 and y != 560 and y != 20 and
                        y != 40 and y != 540 and y != 520 and y != 60 and y != 460 and y != 80 and y != 500 and
                        y != 480 and y != 60 and y != 120):
                    duvar_rectangle = pygame.Rect((180, y), (20, 20))
                    pygame.draw.rect(surface, self.duvar_renk, duvar_rectangle)
                    if (self.snake_positions[0] == (180, y)):
                        self.reset()
        for y in range(581):
            if (y % 20 == 0):
                if (
                        y != 0 and y != 580 and y != 560 and y != 20 and y != 40 and y != 540 and y != 520 and y != 60 and y != 460 and y != 80 and y != 500 and y != 480 and y != 60 and y != 120 and y != 420 and y != 160):
                    duvar_rectangle = pygame.Rect((y, 180), (20, 20))
                    pygame.draw.rect(surface, self.duvar_renk, duvar_rectangle)
                    if (self.snake_positions[0] == (y, 180)):
                        self.reset()
        for y in range(581):
            if (y % 20 == 0):
                if (y != 580 and y != 60 and y != 180 and y != 160 and y != 480 and y != 460
                        and y != 100 and y != 120 and y != 540 and y != 40 and y != 80 and
                        y != 520 and y != 100 and y != 500 and y != 0 and y != 580 and y != 560 and y != 20 and
                        y != 40 and y != 540 and y != 520 and y != 60 and y != 460 and y != 80 and y != 500 and
                        y != 480 and y != 60 and y != 120 and y != 420):
                    duvar_rectangle = pygame.Rect((400, y), (20, 20))
                    pygame.draw.rect(surface, self.duvar_renk, duvar_rectangle)
                    if (self.snake_positions[0] == (400, y)):
                        self.reset()

    def draw_snake(self, surface):
        for p in self.snake_positions:
            rect = pygame.Rect((p[0], p[1]), (gridsize, gridsize))
            pygame.draw.rect(surface, self.snake_color, rect, border_radius=5)

    def snake_keyboard_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.snake_turn(up)
                elif event.key == pygame.K_s:
                    self.snake_turn(down)
                elif event.key == pygame.K_d:
                    self.snake_turn(right)
                elif event.key == pygame.K_a:
                    self.snake_turn(left)
                elif (event.key == pygame.K_SPACE):
                    self.pause_game()

    def snake_move(self):
        current = self.snake_positions[0]
        x, y = self.snake_direction
        new = ((current[0] + (x * gridsize)), ((current[1]) + (y * gridsize)))
        if (new[0] in range(0, screen_width) and new[1] in range(0, screen_height) and not new in self.snake_positions[
                                                                                                  2:]):
            self.snake_positions.insert(0, new)
            if len(self.snake_positions) > self.snake_lenght:
                self.snake_positions.pop()
        else:
            self.reset()

    def reset(self):
        global speed
        self.play_sfx("crash", "start", _sfx_config)
        self.snake_lenght = 5
        self.snake_positions = [(0, 580)]
        self.snake_direction = up
        self.snake_score = 0
        speed = 10

    def snake_turn(self, direction):
        if (direction[0] * -1, direction[1] * -1) == self.snake_direction:
            return
        else:
            self.snake_direction = direction

    def draw_food(self, surface):
        if (_epilepsy_mode):
            food_color = (255, 0, 255)
            rect = pygame.Rect((280, 320), (gridsize, gridsize))
            pygame.draw.rect(surface, food_color, rect, border_radius=15)
        else:
            food_color = random.choice(food_color_list)
            rect = pygame.Rect((280, 320), (gridsize, gridsize))
            pygame.draw.rect(surface, food_color, rect, border_radius=15)

    def pause_game(self):
        global paused, myimage
        paused = True
        self.play_music("game_bg_music", "pause", _music_config)
        self.play_music("pause_menu_music", "start", _music_config)
        self.pause_menu.enable()

    def continue_game(self):
        global paused
        paused = False
        self.play_music("pause_menu_music", "pause", _music_config)
        self.play_music("game_bg_music", "continue", _music_config)
        self.pause_menu.disable()

    def back_to_main_menu(self):
        global can_back_main_menu, speed
        can_back_main_menu = True
        self.pause_menu.disable()
        self.snake_lenght= 1
        self.snake_score = 0
        self.snake_direction = up
        speed = 10
        self.snake_positions = [(580,0)]
        self.play_music("game_bg_music", "pause", _music_config)
        self.play_music("pause_menu_music", "pause", _music_config)
        menu_sfx_music("main_menu_bg_music", "start", _music_config)


        
        self.anamenu.mainloop(main_menu_surface)

    def draw_grid(self, surface):
        for y in range(0, int(grid_hight)):
            for x in range(0, int(grid_width)):
                if (x + y) % 2 == 0:
                    light = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                    pygame.draw.rect(surface, siyah, light)
                else:
                    dark = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                    pygame.draw.rect(surface, acik_siyah, dark)

    def passing_episode(self):
        self.reset()
        self.play_music("game_bg_music", "pause", _music_config)
        self.play_sfx("gecme", "start", _sfx_config)
        self.bolumu_gectiniz_font_render = self.passed_episode_font.render("PASSED EPISODE", True, (255, 0, 0))
        screen.blit(self.bolumu_gectiniz_font_render, (80, 300))
        pygame.display.update()
        self.finish_ep_save()
        pygame.time.wait(10000)
        menu_sfx_music("main_menu_bg_music", "start", _music_config)


    def start_game(self):
        pygame.mixer.Channel(0).stop()
        self.play_music("game_bg_music", "start", _music_config)
        global speed, paused, can_back_main_menu
        paused = False
        speed = 10
        while True:
            self.snake_keyboard_input()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            joystick_count = pygame.joystick.get_count()
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                axis0 = joystick.get_axis(0)
                axis1 = joystick.get_axis(1)
                if (axis1 == -1.000):
                    self.snake_turn(up)
                elif (axis1 == 0.999969482421875):
                    self.snake_turn(down)
                if (axis0 == -1.000):
                    self.snake_turn(left)
                if (axis0 == 0.999969482421875):
                    self.snake_turn(right)
            clock.tick(speed)
            self.snake_move()
            self.draw_grid(game_surface)
            """k, j = pygame.mouse.get_pos()
            print("MOUSE POSITONS", (k, j))"""
            if self.snake_positions[0] == self.yemek_pozisyon:
                self.passing_episode()
                break
            self.draw_wall(game_surface)
            self.draw_snake(game_surface)
            self.draw_food(game_surface)

            screen.blit(game_surface, (0, 0))
            episode_name_text = self.episode_name_text.render("EPISODE 1", True, (255, 0, 0))
            version_text = version_font.render("PYSNAKE V1.0 RELEASE", True, (255, 0, 0))
            screen.blit(version_text, (250, 5))
            screen.blit(episode_name_text, (10, 5))
            pygame.display.update()

            while paused == True:
                if (can_back_main_menu != True):
                    self.pause_menu.mainloop(screen)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                paused = False
                                self.play_music("pause_menu_music", "pause", _music_config)
                                self.play_music("game_bg_music", "continue", _music_config)
                else:
                    self.reset()
                    can_back_main_menu = False
                    break


class free_mode():
    def __init__(self):
        pause_menu = pygame_menu.Menu('PAUSED', 600, 600, theme=pause_menu_theme)
        pause_menu.add.button("CONTINUE GAME", self.continue_game)
        pause_menu.add.button("RESTART GAME", self.restart_game)
        pause_menu.add.button("MAIN MENU", self.back_to_main_menu)

        self.pause_menu = pause_menu
        self.anamenu = main_menu
        self.episode_choice_menu = episode_choice_menu
        self.food_random_position()
        self.snake_positions = [((screen_width / 2), (screen_height / 2))]
        self.snake_start_positions = (0, 580)
        self.snake_lenght = 1
        self.snake_direction = random.choice([up, down, right, left])
        self.snake_color = self_color
        self.snake_score = 0
        self.food_positions = (random.randint(0,grid_width-1)*gridsize,random.randint(0,grid_hight-1)*gridsize)

    def restart_game(self):
        self.reset()
        self.play_music("pause_menu_music", "pause", _music_config)
        self.oyunu_baslat()


    def play_music(self, music_name, action, state):
        if (state != 0):
            if (music_name == "game_bg_music"):
                if (action == "start"):
                    pygame.mixer.Channel(1).play(free_mode_bg_music, 64)
                elif (action == "pause"):
                    pygame.mixer.Channel(1).pause()
                elif (action == "continue"):
                    pygame.mixer.Channel(1).unpause()

            elif (music_name == "pause_menu_music"):
                if (action == "start"):
                    pygame.mixer.Channel(2).play(pause_menu_bg_music, 64)
                elif (action == "pause"):
                    pygame.mixer.Channel(2).pause()
                elif (action == "continue"):
                    pygame.mixer.Channel(2).unpause()

    def play_sfx(self, sfx_name, action, state):
        if (state != 0):
            if (sfx_name == "eat"):
                if (action == "start"):
                    pygame.mixer.Channel(3).play(eat_sfx)
                elif (action == "pause"):
                    pygame.mixer.Channel(3).pause()
                elif (action == "continue"):
                    pygame.mixer.Channel(3).unpause()
            elif (sfx_name == "crash"):
                if (action == "start"):
                    pygame.mixer.Channel(4).play(crash_sfx)
                elif (action == "pause"):
                    pygame.mixer.Channel(4).pause()
                elif (action == "continue"):
                    pygame.mixer.Channel(4).unpause()

    def yılanı_çiz(self, surface):
        for p in self.snake_positions:
            rect = pygame.Rect((p[0], p[1]), (gridsize, gridsize))
            pygame.draw.rect(surface, self.snake_color, rect, border_radius=5)

    def snake_keyboard_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.yılan_turn(up)
                elif event.key == pygame.K_s:
                    self.yılan_turn(down)
                elif event.key == pygame.K_d:
                    self.yılan_turn(right)
                elif event.key == pygame.K_a:
                    self.yılan_turn(left)
                elif (event.key == pygame.K_SPACE):
                    self.pause_game()

    def yılan_move(self):
        current = self.snake_positions[0]

        x, y = self.snake_direction
        new = ((current[0] + (x * gridsize)), ((current[1]) + (y * gridsize)))
        if (new[0] in range(0, screen_width) and new[1] in range(0, screen_height) and not new in self.snake_positions[
                                                                                                  2:]):
            self.snake_positions.insert(0, new)
            if len(self.snake_positions) > self.snake_lenght:
                self.snake_positions.pop()
        else:
            self.reset()

    def reset(self):
        global speed
        self.play_sfx("crash", "start", _sfx_config)
        self.snake_lenght = 1
        self.snake_positions = [((screen_width / 2), (screen_height / 2))]
        self.snake_direction = random.choice([up, down, right, left])
        self.snake_score = 0
        speed = 10

    def yılan_turn(self, direction):
        if (direction[0] * -1, direction[1] * -1) == self.snake_direction:
            return
        else:
            self.snake_direction = direction

    def food_random_position(self):
        self.food_positions = (
            random.randint(0, grid_width - 1) * gridsize, random.randint(0, grid_hight - 1) * gridsize)

    def food_draw(self, surface):
        if (_epilepsy_mode):
            food_color = (255, 0, 255)
            rect = pygame.Rect((self.food_positions[0], self.food_positions[1]), (gridsize, gridsize))
            pygame.draw.rect(surface, food_color, rect, border_radius=25)
        else:
            food_color = random.choice(food_color_list)
            rect = pygame.Rect((self.food_positions[0], self.food_positions[1]), (gridsize, gridsize))
            pygame.draw.rect(surface, food_color, rect, border_radius=25)

    def pause_game(self):
        global paused, myimage
        paused = True
        self.pause_menu.enable()
        self.play_music("game_bg_music", "pause", _music_config)
        self.play_music("pause_menu_music", "start", _music_config)

    def continue_game(self):
        global paused
        paused = False
        self.play_music("pause_menu_music", "pause", _music_config)
        self.play_music("game_bg_music", "continue", _music_config)
        self.pause_menu.disable()

    def back_to_main_menu(self):
        self.play_music("pause_menu_music", "pause", _music_config)
        self.play_music("game_bg_music", "durakat", _music_config)
        menu_sfx_music("main_menu_bg_music", "start", _music_config)  # Playing main menu background music.
        global can_back_main_menu, speed
        can_back_main_menu = True
        self.pause_menu.disable()
        self.snake_lenght = 1
        self.snake_score = 0
        speed = 10
        self.anamenu.mainloop(main_menu_surface)

    def draw_grid(self, surface):
        for y in range(0, int(grid_hight)):
            for x in range(0, int(grid_width)):
                if (x + y) % 2 == 0:
                    light = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                    pygame.draw.rect(surface, siyah, light)
                else:
                    dark = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                    pygame.draw.rect(surface, acik_siyah, dark)

    def oyunu_baslat(self):
        pygame.mixer.Channel(0).stop()
        self.play_music("game_bg_music", "start", _music_config)
        global speed, paused, can_back_main_menu
        paused = False
        speed = 10
        while True:
            self.snake_keyboard_input()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            joystick_count = pygame.joystick.get_count()
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                axis0 = joystick.get_axis(0)
                axis1 = joystick.get_axis(1)
                if (axis1 == -1.000):
                    self.yılan_turn(up)
                elif (axis1 == 0.999969482421875):
                    self.yılan_turn(down)
                if (axis0 == -1.000):
                    self.yılan_turn(left)
                if (axis0 == 0.999969482421875):
                    self.yılan_turn(right)
            clock.tick(speed)
            self.yılan_move()
            self.draw_grid(game_surface)
            if self.snake_positions[0] == self.food_positions:
                self.play_sfx("eat", "start", _sfx_config)
                self.snake_lenght += 1
                self.snake_score += 1
                self.food_random_position()
                speed += 1
                clock.tick(speed)

            self.yılanı_çiz(game_surface)
            self.food_draw(game_surface)

            screen.blit(game_surface, (0, 0))
            score_text = score_font.render("Score: {}".format(self.snake_score), True, (255, 0, 0))
            surum_text = version_font.render("PYSNAKE V1.0 RELEASE", True, (255, 0, 0))
            screen.blit(surum_text, (250, 5))
            screen.blit(score_text, (10, 5))
            pygame.display.update()

            while paused == True:
                if (can_back_main_menu != True):
                    self.pause_menu.mainloop(pause_menu_surface)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                self.continue_game()
                else:
                    self.reset()
                    can_back_main_menu = False
                    break


episode_choice_menu.add.button("EPISODE 1", ep1().start_game)
episode_choice_menu.add.button("FREE MODE", free_mode().oyunu_baslat)
main_menu.add.button('START GAME', episode_choice_menu)

menu_sfx_music("main_menu_bg_music", "start", _music_config)

main_menu.mainloop(main_menu_surface)
