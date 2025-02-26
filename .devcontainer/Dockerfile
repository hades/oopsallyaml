FROM python:3.9

RUN groupadd --gid 2000 develop && \
    useradd --uid 2000 --gid 2000 -m develop && \
    pip install poetry

USER develop
