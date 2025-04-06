def taste(filename, kind) -> list:
    '''

    Args:
        filename: The file to taste
        kind: The kind of file to be tasted (.csv, .xlsx, etc.)

    Returns:
        A list that is the first line of the file (the header) or an empty list

    Raises:
        Error if file is not found
        Error if kind is not known by the function

    '''
    import pandas as pd
    got_one = 0
    match kind:
        case "xlsx":
            try:
                df = pd.read_excel(filename, nrows=1)
                got_one = 1
            except FileNotFoundError:
                print(f"Error: Excel file '{filename}' not found.")
        case "csv":
            try:
                df = pd.read_csv(filename, nrows=1)
                got_one = 1
            except FileNotFoundError:
                print(f"Error: csv file '{filename}' not found.")
        case "json":
            try:
                df = pd.read_json(filename, nrows=1)
                got_one = 1
            except FileNotFoundError:
                print(f"Error: JSON file '{filename}' not found.")
        case _:
            print(f"Error: Unknown kind of file: '{kind}'.")

    if got_one:
        return list(df.columns)
    else:
        return []

