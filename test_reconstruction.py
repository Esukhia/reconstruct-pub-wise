from pathlib import Path
import pytest

from reconstruct_pub_wise import *

def get_collated_text_parts():
    collated_text = Path('./tests/data/collated_text/D007.txt').read_text(encoding='utf-8')
    text_parts = split_text(collated_text)
    return text_parts

def test_derge_dip():
    parma  = "སྡེ་དགེ"
    expected_text = Path(f'./tests/data/{parma}/D007.txt').read_text(encoding='utf-8')
    text_parts = get_collated_text_parts()
    diplomatic_text = get_diplomatic_text(parma, text_parts)
    assert diplomatic_text == expected_text


def test_narthang_dip():
    parma  = "སྣར་ཐང"
    expected_text = Path(f'./tests/data/{parma}/D007.txt').read_text(encoding='utf-8')
    text_parts = get_collated_text_parts()
    diplomatic_text = get_diplomatic_text(parma, text_parts)
    assert diplomatic_text == expected_text


def test_peking_dip():
    parma  = "པེ་ཅིན"
    expected_text = Path(f'./tests/data/{parma}/D007.txt').read_text(encoding='utf-8')
    text_parts = get_collated_text_parts()
    diplomatic_text = get_diplomatic_text(parma, text_parts)
    assert diplomatic_text == expected_text

def test_chone_dip():
    parma  = "ཅོ་ནེ"
    expected_text = Path(f'./tests/data/{parma}/D007.txt').read_text(encoding='utf-8')
    text_parts = get_collated_text_parts()
    diplomatic_text = get_diplomatic_text(parma, text_parts)
    assert diplomatic_text == expected_text


if __name__ == "__main__":
    test_narthang_dip()