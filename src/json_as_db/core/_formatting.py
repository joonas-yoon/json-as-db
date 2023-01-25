from typing import List, Tuple


def split_first_last(l: list, k: int) -> Tuple[list, list]:
    _len = len(l)
    if _len <= 1:
        return l, []
    is_odd = k % 2
    k = min(k // 2, _len // 2)
    return l[:(k+int(is_odd))], l[-k:]


def to_plural(unit_str: str, k: int) -> str:
    return unit_str + ('' if k < 2 else 's')


def collapsed_row(l: list, is_skip: bool) -> list:
    _first, _last = split_first_last(l, len(l))
    return _first + (['...'] if is_skip else []) + _last


def collapse_str(s: str, width: int) -> str:
    if len(s) <= width:
        return s
    return s[:min(len(s), width - 3)] + '...'


def row_str(l: list, delimiter: str = '') -> str:
    return f" {delimiter} ".join(l) + "\n"


def row_padded(row: list, widths: list) -> List[str]:
    return [row[i].ljust(widths[i]) for i in range(len(row))]


def stringify(all_items: List[dict]) -> str:
    """Return 3 each rows from the top and the bottom.

    Returns:
        str: The first and last 3 rows of the caller object.

    Example:
        >>> db
        age  grouped  ...  job                name
        32   True     ...  Camera operator    Layne
        17   False    ...  Flying instructor  Somerled
        9    True     ...  Inventor           Joon-Ho
        ...  ...      ...  ...                ...
        23   None     ...  Publican           Melanie
        54   True     ...  Racing driver      Eike
        41   None     ...  Barrister          Tanja


        [100 items, 9 keys]
    """
    # Collect key names to be column
    keys = set()
    for item in all_items:
        keys |= set(item.keys())
    total_rows = len(all_items)
    total_cols = len(keys)

    # Display options
    keys = sorted(list(keys))
    rows_display = 6
    cols_display = 4
    text_max_width = 12

    # Collect rows by columns and collapse them
    first_cols, last_cols = split_first_last(keys, cols_display)
    first_rows, last_rows = split_first_last(all_items, rows_display)
    rows = first_rows + last_rows
    cols = first_cols + last_cols
    col_widths = [max(3, len(str(col))) for col in cols]
    table = []
    for irow, row in enumerate(rows):
        t_row = []
        for icol, col in enumerate(cols):
            try:
                stringified = str(row[col])
            except KeyError:
                stringified = str(None)
            text = collapse_str(stringified, width=text_max_width)
            col_widths[icol] = max(col_widths[icol], len(text))
            t_row.append(text)
        table.append(t_row)

    # Shortcut functions
    def _clp_row(l): return collapsed_row(l, is_skip=total_cols > cols_display)
    def _make_row_str(l): return row_str(_clp_row(l), delimiter='')
    def _padded(l): return row_padded(l, widths=col_widths)

    # Create result strings
    result = _make_row_str(_padded(first_cols + last_cols))
    for irow, row in enumerate(table):
        s = _padded(row)
        result += _make_row_str(s)
        if total_rows > rows_display and irow + 1 == len(first_rows):
            result += _make_row_str(_padded(['...'] * (len(cols))))

    result += "\n\n" + ", ".join([
        f"[{total_rows} {to_plural('item', total_rows)}",
        f"{total_cols} {to_plural('key', total_cols)}]",
    ])

    return result
