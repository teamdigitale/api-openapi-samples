#!/usr/bin/bash
set -eo pipefail

die(){
	echo "ERROR: $@"
	exit 1
}
: ${1?Please specify a file to convert}

which docker >&2 || die "You need docker to run this file."

# Eventually build docker image.
docker >&2 build -t api-spec-converter $(dirname $(readlink -f $0))  || die "Cannot build docker image."

FROM="$(readlink -f $1)"; shift
test -f "$FROM" || die "File not found: $FROM"


docker run --rm \
	-v $(dirname $FROM):/tmp:z \
        --entrypoint /usr/local/bin/api-spec-converter \
 	api-spec-converter:latest \
	"/tmp/$(basename $FROM)"  $@
	#/usr/local/bin/api-spec-converter "/tmp/$(basename $FROM)" --syntax="${FROM##*.}" --from=openapi_3 --to=swagger_2 

