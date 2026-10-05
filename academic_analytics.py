"""
Academic Analytics and Reporting Utilities
"""

import pandas as pd
import numpy as np

def generate_analytics():
    """Generate detailed analytics datasets"""
    
    # Load academic data
    df = pd.read_csv('/home/ubuntu/academic_data.csv')
    
    # 1. Performance Statistics
    perf_stats = pd.DataFrame({
        'Metric': ['Mean Performance', 'Median Performance', 'Std Dev', 'Min Score', 'Max Score', 'Pass Rate (>60%)'],
        'Value': [
            round(df['Final_Performance'].mean(), 2),
            round(df['Final_Performance'].median(), 2),
            round(df['Final_Performance'].std(), 2),
            round(df['Final_Performance'].min(), 2),
            round(df['Final_Performance'].max(), 2),
            round((df['Final_Performance'] >= 60).sum() / len(df) * 100, 2)
        ]
    })
    perf_stats.to_csv('/home/ubuntu/academic_performance_statistics.csv', index=False)
    
    # 2. Subject-wise Analysis
    subject_analysis = pd.DataFrame({
        'Subject': ['Internal Assessment', 'Assignment Score', 'Lab Work', 'Project Score', 'Classroom Participation'],
        'Mean': [
            round(df['Internal_Assessment'].mean(), 2),
            round(df['Assignment_Score'].mean(), 2),
            round(df['Lab_Work'].mean(), 2),
            round(df['Project_Score'].mean(), 2),
            round(df['Classroom_Participation'].mean(), 2)
        ],
        'Std Dev': [
            round(df['Internal_Assessment'].std(), 2),
            round(df['Assignment_Score'].std(), 2),
            round(df['Lab_Work'].std(), 2),
            round(df['Project_Score'].std(), 2),
            round(df['Classroom_Participation'].std(), 2)
        ],
        'Min': [
            round(df['Internal_Assessment'].min(), 2),
            round(df['Assignment_Score'].min(), 2),
            round(df['Lab_Work'].min(), 2),
            round(df['Project_Score'].min(), 2),
            round(df['Classroom_Participation'].min(), 2)
        ],
        'Max': [
            round(df['Internal_Assessment'].max(), 2),
            round(df['Assignment_Score'].max(), 2),
            round(df['Lab_Work'].max(), 2),
            round(df['Project_Score'].max(), 2),
            round(df['Classroom_Participation'].max(), 2)
        ]
    })
    subject_analysis.to_csv('/home/ubuntu/academic_subject_analysis.csv', index=False)
    
    # 3. Correlation Analysis
    correlation_matrix = df[['Attendance', 'Internal_Assessment', 'Assignment_Score', 
                              'Study_Hours', 'Classroom_Participation', 'Previous_Performance',
                              'Lab_Work', 'Project_Score', 'Final_Performance']].corr()
    correlation_matrix.to_csv('/home/ubuntu/academic_correlation_matrix.csv')
    
    # 4. Performance Categories
    df['Performance_Category'] = pd.cut(df['Final_Performance'], 
                                        bins=[0, 40, 60, 75, 90, 100],
                                        labels=['Poor', 'Average', 'Good', 'Very Good', 'Excellent'])
    
    category_dist = df['Performance_Category'].value_counts().sort_index()
    category_df = pd.DataFrame({
        'Category': category_dist.index,
        'Count': category_dist.values,
        'Percentage': np.round(category_dist.values / len(df) * 100, 2)
    })
    category_df.to_csv('/home/ubuntu/academic_performance_categories.csv', index=False)
    
    # 5. At-Risk Students Analysis
    at_risk = df[df['Final_Performance'] < 60].copy()
    at_risk_summary = pd.DataFrame({
        'Metric': ['Total At-Risk Students', 'Avg Attendance', 'Avg Internal Assessment', 
                   'Avg Study Hours', 'Avg Classroom Participation'],
        'Value': [
            len(at_risk),
            round(at_risk['Attendance'].mean(), 2),
            round(at_risk['Internal_Assessment'].mean(), 2),
            round(at_risk['Study_Hours'].mean(), 2),
            round(at_risk['Classroom_Participation'].mean(), 2)
        ]
    })
    at_risk_summary.to_csv('/home/ubuntu/academic_at_risk_analysis.csv', index=False)
    
    # 6. Attendance Impact
    attendance_bins = pd.cut(df['Attendance'], bins=[0, 70, 80, 90, 100])
    attendance_impact = df.groupby(attendance_bins).agg({
        'Final_Performance': ['mean', 'count', 'std']
    }).round(2)
    attendance_impact.columns = ['Avg_Performance', 'Student_Count', 'Std_Dev']
    attendance_impact.to_csv('/home/ubuntu/academic_attendance_impact.csv')
    
    # 7. Study Hours Impact
    study_bins = pd.cut(df['Study_Hours'], bins=[0, 3, 5, 7, 10])
    study_impact = df.groupby(study_bins).agg({
        'Final_Performance': ['mean', 'count', 'std']
    }).round(2)
    study_impact.columns = ['Avg_Performance', 'Student_Count', 'Std_Dev']
    study_impact.to_csv('/home/ubuntu/academic_study_hours_impact.csv')
    
    # 8. Top Performers
    top_performers = df.nlargest(10, 'Final_Performance')[['Student_ID', 'Attendance', 
                                                             'Internal_Assessment', 'Study_Hours', 
                                                             'Final_Performance']]
    top_performers.to_csv('/home/ubuntu/academic_top_performers.csv', index=False)
    
    print("Analytics generated successfully!")
    print("\nPerformance Statistics:")
    print(perf_stats)
    print("\nSubject-wise Analysis:")
    print(subject_analysis)
    print("\nPerformance Categories:")
    print(category_df)
    print("\nAt-Risk Students Summary:")
    print(at_risk_summary)

if __name__ == "__main__":
    generate_analytics()
