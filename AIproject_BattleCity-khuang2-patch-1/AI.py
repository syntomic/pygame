import pygame
#self.controls = [pygame.K_SPACE, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT]
import random



global pressed, TEST_AI, color

TEST_AI = True
(DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT) = range(4)


def generate_Path_Enemy():
    return [[9, 3], [10, 3], [11, 3], [12, 3], [13, 3], [14, 3], [15, 3], [16, 3], [17, 3], [18, 3], [19, 3], [20, 3], [21, 3], [22, 3], [23, 3], [24, 3], [25, 3], [26, 3], [27, 3], [28, 3], [29, 3], [30, 3], [31, 3], [32, 3], [33, 3], [34, 3], [35, 3], [36, 3], [37, 3], [38, 3], [39, 3], [40, 3], [41, 3], [42, 3], [43, 3], [44, 3], [45, 3], [46, 3], [47, 3], [48, 3], [49, 3], [50, 3], [51, 3], [52, 3], [53, 3], [54, 3], [55, 3], [56, 3], [57, 3], [58, 3], [59, 3], [60, 3], [61, 3], [62, 3], [63, 3], [64, 3], [65, 3], [66, 3], [67, 3], [68, 3], [69, 3], [70, 3], [71, 3], [72, 3], [73, 3], [74, 3], [75, 3], [76, 3], [77, 3], [78, 3], [79, 3], [80, 3], [81, 3], [82, 3], [83, 3], [84, 3], [85, 3], [86, 3], [87, 3], [88, 3], [89, 3], [90, 3], [91, 3], [92, 3], [93, 3], [94, 3], [95, 3], [96, 3], [97, 3], [98, 3], [99, 3], [100, 3], [101, 3], [102, 3], [103, 3], [104, 3], [105, 3], [106, 3], [107, 3], [108, 3], [109, 3], [110, 3], [111, 3], [112, 3], [113, 3], [114, 3], [115, 3], [116, 3], [117, 3], [118, 3], [119, 3], [120, 3], [121, 3], [122, 3], [123, 3], [124, 3], [125, 3], [126, 3], [127, 3], [128, 3], [129, 3], [130, 3], [131, 3], [132, 3], [133, 3], [134, 3], [135, 3], [136, 3], [137, 3], [138, 3], [139, 3], [140, 3], [141, 3], [142, 3], [143, 3], [144, 3], [145, 3], [146, 3], [147, 3], [148, 3], [149, 3], [150, 3], [151, 3], [152, 3], [153, 3], [154, 3], [155, 3], [156, 3], [157, 3], [158, 3], [159, 3], [160, 3], [161, 3], [162, 3], [163, 3], [164, 3], [165, 3], [166, 3], [167, 3], [168, 3], [169, 3], [170, 3], [171, 3], [172, 3], [173, 3], [174, 3], [175, 3], [176, 3], [177, 3], [178, 3], [179, 3], [180, 3], [181, 3], [182, 3], [183, 3], [184, 3], [185, 3], [186, 3], [187, 3], [188, 3], [189, 3], [190, 3], [191, 3], [192, 3], [193, 3], [194, 3], [195, 3], [196, 3], [197, 3], [198, 3], [199, 3], [200, 3], [201, 3], [202, 3], [203, 3], [204, 3], [205, 3], [206, 3], [207, 3], [208, 3], [209, 3], [210, 3], [211, 3], [212, 3], [213, 3], [214, 3], [215, 3], [216, 3], [217, 3], [218, 3], [219, 3], [220, 3], [221, 3], [222, 3], [223, 3], [224, 3], [225, 3], [226, 3], [227, 3], [228, 3], [229, 3]]


def print_Enemy_Path(screen, enemies):
    for enemie in enemies:
        for position in enemie.path:
            p = [position[0] + 493, position[1] + 13]
            screen.fill([0, 0, 255], pygame.Rect(p , [26, 26]))
    return

def drawAstarSearch(screen, enemies):
    #print(enemies[0].direction)
    index = 0
    for enemie in enemies:
        color3 = 50 + 50 * (index % 4)
        color2 = 100 + 50 * (index % 3)
        color1 = 23 * (index % 4)
        for position in enemie.path:
            p = [position[0] + 480, position[1]]
            screen.fill([color3, color2, color1], pygame.Rect(p , [26, 26]))
        index += 1
    return

def generate_map_forai(screen, topleft):

    screen.fill([0, 255, 255], pygame.Rect(topleft, [16, 16]))
    return

def ai_press(key):

    if key == 0:# space, fire
        return pygame.event.Event(pygame.KEYDOWN,scancode= 65, key=pygame.K_SPACE, unicode=u'', mod = 0)
    elif key == 1:# move up
        return pygame.event.Event(pygame.KEYDOWN,scancode= 111, key=pygame.K_UP, unicode=u'', mod = 0)
    elif key == 2:# move right
        return pygame.event.Event(pygame.KEYDOWN,scancode= 114, key=pygame.K_RIGHT, unicode=u'', mod = 0)
    elif key == 3:# move down
        return pygame.event.Event(pygame.KEYDOWN,scancode= 116, key=pygame.K_DOWN, unicode=u'', mod = 0)
    elif key == 4:# move left
        return pygame.event.Event(pygame.KEYDOWN,scancode= 113, key=pygame.K_LEFT, unicode=u'', mod = 0)

def ai_release(key):
    if key == 0:# space, fire
        return pygame.event.Event(pygame.KEYUP,scancode= 65, key=pygame.K_SPACE, mod = 0)
    elif key == 1:# move up
        return pygame.event.Event(pygame.KEYUP,scancode= 111, key=pygame.K_UP, mod = 0)
    elif key == 2:# move right
        return pygame.event.Event(pygame.KEYUP,scancode= 114, key=pygame.K_RIGHT, mod = 0)
    elif key == 3:# move down
        return pygame.event.Event(pygame.KEYUP,scancode= 116, key=pygame.K_DOWN, mod = 0)
    elif key == 4:# move left
        return pygame.event.Event(pygame.KEYUP,scancode= 113, key=pygame.K_LEFT, mod = 0)

pressed = False

def test_nextmove(time_elapse):
    global pressed
    if time_elapse % 1000 in range(1,10) and pressed is False:
        print(time_elapse)
        pressed = True
        return ai_press(1)
    elif time_elapse % 2000 in range(1,10) and pressed is True:
        print(time_elapse)
        pressed = False
        return ai_release(1)
    else:
        return None

def update_astarMap(astar_map, player_position = None, recover = True):
    x = int(round(player_position[1] / 16))
    y = int(round(player_position[0] / 16))

    if recover == True:
        score_player = 1
    else:
        score_player = 99

    astar_map[x][y] = score_player
    if x < 25:
        astar_map[x + 1][y] = score_player
    if y < 25:
        astar_map[x][y + 1] = score_player
    if x < 25 and y < 25:
        astar_map[x + 1][y + 1] = score_player


def update_costmap(astar_map, costmap):

    for i in range(25):
        for j in range(25):
            if(astar_map[i][j] == 9
               or astar_map[i+ 1][j] == 9
               or astar_map[i][j + 1] == 9
               or astar_map[i + 1][j + 1] == 9):
                costmap[i][j] = 9
                costmap[i + 1][j] = 9
                costmap[i][j + 1] = 9
                costmap[i + 1][j + 1] = 9
    print(costmap)
    return costmap
