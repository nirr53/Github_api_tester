import pytest

from Github_utilities import Github_Utilities
from test_create_gists import basic_create_set
from Github_base_utilities import ConfigFile, Pprint


# Pre-tests actions
helper = Github_Utilities()
config = ConfigFile()
pprint = Pprint()
config.set_config_file("github.properties")
GIT_USERNAME = config.get_as_string('REST', 'git_username')


@pytest.mark.CI
def test_get_gists_for_username():
    try:
        gist_desc = helper.wrap_name("test_get_gist_for user")
        res = helper.create_gist(True, gist_desc, basic_create_set)
        gists_list = helper.get_gists_for_user(GIT_USERNAME)
        for gist in gists_list:
            if res['id'] in gist['id']:
                break
        else:
            assert False, "gist {} was not detected !".format(res['id'])
    finally:
        helper.delete_gist(res['id'])


res_type_names1 = ["",
                   "   ",
                   "!@#$'",
                   "';%",
                   "...",
                   GIT_USERNAME + "234"]
@pytest.mark.parametrize("invalid_gist_id", res_type_names1)
def test_get_gists_for_invalid_syntax_username(invalid_gist_id):
    try:
        gist_desc = helper.wrap_name("test_get_gist_for invalid_syntax_git_user")
        res = helper.create_gist(True, gist_desc, basic_create_set)
        helper.get_gists_for_user(invalid_gist_id, 404)
    finally:
        helper.delete_gist(res['id'])


def test_get_all_gists():
    helper.get_all_gists()


res_type_names2 = [(True,  helper.wrap_name("public_gist_test")),
                   (False, helper.wrap_name("private_gist_test"))]
@pytest.mark.parametrize("is_public, gist_desc", res_type_names2)
@pytest.mark.CI
def test_get_public_gists(is_public, gist_desc):
    try:
        res = helper.create_gist(is_public, gist_desc, basic_create_set)
        public_gists_list = helper.get_public_gists()
        for gist in public_gists_list:
            if res['id'] in gist['id']:
                if is_public:
                    break
                else:
                    assert False, "gist {} was detected as public gist!".format(res['id'])
            else:
                pass
        else:
            if is_public:
                assert False, "gist {} was not detected on public gists!".format(gist_desc)
    finally:
        helper.delete_gist(res['id'])


@pytest.mark.CI
def test_get_gist_commits():
    try:
        gist_desc = helper.wrap_name("test_get_gist_commits")
        res = helper.create_gist(True, gist_desc, basic_create_set)
        public_gists_list = helper.get_gist_commits(res['id'])
        assert res['history'][0] == public_gists_list[0]
    finally:
        helper.delete_gist(res['id'])



def test_get_multiple_gist_commits():
    try:
        gist_desc = helper.wrap_name("test_get_gist_commits")
        res = helper.create_gist(True, gist_desc, basic_create_set)
        for desc in ["desc1", "desc2", "desc3"]:
            ed_res = helper.edit_gist(res['id'], desc, basic_create_set)
        gist_commits_list = helper.get_gist_commits(res['id'])
        idx = 0
        for gist_commit in gist_commits_list:
            assert ed_res['history'][idx] == gist_commit
            idx += 1
    finally:
        helper.delete_gist(res['id'])
