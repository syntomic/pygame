import sys, pygame
pygame.init() # pylint: disable=no-member

size = width, height = 320, 240
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("image/intro_ball.gif")
ballrect = ball.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit() # pylint: disable=no-member
                   
        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]

        screen.fill(black) # 防止拖影
        screen.blit(ball, ballrect) # 球图像绘制到屏幕上
        pygame.display.flip() # 更新可见显示