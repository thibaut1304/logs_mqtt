FROM python:3.11-slim

ENV TZ=${TZ}
RUN apt-get update && apt-get install -y tzdata openssh-client rsync && \
    ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime && \
    echo ${TZ} > /etc/timezone && \
    apt-get clean

	WORKDIR /app
COPY ./app .
# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt
# Créer l'utilisateur avec UID / GID
ARG UID
ARG GID
RUN addgroup --gid ${GID} appgroup && \
    adduser --uid ${UID} --gid ${GID} --disabled-password --gecos '' appuser

# Donner les droits
RUN chown -R appuser:appgroup /app

USER appuser

CMD ["python3", "-u", "main.py"]
