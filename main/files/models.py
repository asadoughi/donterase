from django.db import models


class FileUpload(models.Model):
    file_url = models.CharField(max_length=2000)
    date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.file_url


class Tag(models.Model):
    file_upload = models.ForeignKey(FileUpload)
    tag = models.CharField(max_length=200)

    def __unicode__(self):
        return self.tag
