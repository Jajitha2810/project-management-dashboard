from excel_handler import ExcelHandler
from dashboard import ProjectDashboard
from visualize import DashboardVisualizer

def main():
    """
    Main entry point for Project Management Dashboard
    
    Author: Jajitha
    Course: Project Management Tracker - Coursera
    """
    
    print("="*60)
    print("   PROJECT MANAGEMENT DASHBOARD")
    print("   Author: Jajitha")
    print("   Course: Project Management Tracker - Coursera")
    print("="*60)
    
    # Initialize components
    print("\nInitializing dashboard...")
    excel = ExcelHandler()
    dashboard = ProjectDashboard()
    visualizer = DashboardVisualizer()
    
    # Create Excel workbook if not exists
    import os
    if not os.path.exists('data/projects.xlsx'):
        print("\nCreating new Excel workbook...")
        excel.create_workbook()
    
    # Load data
    print("\nLoading project data...")
    dashboard.load_data()
    
    # Print dashboard summary
    dashboard.print_dashboard()
    
    # Get projects for visualization
    projects = dashboard.projects
    
    if not projects:
        print("\nNo projects found!")
        print("Please add projects to data/projects.xlsx")
        return
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    
    print("\n1. Project Status Distribution...")
    visualizer.plot_project_status(projects)
    
    print("\n2. Progress Tracker...")
    visualizer.plot_progress_tracker(projects)
    
    print("\n3. Project Timeline...")
    visualizer.plot_timeline(projects)
    
    # Get health scores
    summary = dashboard.get_dashboard_summary()
    project_health = summary['project_health']
    
    print("\n4. Health Scores...")
    visualizer.plot_health_scores(project_health)
    
    # Interactive menu
    while True:
        print("\n" + "="*50)
        print("DASHBOARD MENU")
        print("-"*30)
        print("1. View All Projects")
        print("2. View By Status")
        print("3. View Overdue Projects")
        print("4. View High Priority")
        print("5. Refresh Dashboard")
        print("0. Exit")
        print("-"*30)
        
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            print("\nALL PROJECTS:")
            print("-"*50)
            for p in projects:
                print(
                    f"[{p.get('Project ID')}] "
                    f"{p.get('Project Name')} | "
                    f"{p.get('Status')} | "
                    f"{p.get('Progress %')}%"
                )
        
        elif choice == '2':
            print("\nSelect Status:")
            print("1. Completed")
            print("2. In Progress")
            print("3. Not Started")
            status_choice = input("Enter choice: ").strip()
            status_map = {
                '1': 'Completed',
                '2': 'In Progress',
                '3': 'Not Started'
            }
            status = status_map.get(status_choice)
            if status:
                filtered = dashboard.get_projects_by_status(
                    status
                )
                print(f"\n{status.upper()} PROJECTS:")
                for p in filtered:
                    print(f"  - {p.get('Project Name')}")
        
        elif choice == '3':
            overdue = dashboard.get_overdue_projects()
            if overdue:
                print("\nOVERDUE PROJECTS:")
                for p in overdue:
                    print(f"  ⚠️  {p.get('Project Name')}")
            else:
                print("\n✅ No overdue projects!")
        
        elif choice == '4':
            high = dashboard.get_projects_by_priority('High')
            print("\nHIGH PRIORITY PROJECTS:")
            for p in high:
                print(
                    f"  🔴 {p.get('Project Name')} | "
                    f"{p.get('Progress %')}%"
                )
        
        elif choice == '5':
            dashboard.load_data()
            dashboard.print_dashboard()
        
        elif choice == '0':
            print("\n✅ Thank you for using Project Dashboard!")
            break
        
        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    main()
