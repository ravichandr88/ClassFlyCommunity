# -*- coding: utf-8 -*-
__copyright__ = "Copyright (c) 2014-2017 Agora.io, Inc."

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.RtmTokenBuilder2 import *


def main():
    app_id = "e73019d92f714c95b9bc47ea63de404c"
    app_certificate = "ed36762fba3f4e42acaf99c6265ec4c3"
    user_id = "2112112121"
    expiration_in_seconds = 3600

    token = RtmTokenBuilder.build_token(app_id, app_certificate, user_id, expiration_in_seconds)
    print("Rtm Token: {}".format(token))


if __name__ == "__main__":
    main()
