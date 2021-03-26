FROM python:3.7

WORKDIR /zb_links
COPY . /zb_links
RUN pip install .
COPY ./config_template.ini /zb_links/config.ini
ENV FLASK_APP="zb_links.app.py"
EXPOSE 5000
ENTRYPOINT ["gunicorn", "--bind",  "0.0.0.0:5000", "wsgi:app"]
