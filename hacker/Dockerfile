# Use Alpine Linux as the base image
FROM ubuntu:latest

# Install curl and tshark
RUN apt-get update && \
    apt-get install -y tshark && \
    apt-get install -y curl && \
    apt-get clean

CMD ["/bin/sh"]