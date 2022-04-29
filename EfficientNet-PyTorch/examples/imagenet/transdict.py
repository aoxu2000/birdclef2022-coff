import json
# from transdict import get_dict_key


def main():
    with open('names.json', 'r') as f:
        dic = json.load(f)
    _dict = {}
    for i in range(len(dic)):
        spe = get_dict_key(dic, i)
        _dict[i] = spe

    with open('names.json', 'w') as g:
        json.dump(_dict, g)


def get_dict_key(dic, value):
    key = list(dic.keys())[list(dic.values()).index(value)]
    return key

main()