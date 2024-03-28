import json
with open("names.json", "r") as file:
    random_sample = file.read().splitlines()


random_sample = random_sample[:5000]

chunk_size = 1000
total_chunks = len(random_sample) // chunk_size + 1

for i in range(total_chunks):
    start = i * chunk_size
    end = (i + 1) * chunk_size
    chunk = random_sample[start:end]

    with open(f"chunk_{i+1}.json", "w") as file:
        # file.write("\n")
        file.write("\n".join(chunk))
        file.write("]")
        
        
    with open(f"chunk_{i+1}.json", "r+") as file:
        if i != 0:
            file.write("[")
        file.seek(0, 2)  # Move the cursor to the end of the file
        pos = file.tell() - 2  # Get the position of the second last character
        file.seek(pos)
        file.truncate()  # Remove the comma
        file.write("]")  # Add the closing bracket