
def check_by_list(data, row, columns_list, item_name: str):
    """ Проверить строку по списку правил """
    def check_cell(column_letter: str, src_value: str, item_type: str):
        template = data.test_templates[item_type][column_letter]    # tuple (re.compile(r"^\s*$"), STRONG_MATCH)
        if template[1]:
            return template[0].fullmatch(src_value)
        return template[0].match(src_value)

    sign_luck = set()
    for column_name in columns_list:
        column_number = data.get_column_number(column_name)
        value_i = data.get_cell_str_value(row, column_number)
        match_result = check_cell(column_name, value_i, item_name)
        sign_luck.add(True) if match_result else sign_luck.add(False)
    if len(sign_luck) > 0:
        return not (False in sign_luck)
    return False
