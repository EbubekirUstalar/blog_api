import pytest

from django.core.exceptions import ValidationError
from entries.models import Entry


def test_entry_blog_without_parent():
    """An blog without parent can exist"""
    new_entry = Entry(type=Entry.Type.BLOG, parent=None)
    new_entry.clean()
    new_entry.save()
    assert Entry.objects.count() == 1


def test_entry_blog_with_parent_as_blog():
    """An blog with parent as blog cannot exist"""
    blog = Entry.objects.create(type=Entry.Type.BLOG)
    with pytest.raises(ValidationError):
        new_entry = Entry(type=Entry.Type.BLOG, parent=blog)
        new_entry.clean()
        new_entry.save()
    assert Entry.objects.count() == 1


def test_entry_blog_with_parent_as_comment():
    """An blog with parent as comment cannot exist"""
    comment = Entry.objects.create(type=Entry.Type.COMMENT)
    with pytest.raises(ValidationError):
        new_entry = Entry(type=Entry.Type.BLOG, parent=comment)
        new_entry.clean()
        new_entry.save()
    assert Entry.objects.count() == 1


def test_entry_comment_without_parent():
    """An comment without parent cannot exist"""
    with pytest.raises(ValidationError):
        new_entry = Entry(type=Entry.Type.COMMENT, parent=None)
        new_entry.clean()
        new_entry.save()
    assert Entry.objects.count() == 0


def test_entry_comment_with_parent_as_blog():
    """An comment with parent as blog can exist"""
    blog = Entry.objects.create(type=Entry.Type.BLOG)
    new_entry = Entry(type=Entry.Type.COMMENT, parent=blog)
    new_entry.clean()
    new_entry.save()
    assert Entry.objects.count() == 2


def test_entry_comment_with_parent_as_comment():
    """An comment with parent as comment can exist"""
    comment = Entry.objects.create(type=Entry.Type.COMMENT)
    new_entry = Entry(type=Entry.Type.COMMENT, parent=comment)
    new_entry.clean()
    new_entry.save()
    assert Entry.objects.count() == 2
