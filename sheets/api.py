import frappe
import uuid 
from datetime import datetime

@frappe.whitelist()
def get_ss_fields():
    from frappe.model import default_fields
    from frappe.model.meta import get_table_columns
    
    spreadsheet_fields = set(get_table_columns("Spreadsheet")) - set(default_fields)

    allowed_for_list = set(['title','created_by','last_modified','size'])

    return list(spreadsheet_fields.intersection(allowed_for_list))
    

@frappe.whitelist()
def create_spreadsheet(title, content):
    spreadsheet = frappe.new_doc("Spreadsheet")
    spreadsheet.name = uuid.uuid4().hex
    spreadsheet.title = title
    spreadsheet.created_by = frappe.session.user
    spreadsheet.created_on = datetime.now()
    spreadsheet.last_modified = spreadsheet.created_on
    spreadsheet.content = content
    spreadsheet.size = 0

    spreadsheet.save()
    return spreadsheet

@frappe.whitelist()
def list_spreadsheets(filters= []):
    sheets = frappe.get_list("Spreadsheet", fields = ["title", "created_by","last_modified","size","name"], filters = [])
    return sheets 