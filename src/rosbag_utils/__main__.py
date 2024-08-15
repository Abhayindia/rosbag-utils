import argparse
from pathlib import Path

from .comparator import RosbagComparator
from .topic_remover import BagTopicRemover
from . import utils as u

def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description="Rosbag utilities")

    subparsers = parser.add_subparsers(dest='command')

    # Subparser for rosbag-compare
    compare_parser = subparsers.add_parser('compare', help='Compare rosbag topics')
    compare_parser.add_argument(
        "-b",
        "--bagfolder",
        help="""Path to the folder that contains rosbags""",
        required=True,
    )
    compare_parser.add_argument(
        "-p",
        "--plot",
        help="Flag for plotting and showing the result",
        action="store_true",
    )
    compare_parser.add_argument(
        "-m",
        "--mode",
        help="""Comparison mode""",
        default="available",
        choices=["available", "missing"],
    )

    # Subparser for rosbag-topic-remove
    remove_parser = subparsers.add_parser('remove', help='Remove topics from rosbag')
    remove_parser.add_argument(
        "inbag",
        type=u.path_type(),
        help="Input bag",
    )
    remove_parser.add_argument(
        "-o",
        "--output",
        "--outbag",
        dest="outbag",
        help="Filtered bag",
    )
    remove_parser.add_argument(
        "-t",
        "--topics",
        type=str,
        nargs="+",
        help="Topics to remove from the rosbag",
    )
    remove_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force output file overwriting",
    )

    return parser.parse_args()

def main():
    """Main function"""
    args = parse_arguments()

    if args.command == 'compare':
        data_path = Path(args.bagfolder)
        is_plot = args.plot
        rosbag_comp = RosbagComparator(data_path, mode=args.mode)
        rosbag_comp.extract_data()
        rosbag_comp.to_json()
        if is_plot:
            rosbag_comp.plot()

    elif args.command == 'remove':
        inpath = args.inbag
        outpath = args.outbag

        rosbag_rem = BagTopicRemover(inpath)
        rosbag_rem.remove(args.topics)
        if outpath:
            rosbag_rem.export(outpath, force_out=args.force)
        else:
            # Default path:
            # /path/to/my/rosbag => /path/to/my/rosbag_filt
            # /path/to/my/rosbag.bag => /path/to/my/rosbag_filt.bag
            inpath = Path(inpath)
            def_outfile = f"{inpath.stem}_filt{inpath.suffix}"
            default_outpath = inpath.parent / def_outfile
            rosbag_rem.export(default_outpath, force_out=args.force)

if __name__ == "__main__":
    main()
