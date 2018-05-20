import math
import json
import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def parse_results_files(results_dir):

    ResultsList = []
    for file in os.listdir(results_dir):

        with open(os.path.join(results_dir, file), 'r') as f:
            json_results = json.loads(f.read())
            ResultsList.append(json_results)

    return ResultsList


def parse_result(report):


    num_players = report["Players"]
    results = report["Results"]

    # What we should do is create a 2d array
    # rows are simulations
    # columns are rounds
    # fill it out as best as possible, then go through and extend the ones
    # that don't fit to the end
    # Goal is to create 5 element dictionary:
    #
    # rounds : [0:num_rounds]
    # coal: []
    # ...
    #
    #

    # Determine max number of rounds from all simulations
    num_sims = len(results)
    max_rounds = max([len(v) for (k, v) in results.items()])

    results_array = np.empty((num_sims, max_rounds), dtype=dict)

    # Extend all simulations to match the maximum number of rounds if less
    for i, (sim_num, replicate) in enumerate(results.items()):

        last_item = None
        for j, (round, usage) in enumerate(replicate.items()):

            results_array[i][j] = replicate[round]
            last_item = replicate[round]

        # Extend to fill out array
        for j in range(max_rounds - len(replicate)):
            results_array[i][j + len(replicate)] = last_item

    # Iterate over all the rounds.
    plot_data = {
        "rounds" : [],
        "coal" : [],
        "coal_error" : [],
        "oil" : [],
        "oil_error" : [],
        "trash" : [],
        "trash_error" : [],
        "uranium" : [],
        "uranium_error": []
    }
    for i in range(max_rounds):

        round_data = results_array[:, i]
        round_data = [x for x in round_data]


        coal    = [x["0"] for x in round_data]
        oil     = [x["1"] for x in round_data]
        trash   = [x["2"] for x in round_data]
        uranium = [x["3"] for x in round_data]

        plot_data["rounds"].append(i)

        plot_data["coal"].append(np.mean(coal))
        plot_data["coal_error"].append(np.std(coal))

        plot_data["oil"].append(np.mean(oil))
        plot_data["oil_error"].append(np.std(oil))

        plot_data["trash"].append(np.mean(trash))
        plot_data["trash_error"].append(np.std(trash))

        plot_data["uranium"].append(np.mean(uranium))
        plot_data["uranium_error"].append(np.std(uranium))

    return (num_players, plot_data)







if __name__ == '__main__':

    # Parse command line args
    parser = argparse.ArgumentParser(description="Analyze simulation results", add_help=True)
    parser.add_argument('-r', dest='result_dir', type=str, help="Path to results from sim")
    args = parser.parse_args()


    full_results = parse_results_files(args.result_dir)


    f, axs = plt.subplots(3, 2)
    axs[0, 1].axis('off')
    plot_handles = []
    for count, item in enumerate(full_results):

        num_players, result = parse_result(item)
        title = "Resource Availability over Time ({0:d} Players)".format(num_players)

        if count < 3:
            i = count
            j = 0
        else:
            i = count - 3 + 1
            j = 1



        ax = axs[i, j]

        # ax[i].xlabel('Round Number')
        # ax[i].ylabel('Available Resources')

        if j == 0:
            ax.set(ylabel='Available Resources')
        if i == 2:
            ax.set(xlabel='Round Number')

        ax.set_title(title)
        ax.grid(True)

        rounds = result["rounds"]
        del result["rounds"]

        ax.errorbar(rounds, result["coal"], yerr=result["coal_error"], label="coal", color="sienna", capsize=2, elinewidth=1)
        ax.errorbar(rounds, result["oil"], yerr=result["oil_error"], label="oil", color="black", capsize=2, elinewidth=1)
        ax.errorbar(rounds, result["trash"], yerr=result["trash_error"], label="trash", color="gold", capsize=2, elinewidth=1)
        ax.errorbar(rounds, result["uranium"], yerr=result["uranium_error"], label="uranium", color="crimson", capsize=2, elinewidth=1)

    handles, labels = axs[0,0].get_legend_handles_labels()
    axs[0, 1].legend(handles, labels, loc='center')


    plt.show()


