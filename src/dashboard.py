import pandas as pd
import numpy as np
from datetime import datetime
from excel_handler import ExcelHandler

class ProjectDashboard:
    """
    Core Project Management Dashboard
    for tracking projects, tasks and team.
    
    Author: Jajitha
    Course: Project Management Tracker - Coursera
    """
    
    def __init__(self):
        self.excel = ExcelHandler()
        self.projects = []
        self.tasks = []
        self.team = []
    
    def load_data(self):
        """Load all data from Excel"""
        try:
            df = self.excel.read_projects()
            if df is not None:
                self.projects = df.to_dict('records')
                print(f"Loaded {len(self.projects)} projects!")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def get_overall_statistics(self):
        """Calculate overall project statistics"""
        if not self.projects:
            return {}
        
        total = len(self.projects)
        completed = len([
            p for p in self.projects
            if p.get('Status') == 'Completed'
        ])
        in_progress = len([
            p for p in self.projects
            if p.get('Status') == 'In Progress'
        ])
        not_started = len([
            p for p in self.projects
            if p.get('Status') == 'Not Started'
        ])
        
        progress_values = [
            p.get('Progress %', 0)
            for p in self.projects
            if p.get('Progress %') is not None
        ]
        avg_progress = np.mean(progress_values) if progress_values else 0
        
        high_priority = len([
            p for p in self.projects
            if p.get('Priority') == 'High'
        ])
        
        return {
            'total_projects': total,
            'completed': completed,
            'in_progress': in_progress,
            'not_started': not_started,
            'completion_rate': f"{(completed/total)*100:.1f}%",
            'average_progress': f"{avg_progress:.1f}%",
            'high_priority_count': high_priority
        }
    
    def get_project_by_id(self, project_id):
        """Get specific project by ID"""
        for project in self.projects:
            if project.get('Project ID') == project_id:
                return project
        return None
    
    def get_overdue_projects(self):
        """Get all overdue projects"""
        overdue = []
        today = datetime.now()
        
        for project in self.projects:
            end_date = project.get('End Date')
            status = project.get('Status')
            
            if end_date and status != 'Completed':
                if isinstance(end_date, str):
                    end_date = datetime.strptime(
                        end_date, '%Y-%m-%d'
                    )
                if end_date < today:
                    overdue.append(project)
        
        return overdue
    
    def get_projects_by_status(self, status):
        """Filter projects by status"""
        return [
            p for p in self.projects
            if p.get('Status') == status
        ]
    
    def get_projects_by_priority(self, priority):
        """Filter projects by priority"""
        return [
            p for p in self.projects
            if p.get('Priority') == priority
        ]
    
    def calculate_project_health(self, project):
        """
        Calculate project health score 0-100
        based on progress, deadline, priority
        """
        score = 100
        progress = project.get('Progress %', 0)
        status = project.get('Status', '')
        
        if status == 'Completed':
            return 100
        
        if status == 'Not Started':
            score -= 30
        
        end_date = project.get('End Date')
        if end_date:
            if isinstance(end_date, str):
                end_date = datetime.strptime(
                    end_date, '%Y-%m-%d'
                )
            days_left = (end_date - datetime.now()).days
            
            if days_left < 0:
                score -= 40
            elif days_left < 7:
                score -= 20
            elif days_left < 30:
                score -= 10
        
        if progress < 25:
            score -= 15
        elif progress < 50:
            score -= 10
        
        return max(0, min(100, score))
    
    def get_dashboard_summary(self):
        """Get complete dashboard summary"""
        stats = self.get_overall_statistics()
        overdue = self.get_overdue_projects()
        
        project_health = []
        for project in self.projects:
            health = self.calculate_project_health(project)
            project_health.append({
                'name': project.get('Project Name'),
                'health': health,
                'status': project.get('Status'),
                'progress': project.get('Progress %', 0)
            })
        
        return {
            'statistics': stats,
            'overdue_count': len(overdue),
            'overdue_projects': overdue,
            'project_health': project_health
        }
    
    def print_dashboard(self):
        """Print dashboard to console"""
        print("\n" + "="*50)
        print("   PROJECT MANAGEMENT DASHBOARD")
        print("   Author: Jajitha")
        print("="*50)
        
        summary = self.get_dashboard_summary()
        stats = summary['statistics']
        
        if not stats:
            print("No projects found!")
            return
        
        print(f"\nTotal Projects  : {stats['total_projects']}")
        print(f"Completed       : {stats['completed']}")
        print(f"In Progress     : {stats['in_progress']}")
        print(f"Not Started     : {stats['not_started']}")
        print(f"Completion Rate : {stats['completion_rate']}")
        print(f"Avg Progress    : {stats['average_progress']}")
        print(f"High Priority   : {stats['high_priority_count']}")
        
        if summary['overdue_count'] > 0:
            print(f"\n⚠️  Overdue Projects: {summary['overdue_count']}")
            for p in summary['overdue_projects']:
                print(f"   - {p.get('Project Name')}")
        
        print("\nProject Health Scores:")
        print("-"*40)
        for ph in summary['project_health']:
            bar_length = int(ph['health'] / 5)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(
                f"{ph['name'][:20]:<20} "
                f"[{bar}] {ph['health']}%"
            )
        
        print("="*50)


if __name__ == "__main__":
    dashboard = ProjectDashboard()
    dashboard.excel.create_workbook()
    dashboard.load_data()
    dashboard.print_dashboard()
