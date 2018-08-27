#!/bin/bash -x
: ${1?Missing OpenAPI Version}

openapi_version=$1; shift
if [ "$openapi_version" == "help" ]; then
	ls  /opt/swagger-codegen-cli-*.jar 
	exit 1
fi

JAR=$(ls /opt/swagger-codegen-cli-$openapi_version*.jar)
java -jar $JAR  $@ -o /outdir -i /swagger.yaml
