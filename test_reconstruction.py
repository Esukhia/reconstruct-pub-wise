from pathlib import Path
import pytest
from reconstruct_pub_wise import *

def get_paths():
    opf_path = Path(f"./tests/data/opf/PB7EAF27B/PB7EAF27B.opf")
    base_path = Path(f"{opf_path}/base/00001.txt")
    layers = list(Path(f"{opf_path}/layers").iterdir())
    for layer in layers:
        durchen_path = Path(f"{layer}/Durchen.yml")
    return durchen_path, base_path

def test_derge_dip():
    parma  = "derge"
    durchen_path, base_path = get_paths()
    durchen_layer = load_yaml(durchen_path)
    base_text = base_path.read_text(encoding='utf-8')
    diplomatic_durchen = get_diplomatic_durchen(durchen_layer, parma)
    diplomatic_text = get_diplomatic_text(base_text, diplomatic_durchen, load_yaml(durchen_path))
    expected_text = Path(f'./tests/data/{parma_dic[parma]}/D007.txt').read_text(encoding='utf-8')
    assert diplomatic_text == expected_text



def test_peking_dip():
    parma  = "peking"
    durchen_path, base_path = get_paths()
    durchen_layer = load_yaml(durchen_path)
    base_text = base_path.read_text(encoding='utf-8')
    diplomatic_durchen = get_diplomatic_durchen(durchen_layer, parma)
    diplomatic_text = get_diplomatic_text(base_text, diplomatic_durchen, load_yaml(durchen_path))
    expected_text = Path(f'./tests/data/{parma_dic[parma]}/D007.txt').read_text(encoding='utf-8')
    assert diplomatic_text == expected_text



def test_narthang_dip():
    parma  = "narthang"
    durchen_path, base_path = get_paths()
    durchen_layer = load_yaml(durchen_path)
    base_text = base_path.read_text(encoding='utf-8')
    diplomatic_durchen = get_diplomatic_durchen(durchen_layer, parma)
    diplomatic_text = get_diplomatic_text(base_text, diplomatic_durchen, load_yaml(durchen_path))
    expected_text = Path(f'./tests/data/{parma_dic[parma]}/D007.txt').read_text(encoding='utf-8')
    assert diplomatic_text == expected_text

def test_chone_dip():
    parma  = "chone"
    durchen_path, base_path = get_paths()
    durchen_layer = load_yaml(durchen_path)
    base_text = base_path.read_text(encoding='utf-8')
    diplomatic_durchen = get_diplomatic_durchen(durchen_layer, parma)
    diplomatic_text = get_diplomatic_text(base_text, diplomatic_durchen, load_yaml(durchen_path))
    expected_text = Path(f'./tests/data/{parma_dic[parma]}/D007.txt').read_text(encoding='utf-8')
    assert diplomatic_text == expected_text


