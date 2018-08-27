# Swagger CodeGen CLI 

This image contains both swagger 2.x and openapi 3.x release of
swagger-codegen-cli. It can be used to generate server code from 
OpenAPI specs.

## Running

The image works mapping openapi spec and output dir to two docker volumes.
The user is preserved via --user parameter to avoid messing with path permissions.
If you don't have SeLinux you can strip the ":z" from the --volume params

You can pass the `swagger-codegen-cli` arguments to the image or wrap it in a script.

Example:


        docker run --rm \
          --user=$UID: \
          -v ~+/simple.yaml:/swagger.yaml:z \
          -v /tmp/outdir:/outdir:z \
          swagger-codegen-cli-multi 3 generate -l jaxrs-resteasy-eap

