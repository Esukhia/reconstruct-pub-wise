import re
from antx import transfer
from pathlib import Path
import urllib.request as r
from bs4 import BeautifulSoup as bs
import json
from urllib.request import urlopen
from openpecha.core.pecha import OpenPechaFS
from openpecha.utils import load_yaml

url = "https://raw.githubusercontent.com/OpenPecha-dev/editable-text/main/t_text_list.json"
response = urlopen(url)
t_text_list_dictionary = json.loads(response.read())


parma_dic = {
    'derge': 'སྡེ་དགེ',
    'narthang': 'སྣར་ཐང',
    'peking': 'པེ་ཅིན',
    'chone': 'ཅོ་ནེ'
}


def get_next_start(num, anns):
    if num == len(anns):
        next_start = None
    else:
        for ann_num,(_, ann_info) in enumerate(anns.items(), 1):
            if ann_num == num+1:
                next_start = ann_info['span']['start']
    return next_start



def get_diplomatic_text(base_text, new_durchen, old_durchen):
    anns = new_durchen['annotations']
    new_base_text = ""
    for ann_num,(ann_id, ann_info) in enumerate(anns.items(), 1):
        default_pub = ann_info['default']
        if default_pub != old_durchen['annotations'][ann_id]['default']:
            start = ann_info["span"]['start']
            end = old_durchen['annotations'][ann_id]['span']['end']
            note = ann_info['options'][default_pub]['note']
            next_start = get_next_start(ann_num, old_durchen['annotations'])
            if ann_num == 1:
                new_base_text += base_text[0:start] + note + base_text[end:next_start]
            elif ann_num == len(anns):
                new_base_text += note + base_text[end:]
            else:
                new_base_text += note + base_text[end:next_start]
        else:
            start = ann_info["span"]['start']
            end = ann_info["span"]['end']
            note = ann_info['options'][default_pub]['note']
            next_start = get_next_start(ann_num, old_durchen['annotations'])
            if ann_num == 1:
                new_base_text += base_text[0:start] + note + base_text[end:next_start]
            elif ann_num == len(anns):
                new_base_text += note + base_text[end:]
            else:
                new_base_text += note + base_text[end:next_start]                
    return new_base_text


def update_durchen_offset(offset, anns, _id):
    start_ann = int(anns[_id]['span']['start'])
    for ann_id, ann_info in anns.items():
        start = int(ann_info['span']['start'])
        end = int(ann_info['span']['end'])
        if start_ann <= start:
            if _id == ann_id:
                ann_info['span']['end'] = int(end + offset)
            else:
                ann_info['span']['start'] = int(start + offset)
                ann_info['span']['end'] = int(end + offset)
    return anns


def check_offset(ann_info, param):
    default_pub = ann_info['default']
    default_word = ann_info['options'][default_pub]['note']
    modern_word = ann_info['options'][param]['note']
    offset = int(len(modern_word)- len(default_word))
    return offset


def get_diplomatic_durchen(durchen, parma):
    anns = durchen['annotations']
    for ann_id, ann_info in anns.items():
        if parma == ann_info['default']:
            continue
        else:
            offset = check_offset(ann_info, parma)
            ann_info['default'] = parma
            if offset != 0:
                anns = update_durchen_offset(offset, anns, ann_id) 
    
    durchen['annotations'].update(anns)
    return durchen
    

def get_text_title(opf_path):
    meta_yml = load_yaml(Path(f"{opf_path}/meta.yml"))
    text_id = meta_yml['source_metadata']['text_id']
    title = t_text_list_dictionary[text_id]['title']
    return title


def get_desired_text_format(diplomatic_text):
    page_number_removed_text = re.sub(r"([0-9]+-[0-9]+)", " ", diplomatic_text)
    desired_text = re.sub(r"\n", " ", page_number_removed_text)
    return desired_text


def get_base_names(opf_path):
    base_names = []
    for base_path in list((opf_path / "base").iterdir()):
        base_names.append(base_path.stem)
    return base_names


def reconstruct_pub_wise(opf_path):
    base_text = Path(f"{opf_path}/base/00001.txt").read_text(encoding='utf-8')
    layers = list(Path(f"{opf_path}/layers").iterdir())
    for layer in layers:
        durchen_path = Path(f"{layer}/Durchen.yml")
        durchen_layer = load_yaml(durchen_path)
        parmas = ['narthang','derge', 'peking', 'chone']
        for parma in parmas:
            diplomatic_durchen = get_diplomatic_durchen(durchen_layer, parma)
            diplomatic_text = get_diplomatic_text(base_text, diplomatic_durchen, load_yaml(durchen_path))
            desired_diplomatic_text = get_desired_text_format(diplomatic_text)
            title = get_text_title(opf_path)
            Path(f'./data/{parma_dic[parma]}/{title}.txt').write_text(desired_diplomatic_text, encoding='utf-8')
    

if __name__ == "__main__":
    pecha_id = 'PB7EAF27B'
    opf_path = Path(f"./data/opf/{pecha_id}/{pecha_id}.opf")
    reconstruct_pub_wise(opf_path)