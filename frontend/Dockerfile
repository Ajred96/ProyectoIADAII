FROM node:18

WORKDIR /app

COPY package*.json ./
RUN npm install --force

COPY . .

ENV NODE_OPTIONS=--openssl-legacy-provider

CMD ["npx", "ng", "serve", "--host", "0.0.0.0", "--port", "4200"]
