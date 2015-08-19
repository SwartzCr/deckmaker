import sys
import subprocess
import os
import json


def parse(text):
    text_list = text.splitlines()
    deck_name = text_list[0]
    card_list = []
    for line in text_list[1:]:
        sb = False
        if line.startswith("SB:"):
            line = line.strip("SB:")
            sb = True
        num, name = line.split(" ", 1)
        card_list.append((num, name, sb))
    return (deck_name, card_list)


def main(text):
    deck_name, card_list = parse(text)
    cwd = os.getcwd()
    nwd = cwd+"/"+deck_name
    os.makedirs(nwd)
    with open('vintage-setbycard.json') as f:
        set_db = json.load(f)
    for card in card_list:
        num, name, sb = card
        card_set = set_db[name]
        image_path = "".join([cwd,"/",card_set,"/",name,".jpg"])
        res = subprocess.check_output(["identify", "-format", "%[fx:w]x%[fx:h]", image_path])
        res = res.rstrip("\n")
        resx, resy = str(res).split("x")
        up = str(int(resy)/11)
        side = str(int(resx)/10)
        text_size = str(int(resx)/24)
        for i in range(int(num)):
            if sb == False:
                call_list = ["convert", image_path, "-pointsize", text_size, "-fill", "white", "-gravity", "South", "-draw", "text 0,"+up+" '%s %s/%s'" %(deck_name,i+1, num ), "-bordercolor", "Black", "-border", "%sx%s" %(side, side), nwd+"/"+name+str(i)+".jpg"]
            if sb == True:
                call_list = ["convert", image_path, "-pointsize", text_size, "-fill", "white", "-gravity", "South", "-draw", "text 0,"+up+" '%s %s/%s - SB'" %(deck_name, i+1, num), "-bordercolor", "Black", "-border", "%sx%s" %(side, side),  nwd+"/sb"+name+str(i)+".jpg"]
            subprocess.call(call_list)


if __name__ == '__main__':
    main(sys.stdin.read())
