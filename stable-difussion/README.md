# Stable Difussion

This is how I'm running Stable Difussion locally, on AMD hardware. Started following the [Install and Run on AMD GPUs](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Install-and-Run-on-AMD-GPUs) guide but found some issues so decided to build things from scratch, relying on Docker and Ubuntu.

To get started, run:

```bash
make build && make dev
```

Then, once inside the container, you should be able to run:

```bash
./run.sh
```

I also found very useful to run this snipped form time to time to check if the GPU is available to PyTorch:

```bash
python3 -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

If you're looking to monitor the GPU usage and related metrics while generating images, you can run `nvtop`!
