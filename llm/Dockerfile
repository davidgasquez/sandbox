FROM rocm/dev-ubuntu-22.04:6.0.2-complete

# Environment variables
ENV GPU_TARGETS=gfx1100
ENV LLAMA_HIPBLAS=1
ENV CC=/opt/rocm/llvm/bin/clang
ENV CXX=/opt/rocm/llvm/bin/clang++

# Install pytorch and llama-cpp-python
RUN pip3 install --pre torch --index-url https://download.pytorch.org/whl/nightly/rocm5.7
RUN CMAKE_ARGS="-DLLAMA_HIPBLAS=1 -DAMDGPU_TARGETS=gfx1100" pip3 install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
