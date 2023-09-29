import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(torch.cuda.current_device()))

tensor = torch.randn(2, 2)
res = tensor.to(0)
