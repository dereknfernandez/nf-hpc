import os
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def evaluate(model_file, input_file, output_file):
    model = joblib.load(model_file)
    df = pd.read_csv(input_file)
    X = df.drop('target', axis=1)
    y = df['target']
    
    predictions = model.predict(X)
    accuracy = accuracy_score(y, predictions)
    precision = precision_score(y, predictions, average='weighted')
    recall = recall_score(y, predictions, average='weighted')
    f1 = f1_score(y, predictions, average='weighted')
    
    _cwd = os.getcwd()
    newdir = os.path.join(_cwd, r'models')
    if not os.path.exists(newdir):
       os.makedirs(newdir)
    
    with open(output_file, 'w+') as f:
        f.write(f'Accuracy: {accuracy}\n')
        f.write(f'Precision: {precision}\n')
        f.write(f'Recall: {recall}\n')
        f.write(f'F1 Score: {f1}\n')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, help='Model file')
    parser.add_argument('--input', required=True, help='Input CSV file')
    parser.add_argument('--output', required=True, help='Output file for evaluation metrics')
    args = parser.parse_args()
    evaluate(args.model, args.input, args.output)
