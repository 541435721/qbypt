# -*- coding: UTF-8 -*-
"""qbypt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth.views import logout
import xmqb.views as views
from django.views.static import serve
import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^login/$', views.login, name='login'),

    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),

    url(r'^register/$', views.register, name='register'),

    url(r'^check_code/$', views.check_code, name='check_code'),

    url(r'^checkcode/$', views.CheckCode, name='CheckCode'),  # 图片验证码生成方法

    url(r'^customer_user_info/$', views.customer_user_info, name='customer_user_info'),

    url(r'^customer_account_info/$', views.customer_account_info, name='customer_account_info'),

    url(r'^customer_password_change/$', views.customer_password_change, name='customer_password_change'),

    url(r'^customer_project_list/$', views.customer_project_list, name='customer_project_list'),

    url(r'^customer_project_delete/$', views.customer_project_delete, name='customer_project_delete'),  # 用户删除项目

    url(r'^customer_project_info/$', views.customer_project_info, name='customer_project_info'),  # 用户查看项目信息

    url(r'^customer_project_alter/$', views.customer_project_alert, name='customer_project_alter'),  # 用户修改项目

    url(r'^customer_file_upload/$', views.customer_file_upload, name='customer_file_upload'),

    url(r'^customer_project_new/$', views.customer_project_new, name='customer_project_new'),

    url(r'^administrator_password_change/$', views.administrator_password_change, name='administrator_password_change'),

    url(r'^customer_project_alert/$', views.customer_project_alert, name='customer_project_alert'),

    url(r'^customer_stl_show/$', views.customer_stl_show, name='customer_stl_show'),

    url(r'^customer_order_list/$', views.customer_order_list, name='customer_order_list'),

    url(r'^customer_order_info/$', views.customer_order_info, name='customer_order_info'),

    url(r'^customer_order_pay/$', views.customer_order_pay, name='customer_order_pay'),

    url(r'^customer_invoice_list/$', views.customer_invoice_list, name='customer_invoice_list'),

    url(r'^customer_invoice_demand/$', views.customer_invoice_demand, name='customer_invoice_demand'),

    url(r'^customer_invoice_info/$', views.customer_invoice_info, name='customer_invoice_info'),

    url(r'^customer_coupon_list/$', views.customer_coupon_list, name='customer_coupon_list'),

    url(r'^customer_message_list/$', views.customer_message_list, name='customer_message_list'),

    url(r'^customer_message_info/$', views.customer_message_info, name='customer_message_info'),

    url(r'^uploadify_script/$', views.uploadify_script, name='uploadify_script'),

    url(r'^profile_upload/$', views.profile_upload, name='profile_upload'),

    url(r'^download/(?P<path>.*)$', serve, {'document_root': settings.DOWNLOAD_DIR, 'show_indexes': False}),

    url(r'^administrator_user_info_list/$', views.administrator_user_info_list, name='administrator_user_info_list'),

    url(r'^administrator_user_info_alter/$', views.administrator_user_info_alter, name='administrator_user_info_alter'),

    url(r'^administrator_account_list/$', views.administrator_account_list, name='administrator_account_list'),

    url(r'^administrator_account_alter/$', views.administrator_account_alter, name='administrator_account_alter'),

    url(r'^administrator_project_list/$', views.administrator_project_list, name='administrator_project_list'),

    url(r'^administrator_project_info/$', views.administrator_project_info, name='administrator_project_info'),

    url(r'^administrator_project_alter/$', views.administrator_project_alter, name='administrator_project_alter'),

    url(r'^administrator_project_delete/$', views.administrator_project_delete, name='administrator_project_delete'),

    url(r'^administrator_work_order_distribute/$', views.administrator_work_order_distribute,
        name='administrator_work_order_distribute'),

    url(r'^administrator_work_order_handle_list/$', views.administrator_work_order_handle_list,
        name='administrator_work_order_handle_list'),

    url(r'^administrator_work_order_handle/$', views.administrator_work_order_handle,
        name='administrator_work_order_handle'),

    url(r'^administrator_file_upload/$', views.administrator_file_upload, name='administrator_upload.html'),

    url(r'^administrator_work_order_assess_list/$', views.administrator_work_order_assess_list,
        name='administrator_work_order_assess_list'),

    url(r'^administrator_work_order_assess_handle/$', views.administrator_work_order_assess_handle,
        name='administrator_work_order_assess_handle'),

    url(r'^administrator_order_list/$', views.administrator_order_list, name='administrator_order_list'),

    url(r'^administrator_order_info/$', views.administrator_order_info, name='administrator_order_info'),

    url(r'^administrator_invoice_list/$', views.administrator_invoice_list, name='administrator_invoice_list'),

    url(r'^administrator_invoice_handle/$', views.administrator_invoice_handle, name='administrator_invoice_handle'),

    url(r'^administrator_invoice_info/$', views.administrator_invoice_info, name='administrator_invoice_info'),

    url(r'^administrator_invoice_create/$', views.administrator_invoice_create, name='administrator_invoice_create'),

    url(r'^administrator_coupon_distribute/$', views.administrator_coupon_distribute,
        name='administrator_coupon_distribute'),

    url(r'^administrator_coupon_list/$', views.administrator_coupon_list, name='administrator_coupon_list'),

    url(r'^administrator_coupon_delete/$', views.administrator_coupon_delete, name='administrator_coupon_delete'),

    url(r'^administrator_coupon_alter/$', views.administrator_coupon_alter, name='administrator_coupon_alter'),

    url(r'^administrator_price_list/$', views.administrator_price_list, name='administrator_price_list'),

    url(r'^administrator_price_new/$', views.administrator_price_new, name='administrator_price_new'),

    url(r'^administrator_part_price_alter/$', views.administrator_part_price_alter,
        name='administrator_part_price_alter'),

    url(r'^administrator_price_alter/$', views.administrator_price_alter, name='administrator_price_alter'),

    url(r'^administrator_message_send/$', views.administrator_message_send, name='administrator_message_send'),

    url(r'^administrator_message_receive/$', views.administrator_message_receive, name='administrator_message_receive'),

    url(r'^administrator_message_read/$', views.administrator_message_read, name='administrator_message_read'),

    url(r'^alipy_notify/$', views.alipy_notify, name='alipy_notify'),  # 支付完成后所做的跳转，用以修改支付状态

    url(r'^customer_message_receive/$', views.customer_message_list, name='customer_message_list'),

    url(r'^customer_message_read/$', views.customer_message_info, name='customer_message_read'),

    url(r'^customer_suggestion/$', views.customer_suggestion, name='consumer_suggestion'),

    url(r'^contact_us/$', views.contact_us, name='contact_us'),

    url(r'^user_agreement', views.user_agreement, name='user_agreement'),
]
