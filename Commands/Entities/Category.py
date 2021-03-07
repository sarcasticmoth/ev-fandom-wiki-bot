from typing import List
from dataclasses import dataclass


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
