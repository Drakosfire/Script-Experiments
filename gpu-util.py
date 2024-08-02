# This is a good idea, it needs a GUI, chatgpt4 recommends Tkagg, worth looking into
import GPUtil
import time
# Uncomment the following lines if you want to plot the data
import matplotlib.pyplot as plt

def get_gpu_memory_usage():
    gpus = GPUtil.getGPUs()
    return [gpu.memoryUsed for gpu in gpus]

# Uncomment these lines to initialize matplotlib for live plotting
plt.ion()
fig, ax = plt.subplots()
memory_usage_data = []

while True:
    memory_usage = get_gpu_memory_usage()
    print(f"GPU Memory Usage: {memory_usage} MB")

    # Uncomment these lines to update the plot with new data
    memory_usage_data.append(memory_usage)
    ax.clear()
    ax.plot(memory_usage_data)
    plt.pause(0.1)

    time.sleep(1)  # Update every 1 second, change as needed
