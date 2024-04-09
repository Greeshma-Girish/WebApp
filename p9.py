import streamlit as st
import pandas as pd
import csv
import matplotlib.pyplot as plt
import re
import seaborn as sns  

username = "user"
password = "password"


def authenticate(username, password):
    if username == "user" and password == "password":
        return True
    else:
        return False

def is_user_logged_in():
    if "username" in st.session_state and "password" in st.session_state:
        return authenticate(st.session_state["username"], st.session_state["password"])
    return False

def save_review(review):
    with open('hotel_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(review)

def validate_username(new_username):
    pattern = r'^[a-zA-Z\s]+$'
    return re.match(pattern, new_username)

def validate_password(new_password):
    return len(new_password) >= 6

def save(data):
    with open('hotel_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

choice = st.sidebar.selectbox("Select Operation", ["Register","Review"])
if choice == "Register":
    username_input = st.sidebar.text_input("Username")
    password_input = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if authenticate(username_input, password_input):
            st.session_state["username"] = username_input
            st.session_state["password"] = password_input
            st.title("WELCOME TO FOOD DELIVERY !")

            name = st.text_input("Name")
            restaurant = st.selectbox("Restaurant:", ["Restaurant A", "Restaurant B", "Restaurant C"])
            food = st.selectbox("Food Item:", ["Pizza", "Burger", "Sandwich", "Noodles", "Rice"])
            location = st.text_input("Location")
            if st.button('Save'):
                data = [name, restaurant, food, location]
                save(data)
                st.success("Added successfully!")
        else:
            st.error("Incorrect username or password. Please try again.")



elif choice =="Review":
    data = {
        'Food': ['Pizza', 'Burger', 'Sushi', 'Pasta', 'Steak', 'Salad'],
        'Rating': [4.5, 3.8, 4.2, 4.0, 4.7, 4.3],
    }

    df = pd.DataFrame(data)

    st.title("Food Rating Dashboard")
    st.sidebar.header("Filters")
    min_rating = st.sidebar.number_input("Minimum Rating", min_value=0.0, max_value=5.0, value=df['Rating'].min())
    max_rating = st.sidebar.number_input("Maximum Rating", min_value=0.0, max_value=5.0, value=df['Rating'].max())

    filtered_data = df[(df['Rating'] >= min_rating) & (df['Rating'] <= max_rating)]

    st.write("Filtered Data:")
    st.write(filtered_data)

    st.header("Data Visualization")

    st.subheader("Histogram of Ratings")
    plt.figure(figsize=(10, 6))
    sns.histplot(filtered_data['Rating'], kde=True)
    st.pyplot(plt.gcf())

    st.subheader("Bar Chart: Food Ratings")
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Food', y='Rating', data=filtered_data)
    plt.xticks(rotation=45)
    st.pyplot(plt.gcf())  
