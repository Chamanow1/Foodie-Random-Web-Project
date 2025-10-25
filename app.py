import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AhanFromFridge",
    page_icon="❄️",
    layout="centered",
    initial_sidebar_state="auto",
)

def load_css(style_file):
    with open(style_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css("style.css")

df = pd.read_json("food.json")
All_Ingredients = set().union(*df["Ingredients"].map(dict.keys))

if "page" not in st.session_state:
    st.session_state.page = "home"
if "PickedMenu" not in st.session_state:
    st.session_state.PickedMenu = None
if "ChosenFood" not in st.session_state:
    st.session_state.ChosenFood = None
if "ShowAllMode" not in st.session_state:
    st.session_state.ShowAllMode = False
if "CookButtonClicked" not in st.session_state:
    st.session_state.CookButtonClicked = False

def HomePage():
    """This function run at home page"""
    st.title("AhanFromFridge:fried_egg:")
    st.header("มีอะไรในตู้เย็นบ้าง?") #เปลี่ยนคำได้นะ
    selected = st.multiselect("", All_Ingredients)

    filtered = df[df["Ingredients"].apply(lambda x: bool(set(selected) & set(x.keys())))]  # x เป็น Ingredients ของแต่ละเมนู

    def RandomOne():
        """This funtion run after click "Random One" button"""
        if filtered.empty:
            st.warning("อย่าลืมใส่วัตถุดิบ") #เปลี่ยนคำได้นะ
            st.session_state.ChosenFood = None
            st.session_state.ShowAllMode = False
            return
        st.session_state.ChosenFood = filtered.sample(1).iloc[0]
        st.session_state.CookButtonClicked = False
        st.session_state.ShowAllMode = False
        st.rerun()

    if st.session_state.ChosenFood is not None and not st.session_state.ShowAllMode:
        ChosenFood = st.session_state.ChosenFood
        with st.container(border=True):
            st.subheader(ChosenFood["Name"])
            st.markdown(", ".join(ChosenFood["Ingredients"]))
            if st.button("Let's Cook!"):
                st.session_state.PickedMenu = ChosenFood["Name"]
                st.session_state.page = "recipe"
                st.session_state.CookButtonClicked = True
                st.rerun()

    def ShowAll():
        """This funtion run after click "Show All" button"""
        if filtered.empty:
            st.warning("อย่าลืมใส่วัตถุดิบ") #เปลี่ยนคำได้นะ
            st.session_state.ChosenFood = None
            st.session_state.ShowAllMode = False
            return
        st.session_state.ShowAllMode = True
        st.session_state.ChosenFood = None
        st.rerun()

    if st.session_state.ShowAllMode:
        for _, menu in filtered.iterrows():
            with st.container(border=True):
                st.subheader(menu["Name"])
                st.markdown(", ".join(menu["Ingredients"]))
                if st.button(f"Let's Cook {menu['Name']}"):
                    st.session_state.PickedMenu = menu["Name"]
                    st.session_state.page = "recipe"
                    st.session_state.CookButtonClicked = True
                    st.rerun()

    if st.button("Random One"):
        RandomOne()

    if st.button(f"Show All ({len(filtered)})"):
        ShowAll()

def RecipeStep(PickedMenu):
    """This funtion run after click "Let's Cook!" button"""
    menu = df[df["Name"] == PickedMenu].iloc[0]
    st.header(menu["Name"])
    st.subheader("Ingredients")
    for ingredient in menu["Ingredients"].values():
        st.write(f"- {ingredient}")
    st.subheader("Recipe Steps")
    for i, step in enumerate(menu["Recipe"], 1):
        st.write(f"{i}. {step}")
    if st.button("Cooking Mode"):
        st.session_state.page = "cooking"
        st.rerun()
    if st.button("Back"):
        st.session_state.page = "home"
        st.session_state.PickedMenu = None
        st.session_state.ChosenFood = None
        st.session_state.ShowAllMode = False
        st.session_state.CookButtonClicked = False
        st.rerun()

def CookingMode():
    """This funtion run after click "Cooking Mode" button"""

if st.session_state.page == "home":
    HomePage()
elif st.session_state.page == "recipe":
    RecipeStep(st.session_state.PickedMenu)
elif st.session_state.page == "cooking":
    CookingMode()
