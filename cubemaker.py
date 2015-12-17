import sys
import subprocess
import os
import json
import db_gen

CARD_DIR = "CCGHQ MTG Pics/Fulls/Base and Expansion Sets"
# this code takes the deck file and generates a list of 3 item tuples
# each with a num, name, and sb attribute used to generate the images
def parse(text):
    text_list = text.splitlines()
    deck_name = text_list[0]
    card_list = []
    for line in text_list[1:]:
        sb = False
        if line.startswith("SB:"):
            line = line.strip("SB:")
            sb = True
        card_list.append(line)
    return (deck_name, card_list)


def main(text):
    deck_name, card_list = parse(text)
    cwd = os.getcwd()
    nwd = cwd+"/"+deck_name
    # make a directory for the deck with the deck name
    # i.e. the first line of the deck file
    os.makedirs(nwd)
    # use the vintage-setbycard.json to find which set each card is in
    # then get the image file from that folder and do magic to it
    #with open('vintage-setbycard.json') as f:
    #    set_db = json.load(f)
    set_db = db_gen.main("/home/swartzcr/Documents/coding/deckmaker/CCGHQ MTG Pics/Fulls/Base and Expansion Sets")
    for card in card_list:
        name= card
        card_set = set_db[name]
        image_path = "".join([cwd,"/",CARD_DIR,"/",card_set,"/",name,".full.jpg"])
        # get the size of the existant card image
        res = subprocess.check_output(["identify", "-format", "%[fx:w]x%[fx:h]", image_path])
        res = res.rstrip("\n")
        resx, resy = str(res).split("x")
        # Figure out how much padding it will need to be printed correctly
        up = str(int(resy)/11)
        side = str(int(resx)/10)
        text_size = str(int(resx)/24)
        # For each iteration of card generate an image with proper padding
        # as well as deck name and 1/# text
        call_list = ["convert", image_path, "-pointsize", text_size, "-fill", "white", "-gravity", "South", "-draw", "text 0,"+up+" '%s' " %(deck_name), "-bordercolor", "Black", "-border", "%sx%s" %(side, side), nwd+"/"+name+".jpg"]
        subprocess.call(call_list)


if __name__ == '__main__':
    main(sys.stdin.read())
