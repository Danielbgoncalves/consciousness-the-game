import pygame
from  game.MapDisplay.Building import Building

def load():
    buildings_data = [
        {"id":1, "x":280, "y":232, "path": "assets/buildings/b1.png"},
        {"id":2, "x":343, "y":240, "path": "assets/buildings/b2.png"},
        {"id":3, "x":405, "y":235, "path": "assets/buildings/b3.png"},
        {"id":4, "x":457, "y":253, "path": "assets/buildings/b4.png"},
        {"id":5, "x":535, "y":272, "path": "assets/buildings/b5.png"},
        {"id":6, "x":467, "y":303, "path": "assets/buildings/b6.png"},
        {"id":7, "x":415, "y":385, "path": "assets/buildings/b7.png"},
        {"id":8, "x":320, "y":320, "path": "assets/buildings/b14.png"},
        {"id":9, "x":240, "y":285, "path": "assets/buildings/b9.png"},
        {"id":10, "x":247, "y":333, "path": "assets/buildings/b10.png"},
        {"id":11, "x":300, "y":395, "path": "assets/buildings/b11.png"},
        {"id":12, "x":480, "y":355, "path": "assets/buildings/b12.png"},
        {"id":13, "x":415, "y":385, "path": "assets/buildings/b7.png"},
        {"id":14, "x":510, "y":430, "path": "assets/buildings/b13.png"}
    ]

    buildings = []
    for data in buildings_data:
        img = pygame.image.load(data["path"]).convert_alpha()
        building = Building(data["id"],data["x"],data["y"],img)
        buildings.append(building)

    return buildings


