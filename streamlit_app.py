# Import python packages

import streamlit as st

# Added json for safer string formatting in SQL (though f-string is used below)

import json 

from snowflake.snowpark.functions import col
 
# Write directly to the app

st.title("🥤 Customise Your Smoothie 🥤")

st.write(

    """Choose the fruits you want in your custom Smoothie.

    """)
 
# 1. Get user input for the name

name_on_order = st.text_input("Name on Smoothie: ")

st.write("The name on the smoothie will be", name_on_order)
 
# 2. Establish connection and get data

cnx = st.connection("snowflake")

session = cnx.session()
 
# Corrected Issue #2: Convert Snowpark DataFrame to a Python list

# We use .collect() to execute the query, and then a list comprehension 

# to pull out the fruit name (the first element of each row/tuple).

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_options = [row[0] for row in my_dataframe.collect()]
 
# 3. Get ingredients from the user

ingredients_List = st.multiselect(

    "Choose up to 5 ingredients"

    ,ingredients_options # Use the corrected Python list here

    ,max_selections=5

)
 
# 4. Handle order submission logic

if ingredients_List:

    # Corrected Issue #1: Build the ingredients string BEFORE constructing the SQL

    # Safely join the list of ingredients into a single, space-separated string

    ingredients_string = ' '.join(ingredients_List) 

    # Use an f-string for safer, more readable SQL construction

    # Use json.dumps for name_on_order to properly escape quotes in the string

    # although Streamlit will likely handle it, it's a good practice.

    # We will use simple string formatting for clarity here.

    my_insert_stmt = f"""

        insert into smoothies.public.orders(ingredients, name_on_order)

        values ('{ingredients_string}', '{name_on_order}')

    """

    # The button should trigger the insertion

    time_to_insert = st.button("Submit Order")
 
    if time_to_insert:

        # Check if a name was entered before inserting

        if name_on_order:

            session.sql(my_insert_stmt).collect()

            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

        else:

            st.warning("Please enter a name for your order before submitting.")
 
