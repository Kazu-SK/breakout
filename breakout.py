
import pygame
import pygame.mixer
from pygame.locals import *
import os
import sys
import math

pygame.init()
pygame.mixer.quit()
#pygame.mixer.pre_init(buffersize = 2048)
pygame.mixer.pre_init(22050, 16, 2, 1024)
#pygame.mixer.init(frequency = 44100)
pygame.mixer.init()


ROOT_DIR = os.path.abspath("sound/")

hit_sound = pygame.mixer.Sound(os.path.join(ROOT_DIR, "se_maoudamashii_system35.wav"))
block_sound = pygame.mixer.Sound(os.path.join(ROOT_DIR, "se_maoudamashii_system27.wav"))
dead_sound = pygame.mixer.Sound(os.path.join(ROOT_DIR, "se_maoudamashii_battle07.wav"))
hit_shorter = pygame.mixer.Sound(os.path.join(ROOT_DIR, "se_maoudamashii_system25.wav"))
hit_longer = pygame.mixer.Sound(os.path.join(ROOT_DIR, "se_maoudamashii_system23.wav"))
hit_reseter = pygame.mixer.Sound(os.path.join(ROOT_DIR, "se_maoudamashii_onepoint20.wav"))
back_music = pygame.mixer.music.load(os.path.join(ROOT_DIR, "oke_song_shiho_shining_star.mp3"))

CLEAR_BGM = os.path.join(ROOT_DIR, "clear.mp3")




class Ball:
    def __init__(self):
        self.ball_x = 600
        self.ball_y = 600

        self.vector_length = 5
        self.init_angle = 45

        self.vector_x = int(self.vector_length * math.sin(self.init_angle * math.pi / 180))
        self.vector_y = int(self.vector_length * math.cos(self.init_angle * math.pi / 180))

        self.vector_x_log = self.vector_x
        self.vector_y_log = self.vector_y

        self.line_length = 30
        self.add_x = int(self.line_length * math.sin(self.init_angle * math.pi / 180))
        self.add_y = int(self.line_length * math.cos(self.init_angle * math.pi / 180))

        self.hit_wall = False
        self.hit_shield = False


    def DrawBall(self, screen):
        self.ball = pygame.draw.circle(screen, (255, 255, 0), (self.ball_x, self.ball_y), 10)


    def DrawVector(self, screen):
        self.line = pygame.draw.line(screen, (255, 100, 0), (self.ball_x, self.ball_y), (self.ball_x + self.add_x, self.ball_y + self.add_y), 2)


    def VectorLog(self):
        self.vector_x_log = self.vector_x
        self.vector_y_log = self.vector_y


    def HitException(self):

        if self.hit_wall == True and self.hit_shield == True:
            self.vector_x = -self.vector_x_log
            self.vector_y = -self.vector_y_log


    def MoveBall(self):
        self.ball_x += self.vector_x
        self.ball_y += self.vector_y
        self.hit_wall = False
        self.hit_shield = False

        self.VectorLog()



class Shield:
    def __init__(self):
        self.shield_x = 80
        self.shield_y = 700

        self.shield_width = 100
        self.shield_height = 40

        self.init_width = self.shield_width

        self.dead_width = 20
        self.dead_height = int(self.shield_height / 2)
        self.dead = [None for i in range(2)]


    def DrawShield(self, screen):
        self.shield = pygame.draw.ellipse(screen, (0,100,0), Rect(self.shield_x,self.shield_y,self.shield_width,self.shield_height), 0)
        self.dead[0] = pygame.draw.rect(screen, (255, 0, 0), Rect(int(self.shield_x - self.dead_width / 2), int(self.shield_y + self.shield_height / 2), self.dead_width, self.dead_height))
        self.dead[1] = pygame.draw.rect(screen, (255, 0, 0), Rect(int(self.shield_x + self.shield_width - self.dead_width / 2), int(self.shield_y + self.shield_height / 2), self.dead_width, self.dead_height))


    def HitShield(self, ball_object):

        if ball_object.ball.collidelist(self.dead) != -1:
            dead_sound.play()
            return False


        if ball_object.ball.colliderect(self.shield) == True:
            ball_object.hit_shield = True
            hit_sound.play()

            #Caluclate ellipse's base point.
            base_x = self.shield_x + self.shield_width / 2
            base_y = self.shield_y + self.shield.height# + self.shield_height / 2
            base_y = self.shield_y + self.shield.height * 1.5

            a1 = base_x - ball_object.ball_x
            a2 = base_y - ball_object.ball_y
            b1 = 1
            b2 = 0

            cos_theta = (a1 * b1 + a2 * b2) / (math.sqrt(a1 * a1 + a2 * a2) * math.sqrt(b1 * b1 + b2 * b2))
            sin_theta = math.sqrt(1 - cos_theta * cos_theta)

            angle = math.acos(cos_theta) * 180 / math.pi
            angle = angle - 90
            angle = math.radians(angle)

            cos_theta = math.cos(angle)
            sin_theta = math.sin(angle)

            ball_object.vector_x = int(ball_object.vector_length * sin_theta)
            ball_object.vector_y = int(-ball_object.vector_length * cos_theta)


        return True


    def MoveShield(self, block_object):
        move_x , move_y = pygame.mouse.get_rel()
        self.shield_x = self.shield_x + move_x

        if self.shield_x < 26:
            self.shield_x = 26
        elif self.shield_x + self.shield_width > 1176:
            self.shield_x = 1176 - self.shield_width

        self.shield.move_ip(self.shield_x, self.shield_y)

        if 'shield_reseter' in block_object.breaked_block:
            self.shield_width = self.init_width
            hit_reseter.play()
        elif 'shield_shorter' in block_object.breaked_block and 'shield_longer' in block_object.breaked_block:
            block_sound.play()
        elif 'shield_shorter' in block_object.breaked_block:
            self.shield_width = int(self.init_width * 0.65)
            hit_shorter.play()
        elif 'shield_longer' in block_object.breaked_block:
            self.shield_width = int(self.init_width * 1.35)
            hit_longer.play()
        elif 'standard' in block_object.breaked_block:
            block_sound.play()
        else:
            pass

        block_object.breaked_block.clear()



class Block:
    def __init__(self):
        self.normal_block = []
        self.breaked_block = []
        self.block_num = list(range(66))

        self.longer_id = [20, 49]
        self.shorter_id = [16, 47, 51]
        self.reset_id = [12]

        self.block_x = []
        self.block_y = []
        self.block_height = 50
        self.block_weight = 80
        x = 0
        y = 50

        for i in range(6):
            y = y + self.block_height + 1
            x = 50
            for j in range(11):
                x = x + self.block_weight + 1
                self.block_x.append(x)
                self.block_y.append(y)


    def DrawBlock(self, screen):
        self.normal_block.clear()

        for i in self.block_num:
            if i in self.longer_id:
                block = pygame.draw.rect(screen, (0,255,255), (self.block_x[i], self.block_y[i], self.block_weight, self.block_height))
            elif i in self.shorter_id:
                block = pygame.draw.rect(screen, (0,0,255), (self.block_x[i], self.block_y[i], self.block_weight, self.block_height))
            elif i in self.reset_id:
                block = pygame.draw.rect(screen, (255,255,255), (self.block_x[i], self.block_y[i], self.block_weight, self.block_height))
            else:
                block = pygame.draw.rect(screen, (100,200,50), (self.block_x[i], self.block_y[i], self.block_weight, self.block_height))


            self.normal_block.append(block)



    def RemainBlock(self, hit_list, ball_object):

        for i in hit_list:
            if ball_object.ball_x < self.normal_block[i].x and ball_object.ball_y < self.normal_block[i].y:
                hit_list.remove(i)
            elif ball_object.ball_x > self.normal_block[i].x + self.normal_block[i].width and ball_object.ball_y < self.normal_block[i].y:
                hit_list.remove(i)
            elif ball_object.ball_x > self.normal_block[i].x + self.normal_block[i].width and ball_object.ball_y > self.normal_block[i].y + self.normal_block[i].height:
                hit_list.remove(i)
            elif ball_object.ball_x < self.normal_block[i].x and ball_object.ball_y > self.normal_block[i].y + self.normal_block[i].height:
                hit_list.remove(i)


    def HitCorner(self, ball_object, corner_x, corner_y, hit_part):

        if hit_part == 'upper_left':
            if ball_object.vector_x_log > 0 and ball_object.vector_y_log > 0: #ok
                ball_object.vector_x *= -1
                ball_object.vector_y *= -1
            elif ball_object.vector_x_log <= 0 and ball_object.vector_y_log > 0: #ok
                ball_object.vector_y *= -1
            elif ball_object.vector_x_log > 0 and ball_object.vector_y_log < 0:
                ball_object.vector_x *= -1

        if hit_part == 'upper_right':
            if ball_object.vector_x_log < 0 and ball_object.vector_y_log > 0: #ok
                ball_object.vector_x *= -1
                ball_object.vector_y *= -1
            elif ball_object.vector_x_log >= 0 and ball_object.vector_y_log > 0: #ok
                ball_object.vector_y *= -1
            elif ball_object.vector_x_log < 0 and ball_object.vector_y_log < 0: #ok
                ball_object.vector_x *= -1

        if hit_part == 'lower_right':
            if ball_object.vector_x_log < 0 and ball_object.vector_y_log < 0: #ok
                ball_object.vector_x *= -1
                ball_object.vector_y *= -1
            elif ball_object.vector_x_log < 0 and ball_object.vector_y_log > 0: #ok
                ball_object.vector_x *= -1
            elif ball_object.vector_x_log >= 0 and ball_object.vector_y_log < 0: #ok
                ball_object.vector_y *= -1

        if hit_part == 'lower_left':
            if ball_object.vector_x_log > 0 and ball_object.vector_y_log < 0: #ok
                ball_object.vector_x *= -1
                ball_object.vector_y *= -1
            elif ball_object.vector_x_log > 0 and ball_object.vector_y_log > 0: #ok
                ball_object.vector_x *= -1
            elif ball_object.vector_x_log <= 0 and ball_object.vector_y_log < 0: #ok
                ball_object.vector_y *= -1


    def HitBlock(self, ball_object):
        hit_list = ball_object.ball.collidelistall(self.normal_block)
        hit_num = len(hit_list)

        delete_block = []

        if len(hit_list) > 2:
            self.RemainBlock(hit_list, ball_object)

        for i in hit_list:
            if ball_object.ball_x < self.normal_block[i].x and ball_object.ball_y < self.normal_block[i].y and hit_num == 1:
                self.HitCorner(ball_object, self.normal_block[i].x, self.normal_block[i].y, 'upper_left')
            elif ball_object.ball_x > self.normal_block[i].x + self.normal_block[i].width and ball_object.ball_y < self.normal_block[i].y and hit_num == 1:
                self.HitCorner(ball_object, self.normal_block[i].x + self.normal_block[i].width, self.normal_block[i].y, 'upper_right')
            elif ball_object.ball_x > self.normal_block[i].x + self.normal_block[i].width and ball_object.ball_y > self.normal_block[i].y + self.normal_block[i].height and hit_num == 1:
                self.HitCorner(ball_object, self.normal_block[i].x + self.normal_block[i].width, self.normal_block[i].y + self.normal_block[i].height, 'lower_right')
            elif ball_object.ball_x < self.normal_block[i].x and ball_object.ball_y > self.normal_block[i].y + self.normal_block[i].height and hit_num == 1:
                self.HitCorner(ball_object, self.normal_block[i].x, self.normal_block[i].y + self.normal_block[i].height, 'lower_left')
            elif ball_object.ball_x >= self.normal_block[i].x and ball_object.ball_x <= self.normal_block[i].x + self.normal_block[i].width and ball_object.ball_y < self.normal_block[i].y:
                ball_object.vector_y *= -1
            elif ball_object.ball_x > self.normal_block[i].x + self.normal_block[i].width and ball_object.ball_y >= self.normal_block[i].y and ball_object.ball_y <= self.normal_block[i].y + self.normal_block[i].height:
                ball_object.vector_x *= -1
            elif ball_object.ball_x >= self.normal_block[i].x and ball_object.ball_x <= self.normal_block[i].x + self.normal_block[i].width and ball_object.ball_y > self.normal_block[i].y + self.normal_block[i].height:
                ball_object.vector_y *= -1
            elif ball_object.ball_x < self.normal_block[i].x and ball_object.ball_y >= self.normal_block[i].y and ball_object.ball_y <= self.normal_block[i].y + self.normal_block[i].height:
                ball_object.vector_x *= -1
            else:
                pass

        for i in hit_list:
            delete_block.append(self.block_num[i])

        for i in delete_block:
            self.block_num.remove(i)

            if i in self.longer_id:
                self.breaked_block.append('shield_longer')
            elif i in self.shorter_id:
                self.breaked_block.append('shield_shorter')
            elif i in self.reset_id:
                self.breaked_block.append('shield_reseter')
            else:
                self.breaked_block.append('standard')



    def NumberBlock(self):   # Number of Block on field
        return len(self.block_num)


class Wall:
    def __init__(self):
        self.line_list = [None for i in range(4)]

    def DrawWall(self, screen, screen_height, line_width):
        self.line_list[0] = pygame.draw.line(screen, (255, 165, 0), (20, 0), (20, screen_height), line_width)
        self.line_list[1] = pygame.draw.line(screen, (255, 165, 0), (1180, 0), (1180, screen_height), line_width)
        self.line_list[2] = pygame.draw.line(screen, (255, 165, 0), (25, 4), (1175, 4), line_width)
        self.line_list[3] = pygame.draw.line(screen, (255, 165, 0), (25, 795), (1175, 795), line_width)


    def HitWall(self, ball_object):
        game_continue = True
        wall_collision = ball_object.ball.collidelistall(self.line_list)

        if len(wall_collision) > 0:
            ball_object.hit_wall = True

        for collision_num in wall_collision:
            if collision_num == 0 or collision_num == 1:
                hit_sound.play()
                ball_object.vector_x = -ball_object.vector_x
            elif collision_num == 2:
                hit_sound.play()
                ball_object.vector_y = -ball_object.vector_y
            elif collision_num == 3:
                dead_sound.play()
                game_continue = False
            else:
                pass


        return game_continue



def main():

    print('hello breakout!')
    screen_height = 800
    screen_width = 1200
    line_width = 10

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Breakout")
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)


    ball_vel = 7 #[ms]
    past_time = pygame.time.get_ticks()

    ball_object = Ball()
    wall_object = Wall()
    shield_object = Shield()
    block_object = Block()

    game_start = False


    while True:
        screen.fill((0,0,0))

        ball_object.DrawBall(screen)
        shield_object.DrawShield(screen)
        block_object.DrawBlock(screen)
        wall_object.DrawWall(screen, screen_height, line_width)

        pygame.display.update()

        if block_object.NumberBlock() == 0:
            pygame.mixer.music.stop()
            clear_bgm = pygame.mixer.music.load(CLEAR_BGM)
            pygame.mixer.music.play(loops = 1, start = 0.0)
            pygame.time.delay(6000)
            print('Game clear!!')
            break

        if pygame.key.get_mods() & KMOD_CTRL and game_start == False:
            game_start = True
            pygame.mixer.music.play(loops = -1, start = 0.0)

        if game_start == False:
            ball_object.DrawVector(screen)

        if pygame.time.get_ticks() - past_time > ball_vel and game_start == True:
            if wall_object.HitWall(ball_object) != True or shield_object.HitShield(ball_object) != True:
                pygame.mixer.music.stop()
                pygame.time.delay(1000)
                print('Game over.')
                break

            ball_object.HitException()

            block_object.HitBlock(ball_object)
            ball_object.MoveBall()
            past_time = pygame.time.get_ticks()


        shield_object.MoveShield(block_object)

        #pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                print('Game over.')
                pygame.mixer.quit()
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()

    pygame.mixer.quit()
    pygame.quit()
    sys.exit()
