import flask
import typing

dict_ss = dict[str, str]
dict_ss_imb = dict[str, typing.Union[str, dict_ss]]
dict_ssl_imb = dict[str, typing.Union[str, list[str]]]
new_que = dict[str, typing.Union[str, list[dict_ss]]]

ty_que = list[dict[str, typing.Union[str, list[dict[str, str]]]]]

union_s_n = typing.Union[str, None]
union_dss_n = typing.Union[dict_ss, str]
union_sl_n = typing.Union[None, list[dict_ss]]

func_resp = typing.Union[dict_ss_imb, flask.Response]
