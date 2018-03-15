FROM node:9
MAINTAINER robipolli@gmail.com

RUN npm install -g git+https://github.com/LucyBot-Inc/api-spec-converter.git --unsafe-perm=true --allow-root
ENTRYPOINT /usr/local/bin/api-spec-converter
CMD /usr/local/bin/api-spec-converter

