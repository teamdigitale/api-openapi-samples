"""This script resolves references in a yaml file and dumps it
    removing all of them.

    It expects references are defined in `x-commons` object.
    This object will be removed before serialization.
"""
from __future__ import print_function
from sys import argv
import yaml
from six.moves.urllib.parse import urldefrag
from six.moves.urllib.request import urlopen
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

yaml_cache = {}

ROOT_NODE = object()


def traverse(node, key=ROOT_NODE, parents=None, cb=print):
    """ Recursively call nested elements."""
    parents = parents[-4:] if parents else []
    if isinstance(node, (dict, list)):
        valuelist = node.items() if isinstance(node, dict) else enumerate(node)
        if key is not ROOT_NODE:
            parents.append(key)
        parents.append(node)
        for k, i in valuelist:
            traverse(i, k, parents, cb)
    else:
        if key == '$ref' and node.startswith("http"):
            ancestor, needle = parents[-3:-1]
            #log.info(f"replacing: {needle} in {ancestor} with ref {node}")
            ancestor[needle] = cb(key, node)
            if isinstance(ancestor[needle], (dict, list)):
                traverse(ancestor[needle], key, parents, cb)


def test_traverse():
    oat = {
        'a': 1,
        'list_of_refs': [
            {'$ref': 'https://teamdigitale.github.io/openapi/parameters/v3.yaml#/sort'}
        ],
        'object': {'$ref': 'https://teamdigitale.github.io/openapi/parameters/v3.yaml#/sort'}
    }
    traverse(oat, cb=resolve_node)
    assert(oat == {'a': 1, 'list_of_refs': [{'name': 'sort', 'in': 'query', 'description': 'Sorting order', 'schema': {
           'type': 'string', 'example': '+name'}}], 'object': {'name': 'sort', 'in': 'query', 'description': 'Sorting order', 'schema': {'type': 'string', 'example': '+name'}}})
    print(oat)


def test_traverse_list():
    oat = [
        {'$ref': 'https://teamdigitale.github.io/openapi/parameters/v3.yaml#/sort'}
    ]
    traverse(oat, cb=resolve_node)
    assert(oat == [{'name': 'sort', 'in': 'query', 'description': 'Sorting order', 'schema': {
           'type': 'string', 'example': '+name'}}])
    print(oat)


def test_traverse_object():
    oas = {'components': {'parameters': {'limit': {'$ref': 'https://teamdigitale.github.io/openapi/parameters/v3.yaml#/limit'},
                                         'sort': {'$ref': 'https://teamdigitale.github.io/openapi/parameters/v3.yaml#/sort'}},
                          'headers': {'X-RateLimit-Limit': {'$ref': 'https://teamdigitale.github.io/openapi/headers/v3.yaml#/X-RateLimit-Limit'},
                                      'Retry-After': {'$ref': 'https://teamdigitale.github.io/openapi/headers/v3.yaml#/Retry-After'}},
                          }}
    traverse(oas, cb=resolve_node)
    print(yaml.dump(oas, default_flow_style=0))


def test_nested_reference():
    oat = {'400BadRequest': {'$ref': 'https://teamdigitale.github.io/openapi/responses/v3.yaml#/400BadRequest'}}
    traverse(oat, cb=resolve_node)
    print(yaml.dump(oat, default_flow_style=0))


def get_yaml_reference(f, yaml_cache=None):
    #log.info(f"Downloading {f}")
    host, fragment = urldefrag(f)
    if host not in yaml_cache:
        yaml_cache[host] = urlopen(host).read()

    f_yaml = yaml.load(yaml_cache[host])
    if fragment.strip("/"):
        f_yaml = finddict(f_yaml, fragment.strip("/").split("/"))
    return f_yaml


def finddict(_dict, keys):
    #log.debug(f"search {keys} in {_dict}")
    p = _dict
    for k in keys:
        p = p[k]
    return p


def resolve_node(key, node):
    #log.info(f"Resolving {node}")
    _yaml = get_yaml_reference(node, yaml_cache=yaml_cache)
    return _yaml


def should_use_block(value):
    for c in u"\u000a\u000d\u001c\u001d\u001e\u0085\u2028\u2029":
        if c in value:
            return True
    return False


def my_represent_scalar(self, tag, value, style=None):
    if should_use_block(value):
        style = '|'
    else:
        style = self.default_style

    node = yaml.representer.ScalarNode(tag, value, style=style)
    if self.alias_key is not None:
        self.represented_objects[self.alias_key] = node
    return node


def main(src_file, dst_file):
    # Resolve references in yaml file.
    yaml.Dumper.ignore_aliases = lambda *args: True

    # Dump long lines as "|".
    yaml.representer.BaseRepresenter.represent_scalar = my_represent_scalar

    with open(src_file) as fh_src, open(dst_file, 'w') as fh_dst:
        ret = yaml.load(fh_src)
        traverse(ret, cb=resolve_node)
        # Remove x-commons containing references and aliases.
        if 'x-commons' in ret:
            del ret['x-commons']

        content = yaml.dump(ret, default_flow_style=False, allow_unicode=True)
        fh_dst.write(content)

if __name__ == '__main__':
    try:
        progname, src_file, dst_file = argv
    except:
        raise SystemExit("usage: src_file.yaml.src dst_file.yaml", argv)

    main(src_file, dst_file)
