# ldap
Retrieve LDAP passwords, using Django

需要在LINUX中执行如下命令 pip install ldap,pip install django==1.8
安装好以后将代码copy到/opt目录下面
执行python manage.py syncdb
设置登录账号密码

修改manage_ops/ldapmanage.py 文件 
以下内容需要修改成自己服务器的配置
LDAP_HOST = 'openldap.intra.wexin.com'
USER = 'cn=admin,dc=wexin,dc=com'
PASSWORD = 'wexin.com'
BASE_DN = 'ou=People,dc=wexin,dc=com'


修改manage_ops/mail.py 文件
以下内容需要修改成自己服务器的配置
 mail_from = 'ops@wexin.com'
 smtpserver = 'smtp.exmail.qq.com'
 user = 'ops@wexin.com'
 pwd = 'wexin.com'
 
 修改完成以后执行启动 python manage.py runserver 0.0.0.0:80
  



