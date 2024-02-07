FROM node:14.17-buster

ENV METEOR_ALLOW_SUPERUSER=true
ENV ROOT_URL="http://34.69.232.63"
ENV MONGO_URL="mongodb+srv://ondc-hackathon:wEqIj1KfrBd50FME@ondc.a3agffn.mongodb.net/?retryWrites=true&w=majority"
RUN curl https://install.meteor.com/ | sh

WORKDIR /code

COPY package.json package.json
COPY package-lock.json package-lock.json

COPY .meteor/release .meteor/release
COPY .meteor/platforms .meteor/platforms
COPY .meteor/packages .meteor/packages
COPY .meteor/versions .meteor/versions

RUN meteor npm install

COPY . .

RUN chmod -R 700 /code/.meteor/local

EXPOSE 3000

CMD [ "meteor" ,"run","--settings=settings.json"]
