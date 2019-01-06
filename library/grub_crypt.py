#!/usr/bin/env python

import random
import string
import crypt


def genPass(size=16, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def genSalt(salt):
    '''
    Generate a random salt.
    '''
    ret = ''
    if not salt:
        with open('/dev/urandom', 'rb') as urandom:
            while True:
                byte = urandom.read(1)
                if byte in (
                        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
                        './0123456789'):
                    ret += byte
                    if len(ret) == 16:
                        break
        return '$6$%s' % ret
    else:
        return '$6$%s' % salt


def main():
    module = AnsibleModule(
        argument_spec=dict(
            salt=dict(required=False, default=None),
            password=dict(
                no_log=True, required=False, default='random', type='str'),
        ))
    salt = module.params['salt']
    password = module.params['password']
    if password == 'random':
        password = genPass()
    sha512Salt = genSalt(salt)
    saltedPass = crypt.crypt(password, sha512Salt)
    module.exit_json(changed=False, passhash=saltedPass)


from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
