FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3.12 \
        python3.12-venv \
        git \
        curl \
        build-essential \
        postgresql \
        postgresql-contrib \
        sudo \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /usr/bin/python3.12 /usr/bin/python3

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Allow the default ubuntu user to start PostgreSQL without a password prompt.
RUN echo "ubuntu ALL=(postgres) NOPASSWD:ALL" >> /etc/sudoers.d/ubuntu-postgres \
    && chmod 0440 /etc/sudoers.d/ubuntu-postgres
