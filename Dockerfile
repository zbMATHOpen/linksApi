# syntax = docker/dockerfile:1.2
FROM python:3.7

WORKDIR /zb_links
COPY setup.py setup.cfg /zb_links/
RUN --mount=source=.git,target=.git,type=bind \
    mkdir src && pip install .[test]
COPY . /zb_links
RUN pip install -e .
EXPOSE 5000
ENTRYPOINT ["gunicorn", "--bind",  "0.0.0.0:5000", "zb_links.app:create_app()"]
