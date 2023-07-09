from utilites import SourceData, tables, read_tables
from utilites import read_tables

fp = r"F:\Kazak\Google Диск\1_KK\Job_CNAC\office_targets\tasck_2\sources"
fn = r"template_3_68_v_2.xlsx"

data = SourceData(file_name=fn, file_path=fp, sheet_name='name')
print(data)

read_tables(data)

