from django.db import models
from django.core.exceptions import ValidationError


def validate_comment_parent(value):
    if not value.parent_id:
        raise ValidationError('Comments must be associated with another object (blog or comment)')


def validate_blog_parent(value):
    if value.parent_id:
        raise ValidationError('Blog entries cannot be associated with other blog entries')


class Entry(models.Model):
    class Type(models.TextChoices):
        BLOG = 'blog'
        COMMENT = 'comment'

    type = models.CharField(max_length=10, choices=Type.choices, blank=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    content = models.TextField()
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.id}: {self.content}"

    def clean(self):
        if self.type == self.Type.COMMENT:
            validate_comment_parent(self)
        elif self.type == self.Type.BLOG:
            validate_blog_parent(self)
