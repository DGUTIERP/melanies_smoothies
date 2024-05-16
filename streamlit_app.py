# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits your want in your custom Smoothie!
    """)

title = st.text_input("Name on Smoothie: ")
st.write("The name on your Smoothie will be:", title)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingrediets_list = st.multiselect(
    'Chose up to 5 ingredients: '
    ,my_dataframe
    ,max_selections=5
)

if ingrediets_list:
    #st.write(ingrediets_list)
    #st.text(ingrediets_list)

    ingredients_string = ''
    name_on_order = title

    for fruit_chosen in ingrediets_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")
