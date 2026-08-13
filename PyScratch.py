import pygame
import time
import math
import inspect

class Mouse:
    LEFT = pygame.BUTTON_LEFT
    MIDDLE = pygame.BUTTON_MIDDLE
    RIGHT = pygame.BUTTON_RIGHT
    WHEELUP = pygame.BUTTON_WHEELUP
    WHEELDOWN = pygame.BUTTON_WHEELDOWN

class Keys:
    pass


for name in dir(pygame):
    if name.startswith("K_"):
        clean_name = name.replace("K_", "")
        setattr(Keys, clean_name, getattr(pygame, name))

class WindowFlags:
    pass

for name in ["SCALED", "FULLSCREEN", "RESIZABLE", "NOFRAME", "SHOWN", "HIDDEN", "DOUBLEBUF"]:
    setattr(WindowFlags, name, getattr(pygame, name))


class Game:
    def __init__(self, fps=60):
        
        self.OBJECTS = []
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.window = None
        
    def mouse_down(self):
        return any(pygame.mouse.get_pressed())
    
    def event_key_pressed(self, key="any"):
        for ev in self.EVENTS:
            if ev.type == pygame.KEYDOWN:
                if key == "any" or ev.key == key:
                    return True
        return False
    
    def event_key_released(self, key="any"):
        for ev in self.EVENTS:
            if ev.type == pygame.KEYUP:
                if key == "any" or ev.key == key:
                    return True
        return False
    
    def key_down(self, key="any"):
        return key == "any" or pygame.key.get_pressed()[key]
    
    def mouse_moving(self):
        return any(ev.type == pygame.MOUSEMOTION for ev in self.EVENTS)
    
    def mouse_pos(self):
        return pygame.mouse.get_pos()
    
    def event_mouse_pressed(self, button="any"):
        for ev in self.EVENTS:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if button == "any" or button == ev.button:
                    return True
        return False
    
    def event_mouse_released(self, button="any"):
        for ev in self.EVENTS:
            if ev.type == pygame.MOUSEBUTTONUP:
                if button == "any" or button == ev.button:
                    return True
        return False
    
    def create_window(self, width=800, height=600, flags=0):
        self.window = pygame.display.set_mode((width, height), flags)
    
    def loop(self,color_fill=(0,0,0)):
        running = True
        if self.window is None:
            self.create_window()
        while running:
            self.EVENTS = pygame.event.get()    
            if any(ev.type == pygame.QUIT for ev in self.EVENTS): 
                running = False
            self.window.fill(color_fill)
            for obj in self.OBJECTS:
                for i in range(len(obj.ACTIVE_SCRIPTS.copy())): 
                    
                    base_script, generator_script, once = obj.ACTIVE_SCRIPTS[i] 
                    try:
                        next(generator_script)
                    except StopIteration:
                       if once:
                           del obj.ACTIVE_SCRIPTS[i]
                       else:
                           obj.ACTIVE_SCRIPTS[i] = (base_script, base_script(obj), once)
                for script in obj.SCRIPTS.copy(): #fuera de if obj.visible porque si en un script haces hide() cagaste
                    func, once = script
                    func(obj)
                    if once:
                        
                        obj.SCRIPTS.remove((func, once))
                if obj.visible:
                    costume = obj.costumes[obj.costume]
                    self.window.blit(costume, (obj.x, obj.y))
            pygame.display.flip()
            self.clock.tick(self.fps)
    

class Object:
    def __init__(self, sprite, game):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.costumes = []
        
        sprites = sprite if isinstance(sprite, list) else [sprite]
        
        for costume in sprites:
            img = pygame.image.load(costume)
            
            img = img.convert_alpha() if costume.lower().endswith(".png") else img.convert()
            self.costumes.append(img)
        
        
        self.costume = 0
        game.OBJECTS.append(self)
        self.visible = True
        self.ACTIVE_SCRIPTS = []
        self.SCRIPTS = []
    
    def add_script(self, script, once=False):
        if inspect.isgeneratorfunction(script):
            self.ACTIVE_SCRIPTS.append((script, script(self), once))
        else:
            self.SCRIPTS.append((script, once))
    
    def add_scripts(self, funcs): #esto es para añadir multiples scripts tipo forevers, no acepta once
        scripts = funcs if isinstance(funcs, list) else [funcs]
        for script in scripts:
            if inspect.isgeneratorfunction(script):
                self.ACTIVE_SCRIPTS.append((script, script(self), False))
            else:
                self.SCRIPTS.append((script, False))
    
    def wait(self, time):
        inicio = pygame.time.get_ticks()
        while pygame.time.get_ticks() - inicio < time * 1000:
            yield
    
    def go_to(self, x,y):
        self.x = x
        self.y = y
    
    def move_steps(self, steps):
        self.x += math.cos(math.radians(self.angle)) * steps
        self.y += math.sin(math.radians(self.angle)) * steps
    
    def set_angle_to(self, angle):
        self.angle = angle
    
    def change_angle_by(self, x):
        self.angle += x
    
    def point_towards(self, x, y):
        self.angle = math.degrees(math.atan2(y - self.y, x - self.x))
    
    def show(self):
        self.visible = True
    
    def hide(self):
        self.visible = False
    
    def next_costume(self):
        if self.costume < len(self.costumes) - 1:
            self.costume += 1
        else:
            self.costume = 0
    
         return False
    
    def event_key_released(self, key="any"):
        for ev in self.EVENTS:
            if ev.type == pygame.KEYUP:
                if key == "any" or ev.key == key:
                    return True
        return False
    

    def key_down(self, key="any"):
        return key == "any" or pygame.key.get_pressed()[key]
    
    def mouse_moving(self):
        return any(ev.type == pygame.MOUSEMOTION for ev in self.EVENTS)
    
    def mouse_pos(self):
        return pygame.mouse.get_pos()
    
    def event_mouse_pressed(self, button="any"):
        for ev in self.EVENTS:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if button == "any" or button == ev.button:
                    return True
        return False
    
    def event_mouse_released(self, button="any"):
        for ev in self.EVENTS:
            if ev.type == pygame.MOUSEBUTTONUP:
                if button == "any" or button == ev.button:
                    return True
        return False
    
    def loop(self, surface,color_fill=(0,0,0)):
        running = True
        while running:
            self.EVENTS = pygame.event.get()    
            if any(ev.type == pygame.QUIT for ev in self.EVENTS): 
                running = False
            surface.fill(color_fill)
            for obj in self.OBJECTS:
                for i in range(len(obj.ACTIVE_SCRIPTS.copy())): 
                    
                    base_script, generator_script, once = obj.ACTIVE_SCRIPTS[i] 
                    try:
                        next(generator_script)
                    except StopIteration:
                       if once:
                           del obj.ACTIVE_SCRIPTS[i]
                       else:
                           obj.ACTIVE_SCRIPTS[i] = (base_script, base_script(obj), once)
                for script in obj.SCRIPTS.copy(): #fuera de if obj.visible porque si en un script haces hide() cagaste
                    func, once = script
                    func(obj)
                    if once:
                        
                        obj.SCRIPTS.remove((func, once))
                if obj.visible:
                    costume = obj.costumes[obj.costume]
                    surface.blit(costume, (obj.x, obj.y))
            pygame.display.flip()
            self.clock.tick(self.fps)
    

class Object:
    def __init__(self, sprite, game):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.costumes = []
        
        sprites = sprite if isinstance(sprite, list) else [sprite]
        
        for costume in sprites:
            img = pygame.image.load(costume)
            
            img = img.convert_alpha() if costume.lower().endswith(".png") else img.convert()
            self.costumes.append(img)
        
        
        self.costume = 0
        game.OBJECTS.append(self)
        self.visible = True
        self.ACTIVE_SCRIPTS = []
        self.SCRIPTS = []
    
    def add_script(self, script, once=False):
        if inspect.isgeneratorfunction(script):
            self.ACTIVE_SCRIPTS.append((script, script(self), once))
        else:
            self.SCRIPTS.append((script, once))
    
    def add_scripts(self, funcs): #esto es para añadir multiples scripts tipo forevers, no acepta once
        scripts = funcs if isinstance(funcs, list) else [funcs]
        for script in scripts:
            if inspect.isgeneratorfunction(script):
                self.ACTIVE_SCRIPTS.append((script, script(self), False))
            else:
                self.SCRIPTS.append((script, False))
    
    def wait(self, time):
        inicio = pygame.time.get_ticks()
        while pygame.time.get_ticks() - inicio < time * 1000:
            yield
    
    def go_to(self, x,y):
        self.x = x
        self.y = y
    
    def move_steps(self, steps):
        self.x += math.cos(math.radians(self.angle)) * steps
        self.y += math.sin(math.radians(self.angle)) * steps
    
    def set_angle_to(self, angle):
        self.angle = angle
    
    def change_angle_by(self, x):
        self.angle += x
    
    def point_towards(self, x, y):
        self.angle = math.degrees(math.atan2(y - self.y, x - self.x))
    
    def show(self):
        self.visible = True
    
    def hide(self):
        self.visible = False
    
    def next_costume(self):
        if self.costume < len(self.costumes) - 1:
            self.costume += 1
        else:
            self.costume = 0
    
 
