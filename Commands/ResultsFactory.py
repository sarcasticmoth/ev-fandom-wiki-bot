import json
from typing import List
import logging

from Commands.Entities.Category import CategoryRoot, CategoryQuery, CategoryMember

logging.getLogger('mainLogger')


class ResultsFactory:

    @staticmethod
    def process_category_list(text):
        decoded_list = json.loads(text)

        cat_members = []

        for row in decoded_list['query']['categorymembers']:
            cat_members.append(CategoryMember(row['pageid'], row['ns'], row['title']))

        cat_root = CategoryRoot(decoded_list['batchcomplete'], CategoryQuery(cat_members))
        return type(cat_root)

    # @staticmethod
    # def replace_space(x):
    #     if ' ' in x:

