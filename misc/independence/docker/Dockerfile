# Dockerfile for PetIBM for use with Batch Shipyard on Azure Batch

FROM nvidia/cuda:8.0-devel-centos7
MAINTAINER Olivier Mesnard <mesnardo@gwu.edu>

# Install base system.
COPY ssh_config /root/.ssh/config
RUN yum update -y && \
    yum install -y openssh-server openssh-clients && \
    yum install -y cpio libmlx4 libmlx5 librdmacm libmthca dapl dapl-utils && \
    yum install -y wget unzip gcc gcc-c++ gcc-gfortran make cmake flex bison && \
    mkdir -p /var/run/sshd && \
    ssh-keygen -A && \
    sed -i 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config && \
    sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/g' /etc/ssh/sshd_config && \
    sed -i 's/#RSAAuthentication yes/RSAAuthentication yes/g' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/g' /etc/ssh/sshd_config && \
    ssh-keygen -f /root/.ssh/id_rsa -t rsa -N '' && \
    chmod 600 /root/.ssh/config && \
    chmod 700 /root/.ssh && \
    cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys

# Install Intel MPI library.
COPY l_mpi_2017.2.174.tgz /tmp/
RUN cd /tmp && \
    tar -xzf l_mpi_2017.2.174.tgz && \
    cd l_mpi_2017.2.174 && \
    sed -i -e 's/^ACCEPT_EULA=decline/ACCEPT_EULA=accept/g' silent.cfg && \
    sed -i -e 's/^ARCH_SELECTED=ALL/ARCH_SELECTED=INTEL64/g' silent.cfg && \
    ./install.sh -s silent.cfg && \
    cd /tmp && \
    rm -rf l_mpi_2017.2.174 l_mpi_2017.2.174.tgz

# Build AmgX-2.0.
COPY amgx-2.0-src.tar /tmp/
RUN source /opt/intel/bin/compilervars.sh -arch intel64 -platform linux && \
    source /opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh && \
    VERSION=2.0 && \
    TARBALL=amgx-2.0-src.tar && \
    SRCDIR=/opt/amgx/${VERSION} && \
    BUILDDIR=${SRCDIR}/build && \
    mkdir -p ${SRCDIR} ${BUILDDIR} && \
    tar -xzf /tmp/${TARBALL} -C ${SRCDIR} && \
    cd ${BUILDDIR} && \
    cmake ${SRCDIR} \
      -DCMAKE_C_COMPILER=mpicc \
      -DCMAKE_CXX_COMPILER=mpicxx \
      -DMPI_C_COMPILER=mpicc \
      -DMPI_CXX_COMPILER=mpicxx \
      -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda-8.0 \
      -DCUDA_ARCH=35 \
      -DCUDA_HOST_COMPILER=/opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpicc && \
    make -j"$(nproc)" all && \
    make install && \
    rm -f /tmp/${TARBALL} /opt/amgx/srcTarball.txt && \
    ldconfig ${SRCDIR}/lib

# Build PETSc-3.7.4 in optimized mode.
RUN source /opt/intel/bin/compilervars.sh -arch intel64 -platform linux && \
    source /opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh && \
    VERSION=3.7.4 && \
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

# Build PetIBM (version 0.2 without check OpenMPI and CUDA versions).
RUN source /opt/intel/bin/compilervars.sh -arch intel64 -platform linux && \
    source /opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh && \
    PETIBM_DIR=/opt/petibm && \
    mkdir -p ${PETIBM_DIR} && \
    ZIP_FILE=0.2-noversionchecks.zip && \
    wget https://github.com/mesnardo/PetIBM/archive/${ZIP_FILE} -P /tmp && \
    cd ${PETIBM_DIR} && \
    unzip /tmp/${ZIP_FILE} -d ${PETIBM_DIR} && \
    cd ${PETIBM_DIR} && \
    mv PetIBM-0.2-noversionchecks 0.2-noversionchecks && \
    cd 0.2-noversionchecks && \
    mkdir build && \
    cd build && \
    ../configure --prefix=/usr/local \
      CXX=mpicxx \
      CXXFLAGS="-O3 -w -std=c++11" \
      --with-petsc-dir=/opt/petsc/3.7.4 \
      --with-petsc-arch=linux-gnu-intel-opt \
      --with-cuda=/usr/local/cuda-8.0 \
      --with-amgx=/opt/amgx/2.0 && \
    make -j"$(nproc)" all && \
    make check && \
    make install && \
    rm -f /tmp/${ZIP_FILE}

# Remove Intel components (runtime will be mounted from the host).
RUN rm -rf /opt/intel

# Set sshd command.
EXPOSE 23
CMD ["/usr/sbin/sshd", "-D", "-p", "23"]
