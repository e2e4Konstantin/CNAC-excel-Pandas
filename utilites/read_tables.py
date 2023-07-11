from .quote_definition import Header, HeaderOption, tables, TableItem
from .settings import SourceData, TABLES_NUMBER_PATTERN, DEBUG_ON
import pprint
import os
import csv
from dataclasses import fields


def read_tables(data: SourceData):
    # списки атрибутов и параметров
    attributes_title: list[Header] = []
    options_title: list[HeaderOption] = []

    def check_cell(column_name: str, src_value: str, sign_strong: bool = False):
        if sign_strong:
            return data.test_points[column_name][0].fullmatch(src_value)
        return data.test_points[column_name][0].match(src_value)

    def check_by_list(row, columns_list):
        sign_luck = set()
        for column_name in columns_list:
            column_number = data.get_column_number(column_name)
            # value_i = x.df.iat[row, column_number]
            value_i = data.get_cell_str_value(row, column_number)
            match_result = check_cell(column_name, value_i, data.test_points[column_name][1])
            sign_luck.add(True) if match_result else sign_luck.add(False)
            # print(' ', row + 1, column_number + 1, f"'{column_name}' {match_result}, '{value_i}'", sign_luck, end='')
        if len(sign_luck) > 0:
            return not (False in sign_luck)
        return False

    def attributes_get_old(row):
        """ Читает названия атрибутов начиная с колонки 'О' до тех пор пока сверху пусто"""
        attributes_title.clear()
        column_a = data.get_column_number("O")
        attribute_name = data.get_cell_str_value(row, column_a)
        up_is_empty = True
        while attribute_name and up_is_empty and column_a < data.column_max:
            attributes_title.append(Header(name_header=attribute_name, column_header=column_a))
            column_a += 1
            attribute_name = data.get_cell_str_value(row, column_a)
            up_is_empty = not bool(data.get_cell_str_value(row - 1, column_a))

    def attributes_get(row) -> int:
        """ Читает названия атрибутов начиная с колонки 'О' до тех пор пока сверху пусто"""
        attributes_title.clear()
        column_a = data.get_column_number("O")
        result = column_a
        for column_i in range(column_a, data.column_max + 1):
            result = column_i
            attribute_name = data.get_cell_str_value(row, column_i)
            if column_i > column_a and bool(data.get_cell_str_value(row - 1, column_i)):
                break
            if attribute_name:
                attributes_title.append(Header(name_header=attribute_name, column_header=column_i))
        return result

    def skip_empty_cells(row, columns) -> int:
        """ Пропускает пустые ячейки в текущей строке начиная с колонки columns """
        for columns_i in range(columns, data.column_max + 1):
            cell_value = data.get_cell_str_value(row, columns_i)
            if cell_value:
                return columns_i
        return data.column_max + 1
        # if columns <= data.column_max:
        #     cell_value = data.get_cell_str_value(row, columns)
        #     while (not cell_value) and (columns < data.column_max):
        #         columns += 1
        #         cell_value = data.get_cell_str_value(row, columns)
        # print(f"\t skip_empty_cells: {row}, {columns}, -> '{cell_value}' ")
        # return columns

    def read_options(row, column) -> int:
        option_name = data.get_cell_str_value(row - 1, column)
        if option_name:
            result = column
            option = HeaderOption(column_header_option=column, name_header_option=option_name)
            for ci in range(column, data.column_max + 1):
                result = ci
                if ci > column and bool(data.get_cell_str_value(row - 1, ci)):
                    break
                option_header = data.get_cell_str_value(row, ci)
                if option_header:
                    option.option_headers.append(Header(name_header=option_header, column_header=ci))
            options_title.append(option)
            return result
        else:
            return data.column_max

    def options_get(row, start_columns):
        """ """
        options_title.clear()
        column_i = skip_empty_cells(row, start_columns)
        while column_i < data.column_max:
            column_i = read_options(row, column_i)
            # column_i += 1
            # column_i = skip_empty_cells(row, column_i)+1

    def pop_in_table_data(row):
        cod_table = data.get_cell_str_value(row, data.get_column_number("F"))
        full_name = data.get_cell_str_value(row, data.get_column_number("H"))
        result = TABLES_NUMBER_PATTERN.search(full_name)
        number_table = full_name[result.span()[0]:result.span()[1]]
        name_table = full_name[result.span()[1]:].strip().capitalize()
        # читаем дерево каталога
        catalog = []
        for column_i in range(data.get_column_number("B"), data.get_column_number("F")):
            catalog.append(data.get_cell_str_value(row, column_i))
        # читаем заголовки атрибутов
        column_options_start = attributes_get(row)
        # читаем заголовки параметров
        # column_options_start = attributes_title[-1:][0].column_header + 1  # номер колонки последнего атрибута +1
        options_get(row, column_options_start)

        tmp_tables = TableItem(cod_table=cod_table, number_table=number_table, name_table=name_table, row_table=row)
        tmp_tables.catalog_table.extend(catalog)
        tmp_tables.attribute_table.extend(attributes_title)
        tmp_tables.options_table.extend(options_title)

        tables[cod_table] = tmp_tables

        if DEBUG_ON:
            print(
                f"#{len(tables):4} row:{row:4}, {number_table:8}, атрибутов: {len(attributes_title)}, параметров: {len(options_title)}, {name_table} "
                f"{cod_table:12} {catalog}\t{attributes_title}\t{options_title=}"
            )
            # print(tables[cod_table], '\n')

    # --------------------------------------------------------------------------------------

    right_format_tables = []
    broken_format_tables = []
    for row_i in range(1, data.row_max):
        base_test = check_by_list(row_i, ['B', 'C', 'D', 'E', 'F', 'G', 'H'])
        if base_test:
            value = data.get_cell_str_value(row_i, data.get_column_number("H"))
            advanced_test = check_by_list(row_i - 1, ['L', 'O'])
            if advanced_test:
                right_format_tables.append((row_i, value[:50]))
                # print(f"таблица {value[:30]}...")
                pop_in_table_data(row_i)
            else:
                broken_format_tables.append((row_i, value))
    print(f"Прочитано таблиц: {len(right_format_tables) + len(broken_format_tables)}")
    print(f"\tправильных: {len(right_format_tables)}")
    print(f"\tкривых: {len(broken_format_tables)}")

    if len(broken_format_tables) > 0:
        fp = r".\output\broken_tables.txt"
        with open(fp, 'w', encoding='utf-8') as file_out:
            for i in range(len(broken_format_tables)):
                file_out.write(f"{i + 1:<5}: {broken_format_tables[i]}\n")

        fp = r".\output\broken_tables.csv"
        with open(fp, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            [writer.writerow(t) for t in broken_format_tables]



