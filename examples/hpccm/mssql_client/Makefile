DOCKER = docker
SINGULARITY = singularity
HPCCM = hpccm
TAG = odbc/1.0

docker: Dockerfile
	sudo $(DOCKER) build -t $(TAG) -f $< .

odbc.sif: odbc.spec
	sudo $(SINGULARITY) build $@ $<

Dockerfile: odbc.py
	$(HPCCM) --recipe $< --format docker > $@

odbc.spec: odbc.py
	$(HPCCM) --recipe $< --format singularity > $@

clean:
	$(RM) Dockerfile odbc.spec odbc.sif

docker-start:
	sudo systemctl start docker

docker-stop:
	sudo systemctl stop docker
