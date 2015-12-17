import subprocess

def load_dirs():
    with open("dirs.txt", 'r') as f:
        out = f.read()
    return out.splitlines()

def main(dir_path):
    dic = {}
    dirs = load_dirs()
    dirs = [dir_.strip("/") for dir_ in dirs]
    for dir_ in dirs:
        cards = subprocess.check_output(['ls', dir_path+"/"+dir_]).splitlines()
        for card in cards:
            card_name = card.split(".")[0]
            if card_name not in dic.keys():
                dic[card_name] = dir_
    return dic

