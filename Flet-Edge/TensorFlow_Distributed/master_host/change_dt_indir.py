import configparser
import os
import subprocess
import linecache


def read_per_section_name():
    host_name = get_host_name()

    config_per_section_name = configparser.ConfigParser()
    file_path = os.path.dirname(os.path.abspath(__file__))
    print("当前位置：", file_path)
    per_section_name_ini_path = "/home/%s/%s/per_section_name_dir/per_section_name.ini" % \
                                (host_name, host_name)

    config_per_section_name.read(per_section_name_ini_path)

    FTE_training_section_name = config_per_section_name.get('from_out_control', 'FTE_training_section_name')
    sub_config_section_name = config_per_section_name.get('from_out_control', 'sub_config_section_name')

    return FTE_training_section_name, sub_config_section_name


def get_host_name():
    host_name = linecache.getline("./host_name.ini", 4)
    print("host_name_change_dt_indir:", host_name)
    host_name = host_name.strip().replace(' ', '').replace('\n', '').replace('\r', '')
    return host_name


def get_host_frameworks_path(frameworks):
    host_name = get_host_name()

    frameworks = frameworks
    host_frameworks_str = host_name + '_' + frameworks

    config_host_frameworks = configparser.ConfigParser()
    FTE_device_config_path = "/home/%s/%s/FTE_device_config.ini" % (host_name, host_name)
    config_host_frameworks.read(FTE_device_config_path)
    host_frameworks = config_host_frameworks.get("FTE_device_config", host_frameworks_str)

    return host_frameworks


def get_worker_list(dt_device_name_list):
    dt_device_name_list_len = len(dt_device_name_list)

    device_config_ip_read = configparser.ConfigParser()
    sub_config_ini_path = "/home/%s/%s/FTE_device_config.ini" % (host_name, host_name)
    device_config_ip_read.read(sub_config_ini_path)

    worker_list = []

    for i in range(dt_device_name_list_len):
        dt_per_device_name = dt_device_name_list[i]

        name_of_device_ip = dt_per_device_name + "_ip_socket"

        dt_per_device_ip = device_config_ip_read.get("FTE_device_config", name_of_device_ip)
        worker_list.append(dt_per_device_ip)

    return worker_list


def get_task_index(dt_device_name_list):
    dt_device_name_list = dt_device_name_list

    host_name = get_host_name()

    task_index = dt_device_name_list.index(host_name)

    return task_index


def get_config_list_indir_to_change(training_batchsize, training_model_name, weights, training_input_size,
                                    optimizer_name, learning_rate_value, epochs, steps_per_epoch, validation_steps,
                                    dataset_name):
    config_list_indir_to_change = []

    device_name = get_host_name()
    training_batchsize = str(training_batchsize)
    training_model_name = training_model_name
    weights = weights
    training_input_size = str(training_input_size)
    optimizer_name = optimizer_name
    learning_rate_value = str(learning_rate_value)
    epochs = str(epochs)
    steps_per_epoch = str(steps_per_epoch)
    validation_steps = str(validation_steps)
    dataset_name = dataset_name

    config_list_indir_to_change.append(device_name)
    config_list_indir_to_change.append(training_batchsize)
    config_list_indir_to_change.append(training_model_name)
    config_list_indir_to_change.append(weights)
    config_list_indir_to_change.append(training_input_size)
    config_list_indir_to_change.append(optimizer_name)
    config_list_indir_to_change.append(learning_rate_value)
    config_list_indir_to_change.append(epochs)
    config_list_indir_to_change.append(steps_per_epoch)
    config_list_indir_to_change.append(validation_steps)
    config_list_indir_to_change.append(dataset_name)

    return config_list_indir_to_change


def popen(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True, executable="/bin/bash")
    out, err = p.communicate()
    return out + err


def convert_list_to_str(worker_list, config_list_indir_to_change):
    worker_list = worker_list
    config_list_indir_to_change = config_list_indir_to_change
    worker_list_str = "_".join(worker_list)
    config_list_indir_to_change_str = "_".join(config_list_indir_to_change)

    return worker_list_str, config_list_indir_to_change_str


def record_of_change_dt_config_popen(FTE_training_section_name, sub_config_section_name, out_of_change_dt_config):
    out_of_change_dt_config = out_of_change_dt_config
    host_name = get_host_name()
    with open('/home/%s/%s/%s/out_of_change_dt_config_on_device_%s.txt' % (
            host_name, host_name, FTE_training_section_name,
            sub_config_section_name), 'a') as f:
        f.write(out_of_change_dt_config)
    print(out_of_change_dt_config)


def get_device_frameworks_activities_path(frameworks):
    host_name = get_host_name()
    frameworks = frameworks

    device_name_frameworks = host_name + "_" + frameworks

    device_name_frameworks_read = configparser.ConfigParser()
    sub_config_ini_path = "/home/%s/%s/FTE_device_config.ini" % (host_name, host_name)
    device_name_frameworks_read.read(sub_config_ini_path)

    frameworks_activities_path = device_name_frameworks_read.get("FTE_device_config", device_name_frameworks)

    return frameworks_activities_path


if __name__ == '__main__':
    FTE_training_section_name, sub_config_section_name = read_per_section_name()

    host_name = get_host_name()
    training_sub_config_read = configparser.ConfigParser()
    sub_config_ini_path = "/home/%s/%s/%s/%s_all_section.ini" % (
        host_name, host_name, FTE_training_section_name, FTE_training_section_name)
    training_sub_config_read.read(sub_config_ini_path)

    training_batchsize = training_sub_config_read.getint(sub_config_section_name, "training_batchsize")
    training_model_name = training_sub_config_read.get(sub_config_section_name, "training_model_name")
    weights = training_sub_config_read.get(sub_config_section_name, "weights")
    training_input_size = training_sub_config_read.getint(sub_config_section_name, "training_input_size")
    optimizer_name = training_sub_config_read.get(sub_config_section_name, "optimizer_name")

    learning_rate_value = training_sub_config_read.getfloat(sub_config_section_name, "learning_rate_value")
    epochs = training_sub_config_read.getint(sub_config_section_name, "epochs")
    steps_per_epoch = training_sub_config_read.getint(sub_config_section_name, "steps_per_epoch")
    validation_steps = training_sub_config_read.getint(sub_config_section_name, "validation_steps")
    dataset_name = training_sub_config_read.get(sub_config_section_name, "dataset_name")
    dt_device_number = training_sub_config_read.getint(sub_config_section_name, "dt_device_number")
    dt_device_name_str = training_sub_config_read.get(sub_config_section_name, "dt_device_name")

    dt_device_name_list = dt_device_name_str.split(" ")

    host_frameworks = get_host_frameworks_path("tensorflow")

    worker_list = get_worker_list(dt_device_name_list)

    task_index = get_task_index(dt_device_name_list)

    config_list_indir_to_change = get_config_list_indir_to_change(training_batchsize, training_model_name, weights,
                                                                  training_input_size,
                                                                  optimizer_name, learning_rate_value, epochs,
                                                                  steps_per_epoch, validation_steps, dataset_name)

    worker_list_str, config_list_indir_to_change_str = convert_list_to_str(worker_list, config_list_indir_to_change)

    frameworks_activities_path = get_device_frameworks_activities_path("tensorflow")

    out_of_change_dt_config = popen("%s;python3 /home/%s/%s/change_dt_config.py %s %s %s" %
                                    (frameworks_activities_path, host_name, host_name, worker_list_str, task_index,
                                     config_list_indir_to_change_str))

    record_of_change_dt_config_popen(FTE_training_section_name, sub_config_section_name, out_of_change_dt_config)