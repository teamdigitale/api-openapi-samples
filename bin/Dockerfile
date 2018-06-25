#
# Image to run various api tools based on 
#  node and python.
#
FROM node:9
MAINTAINER robipolli@gmail.com

# Install python-yaml.
RUN apt update && apt install python-yaml

ADD Dockerfile
RUN npm install -g git+https://github.com/LucyBot-Inc/api-spec-converter.git --unsafe-perm=true --allow-root

ENTRYPOINT /usr/local/bin/api-spec-converter
CMD /usr/local/bin/api-spec-converter

