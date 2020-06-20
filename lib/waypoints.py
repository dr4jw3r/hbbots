from core.configurationparser import readconfig

planting_x = int(readconfig()["FARMBOT"]["PlantingLocationX"])
planting_y = int(readconfig()["FARMBOT"]["PlantingLocationY"])

WAYPOINTS = {
    "snake_pit": [
        [(91, 85), 5],
        [(160, 85), 5],
        [(211, 64), 2],
        [(215, 59), 2],
    ],
    "blacksmith": [
        [(58, 101), 5],
        [(63, 96), 2],
        [(63, 92), 0],
    ],
    "shop": [
        [(47, 89), 5],
        [(53, 83), 5], 
        [(61, 72), 2],
        [(63, 70), 0],
    ],
    "shop_inside": [
        [(53, 41), 5],
    ],
    "planting_spot": [
        [(59, 100), 5],
        [(70, 103), 5],
        [(planting_x, planting_y), 0],
    ]
    
}