import pandas as pd
from csv_trimming import CSVTrimmer


def simple_correlation_callback(
    current_row: pd.Series,
    next_row: pd.Series
) -> tuple[bool, pd.Series]:
    """Return the correlation between two rows.
    
    Parameters
    ----------
    current_row : pd.Series
        The current row being analyzed in the DataFrame.
    next_row : pd.Series
        The next row in the DataFrame.

    Returns
    -------
    Tuple[bool, pd.Series]
        A tuple with a boolean indicating if the rows are correlated
        and a Series with the merged row.
    """

    # All of the rows that have a subsequent correlated row are
    # non-empty, and the subsequent correlated rows are always
    # with the first cell empty.
    if pd.isna(next_row.iloc[0]) and all(pd.notna(current_row)):
        return True, pd.concat(
            [
                current_row,
                pd.Series({"surname": next_row.iloc[-1]}),
            ]
        )

    return False, current_row

def clean_up_and_trim(df):


    trimmer = CSVTrimmer()

    trimmed = trimmer.trim(df, drop_padding = True)
    
    removed_dupe_schema = trimmer.trim(trimmed,drop_duplicated_schema = True)
    correlation_call = CSVTrimmer()

    return correlation_call.trim(removed_dupe_schema)









 



