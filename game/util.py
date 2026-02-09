cores = {
    "black": (0,0,0),
    "white": (255, 255, 255),
    "MAP_COLOR": (0, 0, 0),
    "TERMINAL_COLOR": (12, 12, 12),
    "TERMINAL_TXT": (0, 255, 0)  # verde neon
}

screen_config = {
    "size": (1300, 800),
    "width": 1300,
    "height": 800,
}

map_config = {
    "width": 700
}

terminal_config = {
    "width": screen_config["width"] - map_config["width"],
    "heigth": 800,
}

