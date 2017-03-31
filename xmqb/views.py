# -*- coding: UTF-8 -*-
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
import django.contrib.auth as auth
from django.contrib import messages
from django.contrib.auth.models import User
import json
import uuid
import os, random
import forms as xmqb_form
import models as xmqb_model
from django.db.models import Q
import time
# 图片验证码引用包
import StringIO
from xmqb.Helper import Checkcode

# Create your views here.


# 普通用户操作

def index(request):  # 首页
    return render(request, 'index.html')


def login(request):  # 登陆
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == "POST":  # 如果表单FORM提交数据
        form = xmqb_form.LoginForm(request.POST)  # 通过前台表单提交的数据 初始化一个FORM对象
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            if request.user.is_superuser == 1:  # 管理员登录
                return redirect('/administrator_project_list')

            elif request.user.is_superuser == 2:  # 处理员登录
                return redirect('/administrator_work_order_handle_list')

            elif request.user.is_superuser == 3:  # 审核员登录
                return redirect('/administrator_work_order_assess_list')

            elif request.user.is_superuser == 4:  # 财务人员登录
                return redirect('/administrator_order_list')

            elif request.user.is_superuser == 5:  # 市场人员登陆
                return redirect('/administrator_coupon_distribute')

            elif request.user.is_superuser == 0:
                return redirect('/customer_project_new')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        return render(request, 'login.html', {'form': xmqb_form.LoginForm()})


def register(request):  # 注册
    if request.method == 'POST':
        form = xmqb_form.RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']  # 接收表单信息
            password = form.cleaned_data['password']
            cellphone = form.cleaned_data['cellphone']
            identifying_code = form.cleaned_data['identifying_code']

            User.objects.create_user(username=username, password=password)  # 系统中创建用户
            user = auth.authenticate(username=username, password=password)
            user_info = xmqb_model.UserInfo(user=user)  # 创建用户表
            user_info.user_telephone = cellphone
            user_info.save()
            auth.login(request, user)  # 用户登录
            # classifys=xmqb_model.Classify.objects.all()
            # for item in classifys:
            #     print item.classify_name
            #     # timefield需要的格式 YYYY-MM-DD HH:MM 暂定优惠券有效时间为60天
            #     coupon=xmqb_model.Coupon(coupon=str(user.id)+str(uuid.uuid1())[0:20],user=user,amount=500,rest_amount=500,type=item,
            #                              deliver_time=time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())),
            #                              deadline_time=time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()+60*60*24*60)))
            #     coupon.save()
            return render(request,'index.html')
        else:
            return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': xmqb_form.RegisterForm()})

def customer_user_info(request):  # 用户个人信息
    if not request.user.is_authenticated:
        return redirect('/login')
    user = request.user
    if request.method == 'GET':
        form = xmqb_form.UserInform(instance=user, initial={
            'user_name': user.userinfo.user_name,
            'user_telephone': user.userinfo.user_telephone,
            'email': user.userinfo.user_email,
            'user_identify': user.userinfo.user_identify,
            'hospital': user.userinfo.hospital,
            'department': user.userinfo.department,
            'position': user.userinfo.position,
            'address': user.userinfo.address,
            'pic_dir': user.userinfo.pic_dir,
            'abstract': user.userinfo.abstract
        })
        return render(request, 'customer_user_info.html', {'form': form})
    else:
        form = xmqb_form.UserInform(request.POST)
        if form.is_valid():
            user_info = xmqb_model.UserInfo.objects.get(user=user)
            user_info.user_name = form.cleaned_data['user_name']
            user_info.user_telephone = form.cleaned_data['user_telephone']
            user_info.user_email = form.cleaned_data['email']
            user_info.user_identify = form.cleaned_data['user_identify']
            user_info.hospital = form.cleaned_data['hospital']
            user_info.department = form.cleaned_data['department']
            user_info.position = form.cleaned_data['position']
            user_info.address = form.cleaned_data['address']
            # user_info.pic_dir = form.cleaned_data['pic_dir']
            user_info.abstract = form.cleaned_data['abstract']
            user_info.save()
            return redirect('/')
        else:
            return render(request,'customer_user_info.html',{'form':form})


def customer_account_info(request):  # 用户账号信息
    if not request.user.is_authenticated():
        return redirect('/login')
    user_info = xmqb_model.UserInfo.objects.get(user=request.user)
    return render(request, 'customer_account_info.html', {'user_info': user_info,'method':'0'})


def customer_password_change(request):  # 修改密码
    if request.method=='POST':
        form=xmqb_form.ChangePasswordForm(request.POST)
        if form.is_valid():
            identifying_code=form.cleaned_data['identifying_code']
            newpassword=form.cleaned_data['password']
            if request.user.is_authenticated():
                user=request.user
                user.set_password(newpassword)
                user.save()
                user_info = xmqb_model.UserInfo.objects.get(user=request.user)
            # 未登录状态下的修改密码还没写
            # 图片验证码还没做验证
        else:
            return render(request, 'customer_password_change.html',
                          {'method': '0', 'form': form, 'error': "", 'username': '', 'pwd': ''})
        if request.user.is_authenticated():
            return render(request, 'customer_account_info.html', {'method': '1'})
        else:
            return render(request, 'login.html', {'form': form,'method':'2'})
    else:
        form=xmqb_form.ChangePasswordForm()
        return render(request, 'customer_password_change.html', {'method': '0','form':form,'error': "", 'username': '', 'pwd': ''})


def CheckCode(request):      # 图片验证码生成方法
    # mstream是图片验证码的图片的载体
    mstream = StringIO.StringIO()
    validate_code = Checkcode.create_validate_code()
    img = validate_code[0]
    img.save(mstream, "GIF")

    # 将验证码保存到session
    request.session["CheckCode1"] = validate_code[1]
    return HttpResponse(mstream.getvalue())

def customer_project_list(request):  # 用户项目列表
    if not request.user.is_authenticated():
        return redirect('/login/')
    projects=xmqb_model.Project.objects.filter(user=request.user)
    return render(request, 'customer_project_list.html',{'project':projects})



def customer_project_new(request):  # 用户新建项目
    if not request.user.is_authenticated():
        return redirect('/login/')
    if (request.method == 'POST'):
        form = xmqb_form.ProjectForm(request.POST)
        if form.is_valid():
            classify = xmqb_model.Classify.objects.get(classify=form.cleaned_data['classify'])

            project = xmqb_model.Project.objects.create(user=request.user,classify=classify,
                                                        project=time.strftime('%y%m%d%H%M%S') + str((request.user.id)%100000).zfill(4))
            project.project_name = form.cleaned_data['project_name']
            project.classify = classify
            project.status = 0
            project.patient_name = form.cleaned_data['patient_name']
            project.patient_sex = form.cleaned_data['patient_sex']
            project.patient_age = form.cleaned_data['patient_age']
            project.patient_address = form.cleaned_data['patient_address']
            project.remark = form.cleaned_data['remark']
            upload_name=form.cleaned_data['upload_name']
            project.upload_name=upload_name
            if len(upload_name)>0:
                project.status='1'
            else:
                project.status='0'
            project.save()

            partlist = form.cleaned_data['part']
            price = 0

            for everypart in partlist:
                part = xmqb_model.Price.objects.get(part=everypart)
                project_part = xmqb_model.ProjectPart.objects.create(project=project, part=part)
                project_part.save()

                price += part.part_price

            order = xmqb_model.Order.objects.create(order=time.strftime('%y%m%d%H%M%S') + str((request.user.id)%10000).zfill(4) + str((random.randint(0,100)%100)).zfill(2),
                                                    user=request.user, project=project, classify=classify,order_type=u'新建',order_price= price)  # 生成工程的同时再生成 对应的订单
            order.save()

            return redirect('/customer_project_list')
        else:
            part = xmqb_model.Price.objects.all()
            part_relation = xmqb_model.PartRelation.objects.all()
            return render(request, 'customer_project_new.html', {'form': form, 'part': part, 'part_relation': part_relation})
    else:
        form = xmqb_form.ProjectForm()
        part = xmqb_model.Price.objects.all()
        part_relation = xmqb_model.PartRelation.objects.all()

        return render(request, 'customer_project_new.html', {'form': form, 'part': part, 'part_relation': part_relation})

@csrf_exempt
def customer_file_upload(request):
    if request.method=='POST':
        project_ID = request.POST['project_ID']
        classify = request.POST['id_classify']
        upload_name = request.POST['id_upload_name']
        upload_name = str(upload_name).replace("\"", "")
        if len(upload_name)>0:
            project = xmqb_model.Project.objects.get(project=project_ID)
            project.upload_name = upload_name
            project.status = '1'
            project.save()
            return render(request,'customer_project_list.html',{'method':'1'})
        else:
            return render(request, 'customer_project_list.html', {'method': '0'})
    else:
        project_ID=request.GET['porject_ID']
        project=xmqb_model.Project.objects.get(project=project_ID)
        return render(request,'customer_upload.html',{'project':project})


def customer_project_info(request):  # 用户查看项目
    return render(request, 'customer_project_info.html')


def customer_project_alert(request):  # 用户修改项目
    return render(request, 'customer_project_alert.html')


def customer_stl_show(request):  # 用户查看3D模型
    return render(request, 'customer_stl_show.html')


def customer_order_list(request):  # 用户订单列表

    return render(request, 'customer_order_list.html')


def customer_order_info(request):  # 用户订单信息
    return render(request, 'customer_order_info.html')


def customer_order_pay(request):  # 用户订单付款
    return render(request, 'customer_order_pay.html')


def customer_invoice_list(request):  # 用户发票列表
    return render(request, 'customer_invoice_list.html')


def customer_invoice_demand(request):  # 用户发票索取
    return render(request, 'customer_invoice_demand.html')


def customer_invoice_info(request):  # 用户发票信息
    return render(request, 'customer_invoice_info.html')


def customer_coupon_list(request):  # 用户优惠券列表
    return render(request, 'customer_coupon_list.html')


def customer_message_list(request):  # 用户消息列表
    return render(request, 'customer_message_list.html')


def customer_message_info(request):  # 用户消息详情
    return render(request, 'customer_message_info.html')

@csrf_exempt
def uploadify_script(request):  # 前端 uploadify在后台的处理函数，用于上传文件的处理
    ret = "0"  # 记录返回状态
    file = request.FILES.get("Filedata", None)  # 从request中获取文件类
    if file:
        result, path_name = profile_upload(file, request)  # 处理文件函数
        if result:
            ret = "1"
        else:
            ret = "2"
        jsons = path_name
        return HttpResponse(json.dumps(jsons, ensure_ascii=False))
    else:
        jsons = 'failed'
        return HttpResponse(json.dumps(jsons, ensure_ascii=False))


# def userlogout(request):
#     print 11111111111111111
#     auth.logout(request)
#     return render(request,'indexNew.html')


@csrf_exempt
def profile_upload(file, request):  # 处理文件函数，函数之间共享网页传来的参数，传递request就好了想

    project_ID=request.GET['project_id']
    classify=request.GET['classify']
    request.session['classify']=classify
    user=request.user

    sub_dir = 'DICOM'
    if not request.user.is_superuser:
        sub_dir='DICOM'
        user=request.user
    else:
        sub_dir='STL'

    if file:  # 如果文件有效
        path = os.path.join(settings.BASE_DIR, 'upload') + '\\' + str(user.username)+'\\'+ classify +'\\'+project_ID+'\\'+ sub_dir# 生成路径
        if not os.path.exists(path):  # 如果路径不存在 就生成
            os.makedirs(path)
        # file_name=str(uuid.uuid1())+".jpg"
        file_name = str(uuid.uuid1()) + '-' + file.name

        # fname = os.path.join(settings.MEDIA_ROOT,filename)
        path_file = os.path.join(path, file_name)  # 将路径和文件名结合
        fp = open(path_file, 'wb')  # 以二进制方法写文件，生成对象fb
        for content in file.chunks():  # 将文件分段读取
            fp.write(content)  # 写入fb
        fp.close()  # 关闭流
        return (True, file_name)  # change
    return (False, 'failed')  # change

@csrf_exempt
def profile_delte(request):  # 删除文件处理
    del_file = request.POST.get("delete_file", '')
    if del_file:
        os.remove(del_file)
        return JsonResponse(del_file, safe=False)
    else:
        return JsonResponse('failed', safe=False)
# 管理员操作

def administrator_user_info_list(request):  # 管理员用户个人信息管理
    if not request.user.is_authenticated():
        return redirect('/login')
    Users = xmqb_model.UserInfo.objects.all()
    return render(request, 'administrator_user_info_list.html', {'Users': Users})


def administrator_user_info_alter(request):  # 管理员用户个人信息修改
    Id = request.GET['user_id']
    user = xmqb_model.User.objects.get(id=Id)
    if not request.user.is_authenticated():
        print 'not log in'
        return redirect('/weblogin')
    elif not request.user.is_superuser:
        print 'not super user'
        return redirect('/')
    if request.method == 'GET':
        thisUser = xmqb_model.UserInfo.objects.get(user=user)
        form = xmqb_form.UserInform(initial={
            'user_name': thisUser.user_name,
            'email':thisUser.user_email,
            'user_identify': thisUser.user_identify,
            'hospital': thisUser.hospital,
            'department': thisUser.department,
            'position': thisUser.position,
            'address': thisUser.address,
            'pic_dir': thisUser.pic_dir,
            'abstract': thisUser.abstract
        })
        return render(request, 'administrator_user_info_alter.html', {'form': form, 'show_id': Id})
    else:
        form = xmqb_form.UserInform(request.POST)

        if form.is_valid():
            user_info = xmqb_model.UserInfo.objects.get(user=user)
            user_info.user_name = form.cleaned_data['user_name']
            user_info.user_telephone = form.cleaned_data['user_telephone']
            user_info.user_email = form.cleaned_data['email']
            user_info.user_identify = form.cleaned_data['user_identify']
            user_info.hospital = form.cleaned_data['hospital']
            user_info.department = form.cleaned_data['department']
            user_info.position = form.cleaned_data['position']
            user_info.address = form.cleaned_data['address']
            # user_info.pic_dir = form.cleaned_data['pic_dir']
            user_info.abstract = form.cleaned_data['abstract']
            user_info.save()
        else:
            return render(request, 'administrator_user_info_alter.html', {'form': form})
        Users = xmqb_model.UserInfo.objects.all()
        return render(request, 'administrator_user_info_list.html', {'Users': Users})


def administrator_account_list(request):  # 管理员账号管理
    if not request.user.is_authenticated():
        return redirect('/login')
    Users = xmqb_model.UserInfo.objects.all()
    return render(request, 'administrator_account_list.html', {'Users': Users})


def administrator_account_alter(request):  # 管理员账号信息修改
    Id = request.GET['user_id']
    user_info = xmqb_model.UserInfo.objects.get(user=Id)
    return render(request, 'administrator_account_alter.html', {'user_info': user_info, 'method': '0'})


def administrator_password_change(request):  # 修改密码
    Id = request.GET['user_id']
    if request.method == 'POST':
        form = xmqb_form.AdministratorChangePasswordForm(request.POST)
        if form.is_valid():
            newpassword = form.cleaned_data['password']
            if request.user.is_superuser == 1:
                user = xmqb_model.User.objects.get(id=Id)
                user.set_password(newpassword)
                user.save()
            else:
                return redirect('/login')
        user_info = xmqb_model.UserInfo.objects.get(user=Id)
        return render(request, 'administrator_account_alter.html', {'user_info': user_info, 'method': '1'})
    else:
        user_info = xmqb_model.UserInfo.objects.get(user=Id)
        form = xmqb_form.AdministratorChangePasswordForm()
        return render(request, 'administrator_password_change.html',{'user_info':user_info,'form': form})


def administrator_project_list(request):  # 管理员项目管理
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 1:
        return redirect('/login')
    project = xmqb_model.Project.objects.all()
    return render(request, 'administrator_project_list.html', {'project': project})


def administrator_project_info(request):  # 管理员项目信息查看
    if not request.user.is_authenticated():
        return redirect('/login')
    project_id = request.GET['project_id']
    project = xmqb_model.Project.objects.get(project=project_id)
    parts = xmqb_model.ProjectPart.objects.filter(project=project)

    form = xmqb_form.ProjectForm(initial={
        'project_name': project.project_name,
        'classify': project.classify,
        'patient_name': project.patient_name,
        'patient_sex': project.patient_sex,
        'patient_age': project.patient_age,
        'patient_address': project.patient_address,
        'remark': project.remark
    })
    return render(request, 'administrator_project_info.html', {'form': form, 'project': project,'parts':parts})


def administrator_project_alter(request):  # 管理员项目信息修改
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 1:
        return redirect('/login')
    project_id = request.GET['project_id']

    if request.method == 'GET':
        try:
            project = xmqb_model.Project.objects.get(project=project_id)

        except:
            return HttpResponse("请选择项目")

        selected_parts = xmqb_model.ProjectPart.objects.filter(project=project)
        parts = xmqb_model.Price.objects.all()
        part_relation = xmqb_model.PartRelation.objects.all()

        form = xmqb_form.ProjectForm(initial={
            'project_name': project.project_name,
            'classify': project.classify,
            'patient_name': project.patient_name,
            'patient_sex': project.patient_sex,
            'patient_age': project.patient_age,
            'patient_address': project.patient_address,
            'remark': project.remark
        })
        return render(request, 'administrator_project_alter.html', {'form': form, 'project': project, 'selected_parts': selected_parts,'parts': parts, 'part_relation': part_relation })

    else:
        form = xmqb_form.ProjectForm(request.POST)

        if form.is_valid():
            project = xmqb_model.Project.objects.get(project=project_id)
            project.project_name = form.cleaned_data['project_name']
            project.patient_name = form.cleaned_data['patient_name']
            project.patient_sex = form.cleaned_data['patient_sex']
            project.patient_age = form.cleaned_data['patient_age']
            project.patient_address = form.cleaned_data['patient_address']
            project.remark = form.cleaned_data['remark']
            project.save()
            partlist = form.cleaned_data['part']
            price = 0

            for everypart in partlist:
                part = xmqb_model.Price.objects.get(part=everypart)
                try:
                    project_part = xmqb_model.ProjectPart.objects.get(project=project, part=part)
                except:
                    project_part = xmqb_model.ProjectPart.objects.create(project=project, part=part)
                    price += part.part_price

                project_part.save()

            if not price == 0:
                order = xmqb_model.Order.objects.create(
                    order=time.strftime('%y%m%d%H%M%S') + str((project.user.id) % 10000).zfill(4) + str(
                        (random.randint(0, 100) % 100)).zfill(2),
                    user=project.user, project=project, classify=project.classify, order_type=u'修改',
                    order_price=price)  # 生成工程的同时再生成 对应的订单
                order.save()
                project.status = 1
        else:
            return render(request, 'administrator_project_alter.html', {'form': form})
    projects = xmqb_model.Project.objects.all()
    return render(request, 'administrator_project_list.html', {'project': projects})


def administrator_project_delete(request):  # 管理员项目删除
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 1:
        return redirect('/login')
    project_id = request.GET['project_id']
    try:
        project = xmqb_model.Project.objects.get(project=project_id)
        project.delete()
    except:
        return HttpResponse("此项目不存在")
    projects = xmqb_model.Project.objects.all()
    return render(request, 'administrator_project_list.html', {'project': projects})


def administrator_work_order_distribute(request):  # 管理工单分配
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 1:
        return redirect('/login')
    if request.method == 'GET':
        workOrders = xmqb_model.WorkOrder.objects.all()
        processors = xmqb_model.Worker.objects.filter(worker_position='处理员')
        assessors = xmqb_model.Worker.objects.filter(worker_position='审核员')
        return render(request, 'administrator_work_order_distribute.html', {'workOrders': workOrders,'processors':processors,'assessors':assessors})
    else:
        check_box_list = request.POST.getlist('projectCheckbox')
        processors_select = request.POST.getlist('processorRadio')
        assessors_select = request.POST.getlist('assessorRadio')
        for workOrder_id in check_box_list:
            workOrder = xmqb_model.WorkOrder.objects.get(order=workOrder_id)
            assessor = xmqb_model.Worker.objects.get(worker=assessors_select[0])
            processor = xmqb_model.User.objects.get(worker=processors_select[0])
            workOrder.assessor = assessor
            workOrder.processor = processor
            workOrder.status = 1
            workOrder.save()
        workOrders = xmqb_model.WorkOrder.objects.all()
        processors = xmqb_model.Worker.objects.filter(worker_position='处理员')
        assessors = xmqb_model.Worker.objects.filter(worker_position='审核员')
        return render(request, 'administrator_work_order_distribute.html',
                      {'workOrders': workOrders, 'processors': processors, 'assessors': assessors})


def administrator_work_order_handle_list(request):  # 工单处理列表
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 2:
        return redirect('/login')
    workOrders = xmqb_model.WorkOrder.objects.filter(processor=request.user)
    return render(request, 'administrator_work_order_handle_list.html',{'workOrders':workOrders})


def administrator_work_order_handle(request):  # 工单处理
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 2:
        return redirect('/login')
    workorder =xmqb_model.WorkOrder.objects.get(order=request.GET['workorder_id'])
    project_id = workorder.project_id
    project = xmqb_model.Project.objects.get(project=project_id)
    parts = xmqb_model.ProjectPart.objects.filter(project=project)

    form = xmqb_form.ProjectForm(initial={
        'project_name': project.project_name,
        'classify': project.classify,
        'patient_name': project.patient_name,
        'patient_sex': project.patient_sex,
        'patient_age': project.patient_age,
        'patient_address': project.patient_address,
        'remark': project.remark
    })
    return render(request, 'administrator_work_order_handle.html', {'form': form, 'project': project, 'parts': parts})


def administrator_work_order_assess_list(request):  # 工单审核列表
    render(request, 'administrator_work_order_assess.html')


def administrator_work_order_assess_handle(request):  # 工单审核
    render(request, 'administrator_work_order_assess.html')


def administrator_order_list(request):  # 管理员订单列表查看
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 1:
        return redirect('/login')
    orders = xmqb_model.Order.objects.all()
    return render(request, 'administrator_order_list.html', {'orders': orders})


def administrator_order_info(request):  # 管理员订单信息查看
    render(request, 'administrator_order_list.html')


def administrator_invoice_list(request):  # 管理员发票列表
    render(request, 'administrator_order_list.html')


def administrator_invoice_handle(request):  # 管理员发票处理
    render(request, 'administrator_invoice_handle.html')


def administrator_invoice_info(request):  # 管理员发票信息查看
    render(request, 'administrator_invoice_info.html')


def administrator_coupon_distribute(request):  # 管理员优惠券发放
    render(request, 'administrator_coupon_distribute.html')


def administrator_coupon_list(request):  # 管理员优惠券列表
    render(request, 'administrator_coupon_list.html')


def administrator_coupon_delete(request):  # 管理员优惠券删除
    render(request, 'administrator_coupon_delete.html')


def administrator_coupon_alter(request):  # 管理员优惠券修改
    render(request, 'administrator_coupon_alter.html')


def administrator_price_list(request):  # 管理员价格列表
    render(request, 'administrator_price_alter.html')


def administrator_price_alter(request):  # 管理员价格修改
    render(request, 'administrator_price_alter.html')


def administrator_message_send(request):  # 管理员消息发送
    render(request, 'administrator_message_send.html')
