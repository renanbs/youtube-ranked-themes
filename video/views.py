from django.shortcuts import render

from video.models import Video
# Create your views here.


def get_popular_themes(request):
    videos = Video.objects.all()
    themes_with_score = {}
    for video in videos:
        themes = video.themes.all()
        for theme in themes:
            themes_with_score[theme] = video.get_score

    sorted_themes_with_score = sorted(themes_with_score.items(), key=lambda value: value[1], reverse=True)
    context = {
        "title": "Youtube ranked themes",
        "themes": sorted_themes_with_score,
    }
    return render(request, "themes.html", context)
