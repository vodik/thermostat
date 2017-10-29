FROM python:3.6
LABEL maintainer "Simon Gomizelj <simon@vodik.xyz>"

WORKDIR /app
COPY . /app
RUN pip install gunicorn uvloop -e /app

EXPOSE 9305
EXPOSE 9306
ENTRYPOINT ["gunicorn"]
CMD ["sensord.app:app_factory()", "--bind", "0.0.0.0:9306", "--worker-class", "aiohttp.GunicornUVLoopWebWorker"]
