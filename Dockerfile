FROM python:3.12-slim

WORKDIR IMAGE_LABELER_WEB_APP
COPY ./app.py /IMAGE_LABELER_WEB_APP/
COPY ./templates /IMAGE_LABELER_WEB_APP/templates

RUN pip install flask==3.0.0

ENTRYPOINT ["python", "app.py"]