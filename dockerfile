FROM node:20

WORKDIR /app

COPY package*.json ./

RUN yarn install

COPY public ./public
COPY src ./src
COPY .env ./

EXPOSE 3000

CMD ["yarn", "start:client"]
