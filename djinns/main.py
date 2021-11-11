import json
from flask import Blueprint, request

import os
import hashlib

from entrypoint import view_function
from djinns import factory


class Djinns:
    def __init__(self, apispec_file="api_spec.json"):
        self.apispec_file = apispec_file
        self.apispec_json = json.loads(open(apispec_file).read())
        self.apis = self.apispec_json['apis']
        self.app = self.__generate_app()

    def start(self):
        self.app.run()

    def __generate_app(self):
        apis_code = '"""This is an autogenerated file, '
        apis_code += 'please don\'t change it!"""\n\n'
        apis_code += 'apis = {}\n\n'

        api_blueprints = []
        for api, api_file in self.apis.items():
            api_json = json.loads(open(api_file).read())
            api_bp = Blueprint(api, __name__, url_prefix=api)

            api_paths = api_json[api]


            api_name = api[1:]

            apis_code += "from controllers import {} as {}_controller\n".format(api_name, api_name)
            apis_code += 'apis["{}"] = {}_controller\n\n'.format(api, api_name)

            controller_code = '""" In this file, you can edit the behavior of '
            controller_code += 'each controller which # is mapped '
            controller_code += 'to an endpoint of API"""\n\n'

            controller_dir = 'controllers/'
            os.makedirs(controller_dir, exist_ok=True)

            controller_file = "controllers/{}.py".format(api[1:]).replace("//", "/")

            controller_functions = "\n"

            for path_json in api_paths:
                path_signature = hashlib.sha256()
                path_signature.update(json.dumps(path_json).encode())
                path_signature = path_signature.hexdigest()
                path = path_json['path']
                method = path_json['method']
                description = path_json['description']


                api_bp.add_url_rule(
                    path,
                    path_signature,
                    view_function,
                    methods=[method]
                )
     
                full_path = '{}{}'.format(api, path)
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

    import pdb; pdb.set_trace()
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
            open(controller_file, "w").write(controller_code)
            api_blueprints.append(api_bp)
     
        open("apis.py", "w").write(apis_code)
        app = factory.create_app(__name__, api_blueprints)
        return app