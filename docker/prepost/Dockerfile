# Dockerfile to create image of computational environment
# for pre- and post-processing steps.

FROM ubuntu:16.04
MAINTAINER Olivier Mesnard <mesnardo@gwu.edu>

# Install base system.
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        build-essential \
        autotools-dev \
        gfortran \
        vim \
        git \
        wget \
        curl \
        pkg-config && \
    # PETSc dependencies.
    apt-get install -y --no-install-recommends \
        cmake \
        flex \
        bison \
        python-dev && \
    # VisIt dependencies.
    apt-get install -y --no-install-recommends \
        libsm6 \
        libxrender1 \
        libfontconfig1 \
        libxt6 \
        libxext6 \
        libgl1-mesa-dev

# Install OpenMPI-1.8.8.
RUN VERSION=1.8.8 && \
    TARBALL=openmpi-${VERSION}.tar.gz && \
    URL=https://www.open-mpi.org/software/ompi/v1.8/downloads/${TARBALL} && \
    wget --no-check-certificate ${URL} -P /tmp && \
    SRCDIR=/opt/openmpi/${VERSION} && \
    mkdir -p ${SRCDIR} && \
    tar -xzf /tmp/${TARBALL} -C ${SRCDIR} --strip-components=1 && \
    BUILDDIR=${SRCDIR}/linux-gnu-opt && \
    mkdir -p ${BUILDDIR} && \
    cd ${BUILDDIR} && \
    ${SRCDIR}/configure \
        --prefix="/usr/local" \
        CC=gcc-5 CFLAGS="-O3" \
        CXX=g++-5 CXXFLAGS="-O3" \
        FC=gfortran FCFLAGS="-O3" && \
    make -j"$(nproc)" && \
    make install && \
    ldconfig && \
    rm -f /tmp/${TARBALL}

# Build PETSc-3.10.2 in optimized mode.
RUN VERSION=3.10.2 && \
    TARBALL=petsc-lite-${VERSION}.tar.gz && \
    URL=http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/${TARBALL} && \
    wget ${URL} -P /tmp && \
    PETSC_DIR=/opt/petsc/${VERSION} && \
    PETSC_ARCH=linux-gnu-openmpi-opt && \
    mkdir -p ${PETSC_DIR} && \
    tar -xzf /tmp/${TARBALL} -C ${PETSC_DIR} --strip-components=1 && \
    cd ${PETSC_DIR} && \
    ./configure --PETSC_DIR=${PETSC_DIR} --PETSC_ARCH=${PETSC_ARCH} \
      --with-cc=mpicc \
      --with-cxx=mpicxx \
      --with-fc=mpif90 \
      --COPTFLAGS=-O3 \
      --CXXFLAGS=-O3 \
      --FOPTFLAGS=-O3 \
      --with-debugging=0 \
      --download-hdf5 \
      --download-fblaslapack \
      --download-hypre \
      --download-ptscotch \
      --download-metis \
      --download-parmetis \
      --download-superlu_dist && \
    make PETSC_DIR=${PETSC_DIR} PETSC_ARCH=${PETSC_ARCH} all && \
    rm -f /tmp/${TARBALL}

ENV PETSC_DIR=/opt/petsc/3.10.2
ENV PETSC_ARCH=linux-gnu-openmpi-opt

# Build and install PetIBM-0.4.
RUN VERSION=0.4 && \
    TARBALL=v${VERSION}.tar.gz && \
    URL=https://github.com/barbagroup/PetIBM/archive/${TARBALL} && \
    wget ${URL} -P /tmp && \
    SRCDIR=/opt/petibm/${VERSION} && \
    BUILDDIR=${SRCDIR}/build && \
    mkdir -p ${SRCDIR} ${BUILDDIR} && \
    tar -xzf /tmp/${TARBALL} -C ${SRCDIR} --strip-components=1 && \
    cd ${BUILDDIR} && \
    ${SRCDIR}/configure --prefix=/usr/local \
      CXX=mpicxx \
      CXXFLAGS="-O3 -w -std=c++14" \
      --enable-static=no \
      --with-petsc-dir=${PETSC_DIR} \
      --with-petsc-arch=${PETSC_ARCH} \
      --enable-yamlcpp \
      --enable-gtest && \
    make -j"$(nproc)" all && \
    make check && \
    make install && \
    ldconfig /usr/local/lib && \
    rm -f /tmp/${TARBALL}

# Download VisIt-2.12.3.
RUN VERSION=2.12.3 && \
    TARBALL=visit2_12_3.linux-x86_64-ubuntu14-wmesa.tar.gz && \
    URL=http://portal.nersc.gov/project/visit/releases/${VERSION}/${TARBALL} && \
    wget ${URL} -P /tmp && \
    mkdir -p /opt/visit && \
    tar -xzf /tmp/${TARBALL} -C /opt/visit --strip-components=1 && \
    rm -f /tmp/${TARBALL}

ENV VISIT_DIR=/opt/visit/2.12.3
ENV PATH=/opt/visit/bin:${PATH}

# Install Miniconda3-4.5.12.
RUN VERSION=4.5.12 && \
    FILENAME=Miniconda3-${VERSION}-Linux-x86_64.sh && \
    URL=https://repo.anaconda.com/miniconda/${FILENAME} && \
    wget ${URL} -P /tmp && \
    bash /tmp/${FILENAME} -b -p /opt/miniconda3 && \
    echo "source /opt/miniconda3/etc/profile.d/conda.sh" >> /root/.bashrc && \
    echo "conda activate py36-cloud" >> /root/.bashrc && \
    rm -f /tmp/${FILENAME}

# Create conda environment for VisIt.
RUN . /opt/miniconda3/bin/activate && \
    conda create --name=py27-visit python=2.7 numpy pathlib pyyaml

# Create conda environment for Azure-CLI, Batch Shipyard, and petibmpy.
RUN . /opt/miniconda3/bin/activate && \
    conda create --name py36-cloud python=3.6 h5py lxml matplotlib numpy pyyaml

# Install Azure-CLI (2.0.57).
RUN . /opt/miniconda3/bin/activate && \
    conda activate py36-cloud && \
    pip install azure-cli==2.0.57 && \
    conda deactivate

# Install Batch Shipyard (3.6.1).
ADD shipyard-install.sh /tmp
RUN VERSION=3.6.1 && \
    TARBALL=${VERSION}.tar.gz && \
    URL=https://github.com/Azure/batch-shipyard/archive/${TARBALL} && \
    wget ${URL} -P /tmp && \
    SRCDIR=/opt/batch-shipyard/${VERSION} && \
    mkdir -p ${SRCDIR} && \
    tar -xzf /tmp/${TARBALL} -C ${SRCDIR} --strip-components=1 && \
    /bin/bash /tmp/shipyard-install.sh && \
    # rm -f /tmp/shipyard-install.sh && \
    rm -f /tmp/${TARBALL}

ENV PATH=/root/.local/bin:${PATH}
ENV LC_ALL=C.UTF-8

# Install petibmpy (0.1).
ARG PETIBMPY_SHA=0f921da
RUN . /opt/miniconda3/bin/activate && \
    cd /opt && \
    git clone https://github.com/mesnardo/petibmpy && \
    cd petibmpy && \
    conda activate py36-cloud && \
    python setup.py install && \
    conda deactivate
