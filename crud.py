from logging import error
from re import X
import pymongo
import dotenv
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_CONNECT = os.getenv("MONGODB_CONNECT")
# LOCALDB = os.getenv("LOCALDB")

mongoclient = pymongo.MongoClient(MONGODB_CONNECT)

lmam = mongoclient["leave_me_a_message"]



def message_insert(colle,data):
    lmam[colle].insert_one(data)

def user_insert(colle,data):
    lmam[colle].insert_one(data)


def find_uname(colle,data):
    return lmam[colle].count_documents(data)


def update_chat_id(colle,data):
    return
data = {'IP': '192.168.1.101', 'Name': 'charan', 'Msg': 'Hello there!'}
