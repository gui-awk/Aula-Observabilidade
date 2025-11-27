#!/bin/sh
set -e

# Gerar certificado SSL autoassinado se não existir
if [ ! -f /etc/nginx/ssl/nginx.crt ]; then
    echo "Generating self-signed SSL certificate..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/nginx/ssl/nginx.key \
        -out /etc/nginx/ssl/nginx.crt \
        -subj "/C=BR/ST=SP/L=SaoPaulo/O=Observability/OU=DevOps/CN=observability.local"
    chmod 600 /etc/nginx/ssl/nginx.key
fi

# Criar htpasswd se não existir (usuário padrão: admin / senha: LMjz6DuM2UX1Qug6NYxA7tNDJhIb3mOx)
if [ ! -f /etc/nginx/.htpasswd ]; then
    echo "Creating htpasswd file with default credentials (admin/LMjz6DuM2UX1Qug6NYxA7tNDJhIb3mOx)..."
    htpasswd -bc /etc/nginx/.htpasswd admin LMjz6DuM2UX1Qug6NYxA7tNDJhIb3mOx
fi

echo "NGINX is ready!"
echo "Default credentials: admin / LMjz6D****************x"
echo "Access: https://<your-ip>"

# Executar comando original
exec "$@"
