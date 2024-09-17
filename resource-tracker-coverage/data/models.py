from django.db import models

# Create your models here.


class Record(models.Model):
    psm = models.CharField(max_length=200, null=True)
    region = models.CharField(max_length=20, null=True)
    domain = models.URLField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=100, null=True)
    priority = models.CharField(max_length=50, null=True)
    console = models.CharField(max_length=50, null=True)
    operator = models.CharField(max_length=70, null=True)
    # updated owner to psm_owner
    psm_owner = models.CharField(max_length=50, null=True)
    comments = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=50, null=True)
    last_update_datetime_for_record_4_unique_records = models.CharField(
        max_length=200, null=True)
    # new fields
    is_skip = models.BooleanField(default=False, null=True)
    color = models.CharField(max_length=50, null=True)
    coverage_type = models.CharField(max_length=50, null=True)
    protection_mode = models.BooleanField(default=False, null=True)
    alarm_mode = models.BooleanField(default=False, null=True)
    coverage_status = models.BooleanField(default=False, null=True)
    tldr = models.CharField(max_length=20, null=True)

    class Meta:
        unique_together = ['psm', 'region', 'domain', 'location']


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.file.name
