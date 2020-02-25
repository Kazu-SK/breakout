
import pygame
import pygame.mixer
from pygame.locals import *
import os
import sys
import math

pygame.init()
pygame.mixer.init(frequency = 44100)

ROOT_DIR = os.path.abspath("sound/")

HIT_OTHER = os.path.join(ROOT_DIR, "se_maoudamashii_system35.wav")
HIT_BlOCK = os.path.join(ROOT_DIR, "se_maoudamashii_system27.wav")
HIT_DEAD = os.path.join(ROOT_DIR, "se_maoudamashii_battle07.wav")

hit_sound = pygame.mixer.Sound(HIT_OTHER)
block_sound = pygame.mixer.Sound(HIT_BlOCK)
dead_sound = pygame.mixer.Sound(HIT_DEAD)



class Ball:
    def __init__(self):
        self.ball_x = 600
        self.ball_y = 600
        self.vector_length = 5
        self.init_angle = -45
        self.vector_x = int(self.vector_length * math.sin(self.init_angle * math.pi / 180))
        self.vector_y = int(self.vector_length * math.cos(self.init_angle * math.pi / 180))

        self.logvec_x = self.vector_x
        self.logvec_y = self.vector_y

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
        self.logvec_x = self.vector_x
        self.logvec_y = self.vector_y

    def HitException(self):

        if self.hit_wall == True and self.hit_shield == True:
            self.vector_x = -self.logvec_x
            self.vector_y = -self.logvec_y

    def MoveBall(self):
        self.ball_x += self.vector_x
        self.ball_y += self.vector_y
        self.hit_wall = False
        self.hit_shield = False


class Shield:
    def __init__(self):
        self.shield_x = 80
        self.shield_y = 700

        self.shield_width = 100
        self.shield_height = 40

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
            base_y = self.shield_y + self.shield_height# / 2

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


    def MoveShield(self):
        move_x , move_y = pygame.mouse.get_rel()
        self.shield_x = self.shield_x + move_x
        #shield_y = shield_y + 5
        if self.shield_x < 27:
            self.shield_x = 27
        elif self.shield_x + self.shield_width > 1173:
            self.shield_x = 1173 - self.shield_width

        self.shield.move_ip(self.shield_x, self.shield_y)
        #print(self.shield_x)
        #print(self.shield_y)


class Block:
    def __init__(self):
        #self.normal_block = [None for i in range(30)]


        self.normal_block = []
        self.breaked_block = []
        self.block_num = list(range(66))

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
            block = pygame.draw.rect(screen, (100,200,50), (self.block_x[i], self.block_y[i], self.block_weight, self.block_height))
            self.normal_block.append(block)

        #clip_object = self.normal_block[0].clip(self.normal_block[1])
#        print(clip_object.width)
#        print(clip_object.x)
#        print(clip_object.y)
        #block = pygame.draw.rect(screen, (100,200,50), (130, 400, self.block_weight, self.block_height))
        #self.normal_block.append(block)



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

    def HitBlock(self, ball_object):

        hit_list = ball_object.ball.collidelistall(self.normal_block)
        hit_num = len(hit_list)

        delete_block = []

        if len(hit_list) > 0:
            block_sound.play()

        if len(hit_list) > 2:
            print('Triple!!!')
            self.RemainBlock(hit_list, ball_object)


        for i in hit_list:
            #print(i)
            if ball_object.ball_x < self.normal_block[i].x and ball_object.ball_y < self.normal_block[i].y and hit_num == 1:
                ball_object.vector_x *= -1
                ball_object.vector_y *= -1
    #            print('hit1')
            elif ball_object.ball_x > self.normal_block[i].x + self.normal_block[i].width and ball_object.ball_y < self.normal_block[i].y and hit_num == 1:
                ball_object.vector_x *= -1
                ball_object.vector_y *= -1
    #            print('hit2')
            elif ball_object.ball_x > self.normal_block[i].x + self.normal_block[i].width and ball_object.ball_y > self.normal_block[i].y + self.normal_block[i].height and hit_num == 1:
                ball_object.vector_x *= -1
                ball_object.vector_y *= -1
    #            print('hit3')
            elif ball_object.ball_x < self.normal_block[i].x and ball_object.ball_y > self.normal_block[i].y + self.normal_block[i].height and hit_num == 1:
                ball_object.vector_x *= -1
                ball_object.vector_y *= -1
     #           print('hit4')
            elif ball_object.ball_x >= self.normal_block[i].x and ball_object.ball_x <= self.normal_block[i].x + self.normal_block[i].width and ball_object.ball_y < self.normal_block[i].y:
                ball_object.vector_y *= -1
                #print('hit5')
     #           if i == 0:
     #               print('ball_object.ball_x = {0}'.format(ball_object.ball_x))
     #               print('block[{0}].x + width = {1}'.format(i,self.normal_block[i].x + self.normal_block[i].width))
     #           else:
     #               print('ball_object.ball_x = {0}'.format(ball_object.ball_x))
     #               print('block[{0}].x = {1}'.format(i,self.normal_block[i].x))
            elif ball_object.ball_x > self.normal_block[i].x + self.normal_block[i].width and ball_object.ball_y >= self.normal_block[i].y and ball_object.ball_y <= self.normal_block[i].y + self.normal_block[i].height:
                ball_object.vector_x *= -1
     #           print('hit6')
            elif ball_object.ball_x >= self.normal_block[i].x and ball_object.ball_x <= self.normal_block[i].x + self.normal_block[i].width and ball_object.ball_y > self.normal_block[i].y + self.normal_block[i].height:
                ball_object.vector_y *= -1
     #           print('hit7')
            elif ball_object.ball_x < self.normal_block[i].x and ball_object.ball_y >= self.normal_block[i].y and ball_object.ball_y <= self.normal_block[i].y + self.normal_block[i].height:
                ball_object.vector_x *= -1
     #           print('hit8')
            else:
                """
                print('pass')
                print('ball_object.ball_x = {0}'.format(ball_object.ball_x))
                print('ball_object.ball_y = {0}'.format(ball_object.ball_y))
                print('block[{0}].x = {1}'.format(i,self.normal_block[i].x))
                print('block[{0}].x + width = {1}'.format(i,self.normal_block[i].x + self.normal_block[i].width))
                """
                pass


        for i in hit_list:
            delete_block.append(self.block_num[i])

        for i in delete_block:
            self.block_num.remove(i)



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

    print('hello blockout!')
    screen_height = 800
    screen_width = 1200
    line_width = 10

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Blockout")
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)


    ball_vel = 7 #[ms]
    past_time = pygame.time.get_ticks()

    ball_object = Ball()
    wall_object = Wall()
    shield_object = Shield()
    block_object = Block()

    game_start = False
    #game_continue = True

    while True:
        screen.fill((0,0,0))

        ball_object.DrawBall(screen)
        shield_object.DrawShield(screen)
        block_object.DrawBlock(screen)
        wall_object.DrawWall(screen, screen_height, line_width)


        if pygame.key.get_mods() & KMOD_CTRL and game_start == False:
            game_start = True

        if game_start == False:
            ball_object.DrawVector(screen)

        if (pygame.time.get_ticks() - past_time > ball_vel) and game_start == True:
            if wall_object.HitWall(ball_object) != True:
                break
            if shield_object.HitShield(ball_object) != True:
                break

            ball_object.HitException()

            block_object.HitBlock(ball_object)
            ball_object.MoveBall()
            past_time = pygame.time.get_ticks()

        #if game_continue != True:
        #    break

        shield_object.MoveShield()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.time.delay(1000)
                print('Game over.')
                pygame.mixer.quit()
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()

    pygame.time.delay(1000)
    print('Game over.')
    pygame.mixer.quit()
    pygame.quit()
    sys.exit()
