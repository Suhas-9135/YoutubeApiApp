import streamlit as st
import time
from pymongo import MongoClient
from googleapiclient.discovery import build

st.set_page_config(layout="wide",initial_sidebar_state="expanded")

if "channels" not in st.session_state:
    st.session_state.channels = []
if "channel_box" not in st.session_state:
    st.session_state.channel_box = ""
if "api_key" not in st.session_state:
    st.session_state.api_key = "AIzaSyBNAJv0XRR3k6djB6J7Uriwt7KZ4TpEvVA"
if "mongo_data" not in st.session_state:
    st.session_state.mongo_data = []
if "mongo_keys" not in st.session_state:
    st.session_state.mongo_keys = []
if "collection" not in st.session_state:
    client = MongoClient("mongodb+srv://User:User1234@cluster0.weezv0z.mongodb.net/?retryWrites=true&w=majority")
    database = client.youtube_db
    li = len(list(database.list_collections()))
    st.session_state.collection = database["collection_" + str(li)]


def upload_to_mongo():
    if len(st.session_state.mongo_data) == 0:
        st.session_state.mongo_keys = []
    else:
        st.session_state.mongo_keys = []
        for i in range(len(st.session_state.mongo_data)):
            st.session_state.mongo_keys.append(list(st.session_state.mongo_data[i].keys())[0])
    for ind in range(len(st.session_state.channels)):
        ## Creating an googleapi connector
        api_key = st.session_state.api_key
        channel_id = st.session_state.channels[ind]
        youtube = build("youtube", "v3", developerKey=api_key)

        def get_channel_info(youtube, channel_id):
            request = youtube.channels().list(part="snippet,statistics,contentDetails,status", id=channel_id)
            respond = request.execute()
            return respond

        def get_playlist_details(youtube, data):
            ## To get playlist name:
            request = youtube.playlists().list(part="snippet", id=data[channel_id]['playlist']["playlist_id"],
                                               maxResults=50)
            respond = request.execute()
            data[channel_id]['playlist']['playlist_name'] = respond['items'][0]['snippet']['title']
            data[channel_id]['playlist']['channel_id'] = respond['items'][0]['snippet']['channelId']
            ## To get video ids
            temp = []
            request = youtube.playlistItems().list(part="contentDetails",
                                                   playlistId=data[channel_id]['playlist']["playlist_id"],
                                                   maxResults=50)
            respond = request.execute()
            for i in range(len(respond["items"])):
                temp.append(respond["items"][i]["contentDetails"]["videoId"])
            while respond.get("nextPageToken") != None:
                request = youtube.playlistItems().list(part="contentDetails",
                                                       playlistId=data[channel_id]['playlist']["playlist_id"],
                                                       maxResults=50, pageToken=respond.get("nextPageToken"))
                respond = request.execute()
                for i in range(len(respond["items"])):
                    temp.append(respond["items"][i]["contentDetails"]["videoId"])
            data[channel_id]['playlist']['videos'] = [{} for i in range(len(temp))]
            for i in range(len(temp)):
                data[channel_id]['playlist']['videos'][i]['video_id'] = temp[i]

        def get_video_details(youtube, data):
            ## To get video_details
            for i in range(len(data[channel_id]['playlist']['videos'])):
                request = youtube.videos().list(part="snippet,contentDetails,statistics",
                                                id=data[channel_id]['playlist']['videos'][i]['video_id'])
                respond = request.execute()
                ## Adding values to video details
                data[channel_id]['playlist']['videos'][i]["playlist_id"] = data[channel_id]['playlist']['playlist_id']
                data[channel_id]['playlist']['videos'][i]["video_name"] = respond["items"][0]["snippet"]["title"]
                data[channel_id]['playlist']['videos'][i]["video_description"] = respond["items"][0]["snippet"][
                    "description"]
                if 'tags' in respond["items"][0]["snippet"]:
                    data[channel_id]['playlist']['videos'][i]["video_tags"] = respond["items"][0]["snippet"]["tags"]
                else:
                    data[channel_id]['playlist']['videos'][i]["video_tags"] = []
                data[channel_id]['playlist']['videos'][i]["published_date"] = respond["items"][0]["snippet"][
                    "publishedAt"]
                data[channel_id]['playlist']['videos'][i]["view_count"] = int(
                    respond["items"][0]["statistics"]["viewCount"])
                if 'likeCount' in respond['items'][0]['statistics']:
                    data[channel_id]['playlist']['videos'][i]["like_count"] = int(
                        respond["items"][0]['statistics']['likeCount'])
                else:
                    data[channel_id]['playlist']['videos'][i]["like_count"] = 0
                data[channel_id]['playlist']['videos'][i]["favorite_count"] = int(
                    respond["items"][0]["statistics"]["favoriteCount"])
                data[channel_id]['playlist']['videos'][i]["comment_count"] = int(
                    respond["items"][0]["statistics"]["commentCount"])
                data[channel_id]['playlist']['videos'][i]["video_duration"] = respond["items"][0]["contentDetails"][
                    "duration"]
                data[channel_id]['playlist']['videos'][i]["thumbnail_url"] = \
                    respond["items"][0]["snippet"]["thumbnails"]["default"]["url"]
                data[channel_id]['playlist']['videos'][i]["caption_status"] = respond["items"][0]["contentDetails"][
                    "caption"]

        def get_comment_details(youtube, data):
            ## To get comment details
            for i in range(len(data[channel_id]['playlist']['videos'])):
                request = youtube.commentThreads().list(part="snippet",
                                                        videoId=data[channel_id]['playlist']['videos'][i]['video_id'],
                                                        maxResults=50)
                respond = request.execute()
                data[channel_id]['playlist']['videos'][i]['comments'] = []
                for k in range(len(respond["items"])):
                    temp = {}
                    temp['comment_id'] = respond['items'][k]['snippet']['topLevelComment']['id']
                    temp['video_id'] = respond['items'][k]['snippet']['videoId']
                    temp['comment_text'] = respond['items'][k]['snippet']['topLevelComment']['snippet']['textOriginal']
                    temp['comment_author'] = respond['items'][k]['snippet']['topLevelComment']['snippet'][
                        'authorDisplayName']
                    temp['comment_published_at'] = respond['items'][k]['snippet']['topLevelComment']['snippet'][
                        'publishedAt']
                    data[channel_id]['playlist']['videos'][i]['comments'].append(temp)
                while respond.get("nextPageToken") != None:
                    request = youtube.commentThreads().list(part="snippet",
                                                            videoId=data[channel_id]['playlist']["videos"][i][
                                                                'video_id'],
                                                            maxResults=50, pageToken=respond.get("nextPageToken"))
                    respond = request.execute()
                    for k in range(len(respond["items"])):
                        temp = {}
                        temp['comment_id'] = respond['items'][k]['snippet']['topLevelComment']['id']
                        temp['video_id'] = respond['items'][k]['snippet']['videoId']
                        temp['comment_text'] = respond['items'][k]['snippet']['topLevelComment']['snippet'][
                            'textOriginal']
                        temp['comment_author'] = respond['items'][k]['snippet']['topLevelComment']['snippet'][
                            'authorDisplayName']
                        temp['comment_published_at'] = respond['items'][k]['snippet']['topLevelComment']['snippet'][
                            'publishedAt']
                        data[channel_id]['playlist']['videos'][i]['comments'].append(temp)

        if channel_id not in st.session_state.mongo_keys:
            ##Create a dictionary list that contains information of all channels
            data = {channel_id: {}}

            channel_info = get_channel_info(youtube, channel_id)
            with st.spinner("Uploading {}...".format(channel_info["items"][0]["snippet"]["title"])):

                ## Extract required information into data list
                data[channel_id]['channel_id'] = channel_info['items'][0]['id']
                data[channel_id]['channel_name'] = channel_info['items'][0]['snippet']['title']
                data[channel_id]['channel_description'] = channel_info['items'][0]['snippet']['description']
                data[channel_id]['channel_view_count'] = int(channel_info['items'][0]['statistics']['viewCount'])
                data[channel_id]['channel_video_count'] = int(channel_info['items'][0]['statistics']['videoCount'])
                data[channel_id]['channel_subscribers'] = int(channel_info['items'][0]['statistics']['subscriberCount'])
                data[channel_id]['playlist_id'] = channel_info['items'][0]['contentDetails']['relatedPlaylists'][
                    'uploads']
                data[channel_id]['channel_status'] = channel_info['items'][0]['status']['privacyStatus']
                data[channel_id]['playlist'] = {
                    "playlist_id": channel_info['items'][0]['contentDetails']['relatedPlaylists']['uploads']}

                get_playlist_details(youtube, data)

                get_video_details(youtube, data)

                get_comment_details(youtube, data)

                st.session_state.mongo_data.append(data)

        else:
            channel_info = get_channel_info(youtube, channel_id)
            emp3 = st.empty()
            emp3.warning("{} already uploaded".format(channel_info["items"][0]["snippet"]["title"]))
            time.sleep(0.8)
            emp3.empty()

    with st.spinner("Refreshing..."):
        st.session_state.collection.delete_many({})
        st.session_state.collection.insert_many(st.session_state.mongo_data)
    emp = st.empty()
    emp.success("Done!!!")
    time.sleep(1.1)
    emp.empty()


youtube = build("youtube", "v3", developerKey=st.session_state.api_key)
col1, col2 = st.columns([2, 6])
with col1:
    st.write("")
    st.write("")
    st.session_state.channel_box = st.text_input("Enter channel id...")
    button = st.button("Add", key="add_button")
    emp0 = st.empty()
    clear_button = emp0.button("Clear List")
    if clear_button:
        st.session_state.channels.clear()
        st.experimental_rerun()
    emp5 = st.empty()
    clear_data = emp5.button("Clear Database")
    if clear_data:
        st.session_state.mongo_data.clear()
        st.session_state.collection.delete_many({})
        st.experimental_rerun()
    upload_button = st.button("Upload list to MongoDB")
    if upload_button:
        emp1 = st.empty()
        if len(st.session_state.channels) == 0:
            emp1.warning("Add channels to list!!")
            time.sleep(1)
            emp1.empty()
        else:
            upload_to_mongo()
    if button:
        emp1 = st.empty()
        if st.session_state.channel_box in st.session_state.channels:
            emp1.warning("Channel already exists!!")
            time.sleep(0.8)
            emp1.empty()
        elif st.session_state.channel_box == "":
            emp1.warning("Invalid ID!!")
            time.sleep(0.8)
            emp1.empty()
        elif len(st.session_state.channels) == 10:
            emp1.warning("Channels limit reached!!!!")
            time.sleep(0.8)
            emp1.empty()
        else:
            # noinspection PyBroadException
            try:
                temp = youtube.channels().list(part="statistics", id=st.session_state.channel_box).execute()["items"]
                st.session_state.channels.append(st.session_state.channel_box)
            except:
                emp1.warning("Invalid ID!!")
                time.sleep(0.8)
                emp1.empty()
            st.session_state.channel_box = ""

with col2:
    st.write("")
    st.write("")
    if len(st.session_state.mongo_data) == 0:
        pass
    elif len(st.session_state.mongo_data) == 1:
        st.write(f"{len(st.session_state.mongo_data)} channel in MongoDB.   Check Page2 for details..")
    else:
        st.write(f"{len(st.session_state.mongo_data)} channels in MongoDB.  Check Page2 for details..")
    if len(st.session_state.channels) == 0:
        st.info("No Channels Added")
    else:
        st.markdown("##### List preview")
        st.write("-----")
        for i in st.session_state.channels:
            column1, column2, column3 = st.columns([2, 3, 6])
            request = youtube.channels().list(part="snippet,statistics", id=i)
            respond = request.execute()
            with column1:
                st.image(respond["items"][0]["snippet"]["thumbnails"]["default"]["url"], width=120)
            with column2:
                st.subheader(respond["items"][0]["snippet"]["title"])
                st.caption("Stats:")
                st.markdown("###### Subscribers: {}".format(respond["items"][0]["statistics"]["subscriberCount"]))
                st.markdown("###### Total Videos: {}".format(respond["items"][0]["statistics"]["videoCount"]))
            with column3:
                if respond["items"][0]["snippet"]["description"] == "":
                    st.write("")
                    st.write("#No description#")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                elif len(respond["items"][0]["snippet"]["description"]) > 220:
                    st.write(respond["items"][0]["snippet"]["description"][:217] + "...")
                else:
                    st.write(respond["items"][0]["snippet"]["description"])
                remove_button = st.button("Remove {} from list".format(respond["items"][0]["snippet"]["title"]))
                if remove_button:
                    st.session_state.channels.remove(i)
                    st.experimental_rerun()
            st.write("-------------")
