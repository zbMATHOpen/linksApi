FROM python:3.7

WORKDIR /zb_links
COPY setup_docker.py setup.py
COPY test_requirements.txt setup.cfg ./
RUN mkdir src && pip install -r test_requirements.txt
COPY . /zb_links
RUN pip install -e .
COPY ./config_template.ini /zb_links/config.ini
ENV FLASK_APP="zb_links.app.py"
EXPOSE 5000
ENTRYPOINT ["gunicorn", "--bind",  "0.0.0.0:5000", "wsgi:app"]
