FROM python:3.10.7

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE="popell_top100.prod_settings"

WORKDIR /project
COPY Pipfile Pipfile.lock /project/
RUN pip3 install -U pipenv
RUN pipenv install --system
COPY . /project/

EXPOSE 8000
STOPSIGNAL SIGINT
CMD ["sh", "startup.sh"]