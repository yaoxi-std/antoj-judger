FROM python:3.13

# Install docker

RUN apt-get update && \
    apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

RUN echo "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list

RUN apt-get update && \
    apt-get install -y docker-ce docker-ce-cli containerd.io

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Main sources

ADD . /opt/antoj-judger

WORKDIR /opt/antoj-judger

RUN pip install -r requirements.txt

CMD ["python3", "-m", "main"]
