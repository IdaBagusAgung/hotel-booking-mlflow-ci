"""
Hotel Booking Cancellation Prediction - ADVANCE Level (KRITERIA 2 - ADVANCE)
Author: gus_agung
Description: ML model with DagsHub integration, manual logging, and advanced metrics
Level: Advance (4/4 pts)

Features:
- DagsHub MLflow tracking (online)
- Manual logging (not autolog)
- Hyperparameter tuning
- Advanced metrics beyond autolog
"""

import os
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
import dagshub
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, classification_report,
    confusion_matrix, precision_recall_curve, roc_curve,
    matthews_corrcoef, cohen_kappa_score, log_loss
)
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass


def setup_dagshub_mlflow():
    """
    Setup DagsHub and MLflow tracking (ADVANCE LEVEL)
    """
    print("="*70)
    print(" "*15 + "DAGSHUB + MLFLOW SETUP - ADVANCE LEVEL")
    print("="*70)
    
    # Get DagsHub credentials from environment
    username = os.getenv('DAGSHUB_USERNAME', 'gus_agung')
    repo = os.getenv('DAGSHUB_REPO', 'hotel-booking-mlflow')
    token = os.getenv('DAGSHUB_TOKEN', '')
    
    # Initialize DagsHub
    dagshub.init(repo_owner=username, repo_name=repo, mlflow=True)
    
    # Set MLflow tracking URI to DagsHub
    mlflow_tracking_uri = f"https://dagshub.com/{username}/{repo}.mlflow"
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    
    # Set DagsHub credentials for MLflow
    os.environ['MLFLOW_TRACKING_USERNAME'] = username
    os.environ['MLFLOW_TRACKING_PASSWORD'] = token
    
    # Set experiment
    experiment_name = "hotel_booking_advance_experiments"
    mlflow.set_experiment(experiment_name)
    
    print(f"✓ DagsHub Repository: https://dagshub.com/{username}/{repo}")
    print(f"✓ MLflow Tracking URI: {mlflow_tracking_uri}")
    print(f"✓ Experiment: {experiment_name}")
    print(f"✓ Manual Logging: ENABLED (Advance Level)")
    print(f"✓ Advanced Metrics: ENABLED (+2 beyond autolog)")
    print("="*70 + "\n")
    
    return mlflow_tracking_uri


def load_data(data_dir='hotel_bookings_preprocessed'):
    """
    Load preprocessed data
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


def calculate_advanced_metrics(y_true, y_pred, y_pred_proba):
    """
    Calculate advanced metrics beyond autolog (ADVANCE LEVEL REQUIREMENT)
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        y_pred_proba: Predicted probabilities
        
    Returns:
        dict: Dictionary of advanced metrics
    """
    metrics = {}
    
    # Standard metrics (same as autolog)
    metrics['accuracy'] = accuracy_score(y_true, y_pred)
    metrics['precision_weighted'] = precision_score(y_true, y_pred, average='weighted')
    metrics['recall_weighted'] = recall_score(y_true, y_pred, average='weighted')
    metrics['f1_weighted'] = f1_score(y_true, y_pred, average='weighted')
    metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba)
    
    # Per-class metrics
    precision_per_class = precision_score(y_true, y_pred, average=None)
    recall_per_class = recall_score(y_true, y_pred, average=None)
    f1_per_class = f1_score(y_true, y_pred, average=None)
    
    metrics['precision_class_0'] = precision_per_class[0]
    metrics['precision_class_1'] = precision_per_class[1]
    metrics['recall_class_0'] = recall_per_class[0]
    metrics['recall_class_1'] = recall_per_class[1]
    metrics['f1_class_0'] = f1_per_class[0]
    metrics['f1_class_1'] = f1_per_class[1]
    
    # ADVANCED METRICS (Beyond autolog - ADVANCE LEVEL REQUIREMENT)
    # 1. Matthews Correlation Coefficient
    metrics['matthews_corrcoef'] = matthews_corrcoef(y_true, y_pred)
    
    # 2. Cohen's Kappa Score
    metrics['cohen_kappa'] = cohen_kappa_score(y_true, y_pred)
    
    # 3. Log Loss
    metrics['log_loss'] = log_loss(y_true, y_pred_proba)
    
    # 4. Specificity (True Negative Rate)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    metrics['specificity'] = tn / (tn + fp) if (tn + fp) > 0 else 0
    
    # 5. Balanced Accuracy
    metrics['balanced_accuracy'] = (metrics['recall_class_0'] + metrics['recall_class_1']) / 2
    
    # 6. Geometric Mean
    metrics['geometric_mean'] = np.sqrt(metrics['recall_class_0'] * metrics['recall_class_1'])
    
    return metrics


def plot_confusion_matrix(y_true, y_pred, model_name):
    """
    Plot and save confusion matrix
    """
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Not Canceled', 'Canceled'],
                yticklabels=['Not Canceled', 'Canceled'])
    plt.title(f'Confusion Matrix - {model_name}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    
    # Save plot
    plot_path = f'confusion_matrix_{model_name}.png'
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return plot_path


def plot_roc_curve(y_true, y_pred_proba, model_name):
    """
    Plot and save ROC curve
    """
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
    
    # Save plot
    plot_path = f'roc_curve_{model_name}.png'
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return plot_path


def train_model_with_tuning(X_train, X_test, y_train, y_test, model_type="RandomForest"):
    """
    Train model with hyperparameter tuning and MANUAL LOGGING to DagsHub
    (ADVANCE LEVEL REQUIREMENT)
    
    Args:
        X_train, X_test, y_train, y_test: Training and test data
        model_type: Type of model to train
    """
    print("\n" + "="*70)
    print(f"TRAINING {model_type} WITH MANUAL LOGGING (ADVANCE LEVEL)")
    print("="*70)
    
    # Define hyperparameter grids
    if model_type == "RandomForest":
        model = RandomForestClassifier(random_state=42, n_jobs=-1)
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2]
        }
    elif model_type == "GradientBoosting":
        model = GradientBoostingClassifier(random_state=42)
        param_grid = {
            'n_estimators': [100, 200],
            'learning_rate': [0.01, 0.1],
            'max_depth': [3, 5],
            'subsample': [0.8, 1.0]
        }
    elif model_type == "LogisticRegression":
        model = LogisticRegression(random_state=42, max_iter=1000, n_jobs=-1)
        param_grid = {
            'C': [0.1, 1, 10],
            'penalty': ['l2'],
            'solver': ['lbfgs', 'saga']
        }
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    # Start MLflow run with MANUAL LOGGING
    with mlflow.start_run(run_name=f"{model_type}_tuned_manual"):
        
        print(f"\n[INFO] Performing GridSearchCV for {model_type}...")
        
        # Grid Search with Cross-Validation
        grid_search = GridSearchCV(
            model, param_grid,
            cv=3,
            scoring='roc_auc',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        # Get best model
        best_model = grid_search.best_estimator_
        best_params = grid_search.best_params_
        best_score = grid_search.best_score_
        
        print(f"\n✓ Best hyperparameters found:")
        for param, value in best_params.items():
            print(f"  {param}: {value}")
        print(f"✓ Best CV ROC-AUC: {best_score:.4f}")
        
        # MANUAL LOGGING - Log parameters (ADVANCE LEVEL)
        mlflow.log_params(best_params)
        mlflow.log_param("model_type", model_type)
        mlflow.log_param("cv_folds", 3)
        mlflow.log_param("tuning_metric", "roc_auc")
        
        # Make predictions
        y_pred = best_model.predict(X_test)
        y_pred_proba = best_model.predict_proba(X_test)[:, 1]
        
        # Calculate all metrics including advanced ones
        metrics = calculate_advanced_metrics(y_test, y_pred, y_pred_proba)
        
        # MANUAL LOGGING - Log all metrics (ADVANCE LEVEL)
        mlflow.log_metrics(metrics)
        mlflow.log_metric("best_cv_score", best_score)
        
        # Print results
        print(f"\n{'='*70}")
        print(f"MODEL PERFORMANCE - {model_type}")
        print(f"{'='*70}")
        print(f"Standard Metrics:")
        print(f"  Accuracy:        {metrics['accuracy']:.4f}")
        print(f"  Precision (weighted): {metrics['precision_weighted']:.4f}")
        print(f"  Recall (weighted):    {metrics['recall_weighted']:.4f}")
        print(f"  F1-Score (weighted):  {metrics['f1_weighted']:.4f}")
        print(f"  ROC-AUC:         {metrics['roc_auc']:.4f}")
        print(f"\nAdvanced Metrics (Beyond Autolog):")
        print(f"  Matthews Correlation: {metrics['matthews_corrcoef']:.4f}")
        print(f"  Cohen's Kappa:        {metrics['cohen_kappa']:.4f}")
        print(f"  Log Loss:             {metrics['log_loss']:.4f}")
        print(f"  Specificity:          {metrics['specificity']:.4f}")
        print(f"  Balanced Accuracy:    {metrics['balanced_accuracy']:.4f}")
        print(f"  Geometric Mean:       {metrics['geometric_mean']:.4f}")
        print(f"{'='*70}\n")
        
        # Classification report
        print("Classification Report:")
        print(classification_report(y_test, y_pred, 
                                   target_names=['Not Canceled', 'Canceled']))
        
        # Create and log visualizations
        print("\n[INFO] Creating visualizations...")
        
        # Confusion Matrix
        cm_path = plot_confusion_matrix(y_test, y_pred, model_type)
        mlflow.log_artifact(cm_path)
        print(f"✓ Confusion matrix saved and logged")
        
        # ROC Curve
        roc_path = plot_roc_curve(y_test, y_pred_proba, model_type)
        mlflow.log_artifact(roc_path)
        print(f"✓ ROC curve saved and logged")
        
        # Feature importance (if available)
        if hasattr(best_model, 'feature_importances_'):
            feature_importance = pd.DataFrame({
                'feature': X_train.columns,
                'importance': best_model.feature_importances_
            }).sort_values('importance', ascending=False).head(20)
            
            plt.figure(figsize=(10, 8))
            sns.barplot(data=feature_importance, x='importance', y='feature')
            plt.title(f'Top 20 Feature Importances - {model_type}')
            plt.xlabel('Importance')
            plt.tight_layout()
            
            fi_path = f'feature_importance_{model_type}.png'
            plt.savefig(fi_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            mlflow.log_artifact(fi_path)
            print(f"✓ Feature importance plot saved and logged")
        
        # MANUAL LOGGING - Save model locally (DagsHub doesn't support log_model)
        # Save model to local folder
        import joblib
        os.makedirs('models', exist_ok=True)
        model_path = f'models/{model_type}_best_model.pkl'
        joblib.dump(best_model, model_path)
        print(f"✓ Model saved locally: {model_path}")
        
        # Try to log model to MLflow (may fail on DagsHub free tier)
        try:
            mlflow.sklearn.log_model(best_model, "model")
            print(f"✓ Model logged to MLflow")
        except Exception as log_error:
            print(f"⚠ Model artifact logging skipped (DagsHub limitation): {str(log_error)}")
            # Log the local model path as artifact instead
            mlflow.log_artifact(model_path)
            print(f"✓ Model file uploaded as artifact instead")
        
        # Log tags
        mlflow.set_tags({
            "model_type": model_type,
            "level": "ADVANCE",
            "tuning": "GridSearchCV",
            "logging": "Manual",
            "platform": "DagsHub",
            "local_model_path": model_path
        })
        
        # Get run info
        run = mlflow.active_run()
        print(f"\n✓ MLflow Run ID: {run.info.run_id}")
        print(f"✓ View on DagsHub: https://dagshub.com/{os.getenv('DAGSHUB_USERNAME')}/{os.getenv('DAGSHUB_REPO')}/experiments")
        
        return best_model, metrics


def main():
    """
    Main function to run ADVANCE level training
    """
    print("\n" + "="*70)
    print(" "*10 + "HOTEL BOOKING CANCELLATION PREDICTION")
    print(" "*12 + "KRITERIA 2 - ADVANCE LEVEL (4/4 pts)")
    print(" "*15 + "DagsHub + Manual Logging + Tuning")
    print("="*70 + "\n")
    
    # Setup DagsHub and MLflow
    tracking_uri = setup_dagshub_mlflow()
    
    # Load data
    X_train, X_test, y_train, y_test = load_data()
    
    # Train multiple models with tuning
    models_to_train = ["RandomForest", "GradientBoosting", "LogisticRegression"]
    
    results = {}
    
    for model_type in models_to_train:
        try:
            print(f"\n{'='*70}")
            print(f"TRAINING {model_type} WITH MANUAL LOGGING (ADVANCE LEVEL)")
            print(f"{'='*70}\n")
            
            model, metrics = train_model_with_tuning(
                X_train, X_test, y_train, y_test,
                model_type=model_type
            )
            
            # Add to results
            results[model_type] = {
                'model': model,
                **metrics  # Unpack all metrics
            }
            
            print(f"\n{'✓'*35}")
            print(f"✓ {model_type} training completed successfully!")
            print(f"{'✓'*35}\n")
            
        except Exception as e:
            print(f"\n❌ Critical error training {model_type}: {str(e)}\n")
            import traceback
            traceback.print_exc()
            continue  # Continue with next model
    
    # Summary
    print("\n" + "="*70)
    print(" "*20 + "TRAINING SUMMARY")
    print("="*70)
    print(f"✓ Total models trained: {len(results)}")
    print(f"✓ MLflow tracking: DagsHub (Online)")
    print(f"✓ Manual logging: ENABLED")
    print(f"✓ Hyperparameter tuning: GridSearchCV")
    print(f"✓ Advanced metrics: +6 beyond autolog")
    
    if not results:
        print("\n❌ No models were successfully trained!")
        print("Please check the errors above and try again.")
        return
    
    print("\n" + "="*70)
    print("Models Performance Comparison:")
    print("="*70)
    
    for model_type, model_data in results.items():
        print(f"\n{model_type}:")
        print(f"  Accuracy:             {model_data['accuracy']:.4f}")
        print(f"  ROC-AUC:              {model_data['roc_auc']:.4f}")
        print(f"  Matthews Correlation: {model_data['matthews_corrcoef']:.4f}")
        print(f"  Cohen's Kappa:        {model_data['cohen_kappa']:.4f}")
    
    # Find best model
    best_model_type = max(results.items(), key=lambda x: x[1]['roc_auc'])[0]
    best_roc_auc = results[best_model_type]['roc_auc']
    
    print("\n" + "="*70)
    print(f"🏆 BEST MODEL: {best_model_type}")
    print(f"   ROC-AUC: {best_roc_auc:.4f}")
    print("="*70)
    
    print("\n" + "="*70)
    print("✅ ADVANCE LEVEL COMPLETED!")
    print("="*70)
    print("\nNext steps:")
    print(f"1. View on DagsHub: https://dagshub.com/{os.getenv('DAGSHUB_USERNAME')}/{os.getenv('DAGSHUB_REPO')}")
    print("2. Navigate to Experiments tab")
    print("3. Take screenshots:")
    print("   - Dashboard showing all experiments")
    print("   - Individual run showing all metrics")
    print("   - Artifacts page showing model and plots")
    print("   - Compare runs view")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
