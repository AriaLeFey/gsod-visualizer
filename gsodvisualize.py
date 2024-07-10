import plotly.express as px
import pandas as pd
from pathlib import Path
import glob
import argparse
from utils import gsod_download

def main(args):
    gsod_download.download()

    dataset_files = glob.glob(str(Path.cwd() / 'gsod_data/2024/*'))

    ds_list = [pd.read_csv(file, index_col=None) for file in dataset_files]
    df = pd.concat(ds_list, axis=0)

    fig = px.scatter_geo(df.loc[df["DATE"] == args.date], lat="LATITUDE", lon="LONGITUDE", color="TEMP", title=f"GSOD data for {args.date}")

    fig.write_image('result.jpg')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GSOD weather visualizer.")
    
    parser.add_argument("date", help='Date to grab GSOD data. format: YYYY-MM-DD')
    parser.add_argument("-s", "--sample", help="Creates a sample based off a ratio from 0-1")

    args = parser.parse_args()

    main(args)