FROM ghcr.io/astral-sh/uv:python3.9-alpine

RUN groupadd --gid 2000 develop && \
    useradd --uid 2000 --gid 2000 -m develop

USER develop
