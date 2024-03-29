output_file = 'o_combined.txt'

with open(output_file, 'w') as out_f:
    for i in range(1, 29):
        input_file = f'o{i}.txt'
        with open(input_file, 'r') as in_f:
            out_f.write(in_f.read())
