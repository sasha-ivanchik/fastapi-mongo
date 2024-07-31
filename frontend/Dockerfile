FROM node:16.16.0-alpine as build

WORKDIR .

COPY frontend/package*.json ./
RUN npm install
COPY frontend .
RUN npm run build

FROM nginx:stable-alpine

COPY --from=build /dist /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]