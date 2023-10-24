# FROM ubuntu:22.04

# ARG ROCM_VERSION=5.7
# ARG AMDGPU_VERSION=5.7

# RUN echo "Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600" > /etc/apt/preferences.d/rocm-pin-600

# RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ca-certificates curl libnuma-dev gnupg \
#     && curl -sL https://repo.radeon.com/rocm/rocm.gpg.key | apt-key add - \
#     && printf "deb [arch=amd64] https://repo.radeon.com/rocm/apt/$ROCM_VERSION/ jammy main" | tee /etc/apt/sources.list.d/rocm.list \
#     && printf "deb [arch=amd64] https://repo.radeon.com/amdgpu/$AMDGPU_VERSION/ubuntu jammy main" | tee /etc/apt/sources.list.d/amdgpu.list

# RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
#     sudo \
#     libelf1 \
#     kmod \
#     file \
#     python3 \
#     python3-pip \
#     python3-venv \
#     ffmpeg \
#     git \
#     rocm-dev \
#     rocm-libs \
#     build-essential && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# RUN groupadd -g 109 render

# ARG USERNAME=rocmer
# ARG USER_UID=1000
# ARG USER_GID=$USER_UID

# RUN groupadd --gid $USER_GID $USERNAME \
#     && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME  -G "video" \
#     && apt-get update \
#     && apt-get install -y sudo \
#     && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
#     && chmod 0440 /etc/sudoers.d/$USERNAME

# RUN pip3 install --pre torch --index-url https://download.pytorch.org/whl/nightly/rocm5.7
# RUN pip3 install numpy
# ENV HIP_VISIBLE_DEVICES=1
# ENV LLAMA_HIPBLAS=1
# ENV CC=/opt/rocm/llvm/bin/clang
# ENV CXX=/opt/rocm/llvm/bin/clang++
# RUN CMAKE_ARGS="-DLLAMA_HIPBLAS=1" pip3 install llama-cpp-python --force-reinstall --upgrade --no-cache-dir

# USER $USERNAME
# ENV PATH /home/$USERNAME/.local/bin:$PATH
# WORKDIR /home/$USERNAME

# FROM ghcr.io/ggerganov/llama.cpp:full-rocm
FROM rocm/dev-ubuntu-22.04:5.7-complete
ENV HIP_VISIBLE_DEVICES=1
# ENV GPU_TARGETS=???
ENV LLAMA_HIPBLAS=1
ENV CC=/opt/rocm/llvm/bin/clang
ENV CXX=/opt/rocm/llvm/bin/clang++
RUN pip3 install --pre torch --index-url https://download.pytorch.org/whl/nightly/rocm5.7
# RUN CMAKE_ARGS="-DLLAMA_HIPBLAS=1" pip3 install llama-cpp-python --force-reinstall --upgrade --no-cache-dir

# TODO: Use the AMD rocm ubuntu image

# USER $USERNAME
# ENV PATH /home/$USERNAME/.local/bin:$PATH
# WORKDIR /home/$USERNAME
