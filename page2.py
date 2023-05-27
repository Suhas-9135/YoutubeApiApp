import time
import streamlit as st
import pandas as pd
import mysql.connector as connector
import regex as re

st.set_page_config(layout="wide",initial_sidebar_state="expanded")

if "sql_channels" not in st.session_state:
    st.session_state.sql_channels = []
if "sql_channel_names" not in st.session_state:
    st.session_state.sql_channel_names = []
if "mask" not in st.session_state:
    st.session_state.mask = []
if 'db' not in st.session_state:
    st.session_state.db = connector.connect(host='localhost', user='root')
if 'cursor' not in st.session_state:
    st.session_state.cursor = st.session_state.db.cursor()
    st.session_state.cursor.execute("show databases")
    database_list = st.session_state.cursor.fetchall()
    if bytearray(b'youtube_db') in [i for x in database_list for i in x]:
        st.session_state.cursor.execute("drop database youtube_db")
        st.session_state.db.commit()
    st.session_state.cursor.execute("create database youtube_db default charset=utf8mb4 collate=utf8mb4_unicode_ci")
    st.session_state.db.commit()
    st.session_state.cursor.execute("use youtube_db")
    st.session_state.cursor.execute("create table channel(channel_id varchar(50),"
                                    "playlist_id varchar(50),"
                                    "channel_name varchar(100),"
                                    "channel_description text,"
                                    "channel_views int,"
                                    "channel_video_count int,"
                                    "channel_subscribers int,"
                                    "channel_status char(7),"
                                    "primary key(channel_id)) engine=InnoDB default charset=utf8mb4 "
                                    "collate=utf8mb4_unicode_ci")
    st.session_state.db.commit()
    st.session_state.cursor.execute("create table playlist(playlist_id varchar(50),"
                                    "channel_id varchar(50),"
                                    "playlist_name varchar(120),"
                                    "primary key(playlist_id),"
                                    "foreign key(channel_id) references channel(channel_id)) "
                                    "engine=InnoDB default charset=utf8mb4 collate=utf8mb4_unicode_ci")
    st.session_state.db.commit()
    st.session_state.cursor.execute("create table video(video_id varchar(50),"
                                    "playlist_id varchar(50),"
                                    "video_name text,"
                                    "video_description text,"
                                    "video_tags text,"
                                    "published_date datetime,"
                                    "view_count int,"
                                    "like_count int,"
                                    "favorite_count int,"
                                    "comment_count int,"
                                    "video_duration_seconds time,"
                                    "thumbnail_url varchar(100),"
                                    "caption_status char(5),"
                                    "primary key(video_id),"
                                    "foreign key(playlist_id) references playlist(playlist_id)) "
                                    "engine=InnoDB default charset=utf8mb4 collate=utf8mb4_unicode_ci")
    st.session_state.db.commit()
    st.session_state.cursor.execute("create table comment(comment_id varchar(50),"
                                    "video_id varchar(50),"
                                    "comment_text text,"
                                    "comment_author varchar(100),"
                                    "published_at datetime,"
                                    "primary key(comment_id),"
                                    "foreign key(video_id) references video(video_id)) "
                                    "engine=InnoDB default charset=utf8mb4 collate=utf8mb4_unicode_ci")
    st.session_state.db.commit()
    st.session_state.cursor.execute("set names utf8mb4")
    st.session_state.db.commit()


def upload_channel_data(i):
    channel_id = channel_data[i][list(channel_data[i].keys())[1]]["channel_id"]
    channel_name = channel_data[i][list(channel_data[i].keys())[1]]["channel_name"]
    channel_description = channel_data[i][list(channel_data[i].keys())[1]]["channel_description"]
    channel_views = channel_data[i][list(channel_data[i].keys())[1]]["channel_view_count"]
    channel_video_count = channel_data[i][list(channel_data[i].keys())[1]]["channel_video_count"]
    channel_subscribers = channel_data[i][list(channel_data[i].keys())[1]]["channel_subscribers"]
    playlist_id = channel_data[i][list(channel_data[i].keys())[1]]["playlist_id"]
    channel_status = channel_data[i][list(channel_data[i].keys())[1]]["channel_status"]
    st.session_state.cursor.execute(f"insert into channel(channel_id,"
                                    "playlist_id,"
                                    "channel_name,"
                                    "channel_description,"
                                    "channel_views,"
                                    "channel_video_count,"
                                    "channel_subscribers,"
                                    "channel_status) "
                                    f"values('{channel_id}',"
                                    f"\"{playlist_id}\","
                                    f"\"{channel_name}\","
                                    f"\"{channel_description}\","
                                    f"{channel_views},"
                                    f"{channel_video_count},"
                                    f"{channel_subscribers},"
                                    f"\"{channel_status}\")")
    st.session_state.db.commit()


def upload_playlist_data(i):
    playlist_id = channel_data[i][list(channel_data[i].keys())[1]]["playlist"]["playlist_id"]
    channel_id = channel_data[i][list(channel_data[i].keys())[1]]["channel_id"]
    playlist_name = channel_data[i][list(channel_data[i].keys())[1]]["playlist"]["playlist_name"]
    st.session_state.cursor.execute(f"insert into playlist(playlist_id,"
                                    "channel_id,"
                                    "playlist_name)"
                                    f"values(\"{playlist_id}\","
                                    f"\"{channel_id}\","
                                    f"\"{playlist_name}\")")
    st.session_state.db.commit()


def upload_video_data(i):
    for x in channel_data[i][list(channel_data[i].keys())[1]]["playlist"]["videos"]:
        video_id = x["video_id"]
        playlist_id = x["playlist_id"]
        video_name = str(x["video_name"]).replace("'", "")
        video_description = str(x["video_description"]).replace("'", "")
        video_tags = ",".join([y for y in x["video_tags"]])
        published_date = re.sub("[Z]", "", re.sub("[T]", " ", x["published_date"]))
        video_view_count = x["view_count"]
        like_count = x["like_count"]
        favorite_count = x["favorite_count"]
        comment_count = x["comment_count"]
        if 'H' in x["video_duration"]:
            hour = re.findall("T\d+H", x["video_duration"])[0][1:-1]
        else:
            hour = '0'
        if 'M' in x["video_duration"]:
            if 'H' in x["video_duration"]:
                minute = re.findall("H\d+M", x["video_duration"])[0][1:-1]
            else:
                minute = re.findall("T\d+M", x["video_duration"])[0][1:-1]
        else:
            minute = '0'

        if 'S' in x["video_duration"]:
            if 'M' in x["video_duration"]:
                second = re.findall("M\d+S", x["video_duration"])[0][1:-1]
            elif 'H' in x["video_duration"]:
                second = re.findall("H\d+S", x["video_duration"])[0][1:-1]
            else:
                second = re.findall("T\d+S", x["video_duration"])[0][1:-1]
        else:
            second = '0'
        video_duration = hour + ":" + minute + ":" + second
        thumbnail_url = x["thumbnail_url"]
        caption_status = x["caption_status"]

        st.session_state.cursor.execute(f"insert into video(video_id,playlist_id,"
                                        "video_name,video_description,"
                                        "video_tags,published_date,"
                                        "view_count,like_count,"
                                        "favorite_count,comment_count,"
                                        "video_duration_seconds,thumbnail_url,"
                                        "caption_status)"
                                        f"values(\"{video_id}\","
                                        f"\"{playlist_id}\","
                                        f"\"{video_name}\","
                                        f"\"{video_description}\","
                                        f"\"{video_tags}\","
                                        f"\"{published_date}\","
                                        f"{video_view_count},"
                                        f"{like_count},"
                                        f"{favorite_count},"
                                        f"{comment_count},"
                                        f"\"{video_duration}\","
                                        f"\"{thumbnail_url}\","
                                        f"\"{caption_status}\")")
        st.session_state.db.commit()


def upload_comment_data(i):
    for y in channel_data[i][list(channel_data[i].keys())[1]]["playlist"]["videos"]:
        for x in y["comments"]:
            comment_id = x["comment_id"]
            video_id = x["video_id"]
            comment_text = x["comment_text"]
            comment_author = x["comment_author"]
            comment_published_at = re.sub("[Z]", "", re.sub("[T]", " ", x["comment_published_at"]))
            st.session_state.cursor.execute(f"insert into comment(comment_id,"
                                            "video_id,"
                                            "comment_text,"
                                            "comment_author,"
                                            "published_at) "
                                            f"values('{comment_id}',"
                                            f"\"{video_id}\","
                                            f"\"{comment_text}\","
                                            f"\"{comment_author}\","
                                            f"\"{comment_published_at}\")")
            st.session_state.db.commit()


channel_data = list(st.session_state.collection.find())
channel_names = [x[list(x.keys())[1]]["channel_name"] for x in channel_data]
st.session_state.mask = [False for x in channel_data]
st.session_state.cursor.execute("select channel_name from channel")
st.session_state.sql_channel_names = [x[0] for x in st.session_state.cursor.fetchall()]
st.session_state.cursor.execute("select * from channel")
st.session_state.sql_channels = st.session_state.cursor.fetchall()

if len(channel_data) > 0:
    col1, col2 = st.columns([2, 4])
    with col1:
        st.subheader("Channels in MongoDB")
        for i in range(len(channel_data)):
            st.session_state.mask[i] = st.checkbox(channel_names[i])
        st.write("")
        st.write("")
        upload_button = st.button("Migrate channels to MySql")
        clear_sql = st.button("Clear MySql database")
        if upload_button:
            for i in range(len(channel_data)):
                st.session_state.cursor.execute("select channel_name from channel")
                st.session_state.sql_channel_names = [x[0] for x in st.session_state.cursor.fetchall()]
                st.session_state.cursor.execute("select * from channel")
                st.session_state.sql_channels = st.session_state.cursor.fetchall()
                if st.session_state.mask[i]:
                    if channel_names[i] in st.session_state.sql_channel_names:
                        emp = st.empty()
                        emp.warning(f"{channel_names[i]} already in MySql")
                        time.sleep(0.8)
                        emp.empty()
                    else:
                        with st.spinner(f"Migrating {channel_names[i]}..."):
                            upload_channel_data(i)
                            upload_playlist_data(i)
                            upload_video_data(i)
                            upload_comment_data(i)
                            time.sleep(0.5)
            with st.spinner("Refreshing.."):
                st.session_state.cursor.execute("select channel_name from channel")
                st.session_state.sql_channel_names = [x[0] for x in st.session_state.cursor.fetchall()]
                st.session_state.cursor.execute("select * from channel")
                st.session_state.sql_channels = st.session_state.cursor.fetchall()
                st.experimental_rerun()
                time.sleep(0.5)
            st.success("Done")

        if clear_sql:
            with st.spinner("Drooping database.."):
                st.session_state.cursor.execute("delete from comment")
                st.session_state.db.commit()
                st.session_state.cursor.execute("delete from video")
                st.session_state.db.commit()
                st.session_state.cursor.execute("delete from playlist")
                st.session_state.db.commit()
                st.session_state.cursor.execute("delete from channel")
                st.session_state.db.commit()
                time.sleep(0.5)
            with st.spinner("Refreshing.."):
                st.session_state.cursor.execute("select channel_name from channel")
                st.session_state.sql_channel_names = [x[0] for x in st.session_state.cursor.fetchall()]
                st.session_state.cursor.execute("select * from channel")
                st.session_state.sql_channels = st.session_state.cursor.fetchall()
                st.experimental_rerun()
                time.sleep(0.5)
            st.success("Database cleared!!")

    with col2:
        if len(st.session_state.sql_channels) == 0:
            st.subheader("No channels in MySql")
            st.caption("Add channels using Migrate to MySql button..")
        else:
            st.subheader("MySql data..")
            names = [x[2] for x in st.session_state.sql_channels]
            view_count = [x[4] for x in st.session_state.sql_channels]
            video_count = [x[5] for x in st.session_state.sql_channels]
            subscribers = [x[6] for x in st.session_state.sql_channels]
            status = [x[7] for x in st.session_state.sql_channels]
            data = pd.DataFrame({"Channel_name": names, "View_count": view_count, "Video_count": video_count,
                                 "Subscribers": subscribers, "Status": status}).set_index("Channel_name")
            st.write(data)
            st.caption("Check page3 for details")

    st.write("");st.write("")
    st.write("");st.write("")
    st.write("")
    st.subheader("Channel Details..")
    choose_channel = st.selectbox("Select channel", [x[list(x.keys())[1]]["channel_name"] for x in channel_data],
                                  key="choose_channel")
    st.json(channel_data[channel_names.index(st.session_state.choose_channel)])

else:
    st.subheader("No Channels to display")
    st.markdown("##### Add channels to MongoDb from page1")
