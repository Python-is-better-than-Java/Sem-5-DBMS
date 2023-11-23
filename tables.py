import mysql.connector
import pandas as pd
import streamlit as st

st.set_page_config(page_title = "Shooter Game")
st.title("Shooter Game Tables")

# Create a connection object
conn = mysql.connector.connect(host="localhost", user="root", password="mysql", database="shootergame")
cursor = conn.cursor()

options = st.selectbox("Select a table to view:", ("Player Profile", "Player Statistics", "Player Achievements", "Map", "Weapons", "Items", "Leaderboard"))

if (options == "Player Profile"):
    # player_profile table
    cursor.execute("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='shootergame' AND `TABLE_NAME`='player_profile';")
    col = []
    for i in cursor.fetchall():
        col.append(i[0])
    cursor.execute("SELECT * FROM player_profile;")
    results = cursor.fetchall()
    st.write("Player Profile:")
    results = pd.DataFrame(results, columns = col)
    st.dataframe(results)

elif (options == "Player Statistics"):
    # player_statistics table
    cursor.execute("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='shootergame' AND `TABLE_NAME`='player_statistics';")
    col = []
    for i in cursor.fetchall():
        col.append(i[0])
    cursor.execute("SELECT * FROM player_statistics;")
    results = cursor.fetchall()
    st.write("Player Statistics:")
    results = pd.DataFrame(results, columns = col)
    st.dataframe(results)
    
elif (options == "Player Achievements"):
    # player_achievements table
    cursor.execute("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='shootergame' AND `TABLE_NAME`='player_achievements';")
    col = []
    for i in cursor.fetchall():
        col.append(i[0])
    cursor.execute("SELECT * FROM player_achievements;")
    results = cursor.fetchall()
    st.write("Player Statistics:")
    results = pd.DataFrame(results, columns = col)
    st.dataframe(results)
elif (options == "Map"):
    # Map table
    cursor.execute("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='shootergame' AND `TABLE_NAME`='Map';")
    col = []
    for i in cursor.fetchall():
        col.append(i[0])
    cursor.execute("SELECT * FROM Map;")
    results = cursor.fetchall()
    st.write("Map:")
    results = pd.DataFrame(results, columns = col)
    st.dataframe(results)
elif (options == "Weapons"):
    # Weapons table
    cursor.execute("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='shootergame' AND `TABLE_NAME`='Weapons';")
    col = []
    for i in cursor.fetchall():
        col.append(i[0])
    cursor.execute("SELECT * FROM Weapons;")
    results = cursor.fetchall()
    st.write("Weapons:")
    results = pd.DataFrame(results, columns = col)
    st.dataframe(results)
elif (options == "Items"):
    # Items table
    cursor.execute("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='shootergame' AND `TABLE_NAME`='Items';")
    col = []
    for i in cursor.fetchall():
        col.append(i[0])
    cursor.execute("SELECT * FROM Items;")
    results = cursor.fetchall()
    st.write("Items:")
    results = pd.DataFrame(results, columns = col)
    st.dataframe(results)
elif (options == "Leaderboard"):
    # Leaderboard table
    cursor.execute("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='shootergame' AND `TABLE_NAME`='Leaderboard';")
    col = []
    for i in cursor.fetchall():
        col.append(i[0])
    cursor.execute("SELECT * FROM Leaderboard;")
    results = cursor.fetchall()
    st.write("Leaderboard:")
    results = pd.DataFrame(results, columns = col)
    st.dataframe(results)
else:
    pass

# Close the cursor and connection
cursor.close()
conn.close()
