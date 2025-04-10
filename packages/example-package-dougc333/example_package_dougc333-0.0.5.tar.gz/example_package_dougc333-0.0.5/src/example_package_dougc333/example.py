
import torch


def add_one(number):
	return number + 1


def device():
	device = torch.device('cpu')
	if torch.cuda.is_available():
		device = torch.device('cuda')
		gpu_stats = torch.cuda.get_device_properties(0)
		start_gpu_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)
		max_memory = round(gpu_stats.total_memory / 1024 / 1024 / 1024, 3)
		print(f"GPU = {gpu_stats.name}. Max memory = {max_memory} GB.")
		print(f"{start_gpu_memory} GB of memory reserved.")
	torch.set_default_device(device)
	print(f"Using device = {torch.get_default_device()}")



def gpu_memory():
	gpu_stats = torch.cuda.get_device_properties(0)
	start_gpu_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)
	max_memory = round(gpu_stats.total_memory / 1024 / 1024 / 1024, 3)
	print(f"GPU = {gpu_stats.name}. Max memory = {max_memory} GB.")
	print(f"{start_gpu_memory} GB of memory reserved.")
