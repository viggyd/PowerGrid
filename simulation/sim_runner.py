import json
import argparse
from simulation import ResourceAnalysisSim
from powergrid import Plant, ResourceType

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Process simulation parameters", add_help=True)

    parser.add_argument('-n', dest='num_sims', type=int,
                        help="Number of simulations to run")
    parser.add_argument('-c', dest='config_file', type=str,
                        help="Path to the config file")
    parser.add_argument('-o', dest='results_path', type=str,
                        help="Path to store results")



    args = parser.parse_args()

    for num_player in range(2, 7):

        full_report = {}
        report_file = args.results_path
        report_file += "/{0:d}_player_usage.json".format(num_player)

        full_report["Players"] = num_player

        usage = {}
        for sim_number in range(args.num_sims):


            sim = ResourceAnalysisSim(
                num_players=num_player,
                config_file=args.config_file
            )

            results = sim.simulate()
            usage[sim_number] = results

        full_report["Results"] = usage

        with open(report_file, 'w') as f:
            f.write(json.dumps(full_report, indent=2))