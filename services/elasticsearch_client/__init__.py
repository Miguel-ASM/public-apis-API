import os
import json
from pathlib import Path

from .elasticsearch_client import Elastic

mappings_file_path = Path(__file__).parent.joinpath('mappings.json')

ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
ELASTICSEARCH_INDEX = 'apis'

with open(mappings_file_path) as f:
  mappings = json.load(f)

elastic = Elastic(
  hosts=[ELASTICSEARCH_URL],
  mappings=mappings,
  index=ELASTICSEARCH_INDEX
)