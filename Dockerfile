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

RUN conda env create -f environment.yml


RUN echo "source activate reco3" > ~/.bashrc
ENV PATH /opt/conda/envs/reco3/bin:$PATH

EXPOSE 5000

ENTRYPOINT ["./boot.sh"] 