from parse import TitleParser

tests = [
    "Uziyamnika",
    "Kukaikila feat Dragon sounds",
    "Tigwilane Manja Ft Lulu X Lucius Band X Skeffa Chimoto",
    "The Sound ft featuring Uhuru & DJ Bucks",
    "Ndi Ambuye (Ulendo) ft. Applevickie",
    "Golide feat. Sir Patricks [Prod. Tricky Beatz & Stich Fray]"
]

for title in tests:
    parser = TitleParser(title)
    print(parser.getParts())
    print(parser.getFeaturedArtists())
    print(parser.getProducers())
    print("------------------------\n")