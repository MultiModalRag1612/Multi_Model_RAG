# every statment is a layer and be cashed after implement it 
# we put first stable librairies doesnt change in every time 
FROM python:3.11.15-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install additional system dependencies for lxml and other packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libavif-dev pkg-config \
    libjpeg-dev \
    gcc unzip zip \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY Src/requirements.txt .
# uv install libraires parellel 
RUN uv pip install -r requirements.txt --system

COPY Src/ .

RUN mkdir -p /app/models/db_schemes/alembic
COPY docker/app/alembic.ini /app/models/db_schemes/alembic/alembic.ini
# alembic now is in isolated world in build stage he cant see postgres service so we will need to 
#create entrypoint script that run (after) no (during) build dockerfile image 
#copy from local (docker/app.entrypoint.sh) to docker /entrypoint.sh
COPY docker/app/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]

# command to run fastapi application  after build CMD, ENTRYPOINT
# worker to make more capicty to handel more than one request in fast api at the same time 
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000","--workers","4"]
