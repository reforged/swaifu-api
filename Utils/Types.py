from typing import *

sql_query_json_format = dict[str, Union[list[list[str]], dict[str, list[Union[str, list[str]]]]]]
sql_execute_json_format = dict[str, str | list[list[str]]]
