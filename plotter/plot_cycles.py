from typing import Dict
import pickle
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


def load_simulation_data() -> (Dict, pd.DataFrame):
    with open(file='../simulation_result/simulation_result.pickle', mode='rb') as file:
        load_data = pickle.load(file=file)

    configs = load_data[0]

    cycles_data = pd.DataFrame(load_data[2].items(), columns=["Cycle", "Frequency"])
    cycles_data.sort_values(by='Cycle', axis=0, inplace=True)
    cycles_data['Frequency'] /= configs['simulation_configs']['repetition']
    cycles_data.reset_index(drop=True, inplace=True)

    return configs, cycles_data


def plot_cycles(configs: Dict, data: pd.DataFrame) -> None:
    sns.set(font_scale=1.5)
    plt.rcParams['font.weight'] = 'bold'
    sns.set_style(style='ticks')

    fig, ax = plt.subplots(nrows=1, ncols=1)
    sns.lineplot(data=data,
                 x='Cycle', y='Frequency',
                 linewidth=4,
                 ax=ax)
    ax.set_xlabel('Cycles', weight='bold')
    ax.set_ylabel('Probability', weight='bold')

    if not os.path.exists('../graph/'):
        os.makedirs('../graph')

    fig.set_size_inches(7, 5)
    fig.tight_layout()
    # fig.show()
    fig.savefig('../graph/cycles.pdf')
    fig.clf()
    plt.close(fig=fig)


def compute_average(configs: Dict, data: pd.DataFrame) -> float:
    data.sort_values(by='Frequency', axis='index', ascending=False, inplace=True)
    print(data.head(3).to_string())
    return sum(data['Cycle'] * data['Frequency'])


if __name__ == '__main__':
    configs, data = load_simulation_data()
    plot_cycles(configs=configs, data=data)

    average_cycles = compute_average(configs=configs, data=data)
    print(f"Average cycle: {average_cycles:.2f}")
