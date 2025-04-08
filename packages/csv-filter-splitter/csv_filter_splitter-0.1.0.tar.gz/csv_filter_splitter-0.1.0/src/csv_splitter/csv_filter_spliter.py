import re

import pandas as pd
import sys
import os
import shutil



def readDataframe(file):
    print('Reading file...')
    df = pd.read_csv(file, dtype=str)
    print()

    return df


def selectFilter(df):
    column_dict = {}
    column_names = list(df.columns)
    print(column_names)
    for i, column in enumerate(column_names, start=1):
        column_dict.update({i: column})
        print(f' [{i}] {column}')
    #selection = int(input("Column index to use as filter: \n"))
    #filter_ = column_dict[selection]

    #return filter_
    return column_dict


def splitByFilter(df, filter_, dir_path):

    unique_values = df[filter_].nunique()
    #option = input(f'{unique_values} files will be generated. Continue? (y/n) \n')
    filter_name_formatted = re.sub('[^a-zA-Z0-9 \n.]', '', filter_)
    outdir = f'{dir_path}/{filter_name_formatted}'

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    #if option == "y" or option == "Y":

    for i, g in df.groupby(filter_):
        i_formatted = re.sub('[^a-zA-Z0-9 \n.]', '', str(i))
        g.to_csv(f'{outdir}/' + '{}.csv'.format(i_formatted), header=True, index_label=False)
        sys.stdout.write('\r' + f'Saving {i}.csv' + ' ')
        sys.stdout.flush()

    print('Done!')

    #shutil.make_archive(outdir, 'zip', dir_path, filter_name_formatted)
    #print('File ready for download!')
    return filter_name_formatted

    #elif option == "n" or option == "N":

     #   print('Exiting...')
      #  exit()
    #else:

     #   print('invalid option. Exiting...')
      #  exit()







