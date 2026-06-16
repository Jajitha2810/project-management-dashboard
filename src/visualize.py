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
        plt.savefig('results/project_status.png', dpi=150)
        plt.show()
        print("Project status chart saved!")
    
    def plot_progress_tracker(self, projects):
        """Plot progress for all projects"""
        names = [
            p.get('Project Name', 'Unknown')[:15]
            for p in projects
        ]
        progress = [
            p.get('Progress %', 0)
            for p in projects
        ]
        priorities = [
            p.get('Priority', 'Medium')
            for p in projects
        ]
        
        colors = [
            self.colors.get(
                pr.lower(),
                '#9E9E9E'
            )
            for pr in priorities
        ]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        bars = ax.barh(
            names,
            progress,
            color=colors,
            edgecolor='white',
            linewidth=1.5,
            height=0.6
        )
        
        # Add progress labels
        for bar, prog in zip(bars, progress):
            ax.text(
                min(prog + 1, 95),
                bar.get_y() + bar.get_height()/2.,
                f'{prog}%',
                va='center',
                fontweight='bold'
            )
        
        ax.set_xlim(0, 110)
        ax.set_xlabel('Progress (%)')
        ax.set_title(
            'Project Progress Tracker',
            fontsize=14,
            fontweight='bold'
        )
        ax.axvline(x=50, color='gray', linestyle='--', alpha=0.5)
        ax.axvline(x=100, color='green', linestyle='--', alpha=0.5)
        
        # Legend
        legend_patches = [
            mpatches.Patch(
                color=self.colors['high'],
                label='High Priority'
            ),
            mpatches.Patch(
                color=self.colors['medium'],
                label='Medium Priority'
            ),
            mpatches.Patch(
                color=self.colors['low'],
                label='Low Priority'
            )
        ]
        ax.legend(handles=legend_patches, loc='lower right')
        
        plt.tight_layout()
        plt.savefig('results/progress_tracker.png', dpi=150)
        plt.show()
        print("Progress tracker chart saved!")
    
    def plot_timeline(self, projects):
        """Plot project timeline Gantt chart"""
        fig, ax = plt.subplots(figsize=(14, 8))
        
        colors_map = {
            'Completed': self.colors['completed'],
            'In Progress': self.colors['in_progress'],
            'Not Started': self.colors['not_started']
        }
        
        for idx, project in enumerate(projects):
            name = project.get('Project Name', '')[:20]
            start = project.get('Start Date', '')
            end = project.get('End Date', '')
            status = project.get('Status', 'Not Started')
            
            if start and end:
                if isinstance(start, str):
                    start = datetime.strptime(start, '%Y-%m-%d')
                if isinstance(end, str):
                    end = datetime.strptime(end, '%Y-%m-%d')
                
                duration = (end - start).days
                start_num = (
                    start - datetime(2026, 1, 1)
                ).days
                
                color = colors_map.get(status, '#9E9E9E')
                
                ax.barh(
                    idx,
                    duration,
                    left=start_num,
                    color=color,
                    alpha=0.8,
                    edgecolor='white',
                    linewidth=1.5,
                    height=0.6
                )
                
                ax.text(
                    start_num + duration/2,
                    idx,
                    name,
                    ha='center',
                    va='center',
                    fontsize=8,
                    fontweight='bold',
                    color='white'
                )
        
        ax.set_title(
            'Project Timeline (Gantt Chart)',
            fontsize=14,
            fontweight='bold'
        )
        ax.set_xlabel('Days from Jan 2026')
        ax.set_yticks(range(len(projects)))
        ax.set_yticklabels([
            p.get('Project Name', '')[:15]
            for p in projects
        ])
        
        legend_patches = [
            mpatches.Patch(
                color=c,
                label=s
            )
            for s, c in colors_map.items()
        ]
        ax.legend(handles=legend_patches, loc='upper right')
        
        plt.tight_layout()
        plt.savefig('results/timeline.png', dpi=150)
        plt.show()
        print("Timeline chart saved!")
    
    def plot_health_scores(self, project_health):
        """Plot project health scores"""
        names = [ph['name'][:15] for ph in project_health]
        scores = [ph['health'] for ph in project_health]
        
        colors = [
            '#4CAF50' if s >= 70
            else '#FF9800' if s >= 40
            else '#F44336'
            for s in scores
        ]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars = ax.bar(
            names,
            scores,
            color=colors,
            edgecolor='white',
            linewidth=1.5
        )
        
        ax.set_ylim(0, 120)
        ax.axhline(
            y=70,
            color='green',
            linestyle='--',
            alpha=0.7,
            label='Healthy (70+)'
        )
        ax.axhline(
            y=40,
            color='orange',
            linestyle='--',
            alpha=0.7,
            label='At Risk (40-70)'
        )
        
        for bar, score in zip(bars, scores):
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                bar.get_height() + 1,
                f'{score}%',
                ha='center',
                fontweight='bold'
            )
        
        ax.set_title(
            'Project Health Scores',
            fontsize=14,
            fontweight='bold'
        )
        ax.set_ylabel('Health Score (%)')
        ax.legend()
        
        plt.tight_layout()
        plt.savefig('results/health_scores.png', dpi=150)
        plt.show()
        print("Health scores chart saved!")


if __name__ == "__main__":
    visualizer = DashboardVisualizer()
    print("Dashboard Visualizer initialized successfully!")
