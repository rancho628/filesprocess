from django.urls import path,include

import legalfiles.views

app_name = 'legalfiles'
urlpatterns=[
    path(r'to_upload/', legalfiles.views.to_upload, name='to_upload'),
    path(r'process_file/', legalfiles.views.process_file, name='process_file'),
    path(r'to_process/', legalfiles.views.to_process, name='to_process'),
    path(r'upload_file/', legalfiles.views.upload_file, name='upload_file'),
    path(r'detail/<int:txt_id>',  legalfiles.views.get_detail_page,name='get_detail_page'),

    path(r'index/',  legalfiles.views.index,name='index')
]
