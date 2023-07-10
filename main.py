from utilites import SourceData, tables, read_tables
from utilites import read_tables, read_quotes
import pprint
import os

fp = r"F:\Kazak\Google Диск\1_KK\Job_CNAC\office_targets\tasck_2\sources"
# fn = r"template_3_68.xlsx"
# fn = r"template_4_68.xlsx"
fn = r"template_5_67.xlsx"

data = SourceData(file_name=fn, file_path=fp, sheet_name='name')
print(data, "\n")
print(f"кодов расценок в столбце G: {data.df[data.df.columns[6]].count()}", "\n")

read_tables(data)
read_quotes(data)



# q = read_quote(data, 16)
# pprint.pprint(q, width=200)
# # print()
# pprint.pprint(tables, width=200)
# v = data.df.iat[0, data.column_max]
# v2 = data.df.iat[data.row_max, 0]
# print(v,v2, data.df.shape)

