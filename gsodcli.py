import plotly.express as px 
import pandas as pd
from pathlib import Path, PosixPath
import glob
import argparse
from utils import gsod
from datetime import datetime
from modules import visuals
import sys

def main() -> None:
    cli_args = ParseArguments()

    date : datetime = FormatDate(cli_args.date)
    
    if not gsod.find_dir(date):
        print("Archive not found in cache.")
        gsod.download_archive(date)

    dataset_files : list = glob.glob(str(Path.cwd() / f"gsod_data/{date.year}/*"))

    ds_list : list = [pd.read_csv(file, index_col=None) for file in dataset_files]
    df : pd.DataFrame = pd.concat(ds_list, axis=0)

    match cli_args.type:
        case "visual":
            visuals.map_figure(df, date, sample_ratio=cli_args.sample, export_location=cli_args.export)

def ParseArguments() -> None:
    parser = argparse.ArgumentParser(description="GSOD weather visualizer.")
    parser.add_argument("type", help="Types: visual (for now)")
    parser.add_argument("date", help='Date to grab GSOD data. format: YYYY-MM-DD')
    parser.add_argument("-s", "--sample", help="Creates a sample based off a ratio from 0-1")
    parser.add_argument("-e", "--export", help="Exports graphical data to a chosen path")

    return parser.parse_args()

def FormatDate(date_str: str) -> datetime.date:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    
    except ValueError as e:
        print(f"ERROR: Incorrect date format YYYY-MM-DD", file=sys.stderr)
        exit()

if __name__ == "__main__":
    main()