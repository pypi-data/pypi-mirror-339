from typing import List

import yaml

from ..scripts.kawa_tool import KawaTool


class KawaToolKit:

    def __init__(self, name: str, tools: List[KawaTool]):
        self.name: str = name
        self.tools: List[KawaTool] = tools

    def __dict__(self):
        return {'name': self.name, 'tools': [{'name': t.name, 'module': t.module} for t in self.tools]}


def build_kawa_toolkit_from_yaml_file(repo_path: str, file: str) -> KawaToolKit:
    with open(file) as stream:
        try:
            d = yaml.safe_load(stream)
            package_module = file \
                .replace('/kawa-toolkit.yaml', '') \
                .replace(f'{repo_path}/', '') \
                .replace('/', '.')
            tasks = [KawaTool(dd['name'], '{}.{}'.format(package_module, dd['file'].replace('.py', ''))) for dd in
                     d['tools']]

            return KawaToolKit(d['name'], tasks)
        except yaml.YAMLError as exc:
            print(exc)
