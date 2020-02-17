from Gfx.SpriteTemplate import SpriteTemplate
from Misc.Settings import *
import pygame as pg
from random import choice

class Player(SpriteTemplate):
    def __init__(self, game, x, y):
        self.game = game
        super().__init__(game, x, y, self.game.sprites["player"], self.game.sprite_handler.get_tile(1066))
        self.direction = "down"
        self.moving = False
        self.running = False

        self.vel = pg.math.Vector2(0, 0)
        self.vx, self.vy = 0, 0
        self.dest_x, self.dest_y = 0, 0
        self.orig_x, self.orig_y = 0, 0

        self.player_speed = 3

    def get_pos(self):
        for sprite_obj in self.game.sprites["player"]:
            return sprite_obj.x, sprite_obj.y


    def move(self, x=0, y=0):
        if not self.moving and any([x>0, x<0]) or any([y>0, y<0]):
            self.vx, self.vy = 0, 0
            self.direction = "left" if 0 > x else "right" if x > 0 else "down" if y > 0 else "up"

            self.orig_x, self.orig_y = self.rect.x, self.rect.y

            self.dest_x = self.orig_x-TILESIZE*abs(x) if x < 0 else self.orig_x+(TILESIZE*x) if x > 0 else self.orig_x
            self.dest_y = self.orig_y-TILESIZE*abs(y) if y < 0 else self.orig_y+(TILESIZE*y) if y > 0 else self.orig_y

            if self.game.map_handler.path_walkable(self.dest_x, self.dest_y):
                self.moving = True
        else:
            self.move_animation()
            if self.direction == "up":
                    reset = True if self.rect.y < self.dest_y else False
            elif self.direction == "down":
                    reset = True if self.rect.y > self.dest_y else False
            elif self.direction == "left":
                    reset = True if self.rect.x < self.dest_x else False
            elif self.direction == "right":
                    reset = True if self.rect.x > self.dest_x else False

            if reset:
                self.reset_player()
                self.moving = False

    def set_pos(self, x, y):
        self.rect.x = x*TILESIZE
        self.rect.y = y*TILESIZE

    def get_player_image(self):
        image_set = self.game.sprite_handler.load_spriteset("npc_1")
        image = self.image

        if self.moving:
            if self.direction == "down":
                down = image_set[0]
                image = self.game.sprite_handler.get_tile(choice(down))
            elif self.direction == "left":
                left = image_set[1]
                image = self.game.sprite_handler.get_tile(choice(left))
            elif self.direction == "right":
                right = image_set[2]
                image = self.game.sprite_handler.get_tile(choice(right))
            elif self.direction == "up":
                up = image_set[3]
                image = self.game.sprite_handler.get_tile(choice(up))
        self.image = image
        return self.image
    def move_animation(self):
        if self.moving:
            speed = self.player_speed if not self.running else self.player_speed // 1.3

            if self.direction == "up":
                self.rect.y += -TILESIZE//speed
            elif self.direction == "down":
                self.rect.y += TILESIZE //speed
            elif self.direction == "right":
                self.rect.x += TILESIZE//speed
            elif self.direction == "left":
                self.rect.x -= TILESIZE//speed

    def reset_player(self):
        self.moving = False
        self.rect.x = round(self.dest_x/32)*TILESIZE
        self.rect.y = round(self.dest_y/32)*TILESIZE

        if self.game.map_handler.is_teleport_tile(self.dest_x, self.dest_y):
            tele_x, tele_y = self.game.map_handler.get_teleport_location(self.dest_x, self.dest_y)
            self.set_pos(tele_x, tele_y)
        else:
            self.dest_x, self.dest_y = 0, 0

    # Move cyclus.
    def update(self):
        if not self.moving:
            self.rect.x += self.vx * self.game.delta
            self.rect.y += self.vy * self.game.delta
        else:
            self.move()
