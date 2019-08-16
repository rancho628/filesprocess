from django.urls import path, include

import legalfiles.views

app_name = 'legalfiles'
urlpatterns = [
    path(r'to_upload/', legalfiles.views.to_upload, name='to_upload'),
    path(r'process_file/', legalfiles.views.process_file, name='process_file'),
    path(r'to_process/', legalfiles.views.to_process, name='to_process'),
    path(r'upload_file/', legalfiles.views.upload_file, name='upload_file'),
    #path(r'detail/<int:txt_id>', legalfiles.views.get_detail_page, name='get_detail_page'),
    path(r'index/', legalfiles.views.IndexView.as_view(), name='index'),
    path(r'tag/<name1>/', legalfiles.views.TagView.as_view(), name='tag'),#(?P<name>[0-9]+)
    path(r'tag/<name1>/<name2>/', legalfiles.views.TagView.as_view(), name='tag'),#(?P<name>[0-9]+)
    path(r'tag/<name1>/<name2>/<name3>/', legalfiles.views.TagView.as_view(), name='tag'),#(?P<name>[0-9]+)
    path(r'tag/<name1>/<name2>/<name3>/<name4>/', legalfiles.views.TagView.as_view(), name='tag'),#(?P<name>[0-9]+)
    path(r'tag/<name1>/<name2>/<name3>/<name4>/<name5>/', legalfiles.views.TagView.as_view(), name='tag'),#(?P<name>[0-9]+)
    path(r'tag/<name1>/<name2>/<name3>/<name4>/<name5>/<name6>/', legalfiles.views.TagView.as_view(), name='tag'),#(?P<name>[0-9]+)
    path(r'tag/<name1>/<name2>/<name3>/<name4>/<name5>/<name6>/<name7>/', legalfiles.views.TagView.as_view(), name='tag'),#(?P<name>[0-9]+)
    path(r'tag/<name1>/<name2>/<name3>/<name4>/<name5>/<name6>/<name7>/<name8>/', legalfiles.views.TagView.as_view(), name='tag'),#(?P<name>[0-9]+)
    path(r'detail/<int:txt_id>', legalfiles.views.detail, name='detail'),
    path(r'test/', legalfiles.views.test, name='test'),
    path(r'tag_admin/<id>', legalfiles.views.TagAdmin.as_view(), name='tag_admin'),
    path(r'register/', legalfiles.views.register, name='register'),
]
