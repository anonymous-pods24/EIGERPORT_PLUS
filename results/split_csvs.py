import os
import csv

def create_algorithm_csv_files(input_file, output_folder, is_zipf = False):
    rows = []
    algorithms = set()

    with open(input_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            algorithms.add(row['algorithm'])
            rows.append(row)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for algorithm in algorithms:
        algorithm_file_path = os.path.join(output_folder, f'{algorithm}.csv')
        with open(algorithm_file_path, 'w', newline='') as algorithm_file:
            writer = csv.DictWriter(algorithm_file, fieldnames=reader.fieldnames)
            writer.writeheader()
            for row in rows:
                if row['algorithm'] == algorithm:
                    if not is_zipf:
                        # divide latency by 1000 to get ms
                        row['latency'] = float(row['latency']) / 1000
                    writer.writerow(row)


def split_all():
    paths = {
        "Num_Clients" : "/home/luca/ETH/Thesis/EIGERPORT+/results/num_clients.csv",
        "Num_Servers" : "/home/luca/ETH/Thesis/EIGERPORT+/results/num_servers.csv",
        "Zipf" : "/home/luca/ETH/Thesis/EIGERPORT+/results/zipf_not_normal.csv",
        "Normalized_Zipf" : "/home/luca/ETH/Thesis/EIGERPORT+/results/zipf.csv",
    }

    for name, path in paths.items():
        print(name)
        zipf = name == "Normalized_Zipf"
        create_algorithm_csv_files(path, f'/home/luca/ETH/Thesis/EIGERPORT+/results/{name}', zipf)

if __name__ == '__main__':
    split_all()