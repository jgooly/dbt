import dbt.project as project
import os.path
import subprocess
import yaml
import re

from dbt.hosted.api import DbtAPI

class HostedInitializeTask:
    def __init__(self, args):
        self.args = args

    def run(self):
        api = DbtAPI()

        key = api.ensure_token_set()

        if not key:
            return "Failed to get a valid token."

        remote = self.__get_remote()

        # TODO: verify we are in a dbt project

        project = api.get_or_create_project(
            remote
        )

    def __parse(self, remote):
        name = None
        matched = re.match(r'git@github.com:(.*)\.git$', remote)
        if matched:
            name = matched.groups()[0]
        matched = re.match(r'github.com/(.*)\.git$', remote)
        if matched:
            name = matched.groups()[0]

        if name is None:
            raise RuntimeError("Invalid GitHub name? {}".format(name))

        org, repo = name.split("/", 1)
        return org, repo

    def __get_remote(self):
        # git remote get-url origin
        proc = subprocess.Popen(['git', 'remote', 'get-url', 'origin'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if len(err) > 0:
            raise RuntimeError(err.strip())

        return out