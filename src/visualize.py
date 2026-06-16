import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime

class DashboardVisualizer:
    """
    Visualization tools for Project Management Dashboard.
    Creates charts and graphs for project tracking.
    
    Author: Jajitha
    Course: Project Management Tracker - Coursera
    """
    
    def __init__(self):
        plt.style.use('seaborn-v0_8')
        self.colors = {
            'completed': '#4CAF50',
            'in_progress': '#2196F3',
            'not_started': '#F44336',
            'high': '#FF5722',
            'medium': '#FF9800',
            'low': '#8BC34A'
        }
    
    def plot_project_status(self, projects):
        """Plot project status distribution"""
        statuses = [p.get('Status', 'Unknown') for p in projects]
        status_counts = {}
        for status in statuses:
            status_counts[status] = status_counts.get(status, 0) + 1
        
        colors = [
            self.colors.get(
                s.lower().replace(' ', '_'),
                '#9E9E9E'
            )
            for s in status_counts.keys()
        ]
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Pie chart
        axes[0].pie(
            status_counts.values(),
            labels=status_counts.keys(),
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            shadow=True
        )
        axes[0].set_title(
            'Project Status Distribution',
            fontsize=14,
            fontweight='bold'
        )
        
        # Bar chart
        bars = axes[1].bar(
            status_counts.keys(),
            status_counts.values(),
            color=colors,
            edgecolor='white',
            linewidth=1.5
        )
        axes[1].set_title(
            'Projects by Status',
            fontsize=14,
            fontweight='bold'
        )
        axes[1].set_ylabel('Number of Projects')
        
        for bar in bars:
            axes[1].text(
                bar.get_x() + bar.get_width()/2.,
                bar.get_height() + 0.1,
                str(int(bar.get_height())),
                ha='center',
                fontweight='bold'
            )
        
        plt.tight_layout()
        plt.savefig('results/project_status.png'
