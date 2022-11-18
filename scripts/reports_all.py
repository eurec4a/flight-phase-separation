import report
from pathlib import Path
from tqdm import tqdm
import yaml


def main():
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "segments_directory",
        help="directory containing flight segments yaml-files",
        type=Path,
    )
    argparser.add_argument(
        "--output-diretory", help="directory to place reports into", default=Path(".")
    )
    argparser.add_argument(
        "--report-id-format",
        help="format for id in report filename",
        default="{flight_id}.html",
    )
    args = argparser.parse_args()

    segments_filepaths = sorted(list(args.segments_directory.glob("*.yaml")))

    for segments_fp in tqdm(segments_filepaths):
        flightdata = yaml.load(open(segments_fp), Loader=yaml.SafeLoader)
        report_fp = args.report_id_format.format(**flightdata)
        report.create_report(
            flightdata=flightdata, report_filepath=report_fp, sondes_filepath=None
        )


if __name__ == "__main__":
    main()
