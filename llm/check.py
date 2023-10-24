import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(torch.cuda.current_device()))

print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
print(f"CUDA arch list: {torch.cuda.get_arch_list()}")
print(f"CUDNN available: {torch.backends.cudnn.is_available()}")
print(f"CUDNN version: {torch.backends.cudnn.version()}")

tensor = torch.randn(2, 2)
res = tensor.to(0)
