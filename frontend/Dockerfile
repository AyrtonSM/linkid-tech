# FROM nginx
# COPY . /usr/share/nginx/html
# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]

FROM nginx

# Apaga configs default
RUN rm /etc/nginx/conf.d/default.conf

# Copia o site estático
COPY . /usr/share/nginx/html

# Copia sua configuração
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 28000

CMD ["nginx", "-g", "daemon off;"]