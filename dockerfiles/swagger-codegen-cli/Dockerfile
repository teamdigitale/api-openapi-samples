#
# Dockerfile for running different swagger-codegen-cli releases.
#
# Usage:
#  
#     docker run --rm --user=1000: \
#        -v ~+/simple.yaml:/swagger.yaml:z \
#        -v /tmp/outdir:/outdir:z swagger-codegen-cli-multi 3 \
#        generate -l jaxrs-resteasy-eap 
 
FROM java:8
LABEL maintainer="robipolli@gmail.com"

VOLUME /outdir

WORKDIR /opt
RUN wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.3.1/swagger-codegen-cli-2.3.1.jar 
RUN wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/3.0.0-rc1/swagger-codegen-cli-3.0.0-rc1.jar
ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

WORKDIR /
ENTRYPOINT ["/docker-entrypoint.sh"]
