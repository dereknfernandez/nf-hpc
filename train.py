import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

def train(train_file, val_file, params, output_file):
    train_df = pd.read_csv(train_file)
    val_df = pd.read_csv(val_file)
    X_train = train_df.drop('target', axis=1)
    y_train = train_df['target']
    X_val = val_df.drop('target', axis=1)
    y_val = val_df['target']
    
    params_dict = eval(params)
    model = LogisticRegression(**params_dict)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_val)
    accuracy = accuracy_score(y_val, predictions)
    precision = precision_score(y_val, predictions, average='weighted')
    recall = recall_score(y_val, predictions, average='weighted')
    f1 = f1_score(y_val, predictions, average='weighted')
    
    _cwd = os.getcwd()
    newdir = os.path.join(_cwd, r'models')
    if not os.path.exists(newdir):
       os.makedirs(newdir)
       
    joblib.dump(model, output_file)
    with open(output_file.replace('.pkl', '_results.txt'), 'w') as f:
        f.write(f'Params: {params}\n')
        f.write(f'Accuracy: {accuracy}\n')
        f.write(f'Precision: {precision}\n')
        f.write(f'Recall: {recall}\n')
        f.write(f'F1 Score: {f1}\n')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', required=True, help='Train CSV file')
    parser.add_argument('--val', required=True, help='Validation CSV file')
    parser.add_argument('--params', required=False, default='{}', help='Hyperparameters')
    parser.add_argument('--output', required=True, help='Output model file')
    args = parser.parse_args()
    train(args.train, args.val, args.params, args.output)
