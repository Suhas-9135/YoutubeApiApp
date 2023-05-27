This project aims at extracting data from given Youtube channels, stroing it to MongoDB, merging to MySQL for applying queries,
and answering few basic questions below:-

-> What are the names of all the videos and their corresponding channels?
-> Which channels have the most number of videos, and how many videos do they have?
-> What are the top 10 most viewed videos and their respective channels?
-> How many comments were made on each video, and what are their corresponding video names?
-> Which videos have the highest number of likes, and what are their corresponding channel names?
-> What is the total number of likes for each video, and what are their corresponding video names?
-> What is the total number of views for each channel, and what are their corresponding channel names?
-> What are the names of all the channels that have published videos in the year 2022?
-> What is the average duration of all videos in each channel, and what are their corresponding channel names?
-> Which videos have the highest number of comments, and what are their corresponding channel names?

The project end goal is to answer the above questions but its base code can be used to make more complex data analysis.
Major tools used are:-
-> Python
-> Youtube Data Api
-> MongoDb
-> MySQL
-> StreamLit
-> Python libraries (Pandas, Numpy, Matplotlib,etc..)


## Running the Application ##
As environment setup, Python and MySQL should be installed in the environment to run the code.

1.  Extreact this repository files into a folder where your python virtueal environment will run.
2. Place "main.py", "libraries.txt" file in a folder and inside that folder create a "pages" folder and paste "page2.py" and "page3.py" in it.
3. Open command terminal in the folder where libraries.txt is kept and run
          "pip install -r libraries.txt"
    This will install all the required libraries to run this application in your python venv.
4. Now run
          "streamlit run main.py"
    This will run the main.py file using streamlit in a browser. The pages folder acts as pages in the streamlit application.
    Hence you can see the "page2" and "page3" are seperate pages displayed in streamlit app.
5. Once the streamlit application is running, you are ready to use the application!!


## Using the Application ##
1. Extract channel_id's of the youtube channel's whoes data needs to be extracted for analysing.
      Channel_id extraction by:
        -> At youtube.com search the channel name you want to extract data from.
        -> Click on its image to go to its main page.
        -> Right click and select "view_page_source" to see the page details.
        -> Press "Ctrl+F" on Linux, Windows  or press "Cmd+F" on MacOs to start the search.
        -> Search for "ChannelId", you will receive something like
              "channelId":"Uvxgvdchb-dhvhdcvs"
        -> Copy the channel_id to save it to clipboard.
        -> Sample channel id's can be found in "Sample_id.txt" file.
2. Paste the channel id inside the text box and click on "Add" to get a channel preview.
3. Add upto 10 channel to the list on whom analysis is to be done.
      If you want to remove a channel from the list, click on "Remove <channel name> from the list".
      To clear the list click on "Clear list".
4. Once the channels_list is set, click on "Upload to MongoDB" button to upload the channels data to MongoDB.
5. You can a message showing the number of channel stored in MongoDB.
6. Once data uploaded to MongoDB click on page2 from the sidebar to go to page2.

7. On page2 you can see the names of all the channels present in MongoDB. Beneath it you can see the channel details
    showing the data of the respective selected channel.
    To see data of different channel you can select the channel using the select_box given beneath "Channel details"
8. To merge data MySQL, check the checkboxes of the respective channel whoes data needs to be merged to MySQL for analysis.
9. Once checkbox ticked, click on "Merge to MySQL" to merge the channel data to MySQL for analysis.
10. You can see a preview of the channels in MySQL beneath "MySQL data" banner.
11. If required to change the channels inserted in MySQL, click on "Clear MySQL database" and add channels again from check_box list.

12. On page3 we can see all the channel data stored in MySQL in the form of tables.
13. You can select appropriate question from the select_box and the answer to it will be displayed below the check_box.
14. You can also see a visual represented graph aside the answer table for better analysis.
15. You can restart the application by simply refreshing the application tab in the browser.


Hope you find this YoutubeChannel data analysis application useful. The application use does not end here as the application code can be
  tweaked a little to perform more complex quries as per your need to get appropriate data results.
Link to DemoVideo can be found in DemoVideo.txt file!

Linkedin post: https://www.linkedin.com/posts/suhas-kure-2163601a6_github-suhas-9135youtubeapiapp-activity-7068306960617508864-4LXA?utm_source=share&utm_medium=member_desktop
DemoVideo: https://drive.google.com/file/d/1egfCuMJpIbIBDazEJih6Uq_e1N_W40f-/view

----Happy coding----
