from openpyxl import Workbook
import pandas as pd
from app import db
from app.models import Project
    
def generate_app_xlsx(projects):
    workbook = Workbook()
    workbook.iso_dates = True
    sheet = workbook.active
    
    table_header = ["Code (PAP)", "Procurement Project", "PMO/End-User", "Category", "Mode of Procurement", "Date Needed", "Source of Funds", "Estimated Budget", "Remarks"]
    sheet.append(table_header)
    
    count = 0
    for project in projects:
        count += 1
        project_date = str(project.date_needed.date())
        project_to_append = [f'P{count}', project.title, project.submitter.department, project.category, project.initial_mode, project_date, project.source, f'₱ {project.budget}', project.description]
        sheet.append(project_to_append)
        
    workbook.save("tmp/APP.xlsx")
    