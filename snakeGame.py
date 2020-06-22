import pygame


class Player:
    def __init__(self):
        position = []
        self.x = 10
        self.y = 10
        self.speed = 5
        self.score = 0
        self.last_move = "RIGHT"
        self.image = pygame.image.load("img/body.png")

    def get_first_block_rect(self):
        return pygame.rect(self.x, self.y, 20, 20)

    def set_move(self, move):
        self.last_move = move
    
    def make_move(self):
        
        if self.last_move == "UP":
            self.move_up()
        elif self.last_move == "DOWN":
            self.move_down()
        elif self.last_move == "LEFT":
            self.move_left()
        elif self.last_move == "RIGHT":
            self.move_right()
    
    def move_up(self):
        self.y -= self.speed
    
    def move_down(self):
        self.y += speed
    
    def move_right(self):
        self.x += speed
    
    def move_left(self):
        self.x -= speed