import sys, logging, os, random, math, open_color, arcade, time

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 30
SCREEN_TITLE = "Space-shooter"

timeDelay = random.randrange(0, 10)

NUM_ENEMIES = 5
STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 10
ENEMY_BULLET_DAMAGE = 1
ENEMY_HP = 100
PLAYER_HP=5
HIT_SCORE = 10
KILL_SCORE = 110

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/laserBlue02.png", 0.65)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy


    
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/playerShip3_blue.png", 0.5)
        (self.center_x, self.center_y) = STARTING_LOCATION

class Enemy(arcade.Sprite):
    def __init__(self, position):
        '''
        initializes a penguin enemy
        Parameter: position: (x,y) tuple
        '''
        super().__init__("assets/ufoRed.png", 0.5)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position

class Enemy_bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        super().__init__("assets/laserRed02.png", 0.65)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x -= self.dx
        self.center_y -= self.dy


class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.set_mouse_visible(True)
        arcade.set_background_color(open_color.gray_7)
        self.bullet_list = arcade.SpriteList()
        self.enemy_bullet_list=arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0
        self.win="You Win"
        self.background = None
        self.background2 = None
        self.background3 = None

    def setup(self):
        '''
        Set up enemies
        '''
        for i in range(NUM_ENEMIES):
            x = 120 * (i+1) + 40
            y = 500
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy)
        
        self.background = arcade.load_texture("assets/blue.png")
        
        self.health1 = arcade.Sprite("assets/cursor.png", 0.5,center_x=10,center_y=50)
        self.health2 = arcade.Sprite("assets/cursor.png", 0.5,center_x=25,center_y=50)
        self.health3 = arcade.Sprite("assets/cursor.png", 0.5,center_x=40,center_y=50)
        self.health4 = arcade.Sprite("assets/cursor.png", 0.5,center_x=55,center_y=50)       

    def update(self, delta_time):
        self.bullet_list.update()
        self.enemy_bullet_list.update()
        for e in self.enemy_list:
            hit=arcade.check_for_collision_with_list(e,self.bullet_list)
            r=random.randrange(0,150,3)
            if r==6:
                x = e.center_x
                y = e.center_y
                bullet = Enemy_bullet((x,y),(0,10),ENEMY_BULLET_DAMAGE)
                self.enemy_bullet_list.append(bullet)
            for c in hit:
                e.hp-=c.damage
                c.kill()
                if e.hp<=0:
                    self.score+=KILL_SCORE
                    e.kill()
                else:
                    self.score+=HIT_SCORE
                if  self.score>=1000:
                    self.background3=arcade.load_texture("assets/blue3.png")
        
    
        
        p_hit=arcade.check_for_collision_with_list(self.player,self.enemy_bullet_list)
        for i in p_hit:
            for a in self.enemy_bullet_list:
                a.kill()
            global PLAYER_HP
            PLAYER_HP=PLAYER_HP-1
            print(PLAYER_HP)
            if PLAYER_HP<4:
                self.health4 = None
            if PLAYER_HP<3:
                self.health3 = None
            if PLAYER_HP<2:
                self.health2 = None
            if PLAYER_HP<1:
                self.health1 = None
            if PLAYER_HP<=0:
                self.background2=arcade.load_texture("assets/blue2.png")
            if  self.score>=1000:
                self.background3=arcade.load_texture("assets/blue3.png")


    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        if self.background2==arcade.load_texture("assets/blue2.png"):
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,SCREEN_WIDTH, SCREEN_HEIGHT, self.background2)
            
            self.player.center_y=10000
        if self.background3==arcade.load_texture("assets/blue3.png"):
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,SCREEN_WIDTH, SCREEN_HEIGHT, self.background3)
        self.player.draw()
        self.bullet_list.draw()
        self.enemy_bullet_list.draw()
        self.enemy_list.draw()
        self.health1.draw()
        self.health2.draw()
        self.health3.draw()
        self.health4.draw()

            

    def on_mouse_motion(self, x, y, dx, dy):
        '''
        The player moves left and right with the mouse
        '''
        self.player.center_x = x
        

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player.center_x
            y = self.player.center_y + 15
            bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
            self.bullet_list.append(bullet)
    
        


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
    



if __name__ == "__main__":
    main()