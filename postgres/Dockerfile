FROM postgres:latest

# Install openssl (if not already installed)
RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*

# Generate SSL certificates
RUN openssl genpkey -algorithm RSA -out /etc/ssl/private/server.key -pkeyopt rsa_keygen_bits:2048
RUN openssl req -new -x509 -subj "/CN=localhost" -key /etc/ssl/private/server.key -out /etc/ssl/certs/server.crt -days 365

# Set the correct permissions on the key file
RUN chmod 600 /etc/ssl/private/server.key && chown postgres:postgres /etc/ssl/private/server.key

# Configure PostgreSQL to use SSL
RUN echo "ssl = on" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "ssl_cert_file = '/etc/ssl/certs/server.crt'" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "ssl_key_file = '/etc/ssl/private/server.key'" >> /usr/share/postgresql/postgresql.conf.sample && \
    echo "hostssl all all 0.0.0.0/0 md5" >> /usr/share/postgresql/pg_hba.conf.sample