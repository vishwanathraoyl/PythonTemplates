import os
import pandas as pd
import numpy as np
from datetime import datetime

t_year = datetime.now().strftime('%Y')
t_month = datetime.now().strftime('%m')
t_date = datetime.now().strftime('%d')

source = os.listdir('Path')
dest = 'Path'

def readdfexcel(filename):
    filepath = 'Path'
    data = pd.read_excel(filepath + filename)
    df = pd.DataFrame(data)
    return df

files_xlsx = [f for f in source if f[-4:] == 'xlsx']

for i in files_xlsx:
    test_file = readdfexcel(i)
    row = int(test_file[test_file['Unnamed: 0'] == 'Store Nbr'].index[0])
    blank_file = pd.DataFrame(np.nan, index = np.arange(17), columns = ['A'])
    new_file = pd.DataFrame(test_file.values[row:])
    full_output = [blank_file, new_file]
    new_file = pd.concat(full_output)
    new_file = new_file.drop(new_file.columns[0], axis = 1)

    l_value = new_file.iat[17,35]
    l_year = l_value[0:4]
    l_month = l_value[5:7]
    l_date = l_value[8:10]

    print(new_file)

    writer = pd.ExcelWriter('Path//Name_' + t_year + t_month + t_date + '_' + l_year + l_month + l_date + '.xlsx', engine = 'xlsxwriter')
    new_file.to_excel(writer, 'Output', index = False)
    writer.save()