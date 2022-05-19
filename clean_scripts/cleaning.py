import sys
import re


def search_replace_column_name(fix_df, col, ref_df, arg):
    """Rename dataframe's column by finding a column in another dataframe that matches a regex.

    :param fix_df: Pandas dataframe with the column to replace
    :param col: The column name string to replace
    :param ref_df: The Pandas reference dataframe to search for a matching replacement column name
    :param arg: Regex string to find matching column name in reference dataframe
    """
    ref_cols = [c for c in ref_df.columns if re.match('^' + arg, c)]
    if len(ref_cols) == 0:
        print("**** Zero column matches on replace", arg, len(ref_cols), ref_cols[:2])
        sys.exit(1)
    elif len(ref_cols) > 1:
        print("**** Multiple column matches on replace", arg, len(ref_cols), ref_cols[:2])
        sys.exit(1)
    print("Replacing", col, "with", ref_cols[0] + '...')
    fix_df.columns = [ref_cols[0] if c.startswith(col + '.') else c for c in fix_df.columns]


def rename_column_name(fix_df, col, arg):
    col_to_rename = [c for c in fix_df.columns if c.startswith(col + '.')]
    if len(col_to_rename) == 0:
        print("**** Couldn't find column to rename", col)
        sys.exit(1)
    print("Renaming", col, "with", arg + '...')
    fix_df.rename(columns={col_to_rename[0]: arg}, inplace=True)


def delete_column(fix_df, col):
    col_to_delete = [c for c in fix_df.columns if c.startswith(col + '.')]
    if len(col_to_delete) == 1:
        print("Deleting", col)
        fix_df.drop(columns=[col_to_delete[0]], inplace=True)
    else:
        print("**** Incorrect column matching:", col, col_to_delete)
        sys.exit()


def apply_actions(fix_df, ref_df, actions_df):
    for _, row in actions_df.iterrows():
        column = row.loc['QID_2022']
        action = row.loc['Action']
        argument = row.loc['Argument']

        if action == 'SearchReplace':
            search_replace_column_name(fix_df, column, ref_df, argument)
        elif action == 'Rename':
            rename_column_name(fix_df, column, argument)
        elif action == 'Delete':
            delete_column(fix_df, column)
        elif action == 'Ignore':
            pass
