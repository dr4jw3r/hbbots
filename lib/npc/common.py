from time import sleep
from lib.inputcontrol import moveto, click

def clicknpc(npc, scanner, cancellation_token, offset=30):
    if cancellation_token.is_cancelled:
        return

    (npc_pos, has_npc) = scanner.findnpc(npc)

    if has_npc:
        moveto(npc_pos, offset)
        sleep(0.1)
        click()  
        sleep(0.1)
        return True
    
    return False