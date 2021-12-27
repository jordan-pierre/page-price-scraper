import glob
import os
import pandas as pd

def merge_sheets(input_path, output_file):
    all_files = glob.glob(os.path.join(input_path, "*.csv"))
    df_from_each_file = (pd.read_csv(f) for f in all_files)

    concatenated_df = pd.concat(df_from_each_file, ignore_index=True)
    concatenated_df = concatenated_df[['page_titles','product_titles','product_ratings','product_prices','avg_product_price','url','scraped_date']].drop_duplicates().sort_values('page_titles') # select only named columns
    concatenated_df.to_csv(output_file, index=False)
    return concatenated_df


def summarize_table(df, output_file):
    df = df.drop(labels='product_ratings', axis=1)
    summary_df = df.groupby(['page_titles', 'url', 'scraped_date']).mean()
    summary_df.sort_values(summary_df.columns[-1], ascending=False).to_csv(output_file)


def main():
    # Combine all files in output directory
    df = merge_sheets('output', 'products.csv')

    # Create summary file
    summarize_table(df, 'summary.csv')


if __name__=='__main__':
    main()