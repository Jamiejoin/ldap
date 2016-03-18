#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import ldap
import ldap.modlist as modlist
import argparse
import subprocess as sp
import logging
import datetime
import sys
#from mail import sendmail
from time import  time


LDAP_HOST = 'openldap.intra.wexin.com'
USER = 'cn=admin,dc=wexin,dc=com'
PASSWORD = 'wexin.com'
BASE_DN = 'ou=People,dc=wexin,dc=com'

def logwrite(content):
    logpath='/opt/root/oplogs/ldap/'

    if not os.path.isdir(logpath):
        os.makedirs(logpath)

    t=datetime.datetime.now()
    daytime=t.strftime('%Y-%m-%d')
    daylogfile=logpath+'/' + str(daytime)+'.log'
    logging.basicConfig(filename=daylogfile, level=logging.DEBUG)
    logging.info('*'*130)
    logging.debug(str(t) + '{0}\n'.format(content))

def exec_cmd(cmd):
    res =sp.Popen(cmd ,shell = True,close_fds = True,stdout = sp.PIPE,stderr = sp.PIPE)
    out, err = res.communicate()
    ret = res.returncode
    if ret:
        print "[%s] FAILED return code is %s" % (cmd, ret)
        if err:
            print err
        else:
            print out
        sys.exit(22)
    else:
        print "[%s] success  return code is %s" % (cmd, ret)
        return out

def randompwd(length=16):
    pwd = exec_cmd('mkpasswd -l %s' % length)
    return pwd.strip()


class LDAPTool:

    def __init__(self, ldap_host=None, base_dn=None, user=None, password=None):
        if not ldap_host:
            ldap_host = LDAP_HOST
        if not base_dn:
            self.base_dn = BASE_DN
        if not user:
            user = USER
        if not password:
            password = PASSWORD
        try:
            self.ldapconn = ldap.open(ldap_host)
            self.ldapconn.simple_bind(user, password)
        except ldap.LDAPError, e:
            print e

# 根据表单提交的用户名，检索该用户的dn,一条dn就相当于数据库里的一条记录。
# 在ldap里类似cn=username,ou=users,dc=wexin,dc=com,验证用户密码，必须先检索出该DN
    def ldap_search_dn(self, uid=None):
        obj = self.ldapconn
        obj.protocal_version = ldap.VERSION3
        searchScope = ldap.SCOPE_SUBTREE
        retrieveAttributes = None
        searchFilter = "cn=" + uid

        try:
            ldap_result_id = obj.search(self.base_dn, searchScope,
                                        searchFilter, retrieveAttributes)
            result_type, result_data = obj.result(ldap_result_id, 0)
            if result_type == ldap.RES_SEARCH_ENTRY:
                # dn = result[0][0]
                return result_data[0][0]
            else:
                return None
        except ldap.LDAPError, e:
            print e

    def ldap_search_uidnumber(self):
        obj = self.ldapconn
        obj.protocal_version = ldap.VERSION3
        searchScope = ldap.SCOPE_SUBTREE
        searchFilter = '(objectclass=*)'
        attrs = ['uidNumber']

        try:
            res = obj.search_s(self.base_dn, searchScope,
                                        searchFilter, attrs)
            uidnumbers = [ x[1] for x in res ]
            uids = []
            for i in uidnumbers:
                if i.get('uidNumber'):
                    uids.append(int(i['uidNumber'][0]))
            return max(uids)
        except ldap.LDAPError, e:
            print e

    def ldap_add_user(self, uid=None):
        obj = self.ldapconn
        '''
        dn: uid=maxinhua,ou=People,dc=wexin,dc=com
        objectClass: inetOrgPerson
        objectClass: posixAccount
        objectClass: shadowAccount
        cn: maxinhua
        sn: Linux
        userPassword: wexin.com
        loginShell: /bin/bash
        uidNumber: 10007
        gidNumber: 10002
        homeDirectory: /home/maxinhua
        mail: xiaoq@wexin.com
        '''
        obj.protocol_version = ldap.VERSION3
        uidnumber = self.ldap_search_uidnumber() + 1
        gidnumber = '10002'

        cn = uid
        addDN = "uid=%s,ou=People,dc=wexin,dc=com" % cn
        attrs = {}
        attrs['objectclass'] = ['inetOrgPerson', 'posixAccount', 'shadowAccount']
        attrs['cn'] = cn
        attrs['homeDirectory'] = '/home/%s' % uid
        attrs['loginShell'] = '/bin/bash'
        attrs['sn'] = uid
        attrs['uid'] = uid
        attrs['uidNumber'] = str(uidnumber)
        attrs['gidNumber'] = gidnumber
        attrs['userPassword'] = str(randompwd())
        attrs['mail'] = '%s@wexin.com' % uid
        print attrs
        try:
            ldif = modlist.addModlist(attrs)
            obj.add_s(addDN, ldif)
            print uid + ': ' + attrs['userPassword']
            return {uid: attrs['userPassword']}
        except ldap.LDAPError, e:
            print e


# 查询用户记录，返回需要的信息
    def ldap_get_user(self, uid=None):
        obj = self.ldapconn
        obj.protocal_version = ldap.VERSION3
        searchScope = ldap.SCOPE_SUBTREE
        retrieveAttributes = None
        searchFilter = "cn=" + uid
        try:
            ldap_result_id = obj.search(self.base_dn, searchScope,
                                        searchFilter, retrieveAttributes)
            result_type, result_data = obj.result(ldap_result_id, 0)
            if result_type == ldap.RES_SEARCH_ENTRY:
                username = result_data[0][1]['cn'][0]
                email = result_data[0][1]['mail'][0]
                nick = result_data[0][1]['sn'][0]
                result = {'username': username, 'email': email, 'nick': nick}
                return result
            else:
                return None
        except ldap.LDAPError, e:
            print e

# 用户验证，根据传递来的用户名和密码，搜索LDAP，返回boolean值
    def ldap_get_vaild(self, uid=None, passwd=None):
        obj = self.ldapconn
        target_cn = self.ldap_search_dn(uid)
        try:
            if obj.simple_bind_s(target_cn, passwd):
                return True
            else:
                return False
        except ldap.LDAPError, e:
            print e

# 修改用户密码
    def ldap_update_pass(self, uid=None, oldpass=None, newpass=None):
        # modify_entry = [(ldap.MOD_REPLACE, 'userpassword', newpass)]
        obj = self.ldapconn
        target_cn = self.ldap_search_dn(uid)
        try:
            obj.simple_bind_s(target_cn, oldpass)
            obj.passwd_s(target_cn, oldpass, newpass)
            return True
        except ldap.LDAPError, e:
            print e

#重置用户密码
    def ldap_reset_pass(self,uid=None,newpass=None):
        obj = self.ldapconn
        target_cn = self.ldap_search_dn(uid)
        add_pass = [(ldap.MOD_REPLACE, 'userPassword', str(newpass))]
        try:
            obj.modify_s(target_cn,add_pass)
            return True
        except ldap.LDAPError, e:
            return False
        obj.unbind_s()

def main():
    parser = argparse.ArgumentParser(description = 'ldap账号管理')
    parser.add_argument('-u', action = "store", dest = "u", help = "增加的用户名")
    parser.add_argument('-m', action = "store_true", default=False, help = "增加用户名并发送邮件")

    ldp = LDAPTool()
    results = parser.parse_args()
    if results.u and results.m:
        try:
            r = ldp.ldap_add_user(results.u)
            user = results.u + '@wexin.com'
            content = "用户名%s 密码%s" % (results.u, r[results.u])
        except Exception, e:
            print e
    elif results.u:
        ldp.ldap_add_user(results.u)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
