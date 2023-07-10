from .quote_definition import tables, quotes, Attribute, Quote, Option, heap
from .settings import SourceData, DEBUG_ON
from .verifications import check_by_list


def get_quote(data: SourceData, row) -> Quote:
    stat_val = data.get_cell_str_value(row, data.get_column_number("J"))
    unit_quote = Quote(
        row_quote=row,
        table_quote=data.get_cell_str_value(row, data.get_column_number("F")),
        cod_quote=data.get_cell_str_value(row, data.get_column_number("G")),
        name_quote=data.get_cell_str_value(row, data.get_column_number("H")).capitalize(),
        sizer_quote=data.get_cell_str_value(row, data.get_column_number("I")),
        statistics_quote=int(stat_val) if stat_val.isdigit() else 0,
        parameterized_quote=bool(data.get_cell_str_value(row, data.get_column_number("K"))),
        type_quote=data.get_cell_str_value(row, data.get_column_number("L")),
        parent_quote=data.get_cell_str_value(row, data.get_column_number("M"))
    )

    # получить таблицу в которую входит расценка
    own_table = tables.get(unit_quote.table_quote, None)
    # print(f"{own_table.attribute_table = }")
    if own_table:
        # заполняем атрибуты
        if len(own_table.attribute_table) > 0:
            for attribute_i in own_table.attribute_table:
                value_i = data.get_cell_str_value(row, attribute_i.column_header)
                if value_i:
                    unit_quote.attributes_quote.append(
                        (Attribute(name_attribute=attribute_i.name_header, value_attribute=value_i)))
        # else:
        #     if DEBUG_ON: print(
        #         f"get_quote >> у расценки {unit_quote.cod_quote} не найдено атрибутов! Параметризация: {unit_quote.parameterized_quote}")

        # заполняем параметры
        if len(own_table.options_table) > 0:
            for option_i in own_table.options_table:
                tmp_options = Option()  # создаем новый параметр
                tmp_options.name_option = option_i.name_header_option  # имя параметра
                # получаем значения параметра
                for header_option_i in option_i.option_headers:
                    value = data.get_cell_str_value(row, header_option_i.column_header)
                    tmp_options.value_option.append((header_option_i.name_header, value))
                # добавить параметр если есть хоть один не пустое значение
                if any([x[1] for x in tmp_options.value_option]):
                    unit_quote.options_quote.append(tmp_options)
                # else:
                #     if DEBUG_ON: print(
                #         f"get_quote >> у расценки {unit_quote.cod_quote} нет параметров! Параметризация: {unit_quote.parameterized_quote}")
        else:
            if DEBUG_ON: print(
                f"read_quote>> Расценка: {unit_quote.cod_quote}. Атрибутов: {len(unit_quote.attributes_quote)}. "
                f"Параметров: {len(unit_quote.options_quote)}. Параметризация: {'++' if unit_quote.parameterized_quote else '--'}")
    else:
        if DEBUG_ON: print(
            f"read_quote>> не найдена таблица {unit_quote.table_quote} для расценки {unit_quote.cod_quote}")

    return unit_quote


def read_quotes(data: SourceData):
    quotes_without_table = 0
    all_quotes = 0
    for row_i in range(0, data.row_max+1):
        base_test = check_by_list(data, row_i, ['B', 'C', 'D', 'E', 'F', 'G'], "quote")
        if base_test:
            table_cod = data.get_cell_str_value(row_i, data.get_column_number("F"))
            all_quotes += 1
            own_table = tables.get(table_cod, None)
            if own_table:
                quote_i = get_quote(data, row_i)
                if len(quote_i.attributes_quote) > 0 or len(quote_i.options_quote) > 0:
                    quotes.append(quote_i)
                else:
                    heap.append(quote_i)
                    if DEBUG_ON: print(f"\t\tread_quotes >> Расценку {quote_i.cod_quote} "
                                       f"не запоминаем {len(quote_i.attributes_quote)} {len(quote_i.options_quote)}")
        else:
            quotes_without_table += 1

    print("\n", f"Прочитано расценок: {all_quotes}")
    print(f"\tзаписано: {len(quotes)}")
    print(f"\tпустые атрибуты и параметры: {len(heap)}")
    qtable = len(quotes)+len(heap)
    print(f"\tв таблицах: {qtable}")
    print(f"\tбез таблиц: {all_quotes - qtable}")

    fp = r".\output\fine_quotes.txt"
    with open(fp, 'w', encoding='utf-8') as file_out:
        for i in range(len(quotes)):
            file_out.write(f"{i+1:<5}: {quotes[i].short_str()}\n")

    fp = r".\output\bug_quotes.txt"
    with open(fp, 'w', encoding='utf-8') as file_out:
        for i in range(len(heap)):
            file_out.write(f"{i + 1:<5}: {heap[i].short_str()}\n")

