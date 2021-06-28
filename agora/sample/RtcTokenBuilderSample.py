# -*- coding: utf-8 -*-
__copyright__ = "Copyright (c) 2014-2017 Agora.io, Inc."


import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.RtcTokenBuilder import *


def main():
    appID = "e73019d92f714c95b9bc47ea63de404c"
    appCertificate = "ed36762fba3f4e42acaf99c6265ec4c3"
    channelName = "car"
    uid = 2882341279
    userAccount = "2882341279"
    expireTimeInSeconds = 3600
    currentTimestamp = int(time.time())
    privilegeExpiredTs = currentTimestamp + expireTimeInSeconds

    token = RtcTokenBuilder.buildTokenWithUid(appID, appCertificate, channelName, uid, Role_Attendee, privilegeExpiredTs)
    print("Token with int uid: {}".format(token))
    
    token = RtcTokenBuilder.buildTokenWithAccount(appID, appCertificate, channelName, userAccount, Role_Attendee, privilegeExpiredTs)
    print("Token with user account: {}".format(token))

    token = RtcTokenBuilder.buildTokenWithUidAndPrivilege(appID, appCertificate, channelName, uid, 
                                              privilegeExpiredTs, privilegeExpiredTs,
                                              privilegeExpiredTs, privilegeExpiredTs)
    print("Token with int uid user defined privilege: {}".format(token))

    token = RtcTokenBuilder.buildTokenWithUserAccountAndPrivilege(appID, appCertificate, channelName, userAccount,
                                                  privilegeExpiredTs, privilegeExpiredTs,
                                                  privilegeExpiredTs, privilegeExpiredTs)
    print("Token with user account user defined privilege: {}".format(token))

if __name__ == "__main__":
    main()



# 006e73019d92f714c95b9bc47ea63de404cIACChtXnAWoWYpcZbJ2aVsHLd0O0f0g2ne4Re0JNJqvUsp3mPXcAAAAAEAAY899J+TfXYAEAAQD5N9dg
# 006e73019d92f714c95b9bc47ea63de404cIACJ9IADKyTxRAWR7F5I5RkO2CEb3ztJAyIWfC1V7ursfeWuHSYAAAAAEABdBK8DZDTXYAEA6AP08NVg


