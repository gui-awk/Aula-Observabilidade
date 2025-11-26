FROM nginx:alpine

# Instalar apache2-utils para htpasswd
RUN apk add --no-cache apache2-utils openssl

# Copiar configuração do nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Criar diretório para SSL
RUN mkdir -p /etc/nginx/ssl

# Script para gerar certificado autoassinado e htpasswd
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 80 443

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
