import xml.etree.ElementTree as ET
import mysql.connector
import pandas as pd
import streamlit as st

st.set_page_config(page_title = "Brotato")
st.title("Brotato Tables")

# Create a connection object
conn = mysql.connector.connect(host="localhost", user="root", password="mysql", database="Brotato")
cursor = conn.cursor()

options = st.selectbox("Select an option:", ("Insert into tables", "View tables", "Update", "Delete"))

if (options == "Insert into tables"):
    pass
elif (options == "View tables"):
    # Player_Profile table
    cursor.execute("SELECT * FROM Player_Profile;")
    results = cursor.fetchall()
    col = []
    for i in cursor.fetchall():
        col.append(i[0])
    st.write("Player_Profile:")
    results = pd.DataFrame(results, columns = col)
    st.dataframe(results)

    # Weapons table
    cursor.execute("SELECT * FROM Weapons;")
    results = cursor.fetchall()
    col = []
    for i in cursor.fetchall():
        col.append(i[0])
    st.write("Weapons:")
    results = pd.DataFrame(results, columns = col)
    st.dataframe(results)

    # Map table
    cursor.execute("SELECT * FROM Map;")
    results = cursor.fetchall()
    col = []
    for i in cursor.fetchall():
        col.append(i[0])
    st.write("Map:")
    results = pd.DataFrame(results, columns = col)
    st.dataframe(results)

    # Items table
    cursor.execute("SELECT * FROM Items;")
    results = cursor.fetchall()
    col = []
    for i in cursor.fetchall():
        col.append(i[0])
    st.write("Items:")
    results = pd.DataFrame(results, columns = col)
    st.dataframe(results)

    # Leaderboard table
    cursor.execute("SELECT * FROM Leaderboard;")
    results = cursor.fetchall()
    col = []
    for i in cursor.fetchall():
        col.append(i[0])
    st.write("Leaderboard:")
    results = pd.DataFrame(results, columns = col)
    st.dataframe(results)

elif (options == "Update"):
    pass
    """
    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='096_onlinebookstore' AND TABLE_NAME='096_books';")
    col = []
    for i in cursor.fetchall():
        col.append(i[0])
    cursor.execute("SELECT * FROM 096_books;")
    results = cursor.fetchall()
    st.write("096_books:")
    results = pd.DataFrame(results, columns = col)
    st.dataframe(results)
    if (st.button("Update", type = "primary")):
        xml_update = ET.parse("C:/Users/Arya Umesh/PES/Sem 5/Database Management Systems/Lab 7/update.xml")
        quantity = xml_update.getroot()

        # Execute SQL statement
        cursor.execute("UPDATE 096_books SET Quantity = " + str(quantity.text) + " WHERE BookID = 1;")
        conn.commit()

        cursor.execute("SELECT * FROM 096_books;")
        results = cursor.fetchall()
        st.write("096_books after update:")
        results = pd.DataFrame(results, columns = col)
        st.dataframe(results)
    """
else:
    pass
    """
    number = st.number_input("Enter CartID: ", value=None, placeholder = "Type a number...")
    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='096_onlinebookstore' AND TABLE_NAME='096_carts';")
    col = []
    for i in cursor.fetchall():
        col.append(i[0])
    cursor.execute("SELECT * FROM 096_carts;")
    results = cursor.fetchall()
    st.write("096_books:")
    results = pd.DataFrame(results, columns = col)
    st.dataframe(results)
    if (st.button("Delete", type = "primary")):
        # Execute SQL statement
        cursor.execute("DELETE FROM 096_carts WHERE CartID = " + str(number) + ";")
        conn.commit()

        cursor.execute("SELECT * FROM 096_carts;")
        results = cursor.fetchall()
        st.write("096_books after delete:")
        results = pd.DataFrame(results, columns = col)
        st.dataframe(results)
        """

# Close the cursor and connection
cursor.close()
conn.close()