from time import sleep
# 
from lib.waypoints import WAYPOINTS
from lib.inputcontrol import moveto, click
from lib.npc.common import clicknpc
from lib.buttons import buttonrepairall, buttonrepair

def gotoblacksmith(movement, scanner, cancellation_token):
    movement.followwaypoints(WAYPOINTS["blacksmith"], "blacksmith")

    has_blacksmith = False
    while not has_blacksmith:
        if cancellation_token.is_cancelled:
            break

        sleep(1)
        blacksmith_pos = scanner.findnpc("blacksmith")
        has_blacksmith = blacksmith_pos[0] != -1

        if not has_blacksmith:
            movement.gotolastwaypoint(WAYPOINTS["blacksmith"], "blacksmith")

def repair(movement, scanner, cancellation_token):
    clicked = False

    while not clicked:
        clicked = clicknpc("blacksmith", scanner, cancellation_token)

        if not clicked:
            movement.gotolastwaypoint(WAYPOINTS["blacksmith"], "blacksmith")
            continue

        clicked = buttonrepairall()

        if not clicked:
            movement.gotolastwaypoint(WAYPOINTS["blacksmith"], "blacksmith")
            continue
                
        buttonrepair()