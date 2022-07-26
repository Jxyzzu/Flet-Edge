"""
The automatic drawing of histogram is relatively simple, mainly including data transmission, legend and image naming.

note: The function of each method can be known by referring to its method name.
"""
import configparser
import sys
import matplotlib.pyplot as plt
import numpy as np


def plot_combine_bar(pmu_data_path, plot_combine_bar_list, combine_section_name):
    label_bar = []
    results_bar = []

    config_read_pmu_data = configparser.RawConfigParser()
    config_read_pmu_data.optionxform = lambda option: option
    config_read_pmu_data.read(pmu_data_path)

    len_plot_combine_bar_list = len(plot_combine_bar_list)

    for i in range(len_plot_combine_bar_list):
        section_name_i = plot_combine_bar_list[i]
        model_name_i = config_read_pmu_data.get(section_name_i, "model_name")
        device_name_i = config_read_pmu_data.get(section_name_i, "device_name")
        input_size_i = config_read_pmu_data.getint(section_name_i, "input_size")
        pmu_i = config_read_pmu_data.getfloat(section_name_i, "pmu")
        label_bar.append(section_name_i)
        results_bar.append(pmu_i)

    fig, ax = plt.subplots()
    plt.title("Peak Memory Usage of TensorFlow/PyTorch on Jetson Nano")

    plt.xlabel("model_and_config")
    plt.ylabel("Peak Memory Usage(MB)")

    ax.grid(axis='y', alpha=0.3, linewidth=0.7, linestyle='--')

    x = np.arange(len(label_bar))
    bar_width = 0.15

    plt.xticks(x, labels=label_bar, rotation=-15)
    plt.bar(x, results_bar, width=bar_width - 0.02, color='#0780cf')
    plt.savefig(fname="TF_Py_combine_pmu_%s.png" % combine_section_name, format="png", bbox_inches='tight')
    plt.show()

    return None


def str_to_list(plot_combine_bar_list_str):
    plot_combine_bar_list = plot_combine_bar_list_str.split("+")
    return plot_combine_bar_list


if __name__ == '__main__':
    pmu_data_path = sys.argv[1]

    plot_combine_bar_list_str = sys.argv[2]
    combine_section_name = sys.argv[3]

    plot_combine_bar_list = str_to_list(plot_combine_bar_list_str)
    plot_combine_bar(pmu_data_path, plot_combine_bar_list, combine_section_name)
