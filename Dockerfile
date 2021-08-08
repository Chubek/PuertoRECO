FROM continuumio/miniconda:latest

WORKDIR /home/reco_app

COPY faceapp.py ./
COPY boot.sh ./
COPY scripts/ ./
COPY templates/ ./
COPY unit_tests/ ./
COPY .env ./
COPY codes_dict.py ./
COPY requirements.txt ./
COPY README.md ./
COPY main.py ./
COPY environment.yml ./


RUN chmod +x boot.sh


SHELL ["conda", "run", "-n", "reco3", "/bin/bash", "-c"]
SHELL ["pip", "install", "-r", "requirements.txt"]

ENV PATH /opt/conda/envs/reco3/bin:$PATH

EXPOSE 5000

ENTRYPOINT ["./boot.sh"] 