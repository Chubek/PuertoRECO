FROM continuumio/miniconda:latest

WORKDIR /home/docker_conda_template

COPY environment.yml ./
COPY api.py ./
COPY boot.sh ./

RUN chmod +x boot.sh

RUN Conda env create -f environment.yml

RUN echo "source activate reco3" > ~/.bashrc
ENV PATH /opt/conda/envs/reco3/bin:$PATH

EXPOSE 5000

ENTRYPOINT ["./boot.sh"] 