# coding: utf-8


from django.http import HttpResponseRedirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from models import *
from ldapmanage import *
import md5
from mail import mysendmail
import time
from verify_pass import *

reload(sys)
sys.setdefaultencoding('utf8')

#分页
def _paging(result,page):
        paginator = Paginator(result,20)
        try:
                newpage=int(page)
        except ValueError:
                newpage=1
        try:
                contacts = paginator.page(newpage)
        except PageNotAnInteger:
                contacts = paginator.page(1)
        except EmptyPage:
                contacts = paginator.page(paginator.num_pages)
        return contacts

#员工显示列表
def manage_list(request):
    result = manage.objects.all()
    if request.GET.get('page'):
        page=request.GET.get('page')
    else:
        page=1
    rs = _paging(result,page)
    return render_to_response("manage_list.html",{"rs":rs,"request":request})

#运维人员显示列表
def ops_manage_list(request):
    if request.user.is_authenticated():
        result = manage.objects.all()
        if request.GET.get('page'):
            page=request.GET.get('page')
        else:
            page=1
        rs = _paging(result,page)
        return render_to_response("ops_manage_list.html",{"rs":rs,"request":request})
    else:
        return HttpResponseRedirect('/account/login/')

#找回密码
def find_password(request):
    return render_to_response("find_password.html",{"request":request})

#将提交的用户名查询，如果用户名存在，将用户名和当前时间进行MD5 生产16位的KEY 存放在数据库中.并且发送邮件地址到找回密码用户的邮箱中
@csrf_exempt
def find_password_post(request):
    if request.POST.get('username',''):
        username = request.POST.get('username')
        ldp = LDAPTool()
        result = ldp.ldap_search_dn(username)
        if result != None:
            m = md5.new()
            key = username + str(time.mktime(time.localtime()))
            m.update(key)
            keys = m.hexdigest()
            findpasswd.objects.create(key=keys,username=username)
            sub = "微赛找回密码"
            message="如果您并没有找回密码请忽略此封邮件，此邮件地址在1天后将自动失效，如果您需要找回您在微赛的除邮箱密码以外的其他密码\n" \
                    "请点击下面的地址设置你的新密码：http://ldap.intra.wesai.com/verify_key?key=%s&username=%s如果点击此地址依旧无法找回密码\n" \
                    "请联系运维同学朱晓泽/zhuxiaozhe@wesai.com/18611088337 - 李云/liyun@wesai.com/18612615725" %(keys,username)
            address = username + "@wesai.com"


           # sendmail(address,sub,message)
            mysendmail(address,sub,message).start()
            return HttpResponse('ok')
        else:
            return HttpResponse(u'你填入的用户名不存在,只需要填写名字即可，不需要加邮箱后缀')

    else:
        return HttpResponse(u'你为什么不填写邮件地址？为什么？为什么?')

#验证KEY和用户名
@csrf_exempt
def verify_key(request):
    if request.GET.get('key','') and request.GET.get('username',''):
        keys = request.GET.get('key')
        username = request.GET.get('username')
        try:
            db_key = findpasswd.objects.get(key=keys,username=username)
        except:
            return HttpResponse(u'用户名和KEY不匹配')
        if db_key.status == 1:
            return HttpResponse(u'地址已经失效')
        now_time = time.mktime(time.localtime())
        create_time = time.mktime(time.strptime(str(db_key.create_time)[:19], "%Y-%m-%d %H:%M:%S"))
        if ((int(now_time) - int(create_time)) / 60 ) > 1800:
            return HttpResponse(u'地址已经失效')
        else:
            return render_to_response("reset_password.html",{"keys":keys,"username":username})
    else:
        return HttpResponse(u'地址不存在')

#重置密码
@csrf_exempt
def reset_password(request):
    if request.POST.get('username','') and request.POST.get('keys',''):
        username = request.POST.get('username','')
        keys = request.POST.get('keys','')
        try:
            db_key = findpasswd.objects.get(key=keys,username=username)
        except:
            return HttpResponse(u'用户名和KEY不匹配')
        if db_key.status == 1:
            return HttpResponse(u'地址已经失效')
        if request.POST.get('password','') and request.POST.get('password1',''):
            password = request.POST.get('password','')
            password1 = request.POST.get('password1','')
            if password == password1:
                #验证密码复杂度
                if checkPassword(password):
                    ldp = LDAPTool()
                    if ldp.ldap_reset_pass(uid=username,newpass=password):
                        db_key.status = 1
                        db_key.save()
                        return HttpResponse('ok')
                    else:
                        return HttpResponse(u'修改失败,请CALL运维朱晓泽')
                else:
                    return HttpResponse(u'密码必须包含数字,字母,不得小于8位')

            else:
                return HttpResponse(u'两次输入密码不一致')
        else:
            return HttpResponse(u'密码未填写')
    else:
        return HttpResponse(u'非法请求')