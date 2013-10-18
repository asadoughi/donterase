import json

from django.http import HttpResponse, HttpResponseRedirect
from django.utils.timezone import now

from django.views.decorators.csrf import csrf_exempt

from files.models import FileUpload
from files.uploader import FilePicker

MAX_TAGS = 10


def _map_fn(results):
    return map(lambda r: {'id': r.id,
                          'url': r.file_url,
                          'tags': map(lambda t: t.tag, r.tag_set.all()),
                          'datetime': r.date.strftime("%Y/%m/%d %H:%M"),
                          }, results)


def latest(request):
    """Show X latest uploads."""
    latest_files = FileUpload.objects.all().order_by('-date')[:25]
    result = _map_fn(latest_files)

    return HttpResponse(json.dumps(result))


def tags(request):
    """API endpoint for tag-based queries."""
    query = map(lambda t: t.lower(), request.GET['q'].split())
    if len(query) == 0:
        return HttpResponse('Failure.')

    results = FileUpload.objects.filter(tag__tag__contains=query[0])
    for tag in query[1:MAX_TAGS]:
        results = results.filter(tag__tag__contains=tag)
    results = results.order_by('-date')
    results = _map_fn(results)

    return HttpResponse(json.dumps(results))


def _submit(file_url, tags):
    f = None
    try:
        f = FileUpload.objects.create(file_url=file_url, date=now())
        tags = tags.split()
        for tag in set(tags[:MAX_TAGS]):
            f.tag_set.create(tag=tag.lower())
        f.save()
    except:
        return None

    return f


def submit(request):
    """API endpoint for submitting images (url + tags)."""
    return _submit(request.POST['file_url'], request.POST['tags'])


def _upload(request):
    """API endpoint: file + tags -> FilePicker -> _submit(url + tags)"""
    if 'file' not in request.FILES or \
            'tags' not in request.POST or \
            len(request.POST['tags']) == 0:
        return None

    fp = FilePicker()
    result_url = fp.upload(request.FILES['file'])
    if result_url is None:
        return None

    return _submit(result_url, request.POST['tags'])


# TODO: probably not right in the long term when users are added
@csrf_exempt
def upload(request):
    """
    Non-API: _upload(file + tags) -> redirect to target page for image or
    failure in new view
    """
    if request.method == 'POST':
        result = _upload(request)
        if not result:
            return HttpResponseRedirect('/#uploadpage')
        return HttpResponseRedirect('/get/?id=' + str(result.id))
    else:
        return HttpResponseRedirect('/#uploadpage')


def get(request):
    """API endpoint: retrieves specific file by id"""
    if 'id' not in request.GET:
        return HttpResponse('')
    results = FileUpload.objects.filter(id__exact=request.GET['id'])
    results = _map_fn(results)
    return HttpResponse(json.dumps(results))
