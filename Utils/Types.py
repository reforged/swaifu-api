import flask
import typing

dict_ss = dict[str, str]
dict_ss_imb = dict[str, typing.Union[str, dict_ss]]
dict_ssl_imb = dict[str, typing.Union[str, list[str]]]
new_que = dict[str, typing.Union[str, list[dict_ss]]]

union_s_n = typing.Union[str, None]
union_dss_n = typing.Union[dict_ss, str]

func_resp = typing.Union[dict_ss_imb, flask.Response]
