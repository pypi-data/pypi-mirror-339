
import torch
import os

def add_one(number):
	return number + 1

def fix():
	os.system('apt-get update && apt-get upgrade')
	os.system('apt-get install wget')
	os.system('!wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
')
	os.system('dpkg -i cuda-keyring_1.1-1_all.deb')
	os.system('apt-get update')
	os.system('apt-get -y install cuda-toolkit-12-4')



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
