from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy import platform
from kivy.app import App
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Quad, Triangle, Rectangle
from kivy.lang.builder import Builder
from kivy.properties import Clock, NumericProperty, ObjectProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
import random

Builder.load_file("menu.kv")

class MainWidget(RelativeLayout):
    
    from perspective import transform, transform_2D, transform_perspective
    from user_control import keyboard_closed, on_touch_down, on_touch_up, on_keyboard_down, on_keyboard_up
    
    menu_widget = ObjectProperty()
    menu_title = StringProperty("AlpaRun")
    menu_button_title = StringProperty("Yes!")
    current_score = StringProperty('0')
    highest_score = StringProperty('0')
    
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    
    vertical_line_number = 8
    vertical_line_spacing = 0.4
    vertical_lines = []
    
    horizontal_line_number = 15
    horizontal_line_spacing = .1
    horizontal_lines = []
    
    speed_y = 5
    current_offset_y = 0
    current_y_loop = 0
    
    speed_x = 9
    current_speed_x = 0
    current_offset_x = 0
    
    number_of_tiles = 16
    tiles = []
    tiles_coordinates = []
    
    # Triangle
    alpa_width = .1
    alpa_height = 0.035
    alpa_base_y = 0.04
    alpa = None
    alpa_coordinates = [(0, 0), (0, 0), (0, 0)]
    
    # Sprite
    alpa_image = None
    alpa_image_coordinates = [(0, 0), (0, 0), (0, 0), (0, 0)]
    
    # Game states
    game_over = False
    game_started = False
    
    # Audio
    start_sound = None
    alpa_sound = None
    game_over_impact_sound = None
    game_over_voice_sound = None
    music_sound = None
    restart_sound = None
    
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print("INIT W: " + str(self.width) + " H: " + str(self.height))
        self.init_audio()
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_alpa()
        # self.init_alpa_image()
        self.game_restart()
  
        if self.is_desktop():      
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)
            
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        
        
    def init_audio(self):
        self.start_sound = SoundLoader.load("audio/game_start.wav")
        self.game_over_impact_sound = SoundLoader.load("audio/game_over.wav")
        self.game_over_voice_sound = SoundLoader.load("audio/gameover_voice.wav")
        self.music_sound = SoundLoader.load("audio/rainbow.wav")
        self.restart_sound = SoundLoader.load("audio/restart.wav")
        
        # Play music at the start of the app
        self.music_sound.volume = 0.7
        self.music_sound.pitch = 1
        self.music_sound.play()
        self.music_sound.loop = True
        
        
        # Alpaca sound
        self.start_sound.volume = 1
        self.start_sound.pitch = 2.5
        
        self.game_over_impact_sound.volume = 1
        self.game_over_impact_sound.pitch = 2.5
        self.game_over_voice_sound.volume = 0.6
        self.restart_sound.volume = 0.25
        
        
    def game_restart(self):
        
        if int(self.current_score) > int(self.highest_score): # Record the highest score before reset
                self.highest_score = self.current_score
        self.current_score = '0'
        
        
        fade_in = Animation(volume=0.7, duration=1)  # Fade in duration
        fade_in.start(self.music_sound)
        #self.music_sound.volume = 0.8 # Fade in music volume to normal
                
        self.current_offset_y = 0
        self.current_y_loop = 0
        self.current_speed_x = 0
        self.current_offset_x = 0
        
        self.tiles_coordinates = []
        self.starting_tiles_coordinates()
        self.generate_tiles_coordinates()
        
        self.game_over = False
    
        
    def is_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True
        else:
            return False
    
    def init_alpa(self):
        with self.canvas:
            Color(0, 0, 0)
            self.alpa = Triangle()
    
    def update_alpa(self):
        center_x = self.width / 2
        base_y = self.alpa_base_y * self.height
        
        alpa_half_width = self.alpa_width * (self.width / 2)
        alpa_height = base_y + self.alpa_height * self.height
        
        self.alpa_coordinates[0] = center_x - alpa_half_width, base_y
        self.alpa_coordinates[1] = center_x, alpa_height   
        self.alpa_coordinates[2] = center_x + alpa_half_width, base_y
                
        x1, y1 = self.transform(*self.alpa_coordinates[0]) 
        x2, y2 = self.transform(*self.alpa_coordinates[1])
        x3, y3 = self.transform(*self.alpa_coordinates[2])
        
        self.alpa.points = [x1, y1, x2, y2, x3, y3] 
        
    
    def check_player_collision(self):
        for i in range(0, len(self.tiles_coordinates)):
            ti_x, ti_y = self.tiles_coordinates[i]
            
            if ti_y > self.current_y_loop + 1:
                return False
            
            if self.check_player_collision_with_tile(ti_x, ti_y):
                return True
            
        return False
    
    def check_player_collision_with_tile(self, ti_x, ti_y):        
        x_min, y_min = self.get_tile_coordinates(ti_x, ti_y)
        x_max, y_max = self.get_tile_coordinates(ti_x + 1, ti_y + 1)
        
        for i in range(0, 3):
            point_x, point_y = self.alpa_coordinates[i]
            if x_min <= point_x <= x_max and y_min <= point_y <= y_max:
                return True
        return False
        
        
    def init_alpa_image(self):
        self.alpa_image = Image(source='images/alpa.png', fit_mode="contain")
        self.add_widget(self.alpa_image)
        self.bind(size=self.update_alpa_image)
        
    def update_alpa_image(self, *args):

        x = (self.width / 2) - (self.alpa_image.width / 2)
        base_y = self.alpa_base_y * self.height
        alpa_width = self.width * 0.3  # Adjust the size as needed
        alpa_height = self.height * 0.3

        self.alpa_image.pos = (x, base_y)
        self.alpa_image.size = (alpa_width, alpa_height)    
        
        
    def init_vertical_lines(self):
        with self.canvas:
                Color(0.88, 0.77, 0.66)
                for i in range(0, self.vertical_line_number):
                    self.vertical_lines.append(Line())
                    
                
    def init_horizontal_lines(self):
        with self.canvas:
                Color(0.88, 0.77, 0.66)
                for i in range(0, self.horizontal_line_number):
                    self.horizontal_lines.append(Line())


    def init_tiles(self):
        with self.canvas:
                Color(0.88, 0.77, 0.66)
                for i in range(0, self.number_of_tiles):
                    self.tiles.append(Quad())
                    
                    
    def starting_tiles_coordinates(self):
        # 10 tiles in a straight line
        for i in range(0, 10):
            self.tiles_coordinates.append((0, i))
            
    
    def generate_tiles_coordinates(self):
        last_x = 0
        last_y = 0
        
        for i in range(len(self.tiles_coordinates) - 1, -1, -1): # Remove the tiles that are off screen
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]
        
        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1] + 1
        
        for i in range(len(self.tiles_coordinates), self.number_of_tiles):
            random_tiles = random.randint(0, 2)
            self.tiles_coordinates.append((last_x, last_y))   
            
    
            # Prevent tiles to go out of vertical line
            first_index = -int(self.vertical_line_number / 2) + 1
            last_index = first_index + self.vertical_line_number - 1         
            if last_x <= first_index:
                random_tiles = 1
            elif last_x >= last_index - 1:
                random_tiles = 2
                

            if random_tiles == 1: # To the right side
                last_x += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            
            if random_tiles == 2: # To the left side
                last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
             
            last_y += 1
                
    def get_line_x_from_index(self, index):      
        center_line_x = self.perspective_point_x
        offset = index - 0.5
        spacing = self.vertical_line_spacing * self.width
        line_x = center_line_x + (offset * spacing) + self.current_offset_x
        return line_x
    
    
    def get_line_y_from_index(self, index):
        spacing_y = self.horizontal_line_spacing * self.height
        line_y = index * spacing_y - self.current_offset_y      
        return line_y
    
    
    def get_tile_coordinates(self, ti_x, ti_y):
        ti_y = ti_y - self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y
                
    def update_vertical_lines(self):
        first_index = -int(self.vertical_line_number / 2) + 1
        
        for i in range(first_index, first_index + self.vertical_line_number):
            line_x = self.get_line_x_from_index(i)
            
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            
            self.vertical_lines[i].points = [x1, y1, x2, y2]
     
                            
    def update_horizontal_lines(self):
        first_index = -int(self.vertical_line_number / 2) + 1
        last_index = first_index + self.vertical_line_number - 1
        
        x_min = self.get_line_x_from_index(first_index)
        x_max = self.get_line_x_from_index(last_index)
        
        for i in range(0, self.horizontal_line_number):
            line_y = self.get_line_y_from_index(i)
            x1, y1 = self.transform(x_min, line_y)
            x2, y2 = self.transform(x_max, line_y)        
            self.horizontal_lines[i].points = [x1, y1, x2, y2]
    
    
    def update_tiles(self):
        for i in range(0, self.number_of_tiles):
            tile = self.tiles[i]
            tile_coordinates = self.tiles_coordinates[i]
            
            x_min, y_min = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
            x_max, y_max = self.get_tile_coordinates(tile_coordinates[0] + 1, tile_coordinates[1] + 1)
        
            x1, y1 = self.transform(x_min, y_min)
            x2, y2 = self.transform(x_min, y_max)
            x3, y3 = self.transform(x_max, y_max)
            x4, y4 = self.transform(x_max, y_min)
            
            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]
        
    def update(self, dt):
        # print("dt: " + str(dt * 60))
        time_factor = dt * 60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_alpa()
        # self.update_alpa_image()
        
        if self.game_started and not self.game_over: # Keep running the code if the game has not started or is over.)
            self.current_offset_y += self.height * (self.speed_y / 500) * time_factor
            self.current_offset_x += self.width * (self.current_speed_x / 500) * time_factor
            
            spacing_y = self.horizontal_line_spacing * self.height
            
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                
                # Score tracker
                self.current_score = str(self.current_y_loop)
                if int(self.highest_score) < int(self.current_score):
                    self.highest_score = self.current_score
                
                self.generate_tiles_coordinates()
                # print("loop: " + str(self.current_y_loop))
        
        if not self.check_player_collision() and not self.game_over:

            self.game_over_impact_sound.play()
                    
            fade_out = Animation(volume=0.3, duration=0.5)  # Fade out duration
            fade_out.start(self.music_sound)
            
            self.game_over = True

            self.menu_title = "Oops! Try again?"        
            self.menu_button_title = "Yes!"
            self.menu_widget.opacity = 1
            
            # print("Game Over")
            
    def on_menu_button_pressed(self):
        if self.game_over:
            self.start_sound.play()
        elif not self.game_started:
            self.start_sound.play()
        
        # print("Button")
        self.game_restart()
        self.game_started = True
        self.menu_widget.opacity = 0
        
            
class AlpaRun(App):
    pass

AlpaRun().run()