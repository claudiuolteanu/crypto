import sys
import json
import re
import os
from Crypto.Cipher import AES

mail_pattern = re.compile("^[a-zA-Z_0-9\.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$")
BLOCK_SIZE = 32

def from_cookie_to_json(cookie):
    key_value_pairs = cookie.split('&')
    key_value_dict = dict(s.split('=') for s in key_value_pairs)

    return json.dumps(key_value_dict, indent=4, separators=(',', ': '))

def json_to_url_encode(user_profile):
    key_value_dict = json.loads(user_profile)
    result = ""

    for key, value in key_value_dict.iteritems():
        result += key + "=" + str(value) + "&"

    return result[:len(result) - 1]

def profile_for(mail, role='user'):
    return json.dumps({'email': mail, 'uid': 10, 'role': role},
                      sort_keys=True,
                      indent=4,
                      separators=(',', ': '))

def add_admin_role(cookie):
    cookie_to_json = json.loads(from_cookie_to_json(cookie))
    cookie_to_json['role'] = 'admin'

    return json_to_url_encode(json.dumps(cookie_to_json))

if __name__ == "__main__":
    #input_from_user = raw_input('Insert the routine to parse\n')

    #print from_cookie_to_json(input_from_user)

    mail = raw_input('Insert the e-mail address\n')
    if mail_pattern.match(mail) is None:
        print "The e-mail %s is not a valid one " % mail
        sys.exit()

    user_profile = profile_for(mail)
    user_profile_url_encoded = json_to_url_encode(user_profile)

    # generate a random secret key
    secret_key = os.urandom(BLOCK_SIZE)

    # create a cipher obj
    cipher_obj = AES.new(secret_key)

    # add padding to message
    user_profile_url_encoded += (' ' * (16 - len(user_profile_url_encoded) % 16))
    print "Encoded message + padding : %s" % user_profile_url_encoded 

    # encrypt the message
    encrypted_msg = cipher_obj.encrypt(user_profile_url_encoded)
    print "Encrypted message %s" % encrypted_msg

    ### Simulate the attack ###
    # decrypt the message
    decrypted_msg = cipher_obj.decrypt(encrypted_msg)
    print "Decripted message %s " % decrypted_msg
    print "Hacked message    %s " % add_admin_role(json_to_url_encode(profile_for(mail)))
