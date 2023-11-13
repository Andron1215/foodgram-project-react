from enum import Enum


class Pagination(Enum):
    page_size = 6


class RecipesModels(Enum):
    max_len_tag_name = 200
    max_len_unit_name = 200
    max_len_ingredient_name = 200
    max_len_recipe_name = 200
    max_cooking_time = 1440
    min_pos_int = 1


class UsersModels(Enum):
    max_len_user_first_name = 150
    max_len_user_last_name = 150
