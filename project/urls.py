# coding: utf-8
from django.conf.urls import patterns,url,include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)

#管理列表路由
urlpatterns += patterns('project.manage_ops.views',
    url(r'^$','manage_list'),
    url(r'^find_password/$','find_password'),
    url(r'^find_pass_post/$','find_password_post'),
    url(r'^verify_key/$','verify_key'),
    url(r'^reset_password/$','reset_password'),
    url(r'^ops_manage_list/$','ops_manage_list')
)

urlpatterns += patterns('project.account.views',
     url(r'^account/logout/$','logout_view'),
     url(r'^account/login/$','login_view')
)


#urlpatterns += patterns('project.assets.views',
#     url(r'^$','assets_index'),
#     url(r'^assets/$', 'assets'),
#     url(r'^assets_group/(?P<id>\d+)/$','assets_group'),
#     url(r'^assets/search/$','assets_search'),
# )

# urlpatterns += patterns('project.etcd_manage.views',
#     url(r'^etcd_index/$', 'index'),
#     url(r'^add_domain/$','add_domain'),
#     url(r'^del_domain/$','del_domain'),
#     url(r'^edit_domain/$','edit_domain'),
#     url(r'^view_configure/(?P<domain>.*)/$','view_configure'),
#     url(r'^del_domain_configure/$','del_domain_configure')
#
# )
#



#
# urlpatterns += patterns('project.operation_jenkins.views',
#     url(r'^operation_jenkins/$','operation')
# )
#
#
# urlpatterns += patterns('project.deploy_manage.views',
#     url(r'^$','project'),
#     url(r'^deploy/(?P<project_id>\d+)/$','project_branch'),
#     url(r'^deploy/(?P<project_id>\d+)/(?P<branch_id>\d+)/$','branch_build_history'),
#     url(r'^deploy_add/$','deploy_add'),
#     url(r'^deploy_del/$','deploy_del'),
#     url(r'^deploy_status_edit/$','deploy_status_edit'),
#     url(r'^rebuild_salt_deploy_code/$','rebuild_salt_deploy_code'),
#     url(r'^deploy_log/(?P<id>\d+)/$$','deploy_log')
# )
#
