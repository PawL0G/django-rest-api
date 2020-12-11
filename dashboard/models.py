from django.contrib.auth import get_user_model
from django.db import models
from django_quill.fields import QuillField

User = get_user_model()


class Issue(models.Model):
    PRIORITY_CHOICES = (
        (0, "Information"),
        (1, "Warning"),
        (2, "Error"),
        (3, "Critical"),
    )

    STATUS_CHOICES = (
        (0, "Pending"),
        (1, "In progress"),
        (2, "Suspend"),
        (3, "Completed"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name="Название")
    text = QuillField(verbose_name="Описание")
    git = models.URLField(blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    likes = models.ManyToManyField(User, related_name='issue_likes')
    total_likes = models.IntegerField(default=0)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-date_time',)


class Message(models.Model):
    text = models.TextField(verbose_name="Сообщение")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
