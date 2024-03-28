with open("names.json", "r") as file:
    npm_package_names = file.read().splitlines()

import random

# Assuming you have already read the file into npm_package_names
total_count = len(npm_package_names)
sample_count = total_count // 100  # 1% of the total

# Randomly select 1% of the total lines
random_sample = random.sample(npm_package_names, sample_count)

# Now random_sample contains 1% of the total lines
# print(random_sample)
import json

# Assuming random_sample contains the randomly selected lines
with open("random_names.json", "w") as file:
    # json.dump(random_sample, file)
    file.write("\n".join(random_sample))





