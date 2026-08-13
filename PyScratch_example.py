import pygame

from libraries.scratch import Game, Object, Keys


window = pygame.display.set_mode((2000, 1080), pygame.SCALED | pygame.FULLSCREEN)

game = Game()


object1 = Object(["player.png", "player_jump.png"], game)

def test(obj):
    for _ in range(game.fps * 2):
        obj.move_steps(10)
        obj.change_angle_by(10)
        yield
    for _ in range(game.fps * 2):
        obj.move_steps(-10)
        obj.change_angle_by(-10)
        yield 
    yield 

def test2(obj):
    if game.key_down(Keys.SPACE):
        obj.hide()
    else:
        obj.show()
    

def test3(obj):
    yield from obj.wait(5)
    
    obj.next_costume()

def test4(obj):
    if game.mouse_moving():
        mouse_x, mouse_y = game.mouse_pos()
        obj.go_to(mouse_x, mouse_y)

def test6(obj):
    obj.go_to(0, 0)

def test5(obj):
    yield from obj.wait(10)
    obj.add_script(test6, True)

object1.add_scripts([test, test2, test3, test4, test5])



object1.go_to(1000, 540)

game.loop(window)
pygame.quit()