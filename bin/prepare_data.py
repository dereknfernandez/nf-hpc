#!/usr/bin/env python3

import os
import pandas as pd
from sklearn.model_selection import train_test_split

def prepare_data(input_file, train_file, val_file, test_file):
    # df = pd.read_csv(input_file)
    # train_val, test = train_test_split(df, test_size=0.2, random_state=42)
    # train, val = train_test_split(train_val, test_size=0.2, random_state=42)
    
    # _cwd = os.getcwd()
    # newdir = os.path.join(_cwd, r'data')
    # if not os.path.exists(newdir):
    #    os.makedirs(newdir)

    # train.to_csv(train_file, index=False)
    # val.to_csv(val_file, index=False)
    # test.to_csv(test_file, index=False)
    print('Hello, world!')
    print(input_file)
    print(train_file)
    print(val_file)
    print(test_file)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Input CSV file')
    parser.add_argument('--train', required=True, help='Output train CSV file')
    parser.add_argument('--val', required=True, help='Output validation CSV file')
    parser.add_argument('--test', required=True, help='Output test CSV file')
    args = parser.parse_args()
    prepare_data(args.input, args.train, args.val, args.test)
