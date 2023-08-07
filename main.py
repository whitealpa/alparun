from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget

class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    
    vertical_line_number = 10 
    vertical_line_spacing = .1
    vertical_lines = []
    
    horizontal_line_number = 15 
    horizontal_line_spacing = .2
    horizontal_lines = []
    
    
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print("INIT W: " + str(self.width) + " H: " + str(self.height))
        self.init_vertical_lines()
        self.init_horizontal_lines()
            
            
    def on_parent(self, widget, parent):
        # print("ON PARENT W: " + str(self.width) + " H: " + str(self.height))
        pass
    
    
    def on_size(self, *args):
        # print("ON SIZE W: " + str(self.width) + " H: " + str(self.height))
        # self.perspective_point_x = self.width / 2
        # self.perspective_point_y = self.height * 0.75
        self.update_vertical_lines()
        self.update_horizontal_lines()
    
    
    def on_perspective_point_x(self, widget, value):
        # print("PX: " + str(value))      
        pass
    
    
    def on_perspective_point_y(self, widget, value):
        # print("PY: " + str(value))
        pass
    
    
    def init_vertical_lines(self):
        with self.canvas:
                Color(1, 1, 1)
                # self.line = Line(points = [100, 0, 100, 100])
                for i in range(0, self.vertical_line_number):
                    self.vertical_lines.append(Line())
     
                
    def update_vertical_lines(self):
        center_line_x = int(self.width / 2)
        # self.Line.points = [center_x, 0, center_x, 100]
        offset = -int(self.vertical_line_number / 2) + 0.5
        spacing = self.vertical_line_spacing * self.width
        
        for i in range(0, self.vertical_line_number):
            line_x = int(center_line_x + offset * spacing)
            
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            
            self.vertical_lines[i].points = [x1, y1, x2, y2]
            offset += 1
     
            
    def init_horizontal_lines(self):
        with self.canvas:
                Color(1, 1, 1)
                # self.line = Line(points = [100, 0, 100, 100])
                for i in range(0, self.horizontal_line_number):
                    self.horizontal_lines.append(Line())
            
                
    def update_horizontal_lines(self):
        center_line_x = int(self.width / 2)  
        spacing = self.vertical_line_spacing * self.width
        offset = int(self.vertical_line_number / 2) - 0.5

        x_min = center_line_x - (offset * spacing)
        x_max = center_line_x + (offset * spacing)
        spacing_y = self.horizontal_line_spacing * self.height
        
        for i in range(0, self.horizontal_line_number):
            line_y = i * spacing_y
            x1, y1 = self.transform(x_min, line_y)
            x2, y2 = self.transform(x_max, line_y)        
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

                    
            
    def transform(self, x, y):
        # return self.transform_2D(x, y)
        return self.transform_perspective(x, y)
    
    
    def transform_2D(self, x, y):
        return int(x), int(y)
    
    
    def transform_perspective(self, x, y):
        linear_y = y * self.perspective_point_y / self.height
        
        if linear_y > self.perspective_point_y:
            linear_y = self.perspective_point_y
            
        diff_x = x - self.perspective_point_x
        diff_y = self.perspective_point_y - linear_y
        factor_y = diff_y / self.perspective_point_y
        factor_y = factor_y * factor_y 
        
        y_proportion = diff_y / self.perspective_point_y
        
        transform_x = self.perspective_point_x + diff_x * y_proportion
        transform_y = self.perspective_point_y + factor_y * self.perspective_point_y
        
        return int(transform_x), int(transform_y)
 
            
class AlpaRun(App):
    pass

AlpaRun().run()