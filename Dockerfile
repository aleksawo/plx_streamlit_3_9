FROM python:3.9-slim

WORKDIR /plx_streamlit_3_9

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

ARG CACHEBUST=1

RUN git clone https://github.com/aleksawo/plx_streamlit_3_9.git .

RUN pip3 install -r requirements.txt

EXPOSE 10002

HEALTHCHECK CMD curl --fail http://0.0.0.0:10002/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=10002", "--server.address=0.0.0.0"]


