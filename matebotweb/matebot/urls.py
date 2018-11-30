from django.conf.urls import patterns, include, url
from django.contrib import admin
from interface import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Login / logout.
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', views.logout_page),

    # Web portal.
    url(r'^aguarde/', views.processa),
    url(r'^resultado/', views.resultado),
    url(r'^upload/', views.uploadFile),
    url(r'^salvar/', views.salvar),
    url(r'^stress/', views.stress_test),
    url(r'^portal/', views.logado_index),
    
    # Serve static content.
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'static'}),
    
    # todo o resto
    url(r'^$', include('interface.urls')),
    
)
