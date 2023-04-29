# Verwende das offizielle Node.js-Image als Basis
FROM node:14

# Erstelle das Arbeitsverzeichnis
WORKDIR /app

# Kopiere package.json und package-lock.json in das Arbeitsverzeichnis
COPY package*.json ./

# Installiere die Node.js-Abhängigkeiten
RUN npm ci

# Installiere Python 3.9 und pip
RUN curl -O https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tar.xz && \
    tar -xf Python-3.9.9.tar.xz && \
    cd Python-3.9.9 && \
    ./configure && \
    make -j $(nproc) && \
    make altinstall && \
    cd .. && \
    rm -rf Python-3.9.9 Python-3.9.9.tar.xz
RUN update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.9 1
RUN python3.9 -m pip install --upgrade pip

# Kopiere die requirements.txt-Datei und den python_nostr-Ordner in das Arbeitsverzeichnis
COPY requirements.txt ./

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y && \
    export PATH="$HOME/.cargo/bin:$PATH" && \
    rustup install stable && \
    rustup default stable

# Installiere die Python-Abhängigkeiten
RUN python3.9 -m pip install -r requirements.txt

# Kopiere den Rest der Anwendung in das Arbeitsverzeichnis
COPY . .

# Führe das Build-Skript aus
RUN npm run build
