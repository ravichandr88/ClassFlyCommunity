# -*- coding: utf-8 -*-
__copyright__ = "Copyright (c) 2014-2017 Agora.io, Inc."

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.RtcTokenBuilder2 import *


def main():
    app_id = "e73019d92f714c95b9bc47ea63de404c"
    app_certificate = "ed36762fba3f4e42acaf99c6265ec4c3"
    channel_name = "car"
    uid = 2882341273
    account = "2882341273"
    expiration_in_seconds = 3600

    token = RtcTokenBuilder.build_token_with_uid(app_id, app_certificate, channel_name, uid, Role_Subscriber,
                                                 expiration_in_seconds)
    print("Token with int uid: {}".format(token))

    token = RtcTokenBuilder.build_token_with_account(app_id, app_certificate, channel_name, account, Role_Subscriber,
                                                     expiration_in_seconds)
    print("Token with user account: {}".format(token))


if __name__ == "__main__":
    main()
