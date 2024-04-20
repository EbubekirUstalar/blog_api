import csv

from django.http import HttpResponse, JsonResponse
from django.db import transaction

from .models import Entry


SUCCESS_FILE_PATH = "./static/success_entries.csv"
FAIL_FILE_PATH = "./static/fail_entries.csv"

def index(request):
    endpoints = [
        {'Load from CSV successfully': 'http://127.0.0.1:8000/success_load/'},
        {'Load from CSV with error': 'http://127.0.0.1:8000/fail_load/'},
        {'List from DB': 'http://127.0.0.1:8000/list/'},
        {'Delete data from DB': 'http://127.0.0.1:8000/delete/'},
    ]
    return JsonResponse(endpoints, safe=False)


def _load(file_path):
    try:
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            with transaction.atomic():
                for row in reader:
                    new_entry = Entry(
                        id  =row['id'],
                        type=row['type'].lower(),
                        parent_id=row['parent_id'],
                        content=row['content'],
                    )
                    new_entry.clean()
                    new_entry.save()
    except Exception as exception:
        return HttpResponse(f"The following error occured; {exception.message}")
    return HttpResponse("Successfully Loaded")


def success_load(request):
    return _load(SUCCESS_FILE_PATH)

def fail_load(request):
    return _load(FAIL_FILE_PATH)

def _get_comments(entry):
    comments = []
    for child in entry.children.all():
        comments.append({
            'content': child.content,
            'comments': _get_comments(child)
        })
    return comments


def list(request):
    blogs = Entry.objects.filter(type=Entry.Type.BLOG)
    blogs_with_comments_dict = {}

    for blog in blogs:
        comments = _get_comments(blog)
        blogs_with_comments_dict[blog.id] = {
            'content': blog.content,
            'comments': comments
        }

    return JsonResponse(blogs_with_comments_dict)


def delete(request):
    Entry.objects.all().delete()
    return HttpResponse("Deleted")
