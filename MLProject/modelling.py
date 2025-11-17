"""
MLflow Project Model Training Script for CI/CD
Author: gus_agung
Description: Automated model training for CI/CD pipeline
"""

import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, classification_report, 
                             confusion_matrix)
import click
import os
import warnings
warnings.filterwarnings('ignore')


def load_data(data_path):
    """
    Load preprocessed data
    
    Args:
        data_path (str): Path to preprocessed data directory
        
    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    print(f"[INFO] Loading data from {data_path}/")
    
    X_train = pd.read_csv(f'{data_path}/X_train.csv')
    X_test = pd.read_csv(f'{data_path}/X_test.csv')
    y_train = pd.read_csv(f'{data_path}/y_train.csv').values.ravel()
    y_test = pd.read_csv(f'{data_path}/y_test.csv').values.ravel()
    
    print(f"[INFO] Training set: {X_train.shape}")
    print(f"[INFO] Test set: {X_test.shape}")
    
    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train, model_type, n_estimators, max_depth, min_samples_split, tune=False):
    """
    Train machine learning model
    
    Args:
        X_train: Training features
        y_train: Training target
        model_type (str): Type of model
        n_estimators (int): Number of estimators
        max_depth (int): Maximum depth
        min_samples_split (int): Minimum samples for split
        tune (bool): Whether to perform hyperparameter tuning
        
    Returns:
        trained model
    """
    print(f"\n[INFO] Training {model_type} model...")
    
    if tune:
        print("[INFO] Performing hyperparameter tuning...")
        if model_type == 'random_forest':
            base_model = RandomForestClassifier(random_state=42, n_jobs=-1)
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 15, 20],
                'min_samples_split': [2, 5, 10]
            }
        else:
            base_model = GradientBoostingClassifier(random_state=42)
            param_grid = {
                'n_estimators': [100, 200, 300],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 5, 7]
            }
        
        grid_search = GridSearchCV(base_model, param_grid, cv=3, scoring='f1', n_jobs=-1, verbose=1)
        grid_search.fit(X_train, y_train)
        
        print(f"[INFO] Best parameters: {grid_search.best_params_}")
        return grid_search.best_estimator_
    
    else:
        if model_type == 'random_forest':
            model = RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                random_state=42,
                n_jobs=-1
            )
        else:
            model = GradientBoostingClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                random_state=42
            )
        
        model.fit(X_train, y_train)
        return model


def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test target
        
    Returns:
        dict: Evaluation metrics
    """
    print("\n[INFO] Evaluating model...")
    
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_pred_proba)
    }
    
    # Additional metrics
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    metrics['specificity'] = tn / (tn + fp) if (tn + fp) > 0 else 0
    metrics['false_positive_rate'] = fp / (fp + tn) if (fp + tn) > 0 else 0
    
    print("\n[INFO] Model Performance:")
    for metric_name, metric_value in metrics.items():
        print(f"  • {metric_name}: {metric_value:.4f}")
    
    return metrics


@click.command()
@click.option('--data_path', default='hotel_bookings_preprocessed', help='Path to preprocessed data')
@click.option('--model_type', default='random_forest', help='Type of model to train')
@click.option('--n_estimators', default=200, type=int, help='Number of estimators')
@click.option('--max_depth', default=15, type=int, help='Maximum depth')
@click.option('--min_samples_split', default=5, type=int, help='Minimum samples split')
@click.option('--experiment_name', default='hotel_booking_ci', help='MLflow experiment name')
@click.option('--use_dagshub', default='false', help='Use DagsHub for remote tracking')
@click.option('--dagshub_uri', default='', help='DagsHub tracking URI')
@click.option('--tune', default=False, is_flag=True, help='Perform hyperparameter tuning')
def main(data_path, model_type, n_estimators, max_depth, min_samples_split, 
         experiment_name, use_dagshub, dagshub_uri, tune):
    """
    Main training pipeline for MLflow Project
    """
    print("="*60)
    print("MLFLOW PROJECT - MODEL TRAINING")
    print("="*60)
    
    # Setup MLflow
    if use_dagshub.lower() == 'true' and dagshub_uri:
        print(f"[INFO] Using DagsHub: {dagshub_uri}")
        mlflow.set_tracking_uri(dagshub_uri)
    else:
        print("[INFO] Using local MLflow tracking")
        mlflow.set_tracking_uri("file:./mlruns")
    
    mlflow.set_experiment(experiment_name)
    
    # Load data
    X_train, X_test, y_train, y_test = load_data(data_path)
    
    # Start MLflow run
    with mlflow.start_run(run_name=f"{model_type}_ci_run") as run:
        
        print(f"\n[INFO] MLflow Run ID: {run.info.run_id}")
        
        # Log parameters
        mlflow.log_param("data_path", data_path)
        mlflow.log_param("model_type", model_type)
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("min_samples_split", min_samples_split)
        mlflow.log_param("hyperparameter_tuning", tune)
        
        # Train model
        model = train_model(X_train, y_train, model_type, n_estimators, 
                          max_depth, min_samples_split, tune)
        
        # Evaluate model
        metrics = evaluate_model(model, X_test, y_test)
        
        # Log metrics
        for metric_name, metric_value in metrics.items():
            mlflow.log_metric(metric_name, metric_value)
        
        # Log model
        mlflow.sklearn.log_model(
            model, 
            "model",
            registered_model_name=f"hotel_booking_{model_type}_ci"
        )
        
        # Save classification report
        y_pred = model.predict(X_test)
        report = classification_report(y_test, y_pred)
        
        os.makedirs('outputs', exist_ok=True)
        report_path = 'outputs/classification_report.txt'
        with open(report_path, 'w') as f:
            f.write(report)
        mlflow.log_artifact(report_path)
        
        print("\n" + "="*60)
        print("[SUCCESS] Model training completed!")
        print(f"[INFO] Run ID: {run.info.run_id}")
        print("="*60)


if __name__ == "__main__":
    main()
