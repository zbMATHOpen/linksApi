FROM python:3.7

WORKDIR /zb_links
COPY setup.py setup.cfg /zb_links/
RUN mkdir src && \
    SETUPTOOLS_SCM_PRETEND_VERSION=1 pip install -e .[test]
RUN --mount=source=.git,target=.git,type=bind \
    pip install -e .[test]
COPY . /zb_links
EXPOSE 5000
ENTRYPOINT ["gunicorn", "--bind",  "0.0.0.0:5000", "zb_links.app:create_app()"]
