# Verwenden Sie ein offizielles Python-Image als Basis
FROM python:3.9-slim

# Setzen Sie das Arbeitsverzeichnis auf /app
WORKDIR /app

# Kopieren Sie die Anforderungsdatei in das Arbeitsverzeichnis
COPY requirements.txt .

# Installieren Sie alle benötigten Pakete
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Kopieren Sie den Rest des Anwendungscodes in das Arbeitsverzeichnis
# COPY . .

# Öffnen Sie den Port, auf dem die App laufen wird
EXPOSE 8000

# Führen Sie das Python-Script aus
CMD ["python", "src/nostr/nostr_backend.py"]
