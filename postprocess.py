import glob
import os
import pandas as pd

def merge_sheets(input_path, output_file):
    all_files = glob.glob(os.path.join(input_path, "*.csv"))

    df_from_each_file = (pd.read_csv(f) for f in all_files)
    concatenated_df = pd.concat(df_from_each_file, ignore_index=True)

    concatenated_df.to_csv(output_file)
    return concatenated_df


def summarize_table(df, output_file):
    summary_df = df.groupby('page_titles').mean()
    summary_df.to_csv(output_file)


def main():
    # Combine all files in output directory
    df = merge_sheets('output', 'final.csv')

    # Create summary file
    summarize_table(df, 'summary.csv')


if __name__=='__main__':
    main()