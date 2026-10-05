"""
Student Academic Performance Analysis System
Multi-variable regression and educational data analytics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

def generate_academic_data():
    """Generate synthetic student academic data"""
    np.random.seed(42)
    n_students = 500
    
    data = {
        'Student_ID': range(1, n_students + 1),
        'Attendance': np.random.uniform(60, 100, n_students),
        'Internal_Assessment': np.random.uniform(40, 100, n_students),
        'Assignment_Score': np.random.uniform(30, 100, n_students),
        'Study_Hours': np.random.uniform(2, 10, n_students),
        'Classroom_Participation': np.random.uniform(0, 100, n_students),
        'Previous_Performance': np.random.uniform(40, 95, n_students),
        'Lab_Work': np.random.uniform(30, 100, n_students),
        'Project_Score': np.random.uniform(40, 100, n_students)
    }
    
    df = pd.DataFrame(data)
    
    # Generate final performance based on features
    df['Final_Performance'] = (
        0.15 * df['Attendance'] +
        0.20 * df['Internal_Assessment'] +
        0.15 * df['Assignment_Score'] +
        0.10 * df['Study_Hours'] * 5 +
        0.10 * df['Classroom_Participation'] +
        0.15 * df['Previous_Performance'] +
        0.10 * df['Lab_Work'] +
        0.05 * df['Project_Score'] +
        np.random.normal(0, 5, n_students)
    )
    
    df['Final_Performance'] = df['Final_Performance'].clip(0, 100)
    df.to_csv('/home/ubuntu/academic_data.csv', index=False)
    
    return df

def train_models(df):
    """Train regression models"""
    X = df[['Attendance', 'Internal_Assessment', 'Assignment_Score', 
             'Study_Hours', 'Classroom_Participation', 'Previous_Performance',
             'Lab_Work', 'Project_Score']]
    y = df['Final_Performance']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    results = {}
    
    # Linear Regression
    lr_model = LinearRegression()
    lr_model.fit(X_train_scaled, y_train)
    y_pred_lr = lr_model.predict(X_test_scaled)
    results['Linear Regression'] = {
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_lr)),
        'MAE': mean_absolute_error(y_test, y_pred_lr),
        'R2': r2_score(y_test, y_pred_lr),
        'predictions': y_pred_lr
    }
    
    # Random Forest
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    results['Random Forest'] = {
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_rf)),
        'MAE': mean_absolute_error(y_test, y_pred_rf),
        'R2': r2_score(y_test, y_pred_rf),
        'predictions': y_pred_rf,
        'feature_importance': rf_model.feature_importances_
    }
    
    # Gradient Boosting
    gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    gb_model.fit(X_train, y_train)
    y_pred_gb = gb_model.predict(X_test)
    results['Gradient Boosting'] = {
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_gb)),
        'MAE': mean_absolute_error(y_test, y_pred_gb),
        'R2': r2_score(y_test, y_pred_gb),
        'predictions': y_pred_gb,
        'feature_importance': gb_model.feature_importances_
    }
    
    return results, X_test, y_test, X.columns

def generate_visualizations(df, results, X_test, y_test, feature_names):
    """Generate performance visualizations"""
    
    # 1. Performance Distribution
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Student Academic Performance Analysis', fontsize=16, fontweight='bold')
    
    axes[0, 0].hist(df['Final_Performance'], bins=30, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Final Performance Distribution')
    axes[0, 0].set_xlabel('Performance Score')
    axes[0, 0].set_ylabel('Frequency')
    
    axes[0, 1].scatter(df['Attendance'], df['Final_Performance'], alpha=0.6, color='green')
    axes[0, 1].set_title('Attendance vs Final Performance')
    axes[0, 1].set_xlabel('Attendance %')
    axes[0, 1].set_ylabel('Final Performance')
    
    axes[1, 0].scatter(df['Study_Hours'], df['Final_Performance'], alpha=0.6, color='orange')
    axes[1, 0].set_title('Study Hours vs Final Performance')
    axes[1, 0].set_xlabel('Study Hours/Day')
    axes[1, 0].set_ylabel('Final Performance')
    
    axes[1, 1].scatter(df['Previous_Performance'], df['Final_Performance'], alpha=0.6, color='red')
    axes[1, 1].set_title('Previous vs Current Performance')
    axes[1, 1].set_xlabel('Previous Performance')
    axes[1, 1].set_ylabel('Final Performance')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/academic_performance_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Model Comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    models = list(results.keys())
    rmse_vals = [results[m]['RMSE'] for m in models]
    mae_vals = [results[m]['MAE'] for m in models]
    r2_vals = [results[m]['R2'] for m in models]
    
    x = np.arange(len(models))
    width = 0.25
    
    ax.bar(x - width, rmse_vals, width, label='RMSE', color='skyblue')
    ax.bar(x, mae_vals, width, label='MAE', color='lightcoral')
    ax.bar(x + width, r2_vals, width, label='R² Score', color='lightgreen')
    
    ax.set_xlabel('Models', fontweight='bold')
    ax.set_ylabel('Score', fontweight='bold')
    ax.set_title('Model Performance Comparison', fontweight='bold', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/academic_model_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Predictions vs Actual
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle('Predictions vs Actual Performance', fontsize=14, fontweight='bold')
    
    for idx, model_name in enumerate(results.keys()):
        y_pred = results[model_name]['predictions']
        axes[idx].scatter(y_test, y_pred, alpha=0.6, color='blue')
        axes[idx].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        axes[idx].set_xlabel('Actual Performance')
        axes[idx].set_ylabel('Predicted Performance')
        axes[idx].set_title(f'{model_name}\nR² = {results[model_name]["R2"]:.4f}')
        axes[idx].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/academic_predictions_vs_actual.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Feature Importance
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Feature Importance Analysis', fontsize=14, fontweight='bold')
    
    for idx, model_name in enumerate(['Random Forest', 'Gradient Boosting']):
        importance = results[model_name]['feature_importance']
        sorted_idx = np.argsort(importance)
        
        axes[idx].barh(range(len(sorted_idx)), importance[sorted_idx], color='steelblue')
        axes[idx].set_yticks(range(len(sorted_idx)))
        axes[idx].set_yticklabels([feature_names[i] for i in sorted_idx])
        axes[idx].set_xlabel('Importance')
        axes[idx].set_title(f'{model_name} Feature Importance')
        axes[idx].grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/academic_feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Subject-wise Analysis
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Subject-wise Academic Analysis', fontsize=16, fontweight='bold')
    
    axes[0, 0].boxplot([df['Internal_Assessment'], df['Assignment_Score'], df['Lab_Work']])
    axes[0, 0].set_xticklabels(['Internal', 'Assignment', 'Lab'])
    axes[0, 0].set_title('Assessment Scores Distribution')
    axes[0, 0].set_ylabel('Score')
    axes[0, 0].grid(alpha=0.3)
    
    axes[0, 1].hist(df['Classroom_Participation'], bins=20, color='purple', edgecolor='black', alpha=0.7)
    axes[0, 1].set_title('Classroom Participation Distribution')
    axes[0, 1].set_xlabel('Participation Score')
    axes[0, 1].set_ylabel('Frequency')
    
    axes[1, 0].scatter(df['Internal_Assessment'], df['Assignment_Score'], alpha=0.6, color='teal')
    axes[1, 0].set_title('Internal Assessment vs Assignment Score')
    axes[1, 0].set_xlabel('Internal Assessment')
    axes[1, 0].set_ylabel('Assignment Score')
    axes[1, 0].grid(alpha=0.3)
    
    axes[1, 1].scatter(df['Lab_Work'], df['Project_Score'], alpha=0.6, color='brown')
    axes[1, 1].set_title('Lab Work vs Project Score')
    axes[1, 1].set_xlabel('Lab Work')
    axes[1, 1].set_ylabel('Project Score')
    axes[1, 1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/academic_subject_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Visualizations generated successfully!")

def save_model_results(results):
    """Save model results to CSV"""
    results_data = []
    for model_name, metrics in results.items():
        results_data.append({
            'Model': model_name,
            'RMSE': round(metrics['RMSE'], 4),
            'MAE': round(metrics['MAE'], 4),
            'R2_Score': round(metrics['R2'], 4)
        })
    
    df_results = pd.DataFrame(results_data)
    df_results.to_csv('/home/ubuntu/academic_model_results.csv', index=False)
    print("\nModel Results:")
    print(df_results)

def main():
    print("Generating student academic data...")
    df = generate_academic_data()
    
    print("Training regression models...")
    results, X_test, y_test, feature_names = train_models(df)
    
    print("Generating visualizations...")
    generate_visualizations(df, results, X_test, y_test, feature_names)
    
    print("Saving model results...")
    save_model_results(results)
    
    print("\nAcademic Performance Analysis System completed successfully!")

if __name__ == "__main__":
    main()
