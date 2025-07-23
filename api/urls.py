from django.urls import path
from . views import leetcode_helper_view

urlpatterns = [
    path('helper/', leetcode_helper_view, name='helper'),
]