# -*- coding: utf-8 -*-
import json
import re
import itertools
from pathlib import Path

from services.crawl_public_apis_data import fetchreadme



footer = """<br>

## License
[MIT](LICENSE) (c) 2022 public-apis
"""


def removefooter(text):
    return text.replace(footer,'')

def extract_data_from_category_item(row):
    api, description, auth, https, cors = [
        x.strip() for x in row.split('|')[1:-1]]
    api_regex_matches = re.match(r'\[(.*)\]\((.*)\)', api)
    name, url = api_regex_matches.group(1), api_regex_matches.group(2)
    return {
        'name': name,
        'url': url,
        'description': description,
        'auth': auth,
        'https': https,
        'cors': cors
    }

def get_items_from_rows(category, rows):
    return map(
        lambda row: extract_data_from_category_item(row) | {'category': category},
        clean_category_block_content(rows).split('\n')
    )


def clean_category_block_content(x):
    return x.replace(
        "API | Description | Auth | HTTPS | CORS |\n", ''
    ).replace(
        "|---|---|---|---|---|\n", ''
    ).replace("**[⬆ Back to Index](#index)**", '').strip()

def extract_rows_from_category_block(category, rows):
    return get_items_from_rows(category, rows)

def parsereadmetext(text):
    text = removefooter(text)
    categories_blocks_iter = re.finditer(
    r'###\s+(.*?)\n(.*?)(?=\n###|$)', text, re.DOTALL)

    parsed_data = [
        extract_rows_from_category_block(match.group(1), match.group(2))
        for match in categories_blocks_iter
    ]
    parsed_data_flat = list( itertools.chain.from_iterable( [x for x in parsed_data] ) )
    return parsed_data_flat

def main():
    data_dir = Path(__file__).parent.parent.joinpath('data')
    output_file_path = data_dir.joinpath('apis.json')

    text = fetchreadme()
    
    data = parsereadmetext(text)

    with open(output_file_path,'w') as file:
        json.dump(data,file,indent=4)

if __name__ == '__main__':
    main()

