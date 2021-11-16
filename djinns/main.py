import json
from flask import Flask, Blueprint, request
from flask_cors import CORS

import os
import hashlib

from entrypoint import view_function


class Djinns:
    def __init__(self, apispec_file="api_spec.json"):
        self.apispec_file = apispec_file
        self.apispec_json = json.loads(open(apispec_file).read())
        self.apis = self.apispec_json['apis']
        self.blueprints = []
        self.app = Flask(self.apispec_json['title'])
        cors = CORS(self.app)

        self._generate_app()


    def invoke(self):
        self.app.run()

    def __generate_apis_code(self, api, child_apis, url_prefix="/"):
        url_prefix = api if url_prefix == "/" else "{}/<{}_id>/{}".format(
            url_prefix,
            [a for a in url_prefix.split('/') if a != ""][-1],
            api
        ).replace("//", "/")

        api_name = api[1:]

        api_file = "apis/{}.json".format(api_name)
        api_json = json.loads(open(api_file).read())
        api_paths = api_json[api]

        apis_code = "from controllers import {} as {}_controller\n".format(api_name, api_name)
        apis_code += 'apis["{}"] = {}_controller\n\n'.format(api, api_name)
        open("apis.py", "a+").write(apis_code)

        # generating controllers code
        controller_dir = 'controllers/'
        os.makedirs(controller_dir, exist_ok=True)
        full_prefix = url_prefix
        controller_code = self.__generate_controllers_code(api, api_paths, full_prefix)
        controller_file = "controllers/{}.py".format(api[1:]).replace("//", "/")
        open(controller_file, "w").write(controller_code)

        if child_apis != {}:
            for _api, _child_apis in child_apis.items():
                self.__generate_apis_code(_api, _child_apis, url_prefix)


    def _generate_app(self):
        apis_code = '"""This is an autogenerated file, '
        apis_code += 'please don\'t change it!"""\n\n'
        apis_code += 'apis = {}\n\n'
        open("apis.py", "w").write(apis_code)

        for api, child_apis in self.apis.items():
            self.__generate_apis_code(api, child_apis)

        for path, method in set(self.blueprints):
            path_signature = hashlib.sha256()
            path_signature.update(json.dumps(path).encode())
            path_signature = path_signature.hexdigest()

            self.app.add_url_rule(
                path,
                path_signature,
                view_function,
                methods=[method]
            )


    def __generate_controllers_code(self, api, api_paths, full_prefix):
            controller_functions = "\n"

            controller_code = '""" In this file, you can edit the behavior of '
            controller_code += 'each controller which # is mapped '
            controller_code += 'to an endpoint of API"""\n\n'

            for path_json in api_paths:
                path_signature = hashlib.sha256()
                path_signature.update(json.dumps(path_json).encode())
                path_signature = path_signature.hexdigest()
                path = path_json['path']
                method = path_json['method']
                description = path_json['description']

                self.blueprints.append((full_prefix + path, method))

                full_path = '{}{}'.format(full_prefix, path)
                controller_name = "{}{}_{}".format(
                    method.lower(),
                    full_path,
                    path_signature[:8]
                ).replace('/', '_').\
                replace('<', '').\
                replace('>', '').\
                replace("-", "_").\
                replace("__", "_")
     
                path_function = ("""
def {}(*args, **kwargs):
    # path: {}
    # description: {}
    # method: {}

    # TODO: method not implemented

    return {}, 200\n\n""").\
                    format(
                        controller_name,
                        full_path,
                        description,
                        method,
                        "{}"
                    )

                controller_code += path_function
                controller_functions += '    "{}": {},\n'.format(full_path, controller_name)
     
            controller_functions = "\nfunctions = {}{}\n{}".format("{", controller_functions[:-2], "}")
            controller_code += controller_functions

            return controller_code
