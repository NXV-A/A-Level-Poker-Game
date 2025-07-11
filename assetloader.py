import os

imgGroups = {
    "Assets/Cards/": [
            '2 of Hearts',
            '3 of Hearts',
            '4 of Hearts',
            '5 of Hearts',
            '6 of Hearts',
            '7 of Hearts',
            '8 of Hearts',
            '9 of Hearts',
            '10 of Hearts',
            'Jack of Hearts', 
            'Queen of Hearts',
            'King of Hearts',
            'Ace of Hearts',
            '2 of Diamonds',
            '3 of Diamonds',
            '4 of Diamonds',
            '5 of Diamonds',
            '6 of Diamonds',
            '7 of Diamonds',
            '8 of Diamonds',
            '9 of Diamonds',
            '10 of Diamonds',
            'Jack of Diamonds',
            'Queen of Diamonds',
            'King of Diamonds',
            'Ace of Diamonds',
            '2 of Clubs',
            '3 of Clubs',
            '4 of Clubs',
            '5 of Clubs',
            '6 of Clubs',
            '7 of Clubs',
            '8 of Clubs',
            '9 of Clubs',
            '10 of Clubs',
            'Jack of Clubs',
            'Queen of Clubs',
            'King of Clubs',
            'Ace of Clubs',
            '2 of Spades',
            '3 of Spades',
            '4 of Spades',
            '5 of Spades',
            '6 of Spades',
            '7 of Spades',
            '8 of Spades',
            '9 of Spades',
            '10 of Spades',
            'Jack of Spades',
            'Queen of Spades',
            'King of Spades',
            'Ace of Spades',
            'card_back',
            'card_empty',
        ],
    "Assets/Default Pfp/": [
            "gameoil",
            "teams",
            "no image",
            "Graham",
            "Lukas",
            "Bahn",
            "Jim",
            "Jorge",
            "Kallum",
            "Sachet",
            "Red Chief",
            "John",
            "Greg",
            "Joe",
            "Margaret",
            "Barbara",
            'Agatha',
            'Helena',
            'Christine',
            'Jenny'
        ],
    "Assets/Chips/": [
            '1',
            '2',
            '4',
            '8',
            '16',
            'Big blind',
            'Little blind',
            'Dealer',
            'Poker icon',
        ],
    "Assets/Keys/": [
            'Alt',
            'Down',
            'Enter',
            'F',
            'Space',
            'Up',
            'Tab',
        ],
    "Assets/Misc/": [
            'Poker Assistance',
        ],
    "Assets/": ["QR", "Logo"]
    }

imagePaths = {}

def load():
    for (name, group) in imgGroups.items():
        for item in group:
            ext = ".png"
            splitted = item.split(".")
            if len(splitted) > 1:
                item = splitted[0]
                ext = "." + splitted[1]
                
            imagePaths[item] = os.path.join(name, item + ext)
load()