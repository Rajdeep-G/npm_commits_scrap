import json


with open("../random_names.json", "r") as file:
    random_sample = file.read().splitlines()


chunk_size = 1000
total_chunks = len(random_sample) // chunk_size + 1

for i in range(total_chunks):
    start = i * chunk_size
    end = (i + 1) * chunk_size
    chunk = random_sample[start:end]

    with open(f"chunk_{i+1}.json", "w") as file:
        # json.dump(chunk, file)
        file.write("\n".join(chunk))
