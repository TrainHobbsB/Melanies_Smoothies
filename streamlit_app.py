# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.title("🥤Customize Your Smoothie!🥤")

st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

cnx=st.connection("snowflake")
session = cnx.session()

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)


session = get_active_session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)



Ingredients_List = st.multiselect(
    'Choose up to 5 Ingredients:'
    ,my_dataframe
    ,max_selections=5
)

if Ingredients_List:
    #st.write(Ingredients_List)
    #st.text(Ingredients_List)

    Ingredients_String = ''

    for fruit_chosen in Ingredients_List:
        Ingredients_String += fruit_chosen + ' '

    #st.write(Ingredients_String)
    
     
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + Ingredients_String + """','"""+ name_on_order +"""')"""

    #st.write(my_insert_stmt)
    #st.stop()
    
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

