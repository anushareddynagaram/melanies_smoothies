import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

connection_parameters = {
    "account": st.secrets["LDLCAKS-USB34575"],
    "user": st.secrets["ANUSHAREDDY2003"],
    "password": st.secrets["Anushareddy1234@"],
    "role": st.secrets["accountadmin"],
    "warehouse": st.secrets["compute_wh"],
    "database": st.secrets["demo_db"],
    "schema": st.secrets["public"]
}

session = Session.builder.configs(connection_parameters).create()

my_dataframe = session.table(
    "smoothies.public.fruit_options"
).select(col("FRUIT_NAME"))

fruit_list = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

if ingredients_list:

    ingredients_string = " ".join(ingredients_list)

    st.write(ingredients_string)

    if st.button("Submit Order"):

        insert_stmt = f"""
        INSERT INTO smoothies.public.orders
        (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
        """

        session.sql(insert_stmt).collect()

        st.success(
            f"Your Smoothie is ordered, {name_on_order}!",
            icon="✅"
        )
