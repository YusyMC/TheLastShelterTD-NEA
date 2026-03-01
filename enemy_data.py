ENEMY_DATA = {
    "walker": {
        "health": 10,
        "speed": 30,
        "damage": 5,
        "currency": 25
    },
    "runner": {
        "health": 10,
        "speed": 60,
        "damage": 5,
        "currency": 50
    },
    "armoured": {
        "health": 50,
        "speed": 15,
        "damage": 20,
        "currency": 100
    },
    "boss": {
        "health": 100,
        "speed": 30,
        "damage": 100,
        "currency": 500
    }
}

ENEMY_WAVE_DATA = [
    {
        # Wave 1
        "walker": 1,
        "runner": 1,
        "armoured": 1,
        "boss": 1
    },
    {
        # Wave 2
        "walker": 10,
        "runner": 0,
        "armoured": 0,
        "boss": 0
    },
    {
        # Wave 3
        "walker": 10,
        "runner": 3,
        "armoured": 0,
        "boss": 0
    },
    {
        # Wave 4
        "walker": 10,
        "runner": 5,
        "armoured": 1,
        "boss": 0
    },
    {
        # Wave 5
        "walker": 10,
        "runner": 5,
        "armoured": 3,
        "boss": 0
    },
    {
        # Wave 6
        "walker": 10,
        "runner": 5,
        "armoured": 5,
        "boss": 0
    },
    {
        # Wave 7
        "walker": 15,
        "runner": 5,
        "armoured": 5,
        "boss": 0
    },
    {
        # Wave 8
        "walker": 15,
        "runner": 8,
        "armoured": 6,
        "boss": 0
    },
    {
        # Wave 9
        "walker": 15,
        "runner": 8,
        "armoured": 8,
        "boss": 0
    },
    {
        # Wave 10
        "walker": 5,
        "runner": 5,
        "armoured": 5,
        "boss": 1
    }
]