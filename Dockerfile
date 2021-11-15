FROM python:3.7

WORKDIR /zb_links
COPY setup_docker.py setup.py
COPY setup.cfg .
RUN mkdir src && pip install .[test]
COPY . /zb_links
RUN pip install -e .
EXPOSE 5000
ENTRYPOINT ["gunicorn", "--bind",  "0.0.0.0:5000", "zb_links.app:create_app()"]
