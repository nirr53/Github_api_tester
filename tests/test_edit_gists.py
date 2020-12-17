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
edit_create_set = {'hello_world_python3.txt': {
                        "content": "Run `python hello_world3.py` to print Hello World1"},
                    'hello_world_python4.py': {
                        "content": "print(`hello_world_python4.py`)"},
                    'hello_world_python5.txt': {
                        "content": "Run `python hello_world5.py` to print Hello World2"}}


@pytest.mark.CI
def test_star_gist(gist_desc=helper.wrap_name("star_gist")):
    try:
        res = helper.create_gist(False, gist_desc, basic_create_set)
        helper.star_gist(res['id'])
        helper.verify_gist_starred(res['id'])
    finally:
        helper.delete_gist(res['id'])


def test_star_starred_gist(gist_desc=helper.wrap_name("star_starred_gist")):
    try:
        res = helper.create_gist(False, gist_desc, basic_create_set)
        helper.star_gist(res['id'])
        helper.star_gist(res['id'])
    finally:
        helper.delete_gist(res['id'])


@pytest.mark.CI
def test_unstar_gist(gist_desc=helper.wrap_name("unstar_gist")):
    try:
        res = helper.create_gist(False, gist_desc, basic_create_set)
        helper.star_gist(res['id'])
        helper.unstar_gist(res['id'])
        helper.verify_gist_unstarred(res['id'])
    finally:
        helper.delete_gist(res['id'])


def test_unstar_unstarred_gist(gist_desc=helper.wrap_name("unstar_gist")):
    try:
        res = helper.create_gist(False, gist_desc, basic_create_set)
        helper.star_gist(res['id'])
        helper.unstar_gist(res['id'])
        helper.unstar_gist(res['id'])
    finally:
        helper.delete_gist(res['id'])

def test_star_and_unstar_multiple_times(gist_desc=helper.wrap_name("star_and_unstar_multiple_times")):
    try:
        res = helper.create_gist(False, gist_desc, basic_create_set)
        for idx in range(3):
            helper.star_gist(res['id'])
            helper.unstar_gist(res['id'])
        helper.verify_gist_unstarred(res['id'])
    finally:
        helper.delete_gist(res['id'])


res_type_names1 = ["",
                   "fdfds",
                   "   ",
                   "1234"]
@pytest.mark.parametrize("invalid_gist_id", res_type_names1)
def test_star_unstar_invalid_gist(invalid_gist_id, exp_code=404):
    try:
        gist_desc = helper.wrap_name("star_invalid_gist")
        res = helper.create_gist(False, gist_desc, basic_create_set)
        helper.star_gist(invalid_gist_id, exp_code)
        helper.unstar_gist(invalid_gist_id, exp_code)
    finally:
        helper.delete_gist(res['id'])


@pytest.mark.CI
def test_edit_gist():
    try:
        ini_desc, ed_desc = helper.wrap_name("edit_gist_initial_desc1"), helper.wrap_name("edit_gist_edited_desc")
        res = helper.create_gist(False, ini_desc, basic_create_set)
        res = helper.edit_gist(res['id'], ed_desc, edit_create_set)
        assert ed_desc in res['description']
        d4 = dict(basic_create_set)
        d4.update(edit_create_set)
        for key in d4:
            assert key in res['files']
            assert d4[key]['content'] in res['files'][key]['content']
    finally:
        helper.delete_gist(res['id'])


@pytest.mark.CI
def test_get_previous_gist_revision():
    try:
        ini_desc, ed_desc = helper.wrap_name("get_prev_rev_ini_desc"), helper.wrap_name("get_prev_rev_edit_desc")
        res = helper.create_gist(False, ini_desc, basic_create_set)
        edit_res = helper.edit_gist(res['id'], ed_desc, edit_create_set)
        prev_revision = helper.get_previous_revision(res['id'], edit_res['history'][1]['version'])
        assert edit_res['history'][1]['version'] in prev_revision['history'][0]['version']
        for key in basic_create_set:
            assert key in prev_revision['files']
        for key in edit_create_set:
            assert key not in prev_revision['files']
    finally:
        helper.delete_gist(res['id'])


res_type_names2 = [(""     , 404, 404),
                   ("!$%^&", 422, 404),
                   ("     ", 422, 404),
                   ("12345", 422, 422)]
@pytest.mark.parametrize("invalid_data, exp_code1, exp_code2", res_type_names2)
def test_get_invalid_previous_gist_revision(invalid_data, exp_code1, exp_code2):
    try:
        ini_desc, ed_desc = helper.wrap_name("get_inv_prev_rev_ini_desc"), helper.wrap_name("get_inv_prev_rev_edit_desc")
        res = helper.create_gist(False, ini_desc, basic_create_set)
        edit_res = helper.edit_gist(res['id'], ed_desc, edit_create_set)
        helper.get_previous_revision(res['id'], invalid_data, exp_code1)
        helper.get_previous_revision(invalid_data, edit_res['history'][1]['version'], exp_code2)
    finally:
        helper.delete_gist(res['id'])
