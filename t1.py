import pandas as pd
from utilites import SourceData

fp = r"F:\Kazak\Google Диск\1_KK\Job_CNAC\office_targets\tasck_2\sources"
fn = r"template_3_68_v_2.xlsx"

# print("не нулевых значений в столбце G: ", df[df.columns[6]].count())
# print(df.iat[13, 6])
# # print(df.dtypes)


x = SourceData(file_name=fn, file_path=fp, sheet_name='name')
print(x)


def check_cell(column_name: str, src_value: str, sign_strong: bool = False):
    if sign_strong:
        return x.test_points[column_name][0].fullmatch(src_value)
    return x.test_points[column_name][0].match(src_value)


def check_by_list(row, columns_list):
    sign_luck = set()
    for column_name in columns_list:
        column_number = x.get_column_number(column_name)
        # value_i = x.df.iat[row, column_number]
        value_i = x.get_cell_str_value(row, column_number)
        match_result = check_cell(column_name, value_i, x.test_points[column_name][1])
        sign_luck.add(True) if match_result else sign_luck.add(False)
        # print(' ', row + 1, column_number + 1, f"'{column_name}' {match_result}, '{value_i}'", sign_luck, end='')
    if len(sign_luck) > 0:
        return not (False in sign_luck)
    return False


catalog_check_list = ['B', 'C', 'D', 'E', 'F', 'G', 'H']
tables_count = 0
right_format_tables = []
broken_format_tables = []
for row_i in range(1, x.row_max):
    r1 = check_by_list(row_i, catalog_check_list)
    r3 = check_by_list(row_i - 1, ['L', 'O'])
    # print()
    if r1:
        tables_count += 1
        value = x.df.iat[row_i, x.get_column_number("H")]
        # print(f"{value} аргументы: {r3}")
        if r3:
            right_format_tables.append((row_i, value[:50]))
        else:
            broken_format_tables.append((row_i, value[:50]))

print(len(right_format_tables), right_format_tables[0], right_format_tables[len(right_format_tables) - 1])

sm = f"{broken_format_tables[0] if len(broken_format_tables) > 0 else '0'}"
sm1 = f"{broken_format_tables[len(broken_format_tables) - 1] if len(broken_format_tables) > 0 else '0'}"
print(len(broken_format_tables), sm, sm1)


