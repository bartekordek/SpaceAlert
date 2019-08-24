import sys, pygame

import Constants as Const
from GameInit import screen, background, ship_imgs, proj1_imgs
from PlayerShipObject import PlayerShipObject as PlayerShip
from ProjectileObject import ProjectileObject as Projectile
from Support import directions

#-----------------------------------------------------------------------------

# Game will be more in Asteroids type:
# keys left/right - ship rotation
# keys up/down - accelerate/break
# spaceship won't stop moving until player stops it

#-----------------------------------------------------------------------------

screen.blit(background, (0, 0))
screen_center = ((Const.disp_width - Const.ship_size[0]) // 2, (Const.disp_height - Const.ship_size[1]) // 2)

spaceship = PlayerShip(ship_imgs[0], screen_center, speed=0)
old_center = ship_imgs[0].get_rect().center
projectiles = []

rot_delay = 1

while 1:
    for event in pygame.event.get():
        if event.type in (pygame.QUIT,):
            sys.exit()

    screen.blit(background, spaceship.pos, spaceship.pos)
    for proj in projectiles:
        screen.blit(background, proj.pos, proj.pos)

    for x in range(len(projectiles)-1, -1, -1):
        if projectiles[x].dist > projectiles[x].max_dist:
            projectiles.remove(projectiles[x])

    spaceship.move_sp()

    if spaceship.pos.left > Const.disp_width:
        spaceship.pos.right = 0
    if spaceship.pos.top > Const.disp_height:
        spaceship.pos.bottom = 0
    if spaceship.pos.right < 0:
        spaceship.pos.left = Const.disp_width
    if spaceship.pos.bottom < 0:
        spaceship.pos.top = Const.disp_height

    r = pygame.key.get_pressed()[pygame.K_RIGHT]
    l = pygame.key.get_pressed()[pygame.K_LEFT]
    u = pygame.key.get_pressed()[pygame.K_UP]
    d = pygame.key.get_pressed()[pygame.K_DOWN]
    sp = pygame.key.get_pressed()[pygame.K_SPACE]

    if rot_delay > 0:
        rot_delay -= 1

    if r and not rot_delay:
        rot_delay = Const.rot_delay
        spaceship.direc -= 1
        if spaceship.direc < 0:
            spaceship.direc += len(directions)
        spaceship.change_direc(spaceship.direc)

    if l and not rot_delay:
        rot_delay = Const.rot_delay
        spaceship.direc += 1
        spaceship.direc %= len(directions)
        spaceship.change_direc(spaceship.direc)

    if u:
        if spaceship.speed < Const.ship_max_speed:
            spaceship.increase_speed(1)
        spaceship.set_speed_xy_from_direc()

    if d:
        if spaceship.speed > 0:
            spaceship.decrease_speed(1)
        spaceship.set_speed_xy_from_direc()

    if sp:
        n_projs = len(projectiles)
        if n_projs == 0 or projectiles[n_projs-1].dist > Const.proj_delay:
            proj_speed = Const.proj_speed + spaceship.speed     # ???
            b = Projectile(proj1_imgs[0], spaceship.pos.center, ship=spaceship, speed=proj_speed, direc=spaceship.direc)
            projectiles.append(b)

    for proj in projectiles:
        proj.move_sp()
        proj.dist += 1

    screen.blit(spaceship.image, spaceship.pos)
    for proj in projectiles:
        screen.blit(proj.image, proj.pos)

    pygame.display.update()
    pygame.time.delay(Const.time_delay)