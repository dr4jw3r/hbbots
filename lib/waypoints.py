from core.configurationparser import readconfig

planting_x = int(readconfig()["FARMBOT"]["PlantingLocationX"])
planting_y = int(readconfig()["FARMBOT"]["PlantingLocationY"])

WAYPOINTS = {
    "blacksmith": [
        [(58, 101), 5],
        [(63, 96), 2],
        [(64, 93), 0],
    ],
    "shop": [
        [(47, 89), 5],
        [(53, 83), 5], 
        [(61, 72), 2],
        [(61, 50), 0],
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