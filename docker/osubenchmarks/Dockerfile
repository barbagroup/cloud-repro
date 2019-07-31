# Dockerfile to run OSU micro-benchmarks (5.6)
# with Batch Shipyard on Azure Batch.

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

# Install the OSU MPI benchmarks.
RUN . /opt/intel/bin/compilervars.sh -arch intel64 -platform linux && \
    . /opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh && \
    VERSION=5.6 && \
    TARBALL=osu-micro-benchmarks-${VERSION}.tar.gz && \
    URL=http://mvapich.cse.ohio-state.edu/download/mvapich/${TARBALL} && \
    wget ${URL} -P /tmp && \
    SRCDIR=/opt/osu-micro-benchmarks/${VERSION} && \
    mkdir -p ${SRCDIR} && \
    tar -xzf /tmp/${TARBALL} -C ${SRCDIR} --strip-components=1 && \
    cd ${SRCDIR} && \
    ./configure --prefix=/usr/local \
        CC=mpicc \
        CXX=mpicxx \
        --enable-cuda \
        --with-cuda=/usr/local/cuda-8.0 && \
    make -j"$(nproc)" install && \
    ldconfig /usr/local/lib && \
    rm -f /tmp/${TARBALL}

# Remove Intel components (runtime will be mounted from the host).
RUN rm -rf /opt/intel

# Set sshd command.
EXPOSE 23
CMD ["/usr/sbin/sshd", "-D", "-p", "23"]
