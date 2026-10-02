BootStrap: docker
From: ubuntu:25.10
%post
    . /.singularity.d/env/10-docker*.sh

%post
    apt-get update -y
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ack \
        autotools-dev \
        build-essential \
        bzip2 \
        ca-certificates \
        catch2 \
        clang-tidy \
        cppcheck \
        doxygen \
        gcc-offload-nvptx \
        gdb \
        git \
        gzip \
        hyperfine \
        less \
        libarmadillo-dev \
        libboost-all-dev \
        libeigen3-dev \
        liblapack64-dev \
        libopenblas-openmp-dev \
        libtbb-dev \
        make \
        neovim \
        ninja-build \
        openssh-client \
        pkg-config \
        python3-pip \
        strace \
        tar \
        tmux \
        valgrind \
        vim \
        wget
    rm -rf /var/lib/apt/lists/*

# CMake version 3.31.6
%post
    apt-get update -y
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        make \
        wget
    rm -rf /var/lib/apt/lists/*
%post
    cd /
    mkdir -p /var/tmp && wget -q -nc --no-check-certificate -P /var/tmp https://github.com/Kitware/CMake/releases/download/v3.31.6/cmake-3.31.6-linux-x86_64.sh
    mkdir -p /usr/
    /bin/sh /var/tmp/cmake-3.31.6-linux-x86_64.sh --prefix=/usr/ --skip-license
    rm -rf /var/tmp/cmake-3.31.6-linux-x86_64.sh
%environment
    export PATH=/usr/bin:$PATH
%post
    export PATH=/usr/bin:$PATH

# GNU compiler
%post
    apt-get update -y
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        g++-15 \
        gcc-15 \
        gfortran-15
    rm -rf /var/lib/apt/lists/*
%post
    cd /
    update-alternatives --install /usr/bin/g++ g++ $(which g++-15) 30
    update-alternatives --install /usr/bin/gcc gcc $(which gcc-15) 30
    update-alternatives --install /usr/bin/gcov gcov $(which gcov-15) 30
    update-alternatives --install /usr/bin/gfortran gfortran $(which gfortran-15) 30

# LLVM compiler
%post
    apt-get update -y
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        apt-transport-https \
        ca-certificates \
        gnupg \
        wget
    rm -rf /var/lib/apt/lists/*
%post
    mkdir -p /usr/share/keyrings
    rm -f /usr/share/keyrings/llvm-snapshot.gpg.gpg
    wget -qO - https://apt.llvm.org/llvm-snapshot.gpg.key | gpg --dearmor -o /usr/share/keyrings/llvm-snapshot.gpg.gpg
    echo "deb [signed-by=/usr/share/keyrings/llvm-snapshot.gpg.gpg] http://apt.llvm.org/xenial/ llvm-toolchain-xenial main" >> /etc/apt/sources.list.d/hpccm.list
    echo "deb-src [signed-by=/usr/share/keyrings/llvm-snapshot.gpg.gpg] http://apt.llvm.org/xenial/ llvm-toolchain-xenial main" >> /etc/apt/sources.list.d/hpccm.list
    apt-get update -y
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        clang-18 \
        clang-format-18 \
        clang-tidy-18 \
        clang-tools-18 \
        libc++-18-dev \
        libc++1-18 \
        libc++abi1-18 \
        libclang-18-dev \
        libclang1-18 \
        liblldb-18-dev \
        libomp-18-dev \
        lld-18 \
        lldb-18 \
        llvm-18 \
        llvm-18-dev \
        llvm-18-runtime
    rm -rf /var/lib/apt/lists/*
%post
    cd /
    update-alternatives --install /usr/bin/clang clang $(which clang-18) 30
    update-alternatives --install /usr/bin/clang++ clang++ $(which clang++-18) 30
    update-alternatives --install /usr/bin/clang-format clang-format $(which clang-format-18) 30
    update-alternatives --install /usr/bin/clang-tidy clang-tidy $(which clang-tidy-18) 30
    update-alternatives --install /usr/bin/lldb lldb $(which lldb-18) 30
    update-alternatives --install /usr/bin/llvm-config llvm-config $(which llvm-config-18) 30
    update-alternatives --install /usr/bin/llvm-cov llvm-cov $(which llvm-cov-18) 30

%runscript
    exec /bin/bash "$@"


