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
from django.utils import timezone
import os, random
import forms as xmqb_form
import models as xmqb_model
from django.db.models import Q
import time
import copy
# 图片验证码引用包
import StringIO
from xmqb.Helper import Checkcode
# 支付用api
from alipay_API import Alipay
from qbypt.settings import DOWNLOAD_DIR
import json
import top.api
import unicodedata
# Create your views here.

# 创建支付对象，用以生成支付链接
alipay = Alipay(pid='2088421836722555', key='x5b1vxvggtye0br2o0bgl3lp4lz1d2iq',
                seller_email='xmstrongyk@163.com')


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
            classifys = xmqb_model.Classify.objects.all()
            for item in classifys:
                print item.classify_name
                # timefield需要的格式 YYYY-MM-DD HH:MM 暂定优惠券有效时间为60天
                coupon = xmqb_model.Coupon(coupon=str(user.id) + str(uuid.uuid1())[0:20], user=user, amount=500,
                                           rest_amount=500, type=item,
                                           deliver_time=time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())),
                                           deadline_time=time.strftime('%Y-%m-%d %H:%M',
                                                                       time.localtime(time.time() + 60 * 60 * 24 * 60)))
                coupon.save()
            return render(request, 'index.html')
        else:
            return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': xmqb_form.RegisterForm()})

def check_code(request):  # 用户接收短信验证码
    phone_number=request.GET['phone_number']
    users=xmqb_model.UserInfo.objects.filter(user_telephone=phone_number)
    if len(users)>0:
        return HttpResponse("此号码已存在")
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.set_app_info(top.appinfo("23744157", "5e0763455c8f5b66c295f13c6184928e"))
    phone_number=unicodedata.normalize('NFKD',phone_number).encode('ascii','ignore') # 将手机号码转换成ascii编码
    req.extend = ""
    req.sms_type = "normal"
    req.sms_free_sign_name = "王弘轩"
    # 生成随机验证码
    codes=[0,1,2,3,4,5,6,7,8,9]
    random.shuffle(codes)
    code=''
    for i in range(4):
        temp_index=int(random.uniform(0,9))
        code=code+str(codes[temp_index])
    req.sms_param = "{code:'"+code+"'}"
    req.rec_num = phone_number
    req.sms_template_code = "SMS_57820069"
    try:
        resp = req.getResponse()
        print (resp)
        ajax_list={'status':"验证码已发送",'code':code}
        return JsonResponse(ajax_list)
    except Exception, e:
        print (e)
        ajax_list = {'status': "error"}
        return HttpResponse(ajax_list)

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
            return render(request, 'customer_user_info.html', {'form': form})


def customer_account_info(request):  # 用户账号信息
    if not request.user.is_authenticated():
        return redirect('/login')
    user_info = xmqb_model.UserInfo.objects.get(user=request.user)
    return render(request, 'customer_account_info.html', {'user_info': user_info, 'method': '0'})


def customer_password_change(request):  # 修改密码
    if request.method == 'POST':
        form = xmqb_form.ChangePasswordForm(request.POST)
        if form.is_valid():
            identifying_code = form.cleaned_data['identifying_code']

            newpassword = form.cleaned_data['password']
            if request.user.is_authenticated():
                user = request.user
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
            return render(request, 'login.html', {'form': form, 'method': '2'})
    else:
        form = xmqb_form.ChangePasswordForm()
        return render(request, 'customer_password_change.html',
                      {'method': '0', 'form': form, 'error': "", 'username': '', 'pwd': ''})


def CheckCode(request):  # 图片验证码生成方法
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
    projects = xmqb_model.Project.objects.filter(user=request.user)
    pros = []
    # 向前台传递这里生成的字典列表，包括项目信息，订单信息和支付链接
    for foo in projects:
        if foo.status == '1':
            temp_url = {'status': foo.status,
                        'project': foo.project,
                        'project_name': foo.project_name,
                        'classify_name': foo.classify.classify_name,
                        'create_time': foo.create_time,
                        }
        else:
            temp_url = {'status': foo.status,
                        'project': foo.project,
                        'project_name': foo.project_name,
                        'classify_name': foo.classify.classify_name,
                        'create_time': foo.create_time,
                        }
        pros.append(temp_url)
    return render(request, 'customer_project_list.html', {'project': pros})


def customer_project_new(request):  # 用户新建项目
    if not request.user.is_authenticated():
        return redirect('/login/')
    if (request.method == 'POST'):
        form = xmqb_form.ProjectForm(request.POST)
        if form.is_valid():
            classify = xmqb_model.Classify.objects.get(classify=form.cleaned_data['classify'])
            project = xmqb_model.Project.objects.create(user=request.user, classify=classify,
                                                        project=time.strftime('%y%m%d%H%M%S') + str(
                                                            (request.user.id) % 100000).zfill(4))

            project.project_name = form.cleaned_data['project_name']
            project.classify = classify
            project.status = 0
            project.patient_name = form.cleaned_data['patient_name']
            project.patient_sex = form.cleaned_data['patient_sex']
            project.patient_age = form.cleaned_data['patient_age']
            project.patient_address = form.cleaned_data['patient_address']
            project.remark = form.cleaned_data['remark']
            # upload_name = form.cleaned_data['upload_name']
            # project.upload_name = upload_name
            # if len(upload_name) > 0:
            #     project.status = '1'
            # else:
            #     project.status = '0'
            project.save()
            partlist = form.cleaned_data['part']
            coupon_id = request.POST.get('coupon')

            price = 0

            for everypart in partlist:
                part = xmqb_model.Price.objects.get(part=everypart)
                project_part = xmqb_model.ProjectPart.objects.create(project=project, part=part)
                project_part.save()
                price += part.part_price

            try:
                coupon = xmqb_model.Coupon.objects.get(coupon=coupon_id)
                if price >= coupon.rest_amount:
                    price -= coupon.rest_amount
                    coupon.rest_amount = 0
                    coupon.save()
                else:
                    price = 0
                    coupon.rest_amount -= price
                    coupon.save()
            except Exception, e:
                print e

            order = xmqb_model.Order.objects.create(
                order=str(time.strftime('%y%m%d%H%M%S') + str((request.user.id) % 10000).zfill(4) + str(
                    (random.randint(0, 100) % 100)).zfill(2)),
                user=request.user, project=project, classify=classify, order_type=u'新建',
                order_price=price)  # 生成工程的同时再生成 对应的订单
            order.save()

            return redirect('/customer_project_list')
        else:
            part = xmqb_model.Price.objects.all()
            part_relation = xmqb_model.PartRelation.objects.all()
            return render(request, 'customer_project_new.html',
                          {'form': form, 'part': part, 'part_relation': part_relation})
    else:
        form = xmqb_form.ProjectForm()
        part = xmqb_model.Price.objects.all()
        part_relation = xmqb_model.PartRelation.objects.all()
        coupons = xmqb_model.Coupon.objects.filter(user=request.user,rest_amount__gt = 0, deadline_time__gte=timezone.now())
        return render(request, 'customer_project_new.html',
                      {'form': form, 'part': part, 'part_relation': part_relation, 'coupons': coupons})


@csrf_exempt
def customer_file_upload(request):
    if request.method == 'POST':
        project_ID = request.POST['project_ID']
        classify = request.POST['id_classify']
        upload_name = request.POST['id_upload_name']
        if len(upload_name) > 0:
            project = xmqb_model.Project.objects.get(project=project_ID)
            project.upload_name = upload_name
            project.status = '1'
            project.save()
            return render(request, 'customer_project_list.html', {'method': '1'})
        else:
            return render(request, 'customer_project_list.html', {'method': '0'})
    else:
        project_ID = request.GET['project_ID']
        project = xmqb_model.Project.objects.get(project=project_ID)
        return render(request, 'customer_upload.html', {'project': project})


def customer_project_info(request):  # 用户查看项目
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
    return render(request, 'customer_project_info.html', {'form': form, 'project': project, 'parts': parts})


def customer_project_alert(request):  # 用户修改项目
    if not request.user.is_authenticated():
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
        return render(request, 'customer_project_alert.html',
                      {'form': form, 'project': project, 'selected_parts': selected_parts, 'parts': parts,
                       'part_relation': part_relation})

    else:
        form = xmqb_form.ProjectForm(request.POST)
        print form.is_valid()
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

            if project.status == '3' or project.status == '2':          # 用户已付款的情况下修改订单
                if not price == 0:
                    order = xmqb_model.Order.objects.create(
                        order=time.strftime('%y%m%d%H%M%S') + str((project.user.id) % 10000).zfill(4) + str(
                            (random.randint(0, 100) % 100)).zfill(2),
                        user=project.user, project=project, classify=project.classify, order_type=u'修改',
                        order_price=price)  # 生成工程的同时再生成 对应的订单
                    order.save()
                    project.status = 1
                    project.save()
            else:                                                       # 用户该项还没有付款情况下 修改订单
                if not price == 0:
                    project = xmqb_model.Project.objects.get(project=project_id)
                    try:
                        order = xmqb_model.Order.objects.get(project=project,is_pay=0)
                        order.order_price += price
                        order.save()
                    except Exception,e:
                        return HttpResponse('支付异常')

        else:
            return render(request, 'customer_project_alert.html', {'form': form})
    projects = xmqb_model.Project.objects.filter(user=request.user)
    return render(request, 'customer_project_list.html', {'project': projects})


def customer_project_delete(request):  # 用户项目删除
    if not request.user.is_authenticated():
        return redirect('/login')
    project_id = request.GET['project_id']
    try:
        project = xmqb_model.Project.objects.get(project=project_id)
        project.delete()
    except:
        return HttpResponse("此项目不存在")
    # projects = xmqb_model.Project.objects.all()
    return redirect('/customer_project_list/')


def customer_stl_show(request):  # 用户查看3D模型
    if not request.user.is_authenticated():
        return redirect('/login')
    if request.method == "GET":
        try:
            project_id = request.GET['project_id']
            if project_id:
                record = xmqb_model.Project.objects.get(project=project_id)
                url = u'' + DOWNLOAD_DIR + '/' + str(record.user.username) + '/' + str(record.classify_id) + '/' + str(
                    record.project) + '/STL/'
                url = url.replace('\\', '/')
                sub_url = u'' + '/download' + '/' + str(record.user.username) + '/' + str(
                    record.classify_id) + '/' + str(record.project) + '/STL/'
                sub_url = sub_url.replace('\\', '/')
                part_url = os.listdir(url)
                part_name = copy.copy(part_url)
                index = []
                for x in xrange(len(part_name)):
                    part_name[x] = part_name[x][0:-4]
                    index.append(x + 1)
                for i in xrange(len(part_url)):
                    part_url[i] = sub_url + part_url[i]
                part_name = zip(zip(part_name, index), part_url)
                project = {'name': record.project_name,
                           'part_name': part_name,
                           'stl_url': part_url,
                           'num': len(part_name)}
                return render(request, 'stl_show.html', {'project': project, 'urls': json.dumps(part_url)})
        except Exception, e:
            print e
            pass

    record = xmqb_model.Project.objects.filter(user_id=request.user, order__is_complete='1')
    return render(request, 'customer_stl_show.html', {'project': record})


def customer_order_list(request):  # 用户订单列表
    orders = xmqb_model.Order.objects.filter(user=request.user)
    pays = []
    for foo in orders:
        if not foo.is_pay:
            temp_url = {'is_complete': foo.is_complete,
                        'username': foo.user.username,
                        'is_pay': foo.is_pay,
                        'project': foo.project,
                        'project_name': foo.project.project_name,
                        'classify_name': foo.project.classify.classify_name,
                        'start_date': foo.start_date,
                        'order_price': foo.order_price,
                        'out_trade_no': foo.order,
                        'url': alipay.create_direct_pay_by_user_url(out_trade_no=foo.order,
                                                                    subject=u'测试', total_fee=foo.order_price,
                                                                    return_url='http://127.0.0.1:8000/customer_project_list',
                                                                    notify_url='http://www.tencent.com/')
                        }
        else:
            temp_url = {'is_complete': foo.is_complete,
                        'username': foo.user.username,
                        'is_pay': foo.is_pay,
                        'project': foo.project,
                        'project_name': foo.project.project_name,
                        'classify_name': foo.project.classify.classify_name,
                        'start_date': foo.start_date,
                        'order_price': foo.order_price,
                        'out_trade_no': foo.order,
                        'url': "/"
                        }
        pays.append(temp_url)
    return render(request, 'customer_order_list.html', {'orders': pays})


def customer_order_info(request):  # 用户订单信息
    if not request.user.is_authenticated():
        return redirect('/login')
    if request.method == "GET":
        record = xmqb_model.Order.objects.get(order=request.GET['order_id'])
        invoice = xmqb_model.Invoice.objects.filter(order_id=record.order)
        if invoice:
            invoice = True
        else:
            invoice = False
        order_detial = {'order': record.order,
                        'time': record.start_date,
                        'price': record.order_price,
                        'invoice': invoice,
                        'project': record.project_id}

        return render(request, 'customer_order_info.html', {'order': order_detial})

    return render(request, 'customer_order_info.html')


def customer_order_pay(request):  # 用户订单付款
    return render(request, 'customer_order_pay.html')


def customer_invoice_list(request):  # 用户发票列表
    if not request.user.is_authenticated():
        return redirect('/login')
    orders=xmqb_model.Order.objects.filter(user=request.user,is_complete='1')
    invoices=xmqb_model.Invoice.objects.filter(user=request.user)
    return render(request, 'customer_invoice_list.html',{'orders':orders,'invoices':invoices})


def customer_invoice_demand(request):  # 用户发票索取
    if not request.user.is_authenticated():
        return redirect('/login/')
    if request.method=='GET':
        order_id=request.GET['order_id']
        form = xmqb_form.InvoiceDemandForm()
        try:
            order=xmqb_model.Order.objects.get(order=order_id)
        except:
            return render(request, 'customer_invoice_demand.html', {'order_id': order_id, 'form': form})
        return render(request,'customer_invoice_demand.html',{'order_id':order_id,'form':form,'order':order})
    if (request.method == 'POST'):
        form = xmqb_form.InvoiceDemandForm(request.POST)
        if form.is_valid():
            order_id=request.POST['order']
            amount=request.POST['amount']
            order=xmqb_model.Order.objects.get(order=order_id) # 查找发票对应的订单
            title=form.cleaned_data['title']
            demand_type=form.cleaned_data['demand_type']
            invoice_type=form.cleaned_data['invoice_type']
            recipient_name=form.cleaned_data['recipient_name']
            pro_cit=request.POST['pc']    # 获取表单中的省份和城市信息
            address=pro_cit+form.cleaned_data['address']
            telephone=form.cleaned_data['telephone']
            deliver_id=form.cleaned_data['deliver_id']
            deliver_company=form.cleaned_data['deliver_company']
            remark=form.cleaned_data['remark']
            invoice=xmqb_model.Invoice.objects.create(title=title,demand_type=demand_type,order=order,user=order.user,
                                                      invoice_type=invoice_type,recipient_name=recipient_name,
                                                      address=address,telephone=telephone,deliver_id=deliver_id,
                                                      deliver_company=deliver_company,remark=remark,amount=amount
                                                      )
            invoice.save()
            order.is_complete='2'  # 申请发票成功后，修改订单状态
            order.save()
            return redirect('/customer_invoice_list/')
        else:
            return render(request, 'customer_invoice_demand.html',{'form':form})
    else:
        form=xmqb_form.InvoiceDemandForm()
        return render(request, 'customer_invoice_demand.html',{'form':form})


def customer_invoice_info(request):  # 用户发票信息
    order_id=request.GET['order_id']
    order=xmqb_model.Order.objects.get(order=order_id)
    invoice=xmqb_model.Invoice.objects.get(order=order)
    form=xmqb_form.InvoiceDemandForm(initial={
                                    'title':invoice.title,'demand_type':invoice.demand_type,
                                    'invoice_type':invoice.invoice_type,
                                    'recipient_name':invoice.recipient_name,
                                    'address':invoice.address,
                                    'telephone':invoice.telephone,
                                    'deliver_id':invoice.deliver_id,
                                    'deliver_company':invoice.deliver_company,
                                    'remark':invoice.remark})
    return render(request, 'customer_invoice_info.html',{'invlice':invoice,'form':form})


def customer_coupon_list(request):  # 用户优惠券列表
    return render(request, 'customer_coupon_list.html')


def customer_message_list(request):  # 用户消息列表
    if not request.user.is_authenticated():
        return redirect('/login')
    record = xmqb_model.Message.objects.filter(user_id=request.user.id)
    print request.user.id
    not_read = len(xmqb_model.Message.objects.filter(user_id=request.user.id, is_read=0))
    return render(request, 'customer_message_receive.html', {'messages': record, 'message': not_read})

def customer_message_info(request):  # 用户消息详情
    if not request.user.is_authenticated():
        return redirect('/login')

    if request.method == "GET":
        id = request.GET['message']
        record = xmqb_model.Message.objects.get(message=id)

        forms = xmqb_form.Read_Message(
            initial={'receiver': record.user_id, 'title': record.title, 'context': record.message_content})

        record.is_read = 1
        record.read_time = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        record.save()

        return render(request, 'customer_message_read.html', {'form': forms})
    else:
        return redirect('/customer_message_receive')

def customer_suggestion(request):
    return render(request, 'customer_suggestion.html')

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
    project_ID = request.GET['project_id']
    classify = request.GET['classify']
    request.session['classify'] = classify
    project = xmqb_model.Project.objects.get(project=project_ID)
    user = project.user
    sub_dir = 'DICOM'
    if not request.user.is_superuser:
        sub_dir = 'DICOM'
        user = request.user
    else:
        sub_dir = 'STL'
    if file:  # 如果文件有效
        path = os.path.join(settings.BASE_DIR, 'upload') + '\\' + str(
            user.username) + '\\' + classify + '\\' + project_ID + '\\' + sub_dir  # 生成路径
        if not os.path.exists(path):  # 如果路径不存在 就生成
            os.makedirs(path)
        # file_name=str(uuid.uuid1())+".jpg"
        file_name = file.name

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

        return redirect('/weblogin')
    elif not request.user.is_superuser:
        return redirect('/')
    if request.method == 'GET':
        thisUser = xmqb_model.UserInfo.objects.get(user=user)
        form = xmqb_form.UserInform(initial={
            'user_name': thisUser.user_name,
            'email': thisUser.user_email,
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
        return redirect('/administrator_user_info_list/')


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
        return render(request, 'administrator_password_change.html', {'user_info': user_info, 'form': form})


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
    return render(request, 'administrator_project_info.html', {'form': form, 'project': project, 'parts': parts})


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
        pass
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
        return render(request, 'administrator_project_alter.html',
                      {'form': form, 'project': project, 'selected_parts': selected_parts, 'parts': parts,
                       'part_relation': part_relation})

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
    return redirect('/administrator_project_list/')


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
    pass
    return redirect('/administrator_project_list/')


def administrator_work_order_distribute(request):  # 管理工单分配
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 1:
        return redirect('/login')
    if request.method == 'GET':
        workOrders = xmqb_model.WorkOrder.objects.filter(Q(status=0) | Q(status=1))
        processors = xmqb_model.Worker.objects.filter(worker_position='处理员')
        assessors = xmqb_model.Worker.objects.filter(worker_position='审核员')
        return render(request, 'administrator_work_order_distribute.html',
                      {'workOrders': workOrders, 'processors': processors, 'assessors': assessors})
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
        workOrders = xmqb_model.WorkOrder.objects.filter(Q(status=0) | Q(status=1))
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
    return render(request, 'administrator_work_order_handle_list.html', {'workOrders': workOrders})


def administrator_work_order_handle(request):  # 工单处理
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 2:
        return redirect('/login')
    workorder = xmqb_model.WorkOrder.objects.get(order=request.GET['workorder_id'])
    if request.method == 'GET':
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
        return render(request, 'administrator_work_order_handle.html',
                      {'form': form, 'project': project, 'parts': parts})
    else:
        workorder.status = 2
        workorder.save()
        return redirect('/administrator_work_order_handle_list/')


def administrator_file_upload(request):
    if request.method == 'GET':
        project_ID = request.GET['project_ID']
        project = xmqb_model.Project.objects.get(project=project_ID)
        part_id = request.GET['part']
        part = xmqb_model.ProjectPart.objects.get(project=project, part=part_id)
        return render(request, 'administrator_upload.html', {'project': project, 'part': part})
    else:
        project_ID = request.POST['project_ID']
        part_id = request.POST['id_part']
        project = xmqb_model.Project.objects.get(project=project_ID)
        part = xmqb_model.ProjectPart.objects.get(project=project, part=part_id)
        upload_name = request.POST['id_upload_name']
        if len(upload_name) > 0:
            part.directory = upload_name
            part.save()
            return render(request, 'administrator_work_order_handle.html', {'method': '1'})
        else:
            return render(request, 'administrator_work_order_handle.html', {'method': '0'})


def administrator_work_order_assess_list(request):  # 工单审核列表
    assessor = xmqb_model.Worker.objects.get(worker=request.user)
    workOrders = xmqb_model.WorkOrder.objects.filter(Q(status=2) | Q(status=3) | Q(status=4),assessor=assessor)
    return render(request, 'administrator_work_order_assess_list.html', {'workOrders': workOrders})


def administrator_work_order_assess_handle(request):  # 工单审核
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 3:
        return redirect('/login')
    workorder = xmqb_model.WorkOrder.objects.get(order=request.GET['workorder_id'])
    if request.method == 'GET':
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
        return render(request, 'administrator_work_order_assess_handle.html',
                      {'form': form, 'project': project, 'parts': parts})
    else:
        project_id = workorder.project_id
        project = xmqb_model.Project.objects.get(project=project_id)
        order = workorder.order
        assess = request.POST.get('qualify')
        remark = request.POST.get('remark')
        if assess == '1':
            workorder.status = 4
            workorder.remark = remark
            project.status = '3'
            order.is_complete = 1
            order.save()
            project.save()
        else:
            workorder.status = 3
            workorder.remark = remark
        workorder.save()
        return redirect('/administrator_work_order_assess_list/')


def administrator_order_list(request):  # 管理员订单列表查看
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 4:
        return redirect('/login')
    orders = xmqb_model.Order.objects.all()
    return render(request, 'administrator_order_list.html', {'orders': orders})


def administrator_order_info(request):  # 管理员订单信息查看
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 1:
        return redirect('/login')
    if request.method == "GET":
        order_id = request.GET['order_id']
        record = xmqb_model.Order.objects.get(order=order_id)

        form = xmqb_form.Order_Detial(initial={'order_id': record.order,
                                               'user_name': record.user,
                                               'create_time': record.project.create_time,
                                               'order_price': record.order_price})
        return render(request, 'administrator_order_info.html', {'form': form})
    else:
        return redirect('/administrator_order_list')


def administrator_invoice_list(request):  # 管理员发票列表
    if not request.user.is_superuser:
        return redirect('/login')
    orders=xmqb_model.Order.objects.filter(is_complete='1')
    invoices=xmqb_model.Invoice.objects.all()
    delivered=[]
    undelivered=[]
    for inv in invoices:
        if len(inv.deliver_id)>0:
            delivered.append(inv)
        else:
            undelivered.append(inv)
    return render(request, 'administrator_invoice_list.html',{'orders':orders,'delivered':delivered,'undelivered':undelivered},)

def administrator_invoice_create(request):    # 管理员开发票
    if not request.user.is_superuser:
        return redirect('/login')
    if request.method == 'GET':
        order_id = request.GET['order_id']
        form = xmqb_form.InvoiceDemandForm()
        try:
            order = xmqb_model.Order.objects.get(order=order_id)
        except:
            return render(request, 'administrator_invoice_create.html', {'order_id': order_id, 'form': form})
        return render(request, 'administrator_invoice_create.html', {'order_id': order_id, 'form': form, 'order': order})
    if (request.method == 'POST'):
        form = xmqb_form.InvoiceDemandForm(request.POST)
        if form.is_valid():
            order_id = request.POST['order']
            amount = request.POST['amount']
            order = xmqb_model.Order.objects.get(order=order_id)  # 查找发票对应的订单
            title = form.cleaned_data['title']
            demand_type = form.cleaned_data['demand_type']
            invoice_type = form.cleaned_data['invoice_type']
            recipient_name = form.cleaned_data['recipient_name']
            address = form.cleaned_data['address']
            telephone = form.cleaned_data['telephone']
            deliver_id = form.cleaned_data['deliver_id']
            deliver_company = form.cleaned_data['deliver_company']
            remark = form.cleaned_data['remark']
            invoice = xmqb_model.Invoice.objects.create(title=title, demand_type=demand_type, order=order,
                                                        user=order.user,
                                                        invoice_type=invoice_type, recipient_name=recipient_name,
                                                        address=address, telephone=telephone, deliver_id=deliver_id,
                                                        deliver_company=deliver_company, remark=remark, amount=amount
                                                        )
            invoice.save()
            order.is_complete = '2'  # 申请发票成功后，修改订单状态
            order.save()
            return redirect('/administrator_invoice_list')
        else:
            return render(request, 'administrator_invoice_create.html', {'form': form})
    else:
        form = xmqb_form.InvoiceDemandForm()
        return render(request, 'administrator_invoice_create.html', {'form': form})

def administrator_invoice_handle(request):  # 管理员发票处理
    if not request.user.is_superuser:
        return redirect('/login')
    if request.method == 'GET':
        order_id = request.GET['order_id']
        invoice=xmqb_model.Invoice.objects.get(order=order_id) # 找到与订单对应的发票
        form = xmqb_form.InvoiceDemandForm(initial={'remark':invoice.remark})
        try:
            order = xmqb_model.Order.objects.get(order=order_id)
        except:
            return render(request, 'administrator_invoice_handle.html', {'order_id': order_id, 'form': form})
        return render(request, 'administrator_invoice_handle.html',
                      {'order_id': order_id, 'form': form, 'order': order})
    if request.method=='POST':
            order_id = request.POST['order']
            invoice=xmqb_model.Invoice.objects.get(order=order_id) # 找到与订单对应的发票
            invoice.deliver_id = request.POST['deliver_id']
            invoice.deliver_company = request.POST['deliver_company']
            invoice.remark = request.POST['remark']
            invoice.save()
            return redirect('/administrator_invoice_list')
    else:
        form = xmqb_form.InvoiceDemandForm()
        return render(request, 'administrator_invoice_handle.html',{'form':form})


def administrator_invoice_info(request):  # 管理员发票信息查看
    order_id = request.GET['order_id']
    order = xmqb_model.Order.objects.get(order=order_id)
    invoice = xmqb_model.Invoice.objects.get(order=order)
    form = xmqb_form.InvoiceDemandForm(initial={
        'title': invoice.title, 'demand_type': invoice.demand_type,
        'invoice_type': invoice.invoice_type,
        'recipient_name': invoice.recipient_name,
        'address': invoice.address,
        'telephone': invoice.telephone,
        'deliver_id': invoice.deliver_id,
        'deliver_company': invoice.deliver_company,
        'remark': invoice.remark})
    return render(request, 'administrator_invoice_info.html',{'form':form})


def administrator_coupon_distribute(request):  # 管理员优惠券发放
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 5:
        return redirect('/login')
    if request.method == 'GET':
        form = xmqb_form.CouponForm()
        users = xmqb_model.UserInfo.objects.all()
        return render(request, 'administrator_coupon_distribute.html', {"form": form, "users": users})
    else:
        form = xmqb_form.CouponForm(request.POST)
        if form.is_valid():
            deadline_time = form.cleaned_data['deadline_time']
            amount = form.cleaned_data['amount']
            remark = form.cleaned_data['remark']
            type = form.cleaned_data['type']
            classify = xmqb_model.Classify.objects.get(classify=type)
            checkusers = request.POST.getlist('users')
            for everyUser in checkusers:
                user = xmqb_model.User.objects.get(username=everyUser)
                coupon = xmqb_model.Coupon.objects.create(coupon=str(user.id) + str(uuid.uuid1())[0:20], user=user, deadline_time=deadline_time, amount=amount,
                                                          remark=remark, type=classify, rest_amount=amount)
                coupon.save()
            return redirect('/administrator_coupon_list/')
        else:
            users = xmqb_model.UserInfo.objects.all()
            return render(request, 'administrator_coupon_distribute.html', {"form": form, "users": users})


def administrator_coupon_list(request):  # 管理员优惠券列表
    coupons = xmqb_model.Coupon.objects.all()
    return render(request, 'administrator_coupon_list.html', {'coupons': coupons})


def administrator_coupon_delete(request):  # 管理员优惠券删除
    coupon_id = request.GET['coupon']
    coupon = xmqb_model.Coupon.objects.get(coupon=coupon_id)
    coupon.delete()
    return redirect('/administrator_coupon_list/')


def administrator_coupon_alter(request):  # 管理员优惠券修改
    coupon_id = request.GET['coupon']
    coupon = xmqb_model.Coupon.objects.get(coupon=coupon_id)
    if request.method == 'GET':
        form = xmqb_form.CouponForm(initial={
            'deadline_time': coupon.deadline_time,
            'amount': coupon.rest_amount,
            'type': coupon.type,
            'remark': coupon.remark,
        })
        return render(request, 'administrator_coupon_alter.html', {"form": form, "coupon": coupon})
    else:
        form = xmqb_form.CouponForm(request.POST)
        if form.is_valid():
            coupon.deadline_time = form.cleaned_data['deadline_time']
            coupon.rest_amount = form.cleaned_data['amount']
            classify = xmqb_model.Classify.objects.get(classify=form.cleaned_data['type'])
            coupon.type = classify
            coupon.remark = form.cleaned_data['remark']
            coupon.save()
            return redirect('/administrator_coupon_list/')
        else:
            return render(request, 'administrator_coupon_alter.html', {"form": form, "coupon": coupon})
        return redirect('/administrator_coupon_list/')


def administrator_price_list(request):  # 管理员服务价格列表
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 1:
        return redirect('/login')
    parts = xmqb_model.Price.objects.all()
    return render(request, 'administrator_price_list.html', {'parts': parts})


def administrator_price_new(request):  # 管理员新增服务
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 1:
        return redirect('/login')
    if request.method == "POST":
        form = xmqb_form.Add_Price(request.POST)
        if form.is_valid():
            classify = form.cleaned_data['classify']
            price_name = form.cleaned_data['price_name']
            price = form.cleaned_data['price']
            dis_price = form.cleaned_data['discount_price']
            record = xmqb_model.Price.objects.create(part_name=price_name, part_price=price, classify_id=classify,
                                                     check_all_price=dis_price)
            record.save()
            return redirect('/administrator_price_list')

    form = xmqb_form.Add_Price()
    return render(request, 'administrator_price_new.html', {'form': form})


def administrator_part_price_alter(request):  # 管理员服务价格修改
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 1:
        return redirect('/login')
    if request.method == 'GET':
        part_id = request.GET['part_ID']
        old_price = request.GET['part_price']
        name = xmqb_model.Price.objects.get(part=int(part_id))

        change_price_form = xmqb_form.ChangePriceForm(initial={
            'old_price': old_price,
            'order_id': part_id,
        })
        return render(request, 'administrator_part_price_alter.html',
                      {'form': change_price_form, "name": name.part_name})
    if request.method == 'POST':
        change_price_form = xmqb_form.ChangePriceForm(request.POST)
        if change_price_form.is_valid():
            order_id = change_price_form.cleaned_data['order_id']
            set_price = change_price_form.cleaned_data['set_price']
            order = xmqb_model.Price.objects.get(part=order_id)
            order.part_price = set_price
            order.save()
            return redirect('/administrator_price_list/')
        else:
            print 'invalid'
    else:
        print 'invalid'
    return redirect('/administrator_price_list/')


def administrator_price_alter(request):  # 管理员订单价格修改
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 1:
        return redirect('/login')
    if request.method == 'GET':
        if request.GET['state']:
            order_id = request.GET['order_ID']
            state = request.GET['state']
            record = xmqb_model.Order.objects.get(order=order_id)
            record.is_pay = state
            record.save()
            return redirect('/administrator_order_list')

        order_id = request.GET['order_ID']
        old_price = request.GET['order_price']
        change_price_form = xmqb_form.ChangePriceForm(initial={
            'old_price': old_price,
            'order_id': order_id,
        })
        return render(request, 'administrator_price_alter.html', {'form': change_price_form})
    if request.method == 'POST':
        change_price_form = xmqb_form.ChangePriceForm(request.POST)
        if change_price_form.is_valid():
            order_id = change_price_form.cleaned_data['order_id']
            set_price = change_price_form.cleaned_data['set_price']
            order = xmqb_model.Order.objects.get(order=order_id)
            order.order_price = set_price
            order.save()
        return redirect('/administrator_order_list')


def administrator_message_send(request):  # 管理员消息发送
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 1:
        return redirect('/login')
    if request.method == "GET":
        forms = xmqb_form.Send_Message()
        return render(request, 'administrator_message_send.html', {'form': forms})
    if request.method == "POST":
        forms = xmqb_form.Send_Message(request.POST)
        if forms.is_valid():
            receiver = forms.cleaned_data['receiver']
            title = forms.cleaned_data['title']
            context = forms.cleaned_data['context']

            Title = title
            Context = context
            Is_read = 0
            Send_worker_id = request.user.id
            User_id = receiver

            try:
                message_record = xmqb_model.Message.objects.create(title=Title, message_content=Context,
                                                                   is_read=Is_read,
                                                                   send_worker_id=receiver, user_id=User_id)
                message_record.save()
                forms = xmqb_form.Send_Message()
                return render(request, 'administrator_message_send.html', {'form': forms, 'type': 1})
            except Exception, e:
                forms = xmqb_form.Send_Message()
                return render(request, 'administrator_message_send.html', {'form': forms, 'type': 0})

        else:
            forms = xmqb_form.Send_Message()
            return render(request, 'administrator_message_send.html', {'form': forms, 'type': 0})


def administrator_message_receive(request):  # 管理员消息接受
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 1:
        return redirect('/login')
    record = xmqb_model.Message.objects.filter(user_id=request.user.id)
    not_read = len(xmqb_model.Message.objects.filter(user_id=request.user.id, is_read=0))
    return render(request, 'administrator_message_receive.html', {'messages': record, 'message': not_read})


def administrator_message_read(request):  # 阅读信息
    if not request.user.is_authenticated():
        return redirect('/login')
    if not request.user.is_superuser == 1:
        return redirect('/login')

    if request.method == "GET":
        id = request.GET['message']
        record = xmqb_model.Message.objects.get(message=id)

        forms = xmqb_form.Read_Message(
            initial={'receiver': record.user_id, 'title': record.title, 'context': record.message_content})

        record.is_read = 1
        record.read_time = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        record.save()

        return render(request, 'administrator_message_read.html', {'form': forms})
    else:
        return redirect('/administrator_message_receive')

def alipy_notify(request):
    if request.method == 'POST':
        dic = {"article_list": ['post']}
        dic['article_list'].append(request.POST['is_success'])
        dic['article_list'].append(request.POST['trade_status'])
        return render(request, 'index.html', {'dic', dic})
    elif request.method == 'GET':
        if request.GET['is_success'] == 'T' and request.GET['trade_status'] == 'TRADE_SUCCESS':
            thisorder = xmqb_model.Order.objects.get(order=request.GET['out_trade_no'])
            thisorder.is_pay = True  # 将当前已支付的订单设置为已支付
            thisproject = thisorder.project  # 将当前订单对应的项目设置为已支付状态
            thisproject.status = '2'
            # 支付完成生成工单,默认1号为审核员
            processor = auth.models.User.objects.get(username=1)
            worker = xmqb_model.Worker.objects.get(worker=processor)
            workorder = xmqb_model.WorkOrder.objects.create(project=thisproject, order=thisorder,
                                                            assessor=worker, processor=processor, status=0,
                                                            plan_complete_time=time.strftime('%Y-%m-%d %H:%M',
                                                                                             time.localtime(
                                                                                                 time.time() + 60 * 60 * 24 * 60))
                                                            )
            workorder.save()
            thisorder.save()
            thisproject.save()
            return redirect('/customer_order_list')
        else:
            return render(request, 'index.html', {'dic': 'failed'})
