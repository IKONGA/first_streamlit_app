import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
#streamlit.title('My Parents New Healtlhy Diner')
streamlit.title('My Mom''s New Healtlhy Diner')
#streamlit.header('Breakfast Menu')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
#fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
#fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Cantaloupe'])
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
# streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

# import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response)

# new section
streamlit.header("Fruityvice Fruit Advice!")
#--fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
#fruit_choice = streamlit.text_input('What fruit would you like information about?','Orange')
#--streamlit.write('The user entered ', fruit_choice)
#import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# streamlit.text(fruityvice_response.json()   )
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +"kiwi")
#---fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_choice)
# write your own comment -what does the next line do? 
#---fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
#---streamlit.dataframe(fruityvice_normalized)
# create the  repeatable code block(called function)

#  if not fruit_choice:
#      streamlit.error("Please select a fruit to get information.")

#      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_choice)
#      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
 #     streamlit.dataframe(fruityvice_normalized)
    
def get_fruitivice_data(this_fruit_choise):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choise)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
       streamlit.error("Please select a fruit to get information.")
  else:
        back_frum_function=get_fruitivice_data(fruit_choice)
        streamlit.dataframe(back_frum_function)

except URLError as e:
  streamlit.error()

# don't run anything past here while we troubleshoot
#streamlit.stop()

#import snowflake.connector
#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_cur.execute("SELECT * from fruit_load_list")
# my_data_row = my_cur.fetchone()
#my_data_rows = my_cur.fetchall()
# streamlit.text("Hello from Snowflake:")
# streamlit.text("The fruits load list contains")
# streamlit.header("The fruits load list contains")
streamlit.header("View Our Fruit List - Add Your Favorites!")
# streamlit.text(my_data_row)
# streamlit.dataframe(my_data_row)
#streamlit.dataframe(my_data_rows)


# Snowflake-reloated functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("SELECT * from fruit_load_list")
         return my_cur.fetchall()
#Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows=get_fruit_load_list()
   my_cnx.close()
   streamlit.dataframe(my_data_rows)

# allow end user
# add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
#add_my_fruit = streamlit.text_input('What fruit would you like to add?','Canteloupe')
#streamlit.write('Thanks to adding  ', add_my_fruit)
#my_cur.execute("insert into fruit_load_list values ('from streamlist')")

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"')")
         return "Thanks for adding " + new_fruit
    
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_funtion=insert_row_snowflake(add_my_fruit)
   my_cnx.close()
   streamlit.text(back_from_funtion)




