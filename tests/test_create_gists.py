import pytest

from Github_utilities import Github_Utilities
from Github_base_utilities import Pprint

# Pre-tests actions
helper = Github_Utilities()
pprint = Pprint()


basic_create_set = {'hello_world_python1.txt': {
                        "content": "Run `python hello_world1.py` to print Hello World1"},
                    'hello_world_python2.txt': {
                        "content": "Run `python hello_world2.py` to print Hello World2"}}


res_type_names1 = [(True, "Public gist"),
                   (False, "Private gist")]
@pytest.mark.parametrize("is_public, gist_desc", res_type_names1)
def test_create_gist_public_tests(is_public, gist_desc):
    try:
        gist_desc = helper.wrap_name(gist_desc)
        res = helper.create_gist(is_public, gist_desc, basic_create_set)
        assert res['public'] == is_public
        assert gist_desc in res['description']
    finally:
        helper.delete_gist(res['id'])

res_type_names2 = ["",
                   "S_chars1 !@#$%^&*()",
                   "S_chars2 _+';:<>/'`",
                   "S_chars3 []{}|~±§",
                   "1234567890",
                   "           ",
                   "Very-long-gist-name1,Very-long-gist-name1,Very-long-gist-name1,Very-long-gist-name1,"
                   "Very-long-gist-name1,Very-long-gist-name1,Very-long-gist-name1,Very-long-gist-name1,"]
@pytest.mark.parametrize("gist_desc", res_type_names2)
def test_create_gist_description_tests(gist_desc):
    try:
        gist_desc = helper.wrap_name(gist_desc)
        res = helper.create_gist(True, gist_desc, basic_create_set)
    finally:
        helper.delete_gist(res['id'])


def test_create_gist_check_res_headers(gist_desc="check_res_headers"):
    try:
        gist_desc = helper.wrap_name(gist_desc)
        res = helper.create_gist(True, gist_desc, basic_create_set)
        fields = ['comments', 'comments_url', 'created_at', 'description' , 'user',
                  'files'   , 'forks'       , 'forks_url' , 'git_pull_url', 'git_push_url',
                  'history' , 'html_url'    , 'id'        , 'node_id'     , 'owner',
                  'public'  , 'truncated'   , 'updated_at', 'url']
        for field in fields:
            assert field in res
    finally:
        helper.delete_gist(res['id'])


def test_create_gist_multiple_times(gist_desc="create_gist_multiple_times"):
    for idx in range(3):
        gist_desc = helper.wrap_name(gist_desc)
        try:
            res = helper.create_gist(True, gist_desc, basic_create_set)
        finally:
            helper.delete_gist(res['id'])


res_type_names3 = ["",
                   "fdfds",
                   "   ",
                   "1234"]
@pytest.mark.parametrize("invalid_gist_id", res_type_names3)
def test_delete_gist_failures(invalid_gist_id, gist_desc="delete_gist_failures"):
    try:
        gist_desc = helper.wrap_name(gist_desc)
        res = helper.create_gist(True, gist_desc, basic_create_set)
        helper.delete_gist(invalid_gist_id, 404)
    finally:
        helper.delete_gist(res['id'])


def test_delete_deleted_gist(gist_desc="delete_deleted_gist"):
    res = helper.create_gist(True, gist_desc, basic_create_set)
    helper.delete_gist(res['id'])
    helper.delete_gist(res['id'], 404)






