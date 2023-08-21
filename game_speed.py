from kivy.core.window import Window
from kivy.properties import Clock
from kivy.uix.image import Image

import time
import threading

# Increase the game speed during game loop

def game_speed_increase(self):
     
    if int(self.current_score) == self.interval_score and not self.level_triggered:
        self.alpa_drooling()
        
        self.level_counter += 1
        self.level_text = str(self.level_counter)
        #print("Level: ", self.level_counter)
        
        threading.Thread(target=self.gradual_speed_increase).start()

        self.gallop_sound.pitch += 0.1
        
        self.bell_sound.play()
        self.level_triggered = True
        
        if self.interval_score > 50:
            self.interval_score += int(self.interval_score / 4)
        else:
            self.interval_score += self.interval_score
        #print(self.interval_score)
        
        
    elif int(self.current_score) == self.interval_score and self.level_triggered:
        self.alpa_drooling()
        
        self.level_counter += 1
        self.level_text = str(self.level_counter)
        #print("Level: ", self.level_counter)
        
        threading.Thread(target=self.gradual_speed_increase).start()
        
        self.gallop_sound.pitch += 0.1
        
        self.bell_sound.play()
        self.level_triggered = False
        
        if self.interval_score > 50:
            self.interval_score += int(self.interval_score / 4)
        else:
            self.interval_score += self.interval_score
        #print(self.interval_score)   


def gradual_speed_increase(self):
    time.sleep(0.6)
    self.speed_y += 0.2
    self.speed_x += 0.5
    time.sleep(0.3)
    self.speed_y += 0.2
    self.speed_x += 0.5
    time.sleep(0.1)
    self.speed_y += 0.2
    self.speed_x += 0.5

    self.alpa_image.anim_delay -= 0.01
    

def alpa_drooling(self):
        # Create an instance of Image
        self.drooling = Image(source='images/drooling.gif', fit_mode="contain", anim_delay= 0.1, anim_loop= 1)

        # Set the size and position of the GIF within the RelativeLayout
        self.drooling.size_hint = (None, None)
        self.drooling.size = self.size

        x = (Window.width * 0.46)
        drooling_width = Window.width * 0.2  # Adjust the size as needed
        drooling_height = Window.height * 0.2
    
        self.drooling.pos = (x, self.alpa_image.height)
        self.drooling.size = (drooling_width, drooling_height)
        #print(self.alpa_image.size_hint)
        
        
        self.add_widget(self.drooling)
    

        