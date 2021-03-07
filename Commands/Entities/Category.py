from typing import List


class CategoryMember:
    page_id: int
    ns: int
    title: str


class CategoryQuery:
    category_members: List[CategoryMember]


class CategoryRoot:
    batch_complete: str
    category_query: CategoryQuery

