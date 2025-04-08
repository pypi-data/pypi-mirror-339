import psutil
import sys
import gc

def dedupe_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    unique_lines = sorted(set(line.strip() for line in lines if line.strip()))

    with open(file, 'w') as f:
        for line in unique_lines:
            f.write(f"{line}\n")

def count_lines(filepath):
    with open(filepath, 'r') as f:
        return sum(1 for _ in f)

def append_file(source, target):
    with open(source, 'r') as src, open(target, 'a') as tgt:
        for line in src:
            tgt.write(line)

def memory_load_test(args) -> int:
    """Perform load test on memory to find out how much can be stored in buffer"""
    # first get the available RAM of the system
    available_bytes = psutil.virtual_memory().available
    target_memory = int(available_bytes * 0.8)
    available_gb = available_bytes / (1024 ** 3)
    target_gb = target_memory / (1024 ** 3)
    
    print(f'[i] Available Memory   : {round(available_gb, 2)} GB')
    print(f'[i] Expected Usage     : {round(target_gb, 2)} GB')

    # create sample array, and get the array size
    sample_array = []
    sample_text = f'mylongsamplesubdomainname.{args.domain}'
    process = psutil.Process()
    used_memory = 0
    while True:
        sample_array.append(sample_text)
        used_memory = process.memory_info().rss
        if used_memory >= target_memory:
            max_arr_length = len(sample_array)
            break
        if len(sample_array) == 10000:
            # get the size of array
            arr_size = sys.getsizeof(sample_array) + sum(sys.getsizeof(i) for i in sample_array)
            # calculate array length
            max_arr_length = int((target_memory / arr_size)*10000)
            break
    del sample_array
    gc.collect()
    return max_arr_length