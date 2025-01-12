import random

def move_random_entries(big_file, small_file, num_entries, new_big_file, new_small_file):
    # Read all entries from the big file
    with open(big_file, 'r') as big_infile:
        big_entries = big_infile.readlines()
    
    # Check if we can extract the required number of entries
    if len(big_entries) < num_entries:
        raise ValueError("The big file does not contain enough entries to extract.")

    # Randomly select `num_entries` from the big file
    selected_indices = set(random.sample(range(len(big_entries)), num_entries))
    selected_entries = [big_entries[i] for i in selected_indices]
    remaining_entries = [big_entries[i] for i in range(len(big_entries)) if i not in selected_indices]

    # Append selected entries to the small file
    with open(small_file, 'r') as small_infile:
        small_entries = small_infile.readlines()
    
    updated_small_entries = small_entries + selected_entries

    # Write back the updated files to new files
    with open(new_big_file, 'w') as big_outfile:
        big_outfile.writelines(remaining_entries)

    with open(new_small_file, 'w') as small_outfile:
        small_outfile.writelines(updated_small_entries)

# Example usage:
move_random_entries('big.jsonl', 'small.jsonl', 14995, 'new_big.jsonl', 'new_small.jsonl')

