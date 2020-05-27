from lib.inputcontrol import moveto, click

def go(x, y):
    moveto((x, y))
    click()

def isclose(direction):
    xclose = False
    yclose = False

    DISTANCE_THR = 2

    if abs(direction[0]) <= DISTANCE_THR:
        xclose = True

    if abs(direction[1]) <= DISTANCE_THR:
        yclose = True

    return (xclose, yclose)

def leftup(direction):
    close = isclose(direction)

    x = 363 if close[0] else 48
    y = 274 if close[1] else 48

    go(x, y)

def up(direction):
    close = isclose(direction)

    x = 400
    y = 235 if close[1] else 50

    go(x, y)

def rightup(direction):
    close = isclose(direction)

    x = 435 if close[0] else 560
    y = 270 if close[1] else 150

    go(x, y)

def right(direction):
    close = isclose(direction)

    x = 435 if close[0] else 560 
    y = 300

    go(x, y)

def rightdown(direction):
    close = isclose(direction)

    x = 400 if close[0] else 655
    y = 330 if close[1] else 530

    go(x, y)

def down(direction):
    close = isclose(direction)

    x = 150
    y = 500 if close[1] else 330

    go(x, y)

def leftdown(direction):
    close = isclose(direction)

    x = 370 if close[0] else 180
    y = 340 if close[1] else 530

    go(x, y)

def left(direction):
    close = isclose(direction)

    x = 360 if close[0] else 100
    y = 300

    go(x, y)