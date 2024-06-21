from django.contrib import admin
from . models import registration,services,booking,contactus,feedback
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def export_to_pdf(modeladmin, request, queryset):
   # Create a new PDF
   response = HttpResponse(content_type='application/pdf')
   response['Content-Disposition'] = 'attachment; filename="report.pdf"'

   # Generate the report using ReportLab
   doc = SimpleDocTemplate(response, pagesize=letter)

   elements = []

   # Define the style for the table
   style = TableStyle([
       ('BACKGROUND', (0,0), (-1,0), colors.grey),
       ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
       ('ALIGN', (0,0), (-1,-1), 'CENTER'),
       ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
       ('FONTSIZE', (0,0), (-1,0), 14),
       ('BOTTOMPADDING', (0,0), (-1,0), 12),
       ('BACKGROUND', (0,1), (-1,-1), colors.beige),
       ('GRID', (0,0), (-1,-1), 1, colors.black),
   ])

   # Create the table headers
   headers = ['userid', 'serviceid','start_date','pay_type','contact']

   # Create the table data
   data = []
   for obj in queryset:
       data.append([obj.userid, obj.serviceid, obj.start_date,obj.pay_type,obj.contact])

   # Create the table
   t = Table([headers] + data, style=style)

   # Add the table to the elements array
   elements.append(t)

   # Build the PDF document
   doc.build(elements)

   return response

export_to_pdf.short_description = "Export to PDF"

# Register your models here.

class showregi(admin.ModelAdmin):
    list_display = ["name","dp_photo","gender","email","phone_no","dob","address","r_type"]

admin.site.register(registration,showregi)

class showservices(admin.ModelAdmin):
    list_display = ["sname","sphoto","sprice","sdesc","email_id"]

admin.site.register(services,showservices)

class showbooking(admin.ModelAdmin):
    list_display = ["userid","serviceid","date_time","address","start_date","contact","pay_type","b_status"]
    list_filter = ['date_time']
    actions = [export_to_pdf]

admin.site.register(booking,showbooking)

class showcontact(admin.ModelAdmin):
    list_display = ["name","uemail","phone","subject","message"]

admin.site.register(contactus,showcontact)

class showfeed(admin.ModelAdmin):
    list_display = ["book_id","rating","comment","date_time"]

admin.site.register(feedback,showfeed)