import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import requests

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

connection_parameters = {
    "account": st.secrets["account"],
    "user": st.secrets["user"],
    "password": st.secrets["password"],
    "role": st.secrets["role"],
    "warehouse": st.secrets["warehouse"],
    "database": st.secrets["database"],
    "schema": st.secrets["schema"]
}

session = Session.builder.configs(connection_parameters).create()

my_dataframe = session.table(
    "SMOOTHIES.PUBLIC.FRUIT_OPTIONS"
).select(col("FRUIT_NAME"))

fruit_list = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:", fruit_list, max_selections=5
)

if ingredients_list:
    ingredients_string = ", ".join(ingredients_list)
    st.write("Selected:", ingredients_string)

    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
    #st.text(smoothiefroot_response.json())
    sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    if st.button("Submit Order"):
        safe_name = name_on_order.replace("'", "''")
        safe_ingredients = ingredients_string.replace("'", "''")
        insert_stmt = f"""
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
            VALUES ('{safe_ingredients}', '{safe_name}')
        """
        session.sql(insert_stmt).collect()
        st.success(
            f"Your Smoothie is ordered, {name_on_order}!", icon="✅"
        )
