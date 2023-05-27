import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide",initial_sidebar_state="expanded")

if "channel_labels" not in st.session_state:
    st.session_state.cursor.execute("desc channel")
    st.session_state.channel_labels = [x[0] for x in st.session_state.cursor.fetchall()]
if "playlist_labels" not in st.session_state:
    st.session_state.cursor.execute("desc playlist")
    st.session_state.playlist_labels = [x[0] for x in st.session_state.cursor.fetchall()]
if "video_labels" not in st.session_state:
    st.session_state.cursor.execute("desc video")
    st.session_state.video_labels = [x[0] for x in st.session_state.cursor.fetchall()]
if "comment_labels" not in st.session_state:
    st.session_state.cursor.execute("desc comment")
    st.session_state.comment_labels = [x[0] for x in st.session_state.cursor.fetchall()]

st.subheader("Data Analysis")
st.write("---")
if len(st.session_state.sql_channels) != 0:
    ## Defining figures for each question.
    def figure1():
        ## Channels and their VideoCount figure(1)
        st.session_state.cursor.execute("select channel_name,channel_video_count from channel")
        temp = st.session_state.cursor.fetchall()
        fig, ax = plt.subplots()
        ax.barh([x[0][:7] + "..." for x in temp], [x[1] for x in temp])
        ax.set_xlabel("video_count")
        ax.set_ylabel("channel_name")
        ax.invert_yaxis()
        return fig


    def figure2():
        ## Channels and their VideoCount figure(2)
        st.session_state.cursor.execute(
            "select channel_name,channel_video_count from channel order by channel_video_count desc")
        temp = st.session_state.cursor.fetchall()
        fig, ax = plt.subplots()
        ax.barh([x[0][:7] + "..." for x in temp], [x[1] for x in temp])
        ax.set_xlabel("video_count")
        ax.set_ylabel("channel_name")
        ax.invert_yaxis()
        return fig


    def figure3():
        ## 10 most viewed videos figure(3)
        st.session_state.cursor.execute("select video_name,view_count from video order by view_count desc limit 10")
        temp = st.session_state.cursor.fetchall()
        fig, ax = plt.subplots()
        ax.barh([x[0][:7] + "..." for x in temp], [x[1] for x in temp])
        ax.set_xlabel("view_count")
        ax.set_ylabel("video_name")
        ax.invert_yaxis()
        return fig


    def figure4():
        ## Video comment counts figure(4)
        st.session_state.cursor.execute(
            "select video_name,comment_count from video order by comment_count desc limit 10")
        temp = st.session_state.cursor.fetchall()
        fig, ax = plt.subplots()
        ax.barh([x[0][:7] + ".." for x in temp], [x[1] for x in temp])
        ax.set_xlabel("comment_count")
        ax.set_ylabel("video_name")
        ax.invert_yaxis()
        return fig


    def figure5():
        ## Most liked videos figure(5)
        st.session_state.cursor.execute("select video_name,like_count from video order by like_count desc limit 10")
        temp = st.session_state.cursor.fetchall()
        fig, ax = plt.subplots()
        ax.barh([x[0][:7] + ".." for x in temp], [x[1] for x in temp])
        ax.set_xlabel("like_count")
        ax.set_ylabel("video_name")
        ax.invert_yaxis()
        return fig


    def figure6():
        ## Likes count for videos figure(6)
        st.session_state.cursor.execute("select video_name,like_count from video order by like_count desc limit 10")
        temp = st.session_state.cursor.fetchall()
        fig, ax = plt.subplots()
        ax.barh([x[0][:7] + ".." for x in temp], [x[1] for x in temp])
        ax.set_xlabel("like_count")
        ax.set_ylabel("video_name")
        ax.invert_yaxis()
        return fig


    def figure7():
        ## Channel names and channel views figure(7)
        st.session_state.cursor.execute("select channel_name,channel_views from channel")
        temp = st.session_state.cursor.fetchall()
        fig, ax = plt.subplots()
        ax.barh([x[0][:7] + ".." for x in temp], [x[1] for x in temp])
        ax.set_xlabel("channel_views")
        ax.set_ylabel("channel_name")
        ax.invert_yaxis()
        return fig


    def figure8():
        ## Channels that published video in 2022 figure(8)
        st.session_state.cursor.execute("select channel_name,count(*) as videos_in_2022 "
                                        "from video join playlist on video.playlist_id=playlist.playlist_id"
                                        " join channel on channel.playlist_id=playlist.playlist_id"
                                        " where year(published_date)=2022 group by channel_name")
        temp = st.session_state.cursor.fetchall()
        fig, ax = plt.subplots()
        ax.barh([x[0][:7] + ".." for x in temp], [x[1] for x in temp])
        ax.set_xlabel("videos_in_2022")
        ax.set_ylabel("channel_name")
        ax.invert_yaxis()
        return fig


    def figure9():
        ## Average video duration of channels figure(9)
        st.session_state.cursor.execute("select channel_name,avg(video_duration_seconds)as average_video_duration"
                                        " from video join playlist on video.playlist_id=playlist.playlist_id"
                                        " join channel on channel.playlist_id=playlist.playlist_id"
                                        " group by channel_name")
        temp = st.session_state.cursor.fetchall()
        fig, ax = plt.subplots()
        ax.barh([x[0][:7] + ".." for x in temp], [x[1] for x in temp])
        ax.set_xlabel("average_video_duration_seconds")
        ax.set_ylabel("channel_name")
        ax.invert_yaxis()
        return fig


    def figure10():
        ## Most commented videos figure(10)
        st.session_state.cursor.execute("select video_name,comment_count"
                                        " from video join playlist on video.playlist_id=playlist.playlist_id"
                                        " join channel on channel.playlist_id=playlist.playlist_id"
                                        " order by comment_count desc limit 10")
        temp = st.session_state.cursor.fetchall()
        fig, ax = plt.subplots()
        ax.barh([x[0][:7] + ".." for x in temp], [x[1] for x in temp])
        ax.set_xlabel("video_comments")
        ax.set_ylabel("video_name")
        ax.invert_yaxis()
        return fig


    ## Gathering answers for questions
    ## VideoName and ChannelName (data1)
    st.session_state.cursor.execute("select video_name,channel_name"
                                    " from video join playlist on video.playlist_id=playlist.playlist_id"
                                    " join channel on playlist.playlist_id=channel.playlist_id")
    channel_names = []
    video_names = []
    for i in st.session_state.cursor.fetchall():
        video_names.append((i[0]))
        channel_names.append(i[1])
    data1 = {"channel_name": channel_names, "video_name": video_names}
    data1 = pd.DataFrame(data1)

    ## ChannelName sorted by VideoCount (data2)
    st.session_state.cursor.execute("select channel_name,channel_video_count "
                                    "from channel order by channel_video_count desc")
    channel_names = []
    channel_video_count = []
    for i in st.session_state.cursor.fetchall():
        channel_names.append((i[0]))
        channel_video_count.append(i[1])
    data2 = {"channel_name": channel_names, "channel_video_count": channel_video_count}
    data2 = pd.DataFrame(data2)

    ## Top 10 videos and their channel (data3)
    st.session_state.cursor.execute("select channel_name,video_name,view_count "
                                    "from video join playlist on video.playlist_id=playlist.playlist_id "
                                    "join channel on channel.playlist_id=playlist.playlist_id "
                                    "order by view_count desc limit 10")
    channel_names = []
    video_names = []
    video_views = []
    for i in st.session_state.cursor.fetchall():
        channel_names.append((i[0]))
        video_names.append(i[1])
        video_views.append(i[2])
    data3 = {"channel_name": channel_names, "video_names": video_names, "video_views": video_views}
    data3 = pd.DataFrame(data3)

    ## VideoNames and CommentCount (data4)
    st.session_state.cursor.execute("select video_name,comment_count from video")
    video_names = []
    comment_count = []
    for i in st.session_state.cursor.fetchall():
        video_names.append((i[0]))
        comment_count.append(i[1])
    data4 = {"video_name": video_names, "comment_count": comment_count}
    data4 = pd.DataFrame(data4)

    ## MostLikedVideos and ChannelName (data5)
    st.session_state.cursor.execute("select video_name, channel_name, like_count "
                                    "from video join playlist on video.playlist_id=playlist.playlist_id "
                                    "join channel on channel.playlist_id=playlist.playlist_id "
                                    "order by like_count desc")
    video_names = []
    channel_names = []
    like_count = []
    for i in st.session_state.cursor.fetchall():
        video_names.append((i[0]))
        channel_names.append(i[1])
        like_count.append(i[2])
    data5 = {"channel_name": channel_names, "video_name": video_names, "like_count": like_count}
    data5 = pd.DataFrame(data5)

    ## VideoNames and VideoLikes (data6)
    st.session_state.cursor.execute("select video_name,like_count from video")
    video_names = []
    like_count = []
    for i in st.session_state.cursor.fetchall():
        video_names.append((i[0]))
        like_count.append(i[1])
    data6 = {"video_name": video_names, "like_count": like_count}
    data6 = pd.DataFrame(data6)

    ## ChannelName and ChannelViews (data7)
    st.session_state.cursor.execute("select channel_name,channel_views from channel")
    channel_names = []
    channel_views = []
    for i in st.session_state.cursor.fetchall():
        channel_names.append((i[0]))
        channel_views.append(i[1])
    data7 = {"channel_name": channel_names, "channel_views": channel_views}
    data7 = pd.DataFrame(data7)

    ## ChannelName who published video in 2022 (data8)
    st.session_state.cursor.execute("select channel_name "
                                    "from video join playlist on video.playlist_id=playlist.playlist_id "
                                    "join channel on channel.playlist_id=playlist.playlist_id "
                                    "where year(published_date)=2022 group by channel_name")
    channel_names = []
    for i in st.session_state.cursor.fetchall():
        channel_names.append((i[0]))
    data8 = {"channel_name": channel_names}
    data8 = pd.DataFrame(data8)

    ## AverageVideoDuration and ChannelNames (data9)
    st.session_state.cursor.execute("select channel_name,avg(video_duration_seconds)as average_video_duration "
                                    "from video join playlist on video.playlist_id=playlist.playlist_id "
                                    "join channel on channel.playlist_id=playlist.playlist_id "
                                    "group by channel_name")
    channel_names = []
    average_video_duration = []
    for i in st.session_state.cursor.fetchall():
        channel_names.append((i[0]))
        average_video_duration.append(i[1])
    data9 = {"channel_name": channel_names, "average_video_duration_seconds": average_video_duration}
    data9 = pd.DataFrame(data9)

    ## MostCommentedVideos and ChannelNames (data10)
    st.session_state.cursor.execute("select channel_name,video_name,comment_count "
                                    "from video join playlist on video.playlist_id=playlist.playlist_id "
                                    "join channel on channel.playlist_id=playlist.playlist_id "
                                    "order by comment_count desc")
    channel_names = []
    video_names = []
    comment_count = []
    for i in st.session_state.cursor.fetchall():
        channel_names.append((i[0]))
        video_names.append(i[1])
        comment_count.append(i[2])
    data10 = {"channel_name": channel_names, "video_name": video_names, "comment_count": comment_count}
    data10 = pd.DataFrame(data10)

    col1, col2 = st.columns([7, 4])
    with col1:
        ## Questions select_box
        questions = ["All video names and their corresponding channel",
                     "Channels with most videos and their video count",
                     "Top 10 most viewed videos and their channel name",
                     "Video names and their corresponding comment count",
                     "Videos with most likes and their corresponding channel",
                     "Video names and their like count",
                     "Channel names and their total views",
                     "Channels that have published video in 2022",
                     "Channel names and their average video duration",
                     "Videos with most comments and their corresponding channel name"]

        answers = [data1, data2, data3, data4, data5, data6, data7, data8, data9, data10]

        choose_question = st.selectbox("Choose question..", questions,
                                       key="choose_question")

        st.write(answers[questions.index(choose_question)])

    with col2:
        st.write("")
        st.write("")
        figures = [figure1(), figure2(), figure3(), figure4(), figure5(), figure6(), figure7(), figure8(), figure9(),
                   figure10()]
        st.pyplot(figures[questions.index(choose_question)])

    ## Get Channel Data
    st.write("")
    st.write("")
    st.session_state.cursor.execute("select * from channel")
    values = st.session_state.cursor.fetchall()
    channel_data = {}
    for i in range(len(st.session_state.channel_labels)):
        channel_data[st.session_state.channel_labels[i]] = [k[i] for k in values]
    channel_data = pd.DataFrame(channel_data)
    st.markdown("#### Channel Tabel")
    st.write(channel_data)

    ## Get Playlist Data
    st.write("")
    st.session_state.cursor.execute("select * from playlist")
    values = st.session_state.cursor.fetchall()
    playlist_data = {}
    for i in range(len(st.session_state.playlist_labels)):
        playlist_data[st.session_state.playlist_labels[i]] = [k[i] for k in values]
    playlist_data = pd.DataFrame(playlist_data)
    st.markdown("#### Playlist Tabel")
    st.write(playlist_data)

    ## Get Video Data
    st.write("")
    st.session_state.cursor.execute("select * from video")
    values = st.session_state.cursor.fetchall()
    video_data = {}
    for i in range(len(st.session_state.video_labels)):
        video_data[st.session_state.video_labels[i]] = [k[i] for k in values]
    video_data = pd.DataFrame(video_data)
    video_data["video_duration_seconds"] = [(i // 1000000000) for i in
                                            video_data["video_duration_seconds"].astype("int")]
    st.markdown("#### Video Tabel")
    st.write(video_data)

    ## Get Comment Data
    st.write("")
    st.session_state.cursor.execute("select * from comment")
    values = st.session_state.cursor.fetchall()
    comment_data = {}
    for i in range(len(st.session_state.comment_labels)):
        comment_data[st.session_state.comment_labels[i]] = [k[i] for k in values]
    comment_data = pd.DataFrame(comment_data)
    st.markdown("#### Comment Tabel")
    st.write(comment_data)

else:
    st.write("Merge data to MySql from page2 !!!")
