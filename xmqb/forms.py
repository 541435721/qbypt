# coding=utf-8

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms
from django.contrib import auth
import models
import re
from django.utils.safestring import mark_safe


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-lg'}),
                               max_length=30, required=True, label=u'用户名', error_messages={'required': u'用户名不能为空'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-lg'}),
                               label=u'密码', error_messages={'required': u'密码不能为空'},
                               required=True)

    # 上面主要是对样式的覆盖，不用其实也行，只不过很多想要的效果会消失，比如自定义的错误提示等

    class Meta:  # 和数据模型关联类ModelForm必要的子类
        model = User
        fields = ['username', 'password']
        exclude = ['last_login', 'date_joined', 'email', 'confirm_password']  # 剔除不要的表项

    def __init__(self, *args, **kwargs):  # 初始化的方法
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):  # 提示账号密码错误的方法，并且清除内容
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = auth.authenticate(username=username, password=password)
            if self.user_cache is None:
                self._errors['username'] = self.error_class([u'账号密码不匹配'])
        return self.cleaned_data


class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-lg'}),  # 表单用户名
                               max_length=30, required=True, label=u'用户名', error_messages={'required': u'用户名不能为空'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-lg'}),  # 表单密码
                               label=u'密码', error_messages={'required': u'密码不能为空'},
                               required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-lg'}),  # 表单确认密码选项
                                       label=u'确认密码', error_messages={'required': u'密码不能为空'},
                                       required=True)
    cellphone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-lg'}),  # 表单电话选项
                                required=True,
                                label=u'手机', error_messages={'required': u'手机号码不能为空'},
                                max_length=15)
    identifying_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-lg'}),  # 表单手机验证码
                                       required=True,
                                       label=u'手机验证码', error_messages={'required': u'请输入手机验证码'},
                                       max_length=6)

    class Meta:  # 和数据模型关联类ModelForm必要的子类
        model = User
        fields = ['username', 'password', 'confirm_password', 'cellphone', 'identifying_code']
        exclude = ['last_login', 'date_joined']  # 剔除不要的表项

    def __init__(self, *args, **kwargs):  # 初始化的方法
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean(self):  # 自带的数据清理处理方法
        super(RegisterForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class([u'两次密码不匹配'])
        return self.cleaned_data


class UserInform(forms.ModelForm):
    identify_choice = ((u'医生', u'医生'), (u'病人', u'病人'))
    position_choice = ((u'医师', u'医师'), (u'主任', u'主任'), (u'其他', u'其他'))
    department_choice = (
        (u'呼吸内科', u'呼吸内科'), (u'内分泌科', u'内分泌科'), (u'神经内科', u'神经内科'), (u'肾内科', u'肾内科'), (u'肝病研究所', u'肝病研究所'),
        (u'中医科', u'中医科'), (u'骨肿瘤科', u'骨肿瘤科'), (u'其他', u'其他'))

    user_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                max_length=20, required=True, label=u'姓名', error_messages={'required': u'姓名为必填项'})

    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control input-lg'}),
                            required=True,
                            label=u'电子邮件', error_messages={'required': u'邮箱不能为空'},
                            max_length=75)
    user_telephone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': "readonly"}),
                                     label=u'联系电话', required=False)
    user_identify = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control m-b parsley-validated'}),
                                      label=u'身份', required=False, choices=identify_choice)
    hospital = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                               max_length=20, required=False, label=u'医院')
    department = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control m-b parsley-validated'}),
                                   label=u'部门', required=False, choices=department_choice)

    position = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control m-b parsley-validated'}),
                                 label=u'职位', required=False, choices=position_choice)
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                              max_length=20, required=False, label=u'地址', error_messages={'required': u'地址为必填项'})

    pic_dir = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                              max_length=20, required=False, label=u'图片地址')

    abstract = forms.CharField(widget=forms.Textarea(
        attrs={'class': "form-control", 'rows': "6", 'data-minwords': "6", 'data-required': "true"}), required=False,label=u'备注')

    class Meta:  # 和数据模型关联类ModelForm必要的子类
        model = models.UserInfo
        fields = ['user_name', 'user_email', 'user_identify', 'hospital', 'department', 'position',
                  'address', 'pic_dir', 'abstract']
        exclude = ['user_telephone']


class ProjectForm(forms.Form):
    classify_choice = []
    for obj in models.Classify.objects.all():
        classify_choice.append((obj.classify, obj.classify_name))

    part_choice = []
    for obj in models.Price.objects.all().order_by('part'):
        part_choice.append((obj.part, obj.part_name))

    age_choice=[]
    for i in range(120):
        age_choice.append((i,i))

    sex_choice = ((u'男', u'男'), (u'女', u'女'))

    project_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),  # 表单项目名
                                   max_length=50, required=True, label=u'项目名称',
                                   error_messages={'required': u'项目名称不能为空'})
    classify = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control m-b parsley-validated', 'onchange': 'javascript:change_checkbox()'}),
        label=u'类型', required=True, choices=tuple(classify_choice))  # 表单项目类型选择 下拉框

    # upload_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
    #                               max_length=1000, required=False, label=u'文件名', )

    part = forms.MultipleChoiceField(label=u'选择部位', widget=forms.CheckboxSelectMultiple(
        attrs={'onchange': 'javascript:get_relation_checkbox(this.value)'}), choices=part_choice,
                                     error_messages={'required': u'请选择部位'})  # 表单项目建模部位 多选框

    patient_name = forms.CharField(max_length=10,label=u'病人姓名', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                   error_messages={'required': u'病人姓名不能为空'})  # 表单病人名字

    patient_sex = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                    label=u'病人性别', required=True, choices=sex_choice)  # 表单病人性别

    patient_age = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                     required=True, label=u'病人年龄',choices=age_choice,
                                  error_messages={'required': u'年龄不能为空','invalid':u'请输入数字'})  # 表单病人年龄

    patient_hospital = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     required=True, label=u'病人所在医院',max_length=20,
                                  error_messages={'required': u'请填写病人所在医院','invalid':u'请输入数字'})

    patient_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),  # 表单病人地址
                                      max_length=20, required=False, label=u'病人地区')

    remark = forms.CharField(widget=forms.Textarea(
        attrs={'class': "form-control", 'rows': "6", 'data-minwords': "6", 'data-required': "false"}),
        required=False, label=u'备注')  # 表单备注
    def clean(self):  # 自带的数据清理处理方法
        super(ProjectForm, self).clean()
            # self._errors['password'] = self.error_class([u'两次密码不匹配'])
        return self.cleaned_data


class ChangePasswordForm(forms.ModelForm):  # 修改密码表单

    identifying_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-lg'}),  # 表单手机验证码
                                       required=True,
                                       label=u'验证码', error_messages={'required': u'请输入手机验证码'},
                                       max_length=6)

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-lg'}),  # 表单密码
                               label=u'密码', error_messages={'required': u'密码不能为空'},
                               required=True)

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-lg'}),  # 表单确认密码选项
                                       label=u'确认密码', error_messages={'required': u'密码不能为空'},
                                       required=True)

    class Meta:  # 和数据模型关联类ModelForm必要的子类
        model = User
        fields = ['password']
        exclude = ['username', 'last_login', 'date_joined', 'email', 'confirm_password']  # 剔除不要的表项

    def clean(self):  # 自带的数据清理处理方法
        super(ChangePasswordForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class([u'两次密码不匹配'])
        return self.cleaned_data


class InvoiceDemandForm(forms.ModelForm):
    demand_choice = ((u'企业', u'企业'), (u'个人', u'个人'))  # 发票开具类型选项

    invoice_choice = ((u'增值税发票', u'增值税发票'), (u'普通发票', u'普通发票'))  # 发票类型选项

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),  # 发票抬头
                            max_length=10, required=True, label=u'发票抬头',
                            error_messages={'required': u'发票抬头不能为空'})

    demand_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control m-b parsley-validated'}),
                                    label=u'开具类型', required=True, choices=demand_choice)  # 发票开具类型下拉框

    invoice_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control m-b parsley-validated'}),
                                     label=u'发票类型', required=True, choices=invoice_choice)  # 发票类型

    recipient_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),  # 收件人姓名
                                     max_length=10, required=True, label=u'收件人',
                                     error_messages={'required': u'请填写发票收件人姓名'})

    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),  # 收件人地址
                              max_length=30, required=True, label=u'地址',
                              error_messages={'required': u'请填写接收发票的地址'})

    telephone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),  # 收件人电话
                                max_length=15, required=True, label=u'收件人电话',
                                error_messages={'required': u'请填写收件人电话'})

    deliver_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),  # 物流编号

                                 max_length=30, required=False, label=u'物流编号',
                                 error_messages={'required': u'请填写物流编号'})

    deliver_company = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),  # 物流公司
                                      max_length=30, required=False, label=u'物流公司',

                                      error_messages={'required': u'请填写物流公司'})

    remark = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                             max_length=100, required=False, label=u'备注', )

    class Meta:  # 和数据模型关联类ModelForm必要的子类
        model = models.Invoice
        fields = ['title', 'demand_type', 'invoice_type', 'recipient_name', 'address', 'telephone', 'deliver_id',
                  'deliver_company', 'remark']
        exclude = ['order', 'amount', 'demand_time', 'deliver_time', 'status', 'user', ]  # 剔除不要的表项

    def __init__(self, *args, **kwargs):  # 初始化的方法
        super(InvoiceDemandForm, self).__init__(*args, **kwargs)


class ChangePasswordForm(forms.ModelForm):  # 修改密码表单

    identifying_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-lg'}),  # 表单手机验证码
                                       required=True,
                                       label=u'验证码', error_messages={'required': u'请输入手机验证码'},
                                       max_length=6)

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-lg'}),  # 表单密码
                               label=u'密码', error_messages={'required': u'密码不能为空'},
                               required=True)

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-lg'}),  # 表单确认密码选项
                                       label=u'确认密码', error_messages={'required': u'密码不能为空'},
                                       required=True)

    class Meta:  # 和数据模型关联类ModelForm必要的子类
        model = User
        fields = ['password']
        exclude = ['username', 'last_login', 'date_joined', 'email', 'confirm_password']  # 剔除不要的表项

    def clean(self):  # 自带的数据清理处理方法
        super(ChangePasswordForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class([u'两次密码不匹配'])
        return self.cleaned_data


class AdministratorChangePasswordForm(forms.ModelForm):  # 修改密码表单
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-lg'}),  # 表单密码
                               label=u'密码', error_messages={'required': u'密码不能为空'},
                               required=True)

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-lg'}),  # 表单确认密码选项
                                       label=u'确认密码', error_messages={'required': u'密码不能为空'},
                                       required=True)

    class Meta:  # 和数据模型关联类ModelForm必要的子类
        model = User
        fields = ['password']
        exclude = ['username', 'last_login', 'date_joined', 'email', 'confirm_password']  # 剔除不要的表项

    def clean(self):  # 自带的数据清理处理方法
        super(AdministratorChangePasswordForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class([u'两次密码不匹配'])
        return self.cleaned_data


class HandleInvoiceForm(forms.ModelForm):
    deliver_company = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                      max_length=10, required=True, label=u'物流公司',
                                      error_messages={'required': u'物流公司不能为空'})

    deliver_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                 max_length=10, required=True, label=u'物流编号', error_messages={'required': u'物流编号不能为空'})

    def __init__(self, *args, **kwargs):  # 初始化的方法
        super(HandleInvoiceForm, self).__init__(*args, **kwargs)


class CouponForm(forms.Form):
    classify_choice = []
    for obj in models.Classify.objects.all():
        classify_choice.append((obj.classify, obj.classify_name))

    deadline_time = forms.DateTimeField(widget=forms.TextInput(attrs={'onClick': 'laydate()', 'class': 'form-control'}),
                                        required=True, label=u'过期时间',
                                        error_messages={'required': u'过期时间不能为空'})

    amount = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=5, required=True,
                             label=u'金额', error_messages={'required': u'金额不能为空'})

    type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control m-b parsley-validated'}), label=u'适用范围',
                             required=True, choices=classify_choice)

    remark = forms.CharField(widget=forms.Textarea(
        attrs={'class': "form-control", 'rows': "6", 'data-minwords': "6", 'data-required': "true"}), label=u'备注')

    def __init__(self, *args, **kwargs):  # 初始化的方法
        super(CouponForm, self).__init__(*args, **kwargs)


class PriceForm(forms.Form):
    classify_choice = []
    for obj in models.Classify.objects.all():
        classify_choice.append((obj.classify, obj.classify_name))

    classify = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control m-b parsley-validated'}),
                                 label=u'分类',
                                 required=True, choices=classify_choice)

    part_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=5, required=True,
                                label=u'建模部位', error_messages={'required': u'部位名不能为空'})  # 部位名称

    price = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=5, required=True,
                            label=u'价格', error_messages={'required': u'价格不能为空'})

    def __init__(self, *args, **kwargs):  # 初始化的方法
        super(PriceForm, self).__init__(*args, **kwargs)


class MessageForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=5, required=True,
                            label=u'建模部位',
                            error_messages={'required': u'部位名不能为空'})  # 部位名称

    message_content = forms.CharField(widget=forms.Textarea(
        attrs={'class': "form-control", 'rows': "6", 'data-minwords': "6", 'data-required': "true"}), label=u'备注')


class ChangePriceForm(forms.Form):
    order_id = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label=u'订单编号')
    old_price = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label=u'订单金额')
    set_price = forms.CharField(widget=forms.TextInput(), label=u'修改金额')

    def __init__(self, *args, **kwargs):  # 初始化的方法
        super(ChangePriceForm, self).__init__(*args, **kwargs)


class Send_Message(forms.Form):
    receiver = forms.CharField(
        widget=forms.TextInput(attrs={'class': "input__field input__field--hoshi", 'id': "receiver"}), label='收件人')
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': "input__field input__field--hoshi", 'id': "title"}), label='主题')
    context = forms.CharField(widget=forms.Textarea(attrs={'id': 'editor', 'style': 'font-size:36px;'}), label='正文')

    def __init__(self, *args, **kwargs):  # 初始化的方法
        super(Send_Message, self).__init__(*args, **kwargs)


class Read_Message(forms.Form):
    receiver = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': "input__field input__field--hoshi", 'id': "receiver", 'readonly': 'readonly'}), label='收件人')
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': "input__field input__field--hoshi", 'id': "title", 'readonly': 'readonly'}), label='主题')
    context = forms.CharField(
        widget=forms.Textarea(attrs={'id': 'editor', 'readonly': 'readonly', 'style': 'font-size:36px;'}), label='正文')

    def __init__(self, *args, **kwargs):  # 初始化的方法
        super(Read_Message, self).__init__(*args, **kwargs)


class Add_Price(forms.Form):  # 增加服务表单
    classify_choice = []
    for obj in models.Classify.objects.all():
        classify_choice.append((obj.classify, obj.classify_name))

    classify = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control m-b parsley-validated', 'onchange': 'javascript:change_checkbox()'}),
        label=u'类型', required=True, choices=tuple(classify_choice))  # 表单项目类型选择 下拉框

    price_name = forms.CharField(widget=forms.TextInput(), label='服务名称')
    price = forms.IntegerField(widget=forms.TextInput(), label='服务价格')
    discount_price = forms.IntegerField(widget=forms.TextInput(), label='折扣价格')

    def __init__(self, *args, **kwargs):  # 初始化的方法
        super(Add_Price, self).__init__(*args, **kwargs)


class Order_Detial(forms.Form):
    """"""
    order_id = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='订单号')
    user_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='用户名')
    create_time = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='创建时间')
    order_price = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='订单金额')

    def __init__(self, *args, **kwargs):
        """Constructor for Order_Detial"""
        super(Order_Detial, self).__init__(*args, **kwargs)


class Suggestion(forms.Form):
    context = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'style': 'font-size:18px;width: 500px; height: 300px;'
                         'borderColor:true;'
                         'BORDER-BOTTOM: 2px solid; '
                         'BORDER-LEFT: 2px solid; '
                         'BORDER-RIGHT: 2px solid; '
                         'BORDER-TOP: 2px solid;'
                         'border-color:#65bd77',
                'placeholder': '请输入您对我们的意见或建议',
                'resize': 'none'}),
        label='意见反馈')

    def __init__(self, *args, **kwargs):
        """Constructor for Order_Detial"""
        super(Suggestion, self).__init__(*args, **kwargs)


class ChangePhoneForm(forms.Form):
    identifying_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-lg'}),  # 表单手机验证码
                                       required=True,
                                       label=u'验证码', error_messages={'required': u'请输入手机验证码'},
                                       max_length=6)

    new_phone = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-lg'}),  # 表单密码
                               label=u'新号码', error_messages={'required': u'请输入新号码'},
                               required=True)

    def clean(self):  # 自带的数据清理处理方法
        super(ChangePhoneForm, self).clean()
