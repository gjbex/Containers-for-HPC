# =============================================================================
# Build environment
FROM continuumio/miniconda3:4.10.3-alpine as build

# Install conda pack
RUN conda install -c conda-forge conda-pack

# Create target environment
COPY environment.yml .
RUN conda env create -n env -f environment.yml

# Compress (pack) target environment
RUN conda pack -n env -o env.tar.gz

# =============================================================================
# Runtime environment
FROM debian:bullseye-slim as runtime

# Install the environment pack
COPY --from=build /env.tar.gz .
RUN mkdir /env && \
    tar xvzf /env.tar.gz -C /env && \
    rm -rv /env.tar.gz && \
    /env/bin/python /env/bin/conda-unpack
ENV PATH="/env/bin/:$PATH"
