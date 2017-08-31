from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from datetime import date

# Create your models here.

from theme.models import Theme


def is_video_older_than_1_year(value):
    if (date.today() - value).days > 365:
        raise ValidationError(
            _('%(value)s is older then 1 year'),
            params={'value': value},
        )


class Video(models.Model):
    title = models.CharField(max_length=100)
    date_uploaded = models.DateField(auto_now_add=False, auto_now=False, validators=[is_video_older_than_1_year])
    views = models.PositiveIntegerField()
    themes = models.ManyToManyField(Theme)

    def __str__(self):
        return self.title

    @property
    def get_score(self):
        days_since_upload = date.today() - self.date_uploaded
        time_factor = max(0, 1 - (int(days_since_upload.days) / 365))

        positive_comments = Comment.objects.filter_by_video(self).filter(is_positive=True).count()
        if positive_comments == 0:
            positive_comments = 1  # Just avoiding ZeroDivisionError: division by zero
        negative_comments = Comment.objects.filter_by_video(self).filter(is_positive=False).count()

        thumbs_up = Thumb.objects.filter_by_video(self).filter(is_positive=True).count()
        if thumbs_up == 0:
            thumbs_up = 1  # Just avoiding ZeroDivisionError: division by zero
        thumbs_down = Thumb.objects.filter_by_video(self).filter(is_positive=False).count()

        good_comments = positive_comments / (positive_comments + negative_comments)
        thumbs_up_count = thumbs_up / (thumbs_up + thumbs_down)

        positivity_factor = 0.7 * good_comments + 0.3 * thumbs_up_count

        return self.views * time_factor * positivity_factor


class CommentManager(models.Manager):
    def filter_by_video(self, video):
        qs = super(CommentManager, self).filter(video=video)
        return qs


class Comment(models.Model):
    is_positive = models.BooleanField()
    time = models.DateTimeField(auto_now_add=True, auto_now=False)
    video = models.ForeignKey(Video)

    objects = CommentManager()

    def __str__(self):
        return self.__class__.__name__


class ThumbManager(models.Manager):
    def filter_by_video(self, video):
        qs = super(ThumbManager, self).filter(video=video)
        return qs


class Thumb(models.Model):
    is_positive = models.BooleanField()
    time = models.DateTimeField(auto_now_add=True, auto_now=False)
    video = models.ForeignKey(Video)

    objects = ThumbManager()

    def __str__(self):
        return self.__class__.__name__


