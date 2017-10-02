FROM python:3.6
LABEL maintainer "Simon Gomizelj <simon@vodik.xyz>"

WORKDIR /app
COPY . /app
RUN pip install /app

EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["-m", "aiohttp.web", "sensord.app:app_factory", "-H", "0.0.0.0", "-P", "9306"]
