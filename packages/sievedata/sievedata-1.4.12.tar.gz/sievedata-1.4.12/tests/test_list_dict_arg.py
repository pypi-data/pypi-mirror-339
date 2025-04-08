import sieve
from typing import Dict, List

from sieve.server.grpc.serializer import input_to_type


def test_dict_input_type():
    a = {'a': 'b'}
    try:
        input_to_type(a, Dict)
    except:
        assert False, "Failed to convert dict to Dict"

    try:
        input_to_type(a, dict)
    except:
        assert False, "Failed to convert dict to dict"

    try:
        input_to_type(a, sieve.File)
    except Exception as e:
        assert str(e) == "Invalid input type: Please provide either _fileurl, or path or url"


def test_list_input_type():
    a = ['a', 'b']
    try:
        input_to_type(a, List)
    except:
        assert False, "Failed to convert list to List"

    try:
        input_to_type(a, list)
    except:
        assert False, "Failed to convert list to list"



