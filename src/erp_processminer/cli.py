"""
Defines the command-line interface for the erp-processminer package.
"""

import argparse
import json
from erp_processminer.io_erp.loaders import load_multiple_erp_data
from erp_processminer.io_erp.mappings import apply_mapping
from erp_processminer.eventlog.serialization import export_log_to_csv
from erp_processminer.discovery.directly_follows import discover_dfg
from erp_processminer.visualization.graphs import visualize_dfg

def main():
    """Main function for the CLI."""
    parser = argparse.ArgumentParser(
        description="A toolkit for process mining on ERP event logs."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- erp-to-log command ---
    parser_etl = subparsers.add_parser(
        "erp-to-log", help="Transform ERP CSV files into an event log."
    )
    parser_etl.add_argument(
        "config", help="Path to the JSON mapping configuration file."
    )
    parser_etl.add_argument(
        "in_files", nargs='+', help="Paths to the input CSV files."
    )
    parser_etl.add_argument(
        "-o", "--output", default="log.csv", help="Path to the output event log CSV file."
    )

    # --- discover command ---
    parser_discover = subparsers.add_parser(
        "discover", help="Discover a process model from an event log."
    )
    parser_discover.add_argument(
        "log", help="Path to the event log CSV file."
    )
    parser_discover.add_argument(
        "-m", "--method", default="dfg", choices=["dfg", "heuristics"],
        help="The discovery algorithm to use."
    )
    parser_discover.add_argument(
        "-o", "--output", default="model.png", help="Path for the output visualization."
    )

    args = parser.parse_args()

    if args.command == "erp-to-log":
        run_erp_to_log(args)
    elif args.command == "discover":
        run_discover(args)

def run_erp_to_log(args):
    """Executes the erp-to-log command."""
    print(f"Loading configuration from {args.config}...")
    with open(args.config, 'r') as f:
        config = json.load(f)
    
    print(f"Loading data from {len(args.in_files)} files...")
    dataframes = load_multiple_erp_data(args.in_files)
    
    print("Applying mapping to create event log...")
    event_log = apply_mapping(dataframes, config)
    
    print(f"Exporting event log to {args.output}...")
    export_log_to_csv(event_log, args.output)
    print("Done.")

def run_discover(args):
    """Executes the discover command."""
    from erp_processminer.eventlog.serialization import import_log_from_csv
    from erp_processminer.discovery.heuristics_miner import discover_petri_net_with_heuristics
    from erp_processminer.visualization.graphs import visualize_petri_net

    print(f"Importing event log from {args.log}...")
    log = import_log_from_csv(args.log)

    if args.method == "dfg":
        print("Discovering Directly-Follows Graph...")
        dfg, start_activities, end_activities = discover_dfg(log)
        print(f"Visualizing DFG and saving to {args.output}...")
        visualize_dfg(dfg, start_activities, end_activities, args.output)
    elif args.method == "heuristics":
        print("Discovering Petri net with Heuristics Miner...")
        net = discover_petri_net_with_heuristics(log)
        print(f"Visualizing Petri net and saving to {args.output}...")
        visualize_petri_net(net, args.output)

    print("Done.")

if __name__ == "__main__":
    main()