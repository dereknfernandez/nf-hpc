import os

def parse_metrics(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    metrics = {line.split(': ')[0]: float(line.split(': ')[1].strip()) for line in lines if ': ' in line}
    return metrics

def evaluate_tuning(results_dir, output_file):
    best_params = None
    best_score = 0
    for file in os.listdir(results_dir):
        if file.endswith('_results.txt'):
            metrics = parse_metrics(os.path.join(results_dir, file))
            f1_score = metrics.get('F1 Score', 0)
            if f1_score > best_score:
                best_score = f1_score
                best_params = file.split('_results.txt')[0].split('model_')[1]

    with open(output_file, 'w') as f:
        f.write(f'Best Params: {best_params}\n')
        f.write(f'Best F1 Score: {best_score}\n')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--results_dir', required=True, help='Directory with results files')
    parser.add_argument('--output', required=True, help='Output file for best model parameters')
    args = parser.parse_args()
    evaluate_tuning(args.results_dir, args.output)
