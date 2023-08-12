from kivy.properties import Clock
import time
import threading

# Increase the game speed during game loop

def game_speed_increase(self):
     
    if int(self.current_score) == self.interval_score and not self.level_triggered:
        self.level_counter += 1
        self.level_text = str(self.level_counter)
        #print("Level: ", self.level_counter)
        
        threading.Thread(target=self.gradual_speed_increase).start()

        self.bell_sound.play()
        self.level_triggered = True
        self.interval_score += self.interval_score
        #print(self.interval_score)
        
        
    elif int(self.current_score) == self.interval_score and self.level_triggered:
        self.level_counter += 1
        self.level_text = str(self.level_counter)
        #print("Level: ", self.level_counter)
        
        threading.Thread(target=self.gradual_speed_increase).start()
        
        #self.music_sound.pitch += 0.022
        self.bell_sound.play()
        self.level_triggered = False
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
    

        