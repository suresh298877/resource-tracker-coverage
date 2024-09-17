from django.shortcuts import render, HttpResponse, redirect
import pandas as pd
from .forms import UploadFileForm
from django.core.paginator import Paginator
from . import models
import openpyxl
# Create your views here.


def uploadDAta(request):
    if request.method == "GET":
        form = UploadFileForm()
        return render(request, 'upload-data.html', {'form': form})
    elif request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if not str(request.FILES['file']).endswith('.xlsx'):
                return HttpResponse("<h1>Please upload excel files only(.xlsx) </h1>")
            uploaded_file = form.save()
            file_path = uploaded_file.file.path
            data = pd.read_excel(file_path)
            df = pd.DataFrame(data)
            df = df.fillna("")
            for idx, row in df.iterrows():
                if row['psm'] == "" or row['region'] == "" or row['domain'] == "" or row['location'] == "":
                    models.UploadedFile.objects.all().delete()
                    return HttpResponse("<h1>psm, region, domain and location should not be empty. check your excel file</h1>")
                obj, created = models.Record.objects.get_or_create(
                    psm=row['psm'],
                    region=row['region'],
                    domain=row['domain'],
                    location=row['location']
                )
                obj.category = row['category'] if row['category'] != "" else obj.category
                obj.priority = row['priority'] if row['priority'] != '' else obj.priority
                obj.console = row['console'] if row['console'] != '' else obj.console
                obj.operator = row['operator'] if row['operator'] != "" else obj.operator
                obj.owner = row['psm_owner'] if row['psm_owner'] != "" else obj.psm_owner
                obj.comments = row['comments'] if row['comments'] != "" else obj.comments
                obj.status = row['status'] if row['status'] != "" else obj.status
                obj.last_update_datetime_for_record_4_unique_records = row['last_update_datetime_for_record_4_unique_records'] if row[
                    'last_update_datetime_for_record_4_unique_records'] != "" else obj.last_update_datetime_for_record_4_unique_records
                obj.is_skip = row['is_skip'] if row['is_skip'] != "" else obj.is_skip
                obj.color = row['color'] if row['color'] != "" else obj.color
                obj.coverage_type = row['coverage_type'] if row['coverage_type'] != "" else obj.coverage_type
                obj.protection_mode = row['protection_mode'] if row['protection_mode'] != "" else obj.protection_mode
                print(row['alarm_mode'])
                obj.alarm_mode = row['alarm_mode']
                obj.coverage_status = row['coverage_status'] if row['coverage_status'] != "" else obj.coverage_status
                obj.tldr = row['tldr'] if row['tldr'] != "" else obj.tldr
                obj.save()
            try:
                models.UploadedFile.objects.all().delete()
            except Exception as e:
                return HttpResponse("Failed to delete")

            return redirect('records')
        else:
            form = UploadFileForm()
            return render(request, 'upload-data.html', {'form': form})


def exportToExcel(request):
    data = models.Record.objects.all().values()
    df = pd.DataFrame(list(data))

    if 'id' in df.columns:
        df.drop(columns=['id'], inplace=True)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=data.xlsx'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return response


def records(request):
    if request.method == "GET":
        data = models.Record.objects.all()
        if request.GET.get('psm', None):
            data = data.filter(psm=request.GET.get('psm', None))

        if request.GET.get('region', None):
            data = data.filter(region=request.GET.get('region', None))

        if request.GET.get('domain', None):
            data = data.filter(domain=request.GET.get('domain', None))

        if request.GET.get('location', None):
            data = data.filter(location=request.GET.get('location', None))

        if request.GET.get('category', None):
            data = data.filter(category=request.GET.get('category', None))

        if request.GET.get('priority', None):
            data = data.filter(priority=request.GET.get('priority', None))

        if request.GET.get('console', None):
            data = data.filter(console=request.GET.get('console', None))

        if request.GET.get('operator', None):
            data = data.filter(operator=request.GET.get('operator', None))

        if request.GET.get('psm_owner', None):
            data = data.filter(psm_owner=request.GET.get('psm_owner', None))

        if request.GET.get('comments', None):
            data = data.filter(comments=request.GET.get('comments', None))

        if request.GET.get('status', None):
            data = data.filter(status=request.GET.get('status', None))

        if request.GET.get('last_update_datetime_for_record_4_unique_records', None):
            data = data.filter(last_update_datetime_for_record_4_unique_records=request.GET.get(
                'last_update_datetime_for_record_4_unique_records', None))

        if request.GET.get('is_skip', None):
            data = data.filter(is_skip=request.GET.get('is_skip', None))

        if request.GET.get('color', None):
            data = data.filter(color=request.GET.get('color', None))

        if request.GET.get('coverage_type', None):
            data = data.filter(
                coverage_type=request.GET.get('coverage_type', None))

        if request.GET.get('protection_mode', None):
            data = data.filter(
                protection_mode=request.GET.get('protection_mode', None))

        if request.GET.get('alarm_mode', None):
            print(request.GET.get('alarm_mode', None))
            data = data.filter(alarm_mode=request.GET.get('alarm_mode', None))
            print(data)

        if request.GET.get('coverage_status', None):
            data = data.filter(
                coverage_status=request.GET.get('coverage_status', None))

        if request.GET.get('tldr', None):
            data = data.filter(tldr=request.GET.get('tldr', None))

        page_obj = Paginator(data, 3)
        page_list = request.GET.get("page")
        page = page_obj.get_page(page_list)
        context = {
            "page": page
        }

        return render(request, 'records.html', context)


def deleteRecord(request, pk):
    models.Record.objects.get(pk=pk).delete()
    return redirect('records')


def editRecord(request, pk):
    if request.method == "GET":
        data = models.Record.objects.get(pk=pk)

        return render(request, 'edit.html', {'data': data})
    else:
        psm = request.POST['psm']
        region = request.POST['region']
        domain = request.POST['domain']
        location = request.POST['location']
        category = request.POST['category']
        priority = request.POST['priority']
        console = request.POST['console']
        operator = request.POST['operator']
        psm_owner = request.POST['psm_owner']
        comments = request.POST['comments']
        last_update_datetime_for_record_4_unique_records = request.POST[
            'last_update_datetime_for_record_4_unique_records']

        is_skip = request.POST['is_skip']
        color = request.POST['color']
        coverage_type = request.POST['coverage_type']
        protection_mode = request.POST['protection_mode']
        alarm_mode = request.POST['alarm_mode']
        coverage_status = request.POST['coverage_status']
        tldr = request.POST['tldr']
        obj = models.Record.objects.get(pk=pk)
        obj.psm = psm
        obj.region = region
        obj.domain = domain
        obj.location = location
        obj.category = category
        obj.priority = priority
        obj.console = console
        obj.operator = operator
        obj.psm_owner = psm_owner
        obj.comments = comments
        obj.last_update_datetime_for_record_4_unique_records = last_update_datetime_for_record_4_unique_records
        obj.is_skip = is_skip
        obj.color = color
        obj.coverage_type = coverage_type
        obj.protection_mode = protection_mode
        obj.alarm_mode = alarm_mode
        obj.coverage_status = coverage_status
        obj.tldr = tldr
        try:
            obj.save()
        except Exception as e:
            return HttpResponse('<h1>psm, region, domain and location fields should be unique</h1>')
        return redirect('records')
