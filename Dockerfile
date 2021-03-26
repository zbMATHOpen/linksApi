FROM python:3.7

WORKDIR /zb_links
COPY . /zb_links
RUN pip install .
COPY ./config_template.ini ./config.ini
ENV APP_SETTINGS="config.DevelopmentConfig"
ENV FLASK_APP="zb_links.app.py"
EXPOSE 5000
ENTRYPOINT ["gunicorn", "--bind",  "0.0.0.0:5000", "wsgi:app"]
