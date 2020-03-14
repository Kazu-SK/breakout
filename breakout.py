
import pygame
import pygame.mixer
from pygame.locals import *
import os
import sys
import math

pygame.init()
pygame.mixer.quit()
pygame.mixer.pre_init(22050, 16, 2, 1024)
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

        self.VECTOR_LENGTH = 5
        self.INIT_ANGLE = 45

        self.vector_x = int(self.VECTOR_LENGTH * math.sin(self.INIT_ANGLE * math.pi / 180))
        self.vector_y = int(self.VECTOR_LENGTH * math.cos(self.INIT_ANGLE * math.pi / 180))

        self.vector_x_log= [self.vector_x for i in range(3)]
        self.vector_y_log= [self.vector_y for i in range(3)]

        self.LINE_LENGTH = 30
        self.add_x = int(self.LINE_LENGTH * math.sin(self.INIT_ANGLE * math.pi / 180))
        self.add_y = int(self.LINE_LENGTH * math.cos(self.INIT_ANGLE * math.pi / 180))

        self.hit_wall = False
        self.hit_shield = False


    def DrawBall(self, screen):
        self.ball = pygame.draw.circle(screen, (255, 255, 0), (self.ball_x, self.ball_y), 10)


    def DrawVector(self, screen):
        self.line = pygame.draw.line(screen, (255, 100, 0), (self.ball_x, self.ball_y), (self.ball_x + self.add_x, self.ball_y + self.add_y), 2)


    def VectorLog(self):

        for i in range(2,-1,-1):
            if i == 0:
                self.vector_x_log[i] = self.vector_x
                self.vector_y_log[i] = self.vector_y
            else:
                self.vector_x_log[i] = self.vector_x_log[i-1]
                self.vector_y_log[i] = self.vector_y_log[i-1]


    def HitException(self):

        if self.hit_wall == True and self.hit_shield == True:
            self.vector_x = -self.vector_x_log[2]
            self.vector_y = -self.vector_y_log[2]


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
        self.SHIELD_HEIGHT = 40

        self.init_width = self.shield_width

        self.DEAD_WIDTH = 20
        self.DEAD_HEIGHT = int(self.SHIELD_HEIGHT / 2)
        self.dead = [None for i in range(2)]


    def DrawShield(self, screen):
        self.shield = pygame.draw.ellipse(screen, (0,100,0), Rect(self.shield_x,self.shield_y,self.shield_width,self.SHIELD_HEIGHT), 0)
        self.dead[0] = pygame.draw.rect(screen, (255, 0, 0), Rect(int(self.shield_x - self.DEAD_WIDTH / 2), int(self.shield_y + self.SHIELD_HEIGHT / 2), self.DEAD_WIDTH, self.DEAD_HEIGHT))
        self.dead[1] = pygame.draw.rect(screen, (255, 0, 0), Rect(int(self.shield_x + self.shield_width - self.DEAD_WIDTH / 2), int(self.shield_y + self.SHIELD_HEIGHT / 2), self.DEAD_WIDTH, self.DEAD_HEIGHT))


    def HitShield(self, ball_object):

        if ball_object.ball.collidelist(self.dead) != -1:
            dead_sound.play()
            return False

        if ball_object.ball.colliderect(self.shield) == True:
            ball_object.hit_shield = True
            hit_sound.play()

            #Caluclate ellipse's base point.
            base_x = self.shield_x + self.shield_width / 2
            base_y = self.shield_y + self.shield.height * 1.5

            a1 = ball_object.ball_x - base_x
            a2 = ball_object.ball_y - base_y
            b1 = 1
            b2 = 0

            cos_theta = (a1 * b1 + a2 * b2) / (math.sqrt(a1 * a1 + a2 * a2) * math.sqrt(b1 * b1 + b2 * b2))
            sin_theta = math.sqrt(1 - cos_theta * cos_theta)

            angle = math.acos(cos_theta) * 180 / math.pi
            angle = 90 - angle
            angle = math.radians(angle)

            cos_theta = math.cos(angle)
            sin_theta = math.sin(angle)

            ball_object.vector_x = int(ball_object.VECTOR_LENGTH * sin_theta)
            ball_object.vector_y = int(-ball_object.VECTOR_LENGTH * cos_theta)


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


    def ComboReset(self,ball_object):
        return ball_object.ball.colliderect(self.shield)



class Block:
    def __init__(self):
        self.normal_block = []
        self.breaked_block = []
        self.combo_block = []
        self.block_num = list(range(66))

        self.init_x = 130
        self.init_y = 100

        self.LONGER_ID = [20, 49]
        self.SHORTER_ID = [16, 47, 51]
        self.RESET_ID = [12]

        self.block_x = []
        self.block_y = []
        self.BLOCK_HEIGHT = 50
        self.BLOCK_WEIGHT = 80
        x = 0
        y = 50

        for i in range(6):
            if i == 0:
                y = self.init_y
            else:
                y = y + self.BLOCK_HEIGHT + 1
            #x = 50
            for j in range(11):
                if j == 0:
                    x = self.init_x
                else:
                    x = x + self.BLOCK_WEIGHT + 1
                self.block_x.append(x)
                self.block_y.append(y)


    def DrawBlock(self, screen):
        self.normal_block.clear()

        for i in self.block_num:
            if i in self.LONGER_ID:
                block = pygame.draw.rect(screen, (0,255,255), (self.block_x[i], self.block_y[i], self.BLOCK_WEIGHT, self.BLOCK_HEIGHT))
            elif i in self.SHORTER_ID:
                block = pygame.draw.rect(screen, (0,0,255), (self.block_x[i], self.block_y[i], self.BLOCK_WEIGHT, self.BLOCK_HEIGHT))
            elif i in self.RESET_ID:
                block = pygame.draw.rect(screen, (255,255,255), (self.block_x[i], self.block_y[i], self.BLOCK_WEIGHT, self.BLOCK_HEIGHT))
            else:
                block = pygame.draw.rect(screen, (100,200,50), (self.block_x[i], self.block_y[i], self.BLOCK_WEIGHT, self.BLOCK_HEIGHT))

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
            if ball_object.vector_x_log[0] > 0 and ball_object.vector_y_log[0] > 0:
                ball_object.vector_x *= -1
                ball_object.vector_y *= -1
            elif ball_object.vector_x_log[0] <= 0 and ball_object.vector_y_log[0] > 0:
                ball_object.vector_y *= -1
            elif ball_object.vector_x_log[0] > 0 and ball_object.vector_y_log[0] < 0:
                ball_object.vector_x *= -1

        if hit_part == 'upper_right':
            if ball_object.vector_x_log[0] < 0 and ball_object.vector_y_log[0] > 0:
                ball_object.vector_x *= -1
                ball_object.vector_y *= -1
            elif ball_object.vector_x_log[0] >= 0 and ball_object.vector_y_log[0] > 0:
                ball_object.vector_y *= -1
            elif ball_object.vector_x_log[0] < 0 and ball_object.vector_y_log[0] < 0:
                ball_object.vector_x *= -1

        if hit_part == 'lower_right':
            if ball_object.vector_x_log[0] < 0 and ball_object.vector_y_log[0] < 0:
                ball_object.vector_x *= -1
                ball_object.vector_y *= -1
            elif ball_object.vector_x_log[0] < 0 and ball_object.vector_y_log[0] > 0:
                ball_object.vector_x *= -1
            elif ball_object.vector_x_log[0] >= 0 and ball_object.vector_y_log[0] < 0:
                ball_object.vector_y *= -1

        if hit_part == 'lower_left':
            if ball_object.vector_x_log[0] > 0 and ball_object.vector_y_log[0] < 0:
                ball_object.vector_x *= -1
                ball_object.vector_y *= -1
            elif ball_object.vector_x_log[0] > 0 and ball_object.vector_y_log[0] > 0:
                ball_object.vector_x *= -1
            elif ball_object.vector_x_log[0] <= 0 and ball_object.vector_y_log[0] < 0:
                ball_object.vector_y *= -1


    def HitBlock(self, ball_object, combo_reseter):
        hit_list = ball_object.ball.collidelistall(self.normal_block)
        hit_num = len(hit_list)

        delete_block = []

        if combo_reseter == True:
            self.combo_block.clear()

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

        break_num = 0

        for i in delete_block:
            break_num = break_num + 1

            self.block_num.remove(i)

            if i in self.LONGER_ID:
                self.breaked_block.append('shield_longer')
            elif i in self.SHORTER_ID:
                self.breaked_block.append('shield_shorter')
            elif i in self.RESET_ID:
                self.breaked_block.append('shield_reseter')
            else:
                self.breaked_block.append('standard')

            self.combo_block.append('combo')


        return break_num


    def NumberBlock(self):   # Number of Block on field
        return len(self.block_num)


    def NumberCombo(self):
        return len(self.combo_block)



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



class Score:
    def __init__(self, x, y):
        self.score_font = pygame.font.SysFont(None, 20)
        self.game_score = 0
        (self.POSITION_X, self.POSITION_Y) = (x, y)

        self.BGM_TIME = 276 * 2 #[s] bgm's time * 2

        self.BREAK_POINT = 10
        self.COMBO_POINT = 5


    def DrawScore(self, screen):
        score_img = self.score_font.render("SCORE : " + str(self.game_score), True, (255, 200, 250))
        screen.blit(score_img, (self.POSITION_X, self.POSITION_Y))


    def AddScore(self, break_num, combo_num):

        if break_num > 0 and combo_num > 1:
            self.game_score += self.BREAK_POINT * break_num + self.COMBO_POINT * combo_num
        elif break_num > 0:
            self.game_score += self.BREAK_POINT * break_num


    def AddBonus(self, work_time):
        bonus_score = self.BGM_TIME - int(work_time / 1000)

        if bonus_score > 0:
            print('Bonus : ',bonus_score)
            self.game_score += bonus_score
        else:
            print('No bonus.')


    def OutputScore(self):
        print('SCORE :',self.game_score)



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
    score_object = Score(40, 20)

    game_start = False


    while True:
        screen.fill((0,0,0))

        ball_object.DrawBall(screen)
        shield_object.DrawShield(screen)
        block_object.DrawBlock(screen)
        wall_object.DrawWall(screen, screen_height, line_width)
        score_object.DrawScore(screen)

        if pygame.key.get_mods() & KMOD_CTRL and game_start == False:
            game_start = True
            pygame.mixer.music.play(loops = -1, start = 0.0)
            start_time = pygame.time.get_ticks()


        if game_start == False:
            ball_object.DrawVector(screen)

        pygame.display.update()

        if block_object.NumberBlock() == 0:
            pygame.mixer.music.stop()
            clear_bgm = pygame.mixer.music.load(CLEAR_BGM)
            pygame.mixer.music.play(loops = 1, start = 0.0)
            pygame.time.delay(6000)

            work_time = pygame.time.get_ticks() - start_time
            score_object.AddBonus(work_time)

            score_object.OutputScore()
            print('Game clear!!')
            break

        if pygame.time.get_ticks() - past_time > ball_vel and game_start == True:
            if wall_object.HitWall(ball_object) != True or shield_object.HitShield(ball_object) != True:
                pygame.mixer.music.stop()
                pygame.time.delay(1000)
                score_object.OutputScore()
                print('Game over.')
                break

            ball_object.HitException()

            break_num = block_object.HitBlock(ball_object, shield_object.ComboReset(ball_object))

            score_object.AddScore(break_num, block_object.NumberCombo())

            ball_object.MoveBall()
            past_time = pygame.time.get_ticks()


        shield_object.MoveShield(block_object)

        for event in pygame.event.get():
            if event.type == QUIT:
                print('Game quit.')
                pygame.mixer.quit()
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()

    pygame.mixer.quit()
    pygame.quit()
    sys.exit()
