# Dockerfile for PetIBM-0.4 for use with Batch Shipyard on Azure Batch

FROM nvidia/cuda:8.0-devel-ubuntu16.04
MAINTAINER Olivier Mesnard <mesnardo@gwu.edu>

# Install base system.
COPY ssh_config /root/.ssh/config
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        build-essential \
        autotools-dev \
        gfortran \
        cmake \
        git \
        pkg-config \
        wget \
        curl \
        unzip && \
    # For PETSc
    apt-get install -y --no-install-recommends \
        flex \
        bison \
        python-dev && \
    # Infiniband/RDMA
    apt-get install -y --no-install-recommends \
        cpio \
        libmlx4-1 \
        libmlx5-1 \
        librdmacm1 \
        libibverbs1 \
        libmthca1 \
        libdapl2 \
        dapl2-utils && \
    # Batch-Shipyard dependencies
    apt-get install -y --no-install-recommends \
        openssh-server \
        openssh-client && \
    rm -rf /var/lib/apt/lists/* && \
    # configure ssh server and keys
    mkdir /var/run/sshd && \
    ssh-keygen -A && \
    sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd && \
    ssh-keygen -f /root/.ssh/id_rsa -t rsa -N '' && \
    chmod 600 /root/.ssh/config && \
    chmod 700 /root/.ssh && \
    cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys

# Install Intel MPI library.
ENV MANPATH=/usr/share/man:/usr/local/man \
    COMPILERVARS_ARCHITECTURE=intel64 \
    COMPILERVARS_PLATFORM=linux \
    INTEL_MPI_PATH=/opt/intel/compilers_and_libraries/linux/mpi
ADD l_mpi_2017.2.174.tgz /tmp
RUN cd /tmp/l_mpi_2017.2.174 && \
    sed -i -e 's/^ACCEPT_EULA=decline/ACCEPT_EULA=accept/g' silent.cfg && \
    ./install.sh -s silent.cfg && \
    cd .. && \
    rm -rf l_mpi_2017.2.174

# Build PETSc-3.10.2 in optimized mode.
RUN . /opt/intel/bin/compilervars.sh -arch intel64 -platform linux && \
    . /opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh && \
    VERSION=3.10.2 && \
    TARBALL=petsc-lite-${VERSION}.tar.gz && \
    wget http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/${TARBALL} -P /tmp && \
    PETSC_DIR=/opt/petsc/${VERSION} && \
    PETSC_ARCH=linux-gnu-intel-opt && \
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
    make PETSC_DIR=${PETSC_DIR} PETSC_ARCH=${PETSC_ARCH} test && \
    rm -f /tmp/${TARBALL}

# Build AmgX-2.0.
RUN . /opt/intel/bin/compilervars.sh -arch intel64 -platform linux && \
    . /opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh && \
    VERSION=2.0 && \
    TARBALL=master.tar.gz && \
    wget https://github.com/NVIDIA/AMGX/archive/${TARBALL} -P /tmp && \
    SRCDIR=/opt/amgx/${VERSION} && \
    BUILDDIR=${SRCDIR}/build && \
    mkdir -p ${SRCDIR} ${BUILDDIR} && \
    tar -xzf /tmp/${TARBALL} -C ${SRCDIR} --strip-components=1 && \
    cd ${BUILDDIR} && \
    cmake ${SRCDIR} \
      -DCMAKE_BUILD_TYPE="Release" \
      -DCMAKE_INSTALL_PREFIX="/usr/local" \
      -DCMAKE_C_COMPILER=mpicc \
      -DCMAKE_C_FLAGS_PROFILE="-O3 -DNDEBUG" \
      -DCMAKE_CXX_COMPILER=mpicxx \
      -DCMAKE_CXX_FLAGS_PROFILE="-O3 -DNDEBUG" \
      -DMPI_CXX_COMPILER=mpicxx \
      -DMPI_CXX_COMPILE_FLAGS="-O3" \
      -DMPI_C_COMPILER=mpicc \
      -DMPI_C_COMPILE_FLAGS="-O3" \
      -DCUDA_ARCH="35 37" \
      -DCUDA_HOST_COMPILER=/opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpicc && \
    make -j"$(nproc)" all && \
    make install && \
    rm -f /tmp/${TARBALL} /opt/amgx/srcTarball.txt && \
    ldconfig ${SRCDIR}/lib

# Build PetIBM-0.4.
RUN . /opt/intel/bin/compilervars.sh -arch intel64 -platform linux && \
    . /opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh && \
    VERSION=0.4 && \
    TARBALL=v${VERSION}.tar.gz && \
    wget https://github.com/barbagroup/PetIBM/archive/${TARBALL} -P /tmp && \
    SRCDIR=/opt/petibm/${VERSION} && \
    BUILDDIR=${SRCDIR}/build && \
    mkdir -p ${SRCDIR} ${BUILDDIR} && \
    tar -xzf /tmp/${TARBALL} -C ${SRCDIR} --strip-components=1 && \
    cd ${BUILDDIR} && \
    ${SRCDIR}/configure --prefix=/usr/local \
      CXX=mpicxx \
      CXXFLAGS="-O3 -w -std=c++14" \
      --enable-static=no \
      --with-petsc-dir=/opt/petsc/3.10.2 \
      --with-petsc-arch=linux-gnu-intel-opt \
      --with-cuda-dir=/usr/local/cuda-8.0 \
      --with-amgx-dir=/usr/local \
      --enable-amgxwrapper \
      --enable-yamlcpp \
      --enable-gtest && \
    make -j"$(nproc)" all && \
    make check && \
    make install && \
    ldconfig /usr/local/lib && \
    rm -f /tmp/${TARBALL}

# Remove Intel components (runtime will be mounted from the host).
RUN rm -rf /opt/intel

# Set sshd command.
EXPOSE 23
CMD ["/usr/sbin/sshd", "-D", "-p", "23"]
