"""
URL configuration for stack_over_flow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.core.management import call_command
from django.http import HttpResponse


def run_migrations(request):
    call_command("migrate")
    return HttpResponse("Migrations done.")


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('questions.urls')),
    # namespace is a label you give to a group of URLs — usually from a specific app — so Django knows exactly where to look when resolving a URL.
    path('accounts/', include('accounts.urls', namespace='accounts')),

    path("run-migrations/", run_migrations),
]
