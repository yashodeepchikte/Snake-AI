from pygame.locals import *
import pygame
import enum
import random
import sys
import argparse

INITIAL_LENGTH = 1

class Move(enum.Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    
    NONE = 255
    
    def __int__(self):
        return self.value
    
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        # check for equlaity for 2 positions
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash(str(self.x) + ',' + str(self.y))
    

class Fruit:
    def __init__(self):
        self.position = Position(0, 0)
        self.image = pygame.image.load('img/fruit.png')
        
    def get_rect(self):
        return self.image.get_rect().move((self.position.x, self.position.y))
    
    
class Controller:
    player = None
    def make_move(self):
        pass
    def update_state(self):
        pass

class KeyboardController(Controller):

	player = None
	def make_move(self):
		pygame.event.pump()
		keys = pygame.key.get_pressed()
		move = Move.NONE
        
		if keys[K_RIGHT]:	
			move = Move.RIGHT
		elif keys[K_LEFT]:
			move = Move.LEFT
		elif keys[K_UP]:
			move = Move.UP
		elif keys[K_DOWN]:
			move = Move.DOWN
        
		self.player.set_move(move)
	
	def update_state(self):
		pass
    

class AIController(Controller):
    player = None
    def make_move(self):
        self.player.set_move(Move(random.randint(1,4)))
    def update_state(self):
        pass
    

class Player:
    def __init__(self):
        self.positions = [Position(100, 100)]
        self.last_move = Move.NONE
        self.image = pygame.image.load('img/body.png')
        self.head  = pygame.image.load('img/head.png')
        self.step = self.get_first_block_rect().right - self.get_first_block_rect().left
        
        
    def make_bigger(self):
        # increases the length of the snake
        self.positions.append(Position(0, 0))
        
    
    def get_first_block_rect(self):
        # returns the position of the head
        return self.image.get_rect().move((self.positions[0].x, self.positions[0].y))
    
    def get_snake_length(self):
        # returns the length of the snake
        return len(self.positions)
    
    def get_score(self):
        # retruns the score
        # depending on how we measure it
        # as of now 1 fruit = 1 point
        # in future we may want to add negative points
        return self.get_snake_length() - INITIAL_LENGTH
    
    def set_move(self, move):
        # this function will set the self.last_move value
        # We cannot move directly in the opposite of the current direction
        if move == Move.NONE:
            return
        if abs(int(self.last_move) - int(move)) != 2:
            # this if will ensore that we dont move directly in the opposite direction
            self.last_move = move
        
    def update(self):
        
        for i in range(len(self.positions) - 1, 0, -1):
            self.positions[i].x = self.positions[i-1].x
            self.positions[i].y = self.positions[i-1].y
        
        if self.last_move == Move.UP:
            self.positions[0].y -= self.step
        elif self.last_move == Move.DOWN:
            self.positions[0].y += self.step
        elif self.last_move == Move.LEFT:
            self.positions[0].x -= self.step
        elif self.last_move == Move.RIGHT:
            self.positions[0].x += self.step          
        
        
        
class Game:
    window_width = 800
    window_height = 800
    
    player = None
    fruit = None
    
    def __init__(self, controller, speed):
        # we initialise pygame here all other imp initializations are in  the init() function
        pygame.init()
        self._running = True
        self._display_surf = None
        self.board_rect = None
        self.highscore = 0
        self.game_count = 0
        self.controller = controller
        self.fruit = Fruit()
        self.speed = speed
        
    def _generate_init_player_state(self):
        # Randomly generates a snalke and gives it a random direction for movement
        # we will call this ins the init method
        self.player.positions[0].x = random.randint(self.board_rect.left, self.board_rect.right - 1)
        self.player.positions[0].y = random.randint(self.board_rect.top, self.board_rect.bottom - 1)
        
        self.player.positions[0].x -= self.player.positions[0].x % self.player.step
        self.player.positions[0].y -= self.player.positions[0].y % self.player.step
        
        self.player.set_move(Move(random.randint(1, 4)))
    
    
    def init(self):
        # this method will be called when we start to run the game 
        # see the run method
        self._display_surf = pygame.display.set_mode((self.window_width+200, self.window_height), pygame.HWSURFACE)
        self.board_rect = pygame.Rect(self.border_width, self.border_width, self.window_width - 2 * self.border_width, self.window_height - 2 * self.border_width)
        
        pygame.display.set_caption('AI SNAKE')
        self.player = Player()
        self._generate_init_player_state()
        self.generate_fruit()
        self._running = True
        self.moves_left = 200
        self.controller.player = self.player
        
    
    def is_player_inside_board(self):
        # this basically takes care of the wall collision
        return self.board_rect.contains(self.player.get_first_block_rect())
    
    def get_score(self):
        # this will get the current score form the players get_scoe function
        return self.player.get_score()
    
    def on_event(self, events):
        for event in events:   
            if event.type == pygame.QUIT:
                self._running = False
                pygame.quit()
                sys.exit()
    
    def draw_board(self):
        self._display_surf.fill((0, 0, 0))    # border
        pygame.draw.rect(self._display_surf, (255, 255, 255), self.board_rect) # board where snake moves
        
        
        
    def draw_ui(self):
        myfont = pygame.font.SysFont('Segoe UI', 22)
        myfont_bold = pygame.font.SysFont('Segoe UI', 32, True)
        
        text_game_count = myfont.render('GAME COUNT: ' + str(self.game_count), True, (0, 255, 255))
        text_score = myfont.render('SCORE: '+ str(self.get_score()), True, (0, 255, 255))
        text_highest = myfont.render('HIGHEST SCORE: '+str(self.highscore), True, (0, 255, 255))
        text_moves_left = myfont.render('MOVES LEFT: '+str(self.moves_left), True, (0, 255, 255))   
        dealy_between_frames = myfont.render('DELAY: '+str(self.speed)+"ms", True, (0, 255, 255))   
        
        self._display_surf.blit(text_game_count, (self.window_width - self.border_width + 5,   30))
        self._display_surf.blit(text_score, (self.window_width - self.border_width + 5,  60))
        self._display_surf.blit(text_highest, (self.window_width - self.border_width + 5,  90))
        self._display_surf.blit(text_moves_left, (self.window_width - self.border_width + 5,  120))
        self._display_surf.blit(dealy_between_frames, (self.window_width - self.border_width + 5,  150))
    

    def draw_snake(self):
        # draws the snake based on the positions
        for (i, p) in enumerate(self.player.positions):
            if i == 0:
                self._display_surf.blit(self.player.head, (p.x, p.y))
            else:    
                self._display_surf.blit(self.player.image, (p.x, p.y))
        
        
    def draw_fruit(self):
        self._display_surf.blit(self.fruit.image, (self.fruit.position.x, self.fruit.position.y))
        
        
    def generate_fruit(self):
        self.fruit.position.x = random.randint(self.board_rect.left, self.board_rect.right - 1)
        self.fruit.position.y = random.randint(self.board_rect.top, self.board_rect.bottom - 1)
        
        self.fruit.position.x -= self.fruit.position.x % 20
        self.fruit.position.y -= self.fruit.position.y % 20
        
        # check if fruit is generated on snake body by chance
        # if it is then generate fruit in another spot
        if self.fruit.position in self.player.positions:
            self.generate_fruit()
        
    
    def render(self):
        self.draw_board()
        self.draw_ui()
        self.draw_snake()
        self.draw_fruit()

        pygame.display.flip()
        
        
    def cleanup(self):
        pygame.quit()
        
    def read_move(self):
        last_move = self.player.last_move
        # self.player.set_move(self.controller.get_move())
        self.controller.make_move()
            
        
        if last_move != self.player.last_move:
            # This will restrict the maximum moves any player can make without eating a fruit
            # ai or keyboard  if the snake eats a fruit the remaining moves will increase
            self.moves_left -= 1
        
    def update_snake(self):
        self.player.update()
        
    
    def check_collisions(self):
        # check collision with wall
        if not self.is_player_inside_board():
            self._running = False
            
        # check collision with body
        if len(self.player.positions) != len(set(self.player.positions)):
            # there are duplicates -> snake is colliding with itself
            self._running = False
            
        # Check collision with fruit
        if self.fruit.get_rect().contains(self.player.get_first_block_rect()):
            self.player.make_bigger()
            self.moves_left += 500
            self.generate_fruit()
            if self.player.get_score() > self.highscore:
                self.highscore = self.player.get_score()
        
        # Check if we are running out of moves
        if self.moves_left <= 0:
            self._running = False    
        
    def run(self):
        self.init()
        self.game_count += 1
        while self._running:
            self.render()
            self.read_move()
            self.update_snake()
            
            self.check_collisions()
            
            events = pygame.event.get()
            self.on_event(events)

            self.controller.update_state()
            pygame.time.wait(self.speed)
    
    
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--ai', action='store_true', help="AI controlls snake")
    parser.add_argument("--speed",type=int, default=100, help='Specifiy the delay between the frames in milli-seconds. 0 is the fastest. Default: 100 do note 0 ms is not attainable some delay is introduced becaiuse of the computations')
    parser.add_argument('--count', type=int, default=100, help='Max game count to be played. Default: 100')

    args = parser.parse_args()


    controller = KeyboardController()
    if args.ai:
        controller = AIController()
    
    score_in_game = []
    highscore_in_game = [] 
    
    game = Game(controller, args.speed)
    print("Args recieved = ", args)
    while game.game_count < args.count:
        game.run()
        score_in_game.append(game.get_score())
        highscore_in_game.append(game.highscore)
        
    game.cleanup()