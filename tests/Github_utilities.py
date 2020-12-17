import requests
import json
import time
import random
from Github_base_utilities import ConfigFile
from Github_base_utilities import Pprint


config = ConfigFile()
config.set_config_file("github.properties")
GIT_URL = config.get_as_string('REST', 'git_url')
GIT_USERNAME = config.get_as_string('REST', 'git_username')
GIT_TOKEN = config.get_as_string('REST', 'git_token')


class Github_Utilities:

    def __init__(self):
        self.pprint = Pprint()

    def wrap_name(self, name=""):
        current_milli_time = lambda: int(round(time.time() * 1000))
        return name + "_" + time.strftime("%Y%m%d-%H%M%S") + "_" + str(current_milli_time()) + str(random.randint(0, 1000))

    def get_all_gists(self):
        response = requests.get('{}/gists'.format(GIT_URL), auth=(GIT_USERNAME, GIT_TOKEN))
        assert response.status_code == 200, "returned status-code is {} !".format(response.status_code)
        body = json.loads(response._content.decode('utf-8'))
        return body

    def get_public_gists(self):
        response = requests.get('{}/gists/public'.format(GIT_URL), auth=(GIT_USERNAME, GIT_TOKEN))
        assert response.status_code == 200, "returned status-code is {} !".format(response.status_code)
        body = json.loads(response._content.decode('utf-8'))
        return body

    def get_starred_gists(self):
        response = requests.get('{}/gists/starred'.format(GIT_URL), auth=(GIT_USERNAME, GIT_TOKEN))
        assert response.status_code == 200, "returned status-code is {} !".format(response.status_code)
        body = json.loads(response._content.decode('utf-8'))
        return body

    def get_gists_for_user(self, username, exp_code=200):
        response = requests.get('{}/users/{}/gists'.format(GIT_URL, username), auth=(GIT_USERNAME, GIT_TOKEN))
        assert response.status_code == exp_code, "returned status-code is {} !".format(response.status_code)
        if exp_code == 200:
            body = json.loads(response._content.decode('utf-8'))
            return body

    def get_gist_commits(self, gist_id, exp_code=200):
        response = requests.get('{}/gists/{}/commits'.format(GIT_URL, gist_id), auth=(GIT_USERNAME, GIT_TOKEN))
        assert response.status_code == exp_code, "returned status-code is {} !".format(response.status_code)
        if exp_code == 200:
            body = json.loads(response._content.decode('utf-8'))
            return body

    def create_gist(self, is_public=True, description="", json_files={}):
        gist_data2 = {
            "description": description,
            "public": is_public,
            "files": json_files
        }
        response = requests.post('{}/gists'.format(GIT_URL),
                                 data=json.dumps(gist_data2),
                                 auth=(GIT_USERNAME, GIT_TOKEN),
                                 headers={"accept": "application/vnd.github.v3+json"})
        assert response.status_code == 201
        body = json.loads(response._content.decode('utf-8'))
        return body

    def delete_gist(self, gist_id, exp_status_code=204):
        response = requests.delete('{}/gists/{}'.format(GIT_URL, gist_id),
                                   headers={"accept": "application/vnd.github.v3+json"},
                                   auth=(GIT_USERNAME, GIT_TOKEN))
        assert response.status_code == exp_status_code

    def star_gist(self, gist_id, exp_status_code=204):
        response = requests.put('{}/gists/{}/star'.format(GIT_URL, gist_id), headers={"Content-Length": "0"}, auth=(GIT_USERNAME, GIT_TOKEN))
        assert response.status_code == exp_status_code
        if exp_status_code == 204:
            assert self.check_if_gist_starred(gist_id) == 204

    def unstar_gist(self, gist_id, exp_status_code=204):
        response = requests.delete('{}/gists/{}/star'.format(GIT_URL, gist_id), headers={"Content-Length": "0"}, auth=(GIT_USERNAME, GIT_TOKEN))
        assert response.status_code == exp_status_code
        if exp_status_code == 204:
            assert self.check_if_gist_starred(gist_id) == 404

    def check_if_gist_starred(self, gist_id):
        response = requests.get('{}/gists/{}/star'.format(GIT_URL, gist_id), auth=(GIT_USERNAME, GIT_TOKEN))
        return response.status_code

    def verify_gist_starred(self, gist_id):
        starred_list = self.get_starred_gists()
        for _res in starred_list:
            if gist_id in _res['id']:
                break
        else:
            assert False, "Starred gist {} was not detected !".format(gist_id)

    def verify_gist_unstarred(self, gist_id):
        starred_list = self.get_starred_gists()
        for _res in starred_list:
            if gist_id in _res['id']:
                assert False, "Gist {} is starred !".format(gist_id)

    def edit_gist(self, gist_id, new_desc="", new_json_files={}):
        gist_data2 = {
            "description": new_desc,
            "files": new_json_files
        }
        response = requests.patch('{}/gists/{}'.format(GIT_URL, gist_id),
                                  data=json.dumps(gist_data2),
                                  auth=(GIT_USERNAME, GIT_TOKEN),
                                  headers={"accept": "application/vnd.github.v3+json"})
        assert response.status_code == 200
        body = json.loads(response._content.decode('utf-8'))
        return body

    def get_previous_revision(self, gist_id, previous_version, exp_code=200):
        response = requests.get('{}/gists/{}/{}'.format(GIT_URL, gist_id, previous_version))
        assert response.status_code == exp_code, "returned status-code is {} !".format(response.status_code)
        body = json.loads(response._content.decode('utf-8'))
        return body