"""
Hotel Booking Cancellation Prediction Model - Enhanced Version
Author: gus_agung
Description: Machine Learning model using MLflow with AUTOLOG + MANUAL LOGGING
Level: Enhanced - Autolog + 5 Additional Manual Metrics + Visualizations
"""

import os
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, classification_report,
    confusion_matrix, matthews_corrcoef, cohen_kappa_score,
    log_loss, roc_curve
)
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for threading safety
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Optional: Load from .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass


def setup_mlflow():
    """
    Setup MLflow tracking
    Enhanced: Autolog + Manual Logging with localhost tracking
    """
    print("="*70)
    print(" "*10 + "MLFLOW SETUP - AUTOLOG + MANUAL LOGGING")
    print("="*70)
    
    # Set tracking URI to localhost (required for submission)
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    
    # Set experiment
    experiment_name = "hotel_booking_enhanced_experiments"
    mlflow.set_experiment(experiment_name)
    
    print(f"✓ Tracking URI: {mlflow.get_tracking_uri()}")
    print(f"✓ Experiment: {experiment_name}")
    print(f"✓ Autolog: ENABLED (model artifacts)")
    print(f"✓ Manual Logging: ENABLED (5+ additional metrics)")
    print(f"✓ Visualizations: confusion_matrix, roc_curve, metrics_comparison")
    print("="*70 + "\n")


def load_data(data_dir='hotel_bookings_preprocessed'):
    """
    Load preprocessed data
    
    Args:
        data_dir (str): Directory containing preprocessed data
        
    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    print(f"[INFO] Loading data from {data_dir}/")
    
    X_train = pd.read_csv(f'{data_dir}/X_train.csv')
    X_test = pd.read_csv(f'{data_dir}/X_test.csv')
    y_train = pd.read_csv(f'{data_dir}/y_train.csv').values.ravel()
    y_test = pd.read_csv(f'{data_dir}/y_test.csv').values.ravel()
    
    print(f"✓ Training set: {X_train.shape}")
    print(f"✓ Test set: {X_test.shape}")
    print(f"✓ Class distribution (train): {np.bincount(y_train)}\n")
    
    return X_train, X_test, y_train, y_test


def calculate_additional_metrics(y_true, y_pred, y_pred_proba):
    """
    Calculate 5+ additional metrics beyond autolog
    """
    metrics = {}
    
    # Additional Metric 1: Matthews Correlation Coefficient
    metrics['matthews_corrcoef'] = matthews_corrcoef(y_true, y_pred)
    
    # Additional Metric 2: Cohen's Kappa Score
    metrics['cohen_kappa'] = cohen_kappa_score(y_true, y_pred)
    
    # Additional Metric 3: Log Loss
    metrics['log_loss'] = log_loss(y_true, y_pred_proba)
    
    # Additional Metric 4: Specificity (True Negative Rate)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    metrics['specificity'] = tn / (tn + fp) if (tn + fp) > 0 else 0
    
    # Additional Metric 5: Balanced Accuracy
    recall_per_class = recall_score(y_true, y_pred, average=None)
    metrics['balanced_accuracy'] = np.mean(recall_per_class)
    
    # Additional Metric 6: Geometric Mean
    metrics['geometric_mean'] = np.sqrt(recall_per_class[0] * recall_per_class[1])
    
    return metrics


def create_visualizations(y_true, y_pred, y_pred_proba, model_name):
    """
    Create and save visualizations
    """
    plots = []
    
    # 1. Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Not Canceled', 'Canceled'],
                yticklabels=['Not Canceled', 'Canceled'])
    plt.title(f'Confusion Matrix - {model_name}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    cm_path = f'confusion_matrix_{model_name}.png'
    plt.savefig(cm_path, dpi=300, bbox_inches='tight')
    plt.close()
    plots.append(cm_path)
    
    # 2. ROC Curve
    fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
    roc_auc = roc_auc_score(y_true, y_pred_proba)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve - {model_name}')
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    roc_path = f'roc_curve_{model_name}.png'
    plt.savefig(roc_path, dpi=300, bbox_inches='tight')
    plt.close()
    plots.append(roc_path)
    
    # 3. Metrics Bar Chart
    metrics = {
        'Accuracy': accuracy_score(y_true, y_pred),
        'Precision': precision_score(y_true, y_pred, average='weighted'),
        'Recall': recall_score(y_true, y_pred, average='weighted'),
        'F1-Score': f1_score(y_true, y_pred, average='weighted'),
        'ROC-AUC': roc_auc
    }
    plt.figure(figsize=(10, 6))
    plt.bar(metrics.keys(), metrics.values(), color='skyblue', edgecolor='navy')
    plt.ylim([0, 1.1])
    plt.ylabel('Score')
    plt.title(f'Model Performance Metrics - {model_name}')
    plt.xticks(rotation=45)
    for i, (k, v) in enumerate(metrics.items()):
        plt.text(i, v + 0.02, f'{v:.4f}', ha='center', fontweight='bold')
    plt.tight_layout()
    metrics_path = f'metrics_chart_{model_name}.png'
    plt.savefig(metrics_path, dpi=300, bbox_inches='tight')
    plt.close()
    plots.append(metrics_path)
    
    return plots


def train_model_enhanced(X_train, X_test, y_train, y_test, model_name="RandomForest"):
    """
    Train model using AUTOLOG + MANUAL LOGGING
    - Autolog: Handles model artifacts (model/, estimator.html, etc.)
    - Manual: Logs 5+ additional metrics + visualizations
    """
    print("\n" + "="*70)
    print(f"TRAINING {model_name} - AUTOLOG + MANUAL LOGGING")
    print("="*70)
    
    # Enable autolog for model artifacts
    mlflow.sklearn.autolog(
        log_models=True,
        log_input_examples=True,
        log_model_signatures=True,
        disable=False
    )
    
    # Start MLflow run
    with mlflow.start_run(run_name=f"{model_name}_enhanced"):
        
        # Select model
        if model_name == "RandomForest":
            model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                n_jobs=-1
            )
        elif model_name == "LogisticRegression":
            model = LogisticRegression(
                random_state=42,
                max_iter=1000,
                n_jobs=-1
            )
        elif model_name == "DecisionTree":
            model = DecisionTreeClassifier(
                random_state=42,
                max_depth=10
            )
        else:
            raise ValueError(f"Unknown model: {model_name}")
        
        print(f"\n[INFO] Training {model_name}...")
        
        # Train model - autolog will automatically log params, metrics, model
        model.fit(X_train, y_train)
        
        print(f"✓ Model trained successfully!")
        
        # Make predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
        
        # Calculate metrics (autolog will log these automatically)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        # Print results
        print(f"\n{'='*70}")
        print(f"MODEL PERFORMANCE - {model_name}")
        print(f"{'='*70}")
        print(f"Accuracy:  {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1-Score:  {f1:.4f}")
        
        if y_pred_proba is not None:
            roc_auc = roc_auc_score(y_test, y_pred_proba)
            print(f"ROC-AUC:   {roc_auc:.4f}")
        
        print(f"{'='*70}\n")
        
        # Print classification report
        print("Classification Report:")
        print(classification_report(y_test, y_pred, target_names=['Not Canceled', 'Canceled']))
        
        # MANUAL LOGGING: Calculate 5+ additional metrics
        print(f"\n{'='*70}")
        print("CALCULATING 5+ ADDITIONAL METRICS (Beyond autolog)")
        print(f"{'='*70}")
        
        additional_metrics = calculate_additional_metrics(y_test, y_pred, y_pred_proba if y_pred_proba is not None else y_pred)
        
        # Log additional metrics manually
        for metric_name, value in additional_metrics.items():
            mlflow.log_metric(f"additional_{metric_name}", value)
            print(f"✓ {metric_name}: {value:.4f}")
        
        # MANUAL LOGGING: Create and log visualizations
        print(f"\n{'='*70}")
        print("CREATING & LOGGING VISUALIZATIONS")
        print(f"{'='*70}")
        
        if y_pred_proba is not None:
            plot_paths = create_visualizations(y_test, y_pred, y_pred_proba, model_name)
            for plot_path in plot_paths:
                mlflow.log_artifact(plot_path)
                print(f"✓ Logged: {plot_path}")
                # Delete local file after logging
                if os.path.exists(plot_path):
                    os.remove(plot_path)
        
        # Get run info
        run = mlflow.active_run()
        print(f"\n{'='*70}")
        print(f"✓ MLflow Run ID: {run.info.run_id}")
        print(f"✓ AUTOLOG: Model artifacts (model/, estimator.html) ✓")
        print(f"✓ MANUAL: 6 additional metrics ✓")
        print(f"✓ MANUAL: 3 visualizations (PNG files) ✓")
        print(f"{'='*70}")
        
        return model, {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'roc_auc': roc_auc if y_pred_proba is not None else None,
            **additional_metrics
        }


def main():
    """
    Main function to run Basic level training
    """
    print("\n" + "="*70)
    print(" "*10 + "HOTEL BOOKING CANCELLATION PREDICTION")
    print(" "*15 + "KRITERIA 2 - BASIC LEVEL (2/4 pts)")
    print(" "*15 + "AUTOLOG + MANUAL LOGGING (5+ metrics)")
    print("="*70 + "\n")
    
    # Setup MLflow
    setup_mlflow()
    
    # Load data
    X_train, X_test, y_train, y_test = load_data()
    
    # Train multiple models with autolog + manual logging
    models_to_train = ["RandomForest", "LogisticRegression", "DecisionTree"]
    
    results = {}
    
    for model_name in models_to_train:
        try:
            model, metrics = train_model_enhanced(
                X_train, X_test, y_train, y_test,
                model_name=model_name
            )
            results[model_name] = metrics
            print(f"\n{'✓'*35}")
            print(f"✓ {model_name} training completed successfully!")
            print(f"{'✓'*35}\n")
            
        except Exception as e:
            print(f"\n❌ Error training {model_name}: {str(e)}\n")
            import traceback
            traceback.print_exc()
            continue
    
    # Summary
    print("\n" + "="*70)
    print(" "*20 + "TRAINING SUMMARY")
    print("="*70)
    print(f"✓ Total models trained: {len(results)}")
    print(f"✓ MLflow tracking: http://127.0.0.1:5000")
    print(f"✓ Autolog: ENABLED (model artifacts)")
    print(f"✓ Manual logging: 6 additional metrics + 3 visualizations")
    print("\n" + "="*70)
    print("Models Performance Comparison:")
    print("="*70)
    
    for model_name, metrics in results.items():
        print(f"\n{model_name}:")
        # Show main metrics
        for metric_name in ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']:
            if metric_name in metrics and metrics[metric_name] is not None:
                print(f"  {metric_name}: {metrics[metric_name]:.4f}")
        # Show additional metrics
        print(f"  + 6 additional metrics logged to MLflow")
    
    print("\n" + "="*70)
    print("✅ BASIC LEVEL COMPLETED!")
    print("="*70)
    print("\nNext steps:")
    print("1. Start MLflow UI: mlflow ui --host 127.0.0.1 --port 5000")
    print("2. Open browser: http://localhost:5000 or http://127.0.0.1:5000")
    print("3. Take screenshots showing:")
    print("   - Dashboard with experiments list")
    print("   - Run details showing parameters and metrics")
    print("   - Artifacts page showing:")
    print("     * model/ folder containing:")
    print("       - MLmodel")
    print("       - model.pkl")
    print("       - conda.yaml")
    print("       - python_env.yaml")
    print("       - requirements.txt")
    print("     * estimator.html (for sklearn models)")
    print("     * confusion_matrix_*.png")
    print("     * roc_curve_*.png")
    print("     * metrics_chart_*.png")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
