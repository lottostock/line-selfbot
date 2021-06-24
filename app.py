# -*- coding: utf-8-*-
from Imgood.linepy import *
from Imgood.linepy import (LINE, Channel, OEPoll, OpType)
from Imgood.akad import *
from Imgood.linepy.style import *
from Imgood.linepy.login import *
from justgood import imjustgood
from time import sleep
from gtts import gTTS
from datetime import datetime
from bs4 import BeautifulSoup
from threading import Thread, active_count
import os,traceback,sys,json,time,ast,requests,re,random,pytz
from Liff.ttypes import LiffChatContext, LiffContext, LiffSquareChatContext, LiffNoneContext, LiffViewRequest 


login = json.loads(open('Data/token.json','r').read())
setting = json.loads(open('Data/settings.json','r').read())
cctv = json.loads(open('Data/cctv.json','r').read())
loger = Login()

if login["email"] == "":
   if login["token"] == "":
      data = loger.logqr(cert=None) #You can put your Crt token here
      client = LINE(idOrAuthToken=data)
      login["token"] = data
      with open('Data/token.json', 'w') as fp:
        json.dump(login, fp, sort_keys=True, indent=4)
   else:
   	  try:client = LINE(idOrAuthToken=login["token"])
   	  except:print("TOKEN EXPIRED");sys.exit()
else:
  client = LINE(login["email"],login["password"])


ops = OEPoll(client)
whitelist = [client.profile.mid, client, ]

while True:
    try:
        Operation = ops.singleTrace(count=50)
        if Operation is not None:
            for op in Operation:
                ops.setRevision(op.revision)
                # self.OpInterrupt[op.type], args=(op,)
                thread1 = threading.Thread(target=LINE_OP_TYPE, args=(op,))
                thread1.start()
                thread1.join()
    except Exception as error:
        print(error)


def LINE_OP_TYPE(op):
    if op.type == 25:  # sent message
        message = op.message
        content = message.text
        msg_to = message.to
        msg_from = message._from

        # message only contains text
        if message.contentType == 0:
            if "@everyone" in content and msg_from in whitelist:
                group = client.getGroup(msg_to)
                members = [contact for contact in group.members]
                try:
                    for bubble in range((len(members) // 20) + 1):
                        placement = 0
                        mentionees = []
                        for mems in group.members[bubble * 20: (bubble + 1) * 20]:
                            mentionees.append({
                                "S": str(placement),
                                "E": str(placement + 6),
                                "M": mems.id
                            })
                        client.sendMessage(msg_to, '', contentMetadata={
                                           u'MENTION': json.dumps({'MENTIONEES': mentionees})
                                           }, contentType=0)
                except Exception as e:
                    client.sendMessage(msg_to, str(e))
