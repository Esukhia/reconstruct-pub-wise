import re
from pathlib import Path


def get_pub_wise_note(note):
    note = re.sub('\(\d+\)', '', note)
    pub_mapping = {
        '«པེ་»': 'peking',
        '«སྣར་»': 'narthang',
        '«སྡེ་»': 'derge',
        '«ཅོ་»': 'chone'
    }
    reformat_notes = {
        'peking': '',
        'narthang': '',
        'derge': '',
        'chone': ''
    }
    note_parts = re.split('(«.+?»)', note)
    pubs = note_parts[1::2]
    notes = note_parts[2::2]
    for walker, (pub, note_part) in enumerate(zip(pubs, notes)):
        if note_part:
            reformat_notes[pub_mapping[pub]] = note_part.replace('>', '')
        else:
            if notes[walker+1]:
                reformat_notes[pub_mapping[pub]] = notes[walker+1].replace('>', '')
            else:
                reformat_notes[pub_mapping[pub]] = notes[walker+2].replace('>', '')
    return reformat_notes

def split_text(content):
    text_parts = {
        'text_chunks': None,
        'notes': None
    }
    chunks = re.split(r"(\(\d+\) <.+?>)", content)
    text_chunks = []
    notes = []
    for chunk in chunks:
        if chunk and re.search(r"\(\d+\) <.+?>", chunk):
            notes.append(chunk)
        else:
            text_chunks.append(chunk)
    text_parts['text_chunks'] = text_chunks
    text_parts['notes'] = notes
    return text_parts

def get_last_syl(text):
    chunks = re.split('(་|།།|།)',text)
    reformated_chunks = []
    cur_chunk = ""
    for chunk in chunks:
        if chunk and not is_punct(chunk):
            cur_chunk += chunk
        elif is_punct(chunk) and chunk != "།།":
            cur_chunk += chunk
            reformated_chunks.append(cur_chunk)
            cur_chunk = ""
        elif chunk == "།།":
            reformated_chunks.append(cur_chunk)
            reformated_chunks.append(chunk)
            cur_chunk = ''
    if cur_chunk:
        reformated_chunks.append(cur_chunk)
    last_syl = reformated_chunks[-1]
    return last_syl

def get_old_note(chunk):
    if re.search(':(.|\n)+$', chunk):
        old_note = re.search(':(.|\n)+$', chunk)[0]
        return old_note
    else:
        old_note = get_last_syl(chunk)
    old_note = re.sub('\[.+\]', "", old_note)
    return old_note

def is_punct(string):
    # put in common
    if '༄' in string or '༅' in string or '༆' in string or '༇' in string or '༈' in string or \
        '།' in string or '༎' in string or '༏' in string or '༐' in string or '༑' in string or \
        '༔' in string or '_' in string or '་' == string:
        return True
    else:
        return False

def get_new_note(note, next_chunk):
    new_note = note
    first_char = next_chunk[0]
    if not is_punct(first_char):
        new_note = re.sub('།', '་', new_note)
        new_note = re.sub('་་', '་', new_note)
    elif is_punct(first_char):
        new_note = re.sub('།', '', new_note)
    return new_note

def get_diplomatic_text(parma, text_parts):
    diplomatic_text = ''
    text_chunks = text_parts['text_chunks']
    notes = text_parts['notes']
    for chunk_walker, (text_chunk, note) in enumerate(zip(text_chunks, notes)):
        try:
            next_text_chunk = text_chunks[chunk_walker+1]
        except:
            next_text_chunk = ''
        all_pub_note = get_pub_wise_note(note)
        cur_parma_note = all_pub_note[parma]
        new_chunk = ""
        old_note = get_old_note(text_chunk)
        if cur_parma_note:
            if "-" in cur_parma_note:
                new_chunk = re.sub(old_note+"$", '', text_chunk)
            elif "+" in cur_parma_note:
                new_note = get_new_note(cur_parma_note[1:], next_text_chunk)
                new_chunk = text_chunk + new_note
            else:
                new_note = get_new_note(cur_parma_note, next_text_chunk)
                new_chunk = re.sub(old_note+"$", new_note, text_chunk)
        else:
            new_chunk = re.sub(':', '', text_chunk)
        diplomatic_text += new_chunk
    if len(text_chunks) > len(notes):
        diplomatic_text += text_chunks[-1]
    return diplomatic_text



def reconstruct_pub_wise(text_id):
    base_path = Path('./tests/data/')
    # base_path = Path('./data/tengyur/')
    collated_text = (base_path / 'collated_text' / f'{text_id}.txt').read_text(encoding='utf-8')
    text_parts = split_text(collated_text)
    parmas = ['derge', 'narthang', 'peking', 'chone']
    for parma in parmas:
        diplomatic_text = get_diplomatic_text(parma, text_parts)
        (base_path / parma / f'{text_id}.txt').write_text(diplomatic_text, encoding='utf-8')
    

if __name__ == "__main__":
    text_id = 'D007'
    reconstruct_pub_wise(text_id)