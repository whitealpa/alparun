from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy import platform
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Quad, Triangle, Rectangle
from kivy.properties import NumericProperty, Clock
from kivy.uix.image import Image
from kivy.uix.widget import Widget
import random

class MainWidget(Widget):
    
    from perspective import transform, transform_2D, transform_perspective
    from user_control import keyboard_closed, on_touch_down, on_touch_up, on_keyboard_down, on_keyboard_up
    
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    
    vertical_line_number = 8
    vertical_line_spacing = 0.1
    vertical_lines = []
    
    horizontal_line_number = 15
    horizontal_line_spacing = .1
    horizontal_lines = []
    
    speed_y = 1
    current_offset_y = 0
    current_y_loop = 0
    
    speed_x = 1
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
    alpa_cooridnates = [(0, 0), (0, 0), (0, 0)]
    
    # Sprite
    alpa_image = None
    alpa_image_coordinates = [(0, 0), (0, 0), (0, 0), (0, 0)]
    
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print("INIT W: " + str(self.width) + " H: " + str(self.height))
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_alpa()
        # self.init_alpa_image()
        self.starting_tiles_coordinates()
        self.generate_tiles_coordinates()
  
        if self.is_desktop():      
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)
            
        Clock.schedule_interval(self.update, 1.0 / 60.0)
    
        
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
        self.alpa_coordinates[0] = center_x - alpa_half_width, base_y        
        self.alpa_coordinates[0] = center_x - alpa_half_width, base_y
                
        x1, y1 = self.transform(*self.alpa_coordinates[0]) 
        x2, y2 = self.transform(center_x, alpa_height)
        x3, y3 = self.transform(center_x + alpa_half_width, base_y)
        
        self.alpa.points = [x1, y1, x2, y2, x3, y3] 
        
    
    def check_player_collision(self, ti_x, ti_y):
        xmin, ymin = self.get_tile_coordinates(ti_x, ti_y)
        xmax, ymanx = self.get_title_coordinates(ti_x + 1, ti_y + 1)
        
        
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
        
        self.current_offset_y += self.height * (self.speed_y / 500) * time_factor
        self.current_offset_x += self.width * (self.current_speed_x / 500) * time_factor
        
        spacing_y = self.horizontal_line_spacing * self.height
        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y
            self.current_y_loop += 1
            self.generate_tiles_coordinates()
            print("loop: " + str(self.current_y_loop))
            
class AlpaRun(App):
    pass

AlpaRun().run()