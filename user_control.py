def keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self.on_keyboard_down)
    self._keyboard.unbind(on_key_up=self.on_keyboard_up)
    self._keyboard = None

def on_touch_down(self, touch):
    if touch.x < self.width / 2:
        print("Touch left side")
        self.current_speed_x = self.speed_x
    elif touch.x > self.width / 2:
        print("Touch right side")
        self.current_speed_x = - self.speed_x


def on_touch_up(self, touch):
    print("Up")
    self.current_speed_x = 0
    
    
def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'left':
        print("Left arrow")
        self.current_speed_x = self.speed_x
    elif keycode[1] == 'right':
        print("Right arrow")
        self.current_speed_x = - self.speed_x
    return True

def on_keyboard_up(self, keyboard, keycode):
    print("Key up")
    self.current_speed_x = 0 
    return True    