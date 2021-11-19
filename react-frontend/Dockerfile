FROM node:14-alpine

WORKDIR /usr/src/app
COPY . .
RUN npm install
EXPOSE 3000

ENV CHOKIDAR_USEPOLLING=true
ENTRYPOINT [ "npm", "start" ]