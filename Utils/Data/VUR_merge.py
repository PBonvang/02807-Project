import pandas as pd
import sys, os, glob


if __name__ == "__main__":
    """
    Args:
        VUR_DIR (str): Directory of VUR files e.g "/home/downloads". Defaults to current directory
    """
    if sys.argv[1]:
        VUR_DIR = str(sys.argv[1])
    else:
        VUR_DIR = "."

    subset = ['id']

    joined_files = os.path.join(VUR_DIR, "VUR_*.csv") 
    joined_list = glob.glob(joined_files)
    df = pd.concat(map(lambda file: pd.read_csv(file, sep=';'), joined_list), ignore_index=True)
    print(df.head())
    before = len(df)
    mask = df.duplicated(subset=subset)

    print(f"Before removing duplicates we have {before} rows")

    df.drop_duplicates(subset=subset, inplace=True, ignore_index=True)
    df.to_csv(os.path.join(VUR_DIR, "VUR_joined_with_nulls.csv"), index=False, sep=';')

    print(f"After removing duplicates we have {len(df)} rows")
    print(f"Removed {before - len(df)} rows in total") 
    df.loc[mask].to_csv(os.path.join(VUR_DIR, "VUR_joined_duplicates.csv"), index=False, sep=';')

    df_no_nulls = df.dropna(how='any')
    df_no_nulls.to_csv(os.path.join(VUR_DIR, "VUR_joined.csv"), index=False, sep=';')
    print("Dropped nulls df:", len(df_no_nulls))