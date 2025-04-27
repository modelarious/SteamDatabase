FROM node:18-alpine

# XXX Unneeded, but the whole thing would need to rebuild if I remove this lmao
# EXPOSE 3000

RUN npm create vite@latest steam-indexer-frontend -- --template react 

WORKDIR /steam-indexer-frontend

RUN npm install

# XXX No need for this
# run cat package.json

RUN npm install @chakra-ui/react @emotion/react @emotion/styled framer-motion
RUN npm install react-tabs-redux

RUN npm install websocket
RUN npm install auto-bind
RUN npm install react-dropdown react-router-dom react-tag-input
RUN npm install react-grid-gallery




EXPOSE 5173
ENTRYPOINT [ "npm", "run", "dev", "--", "--host" ]


# COPY steam-indexer-frontend/package.json .
# # COPY package-lock.json .

# RUN npm install

# COPY steam-indexer-frontend/src .

# RUN npm start
