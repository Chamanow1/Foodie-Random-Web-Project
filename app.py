import streamlit as st
import pandas as pd

st.set_page_config(page_title="CheckWatthudip", page_icon=":pizza:")

df = pd.read_csv("FileFood.csv")
def change_ingredients(s): 
    '''Ingredients string to dict'''
    items = s.split(",") 
    Ingre_dict = {}
    for i in items:
        parts = i.split(":",1)
        key = parts[0].strip()
        value = parts[1].strip()
        Ingre_dict[key] = value
    return Ingre_dict
df["Ingredients_dict"] = df["Ingredients"].apply(change_ingredients) # make new column and Ingredients string to dict
df["Recipe_list"] = df["Recipe"].apply(lambda s: [step.strip() for step in s.split("|")]) # make new column and Recipe string to list

#all ingredients
All_Ingredients = set()
for d in df["Ingredients_dict"]:
    All_Ingredients.update(d.keys())

st.title("CheckWatthudip")
st.header("มีอะไรในตู้เย็นบ้าง?")
selected = st.multiselect("", All_Ingredients)

filtered = df[df["Ingredients_dict"].apply(lambda x: bool(set(selected) & set(x.keys())))] # x เป็น Ingredients ของแต่งละเมนู

def RecipeStep(PickedMenu):
    """This funtion run after click Let's Cook! button"""
    menu = df[df["Name"] == PickedMenu].iloc[0]
    st.header(menu["Name"])
    st.subheader("Ingredients")
    for ingredient, qty in menu["Ingredients_dict"].items():
        st.write(f"- {ingredient}:{qty}")
    st.subheader("Recipe Steps")
    for i, step in enumerate(menu["Recipe_list"], 1):
        st.write(f"{i}. {step}")
    #ไม่รู้ทำไมไม่ขึ้น

def RandomOne():
    """This funtion run after click Random One button"""
    if filtered.empty:
        st.warning("No menu matches your ingredients.")
        return
    random_food = filtered.sample(1).iloc[0]
    with st.container(border=True):
        st.write(random_food["Name"])
        st.markdown("  \n".join([f"{k}:{v}"for k,v in random_food["Ingredients_dict"].items()]))
        if st.button("Let's Cook!"):
            RecipeStep(random_food["Name"])

def ShowAll():
    """This funtion run after click Show All button"""
    #ยังไม่ได้ทำ

if st.button("Random One"):
    RandomOne()
if st.button("Show All"):
    ShowAll()
