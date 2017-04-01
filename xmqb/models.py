# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


# Create your models here.


# 用户信息表
class UserInfo(models.Model):
    user = models.OneToOneField(User, primary_key=True)  # 一一对应用户表

    user_name = models.CharField(max_length=10, null=True, blank=True)  # 用户姓名

    user_telephone = models.CharField(max_length=20, null=True, blank=True)  # 电话号码

    user_email = models.EmailField(max_length=20, null=True, blank=True)  # 电子邮件

    user_identify = models.CharField(max_length=10, null=True, blank=True)  # 身份

    hospital = models.CharField(max_length=20, null=True, blank=True)  # 医院

    department = models.CharField(max_length=20, null=True, blank=True)  # 部门

    position = models.CharField(max_length=10, null=True, blank=True)  # 职位

    address = models.CharField(max_length=20, null=True, blank=True)  # 地址

    pic_dir = models.CharField(max_length=50, null=True, blank=True)  # 头像存放目录

    abstract = models.TextField(max_length=100, null=True, blank=True)  # 个人简介

    def __unicode__(self):
        return self.user


# 分类表
class Classify(models.Model):
    classify = models.CharField(primary_key=True, max_length=3, null=False, blank=False)

    classify_name = models.CharField(max_length=30, null=False, blank=False)

    def __unicode__(self):
        return self.classify


# 项目表
class Project(models.Model):
    user = models.ForeignKey(User)  # 属于用户 外键

    project = models.CharField(primary_key=True, max_length=30, null=False, blank=False)  # 项目ID

    project_name = models.CharField(max_length=20, null=False, blank=True)  # 项目命名

    classify = models.ForeignKey(Classify)  # 项目类型

    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间

    status = models.CharField(max_length=5, default='0', null=False, blank=False)  # 完成状态 0未上传 1待处理 2 已完成

    upload_name = models.CharField(max_length=500, null=True, blank=True)  # 用户上传文件名

    remark = models.TextField(max_length=100, null=True)  # 用户备注

    patient_name = models.CharField(max_length=10, null=True, blank=True)  # 病人姓名

    patient_sex = models.CharField(max_length=5, null=True, blank=True)  # 病人性别

    patient_age = models.IntegerField(null=True, blank=True)  # 病人年纪

    patient_address = models.CharField(max_length=20, null=True, blank=True)  # 病人所属地区

    def __unicode__(self):
        return self.project_id


# 部位价格表
class Price(models.Model):
    part = models.AutoField(primary_key=True)

    classify = models.ForeignKey(Classify)  # 所属分类

    part_name = models.CharField(max_length=10, null=False, blank=True)  # 部位名称

    part_price = models.IntegerField(null=False, blank=True)  # 价格

    alter_time = models.DateTimeField(auto_now_add=True)  # 修改时间

    check_all_price = models.IntegerField(null=False, blank=True)  # 全选后的优惠价格

    def __unicode__(self):
        return self.part


# 订单表
class Order(models.Model):
    order = models.CharField(primary_key=True, max_length=30, null=False, blank=False)  # 订单编号

    project = models.ForeignKey(Project)  # 对应项目

    is_pay = models.BooleanField(default=False)  # 是否支付

    classify = models.ForeignKey(Classify)  # 所属分类

    user = models.ForeignKey(User)  # 所属用户 外键

    order_price = models.IntegerField(null=False, blank=True)  # 价格

    is_complete = models.BooleanField(default=False)  # 完成状态 0未完成 1已完成

    start_date = models.DateTimeField(auto_now_add=True, null=True)  # 下订单时间

    expire_date = models.DateTimeField(auto_now_add=False, null=True)  # 过期时间

    trade_status = models.CharField(max_length=50, default='INIT', null=True)  # 支付模块框架所用

    order_type = models.CharField(max_length=5, null=False, blank=True)  # 订单类型

    def __unicode__(self):
        return self.order_id


# 处理员信息表
class Worker(models.Model):
    worker = models.OneToOneField(User, primary_key=True)  # 处理员编号

    worker_name = models.CharField(max_length=10, null=True, blank=True)  # 处理员名字

    worker_position = models.CharField(max_length=5, null=False, blank=False)  # 处理员职位

    project_number = models.IntegerField(null=False, blank=True)  # 正在处理的项目数

    worker_performance = models.IntegerField(null=False, blank=True)  # 绩效（所做项目的总价格）


# 工单表
class WorkOrder(models.Model):
    project = models.ForeignKey(Project)  # 对应项目号

    order = models.OneToOneField(Order, primary_key=True)  # 对应订单号

    assessor = models.ForeignKey(Worker)  # 对应审核员编号

    processor = models.ForeignKey(User)  # 对应数据员编号

    status = models.CharField(max_length=5, null=False, blank=False)
    # 工单状态0未分配 1已分配 2 未审核 3 不合格 4 已完成

    plan_complete_time = models.DateTimeField(auto_now_add=False, null=True)  # 计划完成时间

    finish_time = models.DateTimeField(auto_now_add=False, null=True)  # 实际完成时间

    is_satisfy = models.BooleanField(default=True)  # 用户满意与否

    remark = models.TextField(max_length=100, null=True, blank=True)  # 审核员对项目注释

    evaluate = models.TextField(max_length=100, null=True, blank=True)  # 用户评价


# 项目选择部位表
class ProjectPart(models.Model):
    project = models.ForeignKey(Project)  # 对应项目号

    part = models.ForeignKey(Price)  # 对应部位编号

    directory = models.CharField(max_length=100, null=True, blank=True)  # 目录

    primary = ('project', 'part')


# 发票表
class Invoice(models.Model):
    order = models.OneToOneField(Order, primary_key=True)  # 对应订单号

    amount = models.IntegerField(null=False, blank=True)  # 发票金额

    demand_time = models.DateTimeField(auto_now_add=True, null=True)  # 发票索取时间

    deliver_time = models.DateTimeField(auto_now_add=False, null=True)  # 发票邮寄时间

    title = models.CharField(max_length=20, null=True, blank=True)  # 发票抬头

    status = models.CharField(max_length=5, null=False, blank=False)  # 开票状态

    remark = models.TextField(max_length=100, null=True, blank=True)  # 备注

    user = models.ForeignKey(User)  # 对应用户

    demand_type = models.CharField(max_length=20, null=True, blank=True)  # 开具类型

    invoice_type = models.CharField(max_length=20, null=True, blank=True)  # 发票类型

    deliver_id = models.CharField(max_length=30, null=True, blank=True)  # 物流编号

    deliver_company = models.CharField(max_length=30, null=True, blank=True)  # 物流公司

    address = models.CharField(max_length=30, null=True, blank=True)  # 邮寄地址

    recipient_name = models.CharField(max_length=10, null=True, blank=True)  # 收件人

    telephone = models.CharField(max_length=15, null=True, blank=True)  # 联系电话


# 用户通知中心信息表
class Message(models.Model):
    message = models.AutoField(primary_key=True, null=False)

    user = models.ForeignKey(User)  # 对应用户

    title = models.CharField(max_length=20, null=False)  #
    # 标题

    message_content = models.TextField(max_length=100, null=True, blank=True)  # 信息内容

    send_time = models.DateTimeField(auto_now_add=True)  # 发送时间

    read_time = models.DateTimeField(auto_now_add=False, null=True)  # 阅读时间

    send_worker = models.ForeignKey(Worker)  # 发送信息的工作人员

    is_read = models.BooleanField(default=False)  # 是否阅读


# 优惠券表
class Coupon(models.Model):
    coupon = models.CharField(primary_key=True, max_length=30, null=False, blank=False)  # 优惠券编号

    user = models.ForeignKey(User)  # 所属用户

    deliver_time = models.DateTimeField(auto_now_add=True)  # 发放时间

    deadline_time = models.DateTimeField(auto_now_add=False)  # 过期时间

    amount = models.IntegerField(null=False)  # 抵用金额

    rest_amount = models.IntegerField(null=False)  # 余额

    type = models.ForeignKey(Classify)  # 使用范围

    remark = models.CharField(max_length=30, null=True, blank=True)  # 优惠券备注


class PartRelation(models.Model):
    part_father = models.ForeignKey(Price)

    part_son = models.CharField(max_length=2, null=False, blank=False)
