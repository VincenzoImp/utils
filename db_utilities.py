import json 
from pymongo import MongoClient
import gridfs
from tqdm import tqdm
import os
import pickle 
import pandas as pd
import numpy as np

# MongoDB URI
uri = 'mongodb://localhost:27017'

def get_channel_ids(db_name='Telegram_test'):
    with MongoClient(uri) as client:
        db = client[db_name]
        ids = [ch['_id'] for ch in db.Channel.find({}, {'_id': 1})]
    return list(set(ids))

def get_id_name_map(ch_ids, db_name='Telegram_test'):
    id_name_map = dict()
    with MongoClient(uri) as client:
        db = client[db_name]
        for ch_id in tqdm(ch_ids):    
            ch = db.Channel.find_one({"_id": int(ch_id)})
            title = str(ch['username'])
            if title is None:
                title = ''
            id_name_map[ch_id] = title
    return id_name_map

# Insert the channel in MongoDB
# Parameters:
#   - new_channel -> new channel to insert
#   - db_name -> specify the name of the collection in MongoDB
def insert_channel(new_channel, db_name='Telegram_test'):

    text_messages = new_channel['text_messages'].copy()
    new_channel.pop('text_messages')
    
    with MongoClient(uri) as client:
        db = client[db_name]
        fs = gridfs.GridFS(db)
        channel = db.Channel
        channel.insert_one(new_channel)
        fs.put(pickle.dumps(text_messages), _id=new_channel['_id'])


# Return the text messages of target channel
# Parameters:
#   - id_channel -> ID of the channel from which return the text messages
#   - db_name -> specify the name of the collection in MongoDB
def get_text_messages_by_id_ch(id_channel, db_name='Telegram_test'):
    with MongoClient(uri) as client:
        db = client[db_name]
        fs = gridfs.GridFS(db)
        stream = fs.get(id_channel).read()
        
        return pickle.loads(stream)


# Return the channel with ID id_channel  
# Parameters:
#   - id_channel -> ID of channel to return
#   - db_name -> specify the name of the collection in MongoDB
def get_channel_by_id(id_channel, db_name='Telegram_test', with_text_msgs=True, with_media_msgs=True):
    ch = {}
    with MongoClient(uri) as client:
        db = client[db_name]
        ch = db.Channel.find_one({"_id": id_channel})
        if with_text_msgs:
            ch['text_messages']= get_text_messages_by_id_ch(id_channel, db_name)
        if not with_media_msgs:
            del ch['generic_media']
        ch['_id'] = int(ch['_id'])

    return ch


# Return the channel with target username  
# Parameters:
#   - username -> username of the channel to return
#   - db_name -> specify the name of the collection in MongoDB
def get_channel_by_username(username, db_name='Telegram_test', with_text_msgs=True, with_media_msgs=True):
    ch = {}
    with MongoClient(uri) as client:
        db = client[db_name]        
        ch = db.Channel.find_one({'username': username})
        if with_text_msgs:
            ch['text_messages']= get_text_messages_by_id_ch(ch['_id'], db_name)
        if not with_media_msgs:
            del ch['generic_media']
        ch['_id'] = int(ch['_id'])
    
    return ch


# Return the channels with ID belonging to the given list of IDs
# Parameters:
#   - ids_channels -> IDs list of channels to return
#   - db_name -> specify the name of the collection in MongoDB
def get_channels_by_ids(ids_channels, db_name='Telegram_test', with_text_msgs=True, with_media_msgs=True):
    chs = []
    with MongoClient(uri) as client:
        db = client[db_name]
        
        for ch in db.Channel.find({ '_id': { '$in': ids_channels }}):
            if with_text_msgs:
                ch['text_messages']= get_text_messages_by_id_ch(ch['_id'], db_name)
            if not with_media_msgs:
                del ch['generic_media']
            ch['_id'] = int(ch['_id'])
            chs.append(ch)
    
    return chs


# Return the channeld ID of all the channels stored in MongoDB
# Parameters:
#   - db_name -> specify the name of the collection in MongoDB
def get_channel_ids(db_name='Telegram_test'):
    ids = []
    with MongoClient(uri) as client:
        db = client[db_name]

        ids = [ch['_id'] for ch in db.Channel.find({}, {'_id':1})]
    
    return ids


# Imports the channels from json format to MongoDB
# Parameters:
#   - db_name -> specify the name of the collection to create in MongoDB
def import_channels_to_mongoDB(db_name, root_directory='public_db'):

    file_list = []
    for directory, _, files in os.walk(root_directory):
        for name in files:
            if name.endswith(".json"):
                file_list.append(os.path.join(directory, name))

    for file in tqdm(file_list):
        with open(file) as f:
            print(file)
            channels = json.load(f)

        for ch_id in channels:
            channel = channels[ch_id]
            channel['_id'] = int(ch_id)
            insert_channel(channel, db_name)

def get_ch_info_by_id(ch_id, db_name='Telegram_test'):
    ch_info = get_channel_by_id(ch_id, db_name=db_name, with_text_msgs=False, with_media_msgs=False)
    ch_info_df = pd.DataFrame(ch_info, index=[0]).rename(columns={'_id':'ch_id'})
    ch_info_df[ch_info_df.columns] = ch_info_df[ch_info_df.columns].fillna(value=np.nan)
    ch_info_df['ch_id'] = ch_info_df['ch_id'].astype(int)
    return ch_info_df

def get_chs_info_by_ids(ch_ids, db_name='Telegram_test'):
    chs_info = get_channels_by_ids(ch_ids, db_name=db_name, with_text_msgs=False, with_media_msgs=False)
    chs_info_df = pd.DataFrame(chs_info).rename(columns={'_id':'ch_id'})
    chs_info_df[chs_info_df.columns] = chs_info_df[chs_info_df.columns].fillna(value=np.nan)
    chs_info_df['ch_id'] = chs_info_df['ch_id'].astype(int)
    return chs_info_df

def get_msgs_by_ch_id(ch_id, db_name='Telegram_test'):
    columns = ['msg_id', 'message', 'date', 'author', 'is_forwarded', 'forwarded_from_id', 'forwarded_message_date', 'title', 'extension', 'media_id', 'ch_id']
    text_data = get_text_messages_by_id_ch(ch_id, db_name=db_name)
    media_data = get_channel_by_id(ch_id, db_name=db_name, with_text_msgs=False, with_media_msgs=True)['generic_media']
    text_df = pd.DataFrame.from_dict(text_data, orient='index').reset_index().rename(columns={'index':'msg_id'})
    media_df = pd.DataFrame.from_dict(media_data, orient='index').reset_index().rename(columns={'index':'msg_id'})
    text_df[text_df.columns] = text_df[text_df.columns].fillna(value=np.nan)
    media_df[media_df.columns] = media_df[media_df.columns].fillna(value=np.nan)
    if text_data == {} and media_data == {}:
        ch_msgs_df = pd.DataFrame(columns)
    elif text_data == {} and media_data != {}:
        ch_msgs_df = media_df
    elif text_data != {} and media_data == {}: 
        ch_msgs_df = text_df
    else:
        ch_msgs_df = pd.merge(text_df, media_df, on=['msg_id', 'date', 'author', 'is_forwarded', 'forwarded_from_id', 'forwarded_message_date'], how='outer')
    for col in columns:
        if col not in ch_msgs_df.columns:
            ch_msgs_df[col] = np.nan
    # reorder columns 
    ch_msgs_df = ch_msgs_df[columns]
    ch_msgs_df[ch_msgs_df.columns] = ch_msgs_df[ch_msgs_df.columns].fillna(value=np.nan)
    ch_msgs_df['ch_id'] = ch_id
    ch_msgs_df['msg_id'] = ch_msgs_df['msg_id'].astype(int)
    # not_null_cols
    ch_msgs_df = ch_msgs_df.dropna(subset=['ch_id', 'msg_id', 'date', 'is_forwarded'])
    # not_null_together
    ch_msgs_df = ch_msgs_df[ch_msgs_df['message'].notna() | ch_msgs_df['media_id'].notna()]
    # if_forwarded_not_null_cols
    ch_msgs_df = ch_msgs_df[(ch_msgs_df['is_forwarded'] == False) | ((ch_msgs_df['is_forwarded'] == True) & (ch_msgs_df['forwarded_from_id'].notna()) & (ch_msgs_df['forwarded_message_date'].notna()))]
    # sort and reset
    ch_msgs_df = ch_msgs_df.sort_values('msg_id').reset_index(drop=True)
    return ch_msgs_df

def get_msgs_by_ch_ids(ch_ids, db_name='Telegram_test'):
    msgs = {}
    for ch_id in tqdm(ch_ids):
        tmp_df = get_msgs_by_ch_id(ch_id, db_name=db_name)
        msgs[ch_id] = tmp_df
    return msgs


if __name__ == '__main__':
    import_channels_to_mongoDB('Telegram_test')
