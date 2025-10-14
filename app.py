import streamlit as st
import pandas as pd

st.set_page_config(page_title="CheckWatthudip", page_icon=":pizza:")

df = pd.read_json("food.json")
All_Ingredients = set().union(*df["Ingredients"].map(dict.keys))

st.title("CheckWatthudip")
st.header("มีอะไรในตู้เย็นบ้าง?")
selected = st.multiselect("", All_Ingredients)

filtered = df[df["Ingredients"].apply(lambda x: bool(set(selected) & set(x.keys())))] # x เป็น Ingredients ของแต่งละเมนู

def RecipeStep(PickedMenu):
    """This funtion run after click Let's Cook! button"""
    menu = df[df["Name"] == PickedMenu].iloc[0]
    st.header(menu["Name"])
    st.subheader("Ingredients")
    for ingredient in menu["Ingredients"].values():
        st.write(f"- {ingredient}")
    st.subheader("Recipe Steps")
    for i, step in enumerate(menu["Recipe"], 1):
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
        st.markdown("  \n".join(random_food["Ingredients"].values()))
        if st.button("Let's Cook!"):
            RecipeStep(random_food["Name"])

def ShowAll():
    """This funtion run after click Show All button"""
    #ยังไม่ได้ทำ

if st.button("Random One"):
    RandomOne()
if st.button("Show All"):
    ShowAll()