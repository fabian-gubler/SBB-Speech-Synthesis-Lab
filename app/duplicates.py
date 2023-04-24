#!/usr/bin/env python3

# This script checks for duplicates in the combinations.csv file.

import pandas as pd

file_path = 'combinations.csv'
df = pd.read_csv(file_path)

duplicates = df[df.duplicated()]

if duplicates.empty:
    print("No duplicates found.")
else:
    print("Duplicates found:")
    print(duplicates)


print(len(duplicates))
