#!/usr/bin/env python3
import collections
import logging
import sys
from argparse import ArgumentParser
from os import getcwd, path

import jsonschema
import yaml
from colors import color
from jsonschema.exceptions import RefResolutionError
from openapi_spec_validator import openapi_v3_spec_validator
from openapi_spec_validator.handlers import UrlHandler
from six.moves.urllib.parse import urlparse

logging.basicConfig(level=logging.DEBUG)


def resolve_refs(uri, spec):
    """Resolve JSON references in a given dictionary.

    OpenAPI spec may contain JSON references to its nodes or external
    sources, so any attempt to rely that there's some expected attribute
    in the spec may fail. So we need to resolve JSON references before
    we use it (i.e. replace with referenced object). For details see:

        https://tools.ietf.org/html/draft-pbryan-zyp-json-ref-02

    The input spec is modified in-place despite being returned from
    the function.
    """
    resolver = jsonschema.RefResolver(uri, spec)

    def _do_resolve(node):
        if isinstance(node, collections.Mapping) and "$ref" in node:
            with resolver.resolving(node["$ref"]) as resolved:
                return resolved
        elif isinstance(node, collections.Mapping):
            for k, v in node.items():
                node[k] = _do_resolve(v)
        elif isinstance(node, (list, tuple)):
            for i in range(len(node)):
                node[i] = _do_resolve(node[i])
        return node

    return _do_resolve(spec)


def get_custom_spec(fpath, version):
    italia_oas3_schema = yaml.safe_load(open(fpath))
    print(italia_oas3_schema)
    resolve_refs("", italia_oas3_schema)
    return italia_oas3_schema["oas-" + ".".join(version)]


def validate(url):
    counter = 0

    try:
        handler = UrlHandler("http", "https", "file")

        if not urlparse(url).scheme:
            url = "file://" + path.join(getcwd(), url)

        spec = handler(url)

        for i in openapi_v3_spec_validator.iter_errors(spec, spec_url=url):
            counter += 1
            print_error(
                counter, ":".join(i.absolute_path), i.message, i.instance
            )

    except RefResolutionError as e:
        counter += 1
        print_error(
            counter,
            "",
            f"Unable to resolve {e.__context__.args[0]} in {e.args[0]}",
            "",
        )
    except BaseException:
        counter += 1
        print_error(counter, "", sys.exc_info()[0], "")
    finally:
        if counter > 0:
            print()
            print(
                color(
                    " [FAIL] %d errors found " % counter,
                    fg="white",
                    bg="red",
                    style="bold",
                )
            )
            return 1
        else:
            print_ok(" [PASS] No errors found ")
            return 0


def print_ok(msg):
    print(color(f" {msg} ", fg="white", bg="green", style="bold"))


def print_error(count, path, message, instance):
    print()
    print(
        color("Error #%d in [%s]:" % (count, path or "unknown"), style="bold")
    )
    print("    %s" % message)
    print("    %s" % instance)


def main(
    specfile,
    validation_type="extended",
    schema_file="openapi-v3/metadata.yaml",
):

    # OAS validation.
    spec = yaml.safe_load(open(specfile))
    openapi_version = spec["openapi"].split(".")
    validate(specfile)

    # Interoperability model validation
    if validation_type == "extended":
        api_schema = get_custom_spec(schema_file, openapi_version[:2])
        for g in ("info", "servers"):
            assert g in spec
            jsonschema.validate(instance=spec[g], schema=api_schema[g])

        print_ok(" [PASS] All required metadata are present.")


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "--spec",
        dest="spec",
        required=True,
        help="OAS3 spec file or url",
        default=False,
    )
    parser.add_argument(
        "--schema",
        dest="schema",
        required=False,
        help="Additional schema file to use for validation",
        default="openapi-v3/metadata.yaml",
    )

    parser.add_argument(
        "--type",
        dest="validation_type",
        required=False,
        help="Whether validate just oas3 or extended x-attributes."
        " Valid values: 'oas3', 'extended'",
        default="extended",
    )
    args = parser.parse_args()

    main(args.spec, validation_type=args.validation_type)
