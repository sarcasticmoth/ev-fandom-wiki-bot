from dataclasses import dataclass
from typing import List
import json
from json import JSONEncoder
from collections import namedtuple


@dataclass
class CategoryMember:
    page_id: int
    ns: int
    title: str


@dataclass
class CategoryQuery:
    category_members: List[CategoryMember]


@dataclass
class CategoryRoot:
    batch_complete: str
    category_query: CategoryQuery

