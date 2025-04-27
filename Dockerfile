FROM python:3.9

EXPOSE 3091

WORKDIR /SteamGremlinBackend

COPY backend/requirements.txt .

RUN pip install -r requirements.txt

COPY backend/src .

ENTRYPOINT [ "python", "src/sockets.py" ]
