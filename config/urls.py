"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, reverse, include

from apps.users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('core/', include('apps.core.urls')),
    path('crosses/', include('apps.crosses.urls')),
    path('genomics/', include('apps.genomics.urls')),
    path('phenotyping/', include('apps.phenotyping.urls')),
    path('germplasm/', include('apps.germplasm.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('locations/', include('apps.locations.urls')),
    path('observations/', include('apps.observations.urls')),
    path('pedigree/', include('apps.pedigree.urls')),
    path('traits/', include('apps.traits.urls')),
    path('workflows/', include('apps.workflows.urls')),
]
