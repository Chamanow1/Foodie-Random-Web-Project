import streamlit as st
import pandas as pd
import base64


st.set_page_config(
    page_title="AhanFromFridge",
    page_icon=":fried_egg:",
    layout="centered",
    initial_sidebar_state="auto",
)

def load_css_with_bg(style_file, image_path):
    with open(image_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode()
    
    with open(style_file) as f:
        css = f.read()

    css = css.replace("REPLACE_WITH_BASE64", img_data)

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css_with_bg("style.css", "image/Food_Ingre.png")

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
        with st.container(border=True, key='containerafterrandom'):
            st.subheader(ChosenFood["Name"])
            st.markdown(", ".join(ChosenFood["Ingredients"]))
            if st.button("Let's Cook! 🡢", key="LetsCookinRandomButton"):
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
        for i, menu in filtered.iterrows():
            with st.container(border=True, key=f'containerafterall_{i}'):
                st.subheader(menu["Name"])
                st.markdown(", ".join(menu["Ingredients"]))
                if st.button(f"Let's Cook {menu['Name']}"):
                    st.session_state.PickedMenu = menu["Name"]
                    st.session_state.page = "recipe"
                    st.session_state.CookButtonClicked = True
                    st.rerun()

    if st.button("Random One", key = 'RandomOnemenu'):
        RandomOne()

    if st.button(f"Show All ({len(filtered)})", key="ShowAllButton"):
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
    menu =df[df["Name"] == st.session_state.PickedMenu].iloc[0]
    #title
    st.title(f"Cooking Mode: {menu['Name']}")
    # show picture
    if "Image" in menu:
        st.image(menu["Image"], use_container_width=True)
    if "ImageCredit" in menu:
        st.markdown(f"Credit: ({menu['ImageCredit']})")

    
    #show all ingredients
    with st.expander("show all ingredients"):
        for item in menu["Ingredients"].values():
            st.write(f"- {item}")

    #show step
    if "step_index" not in st.session_state or st.session_state.step_index is None:
        st.session_state.step_index = 0
    steps = menu["Recipe"]
    current = st.session_state.step_index
    st.subheader(f"Step {current+1}/{len(steps)}")
    st.info(steps[current])
    
    #button previous next and finish
    col1,col2 = st.columns([5, 1])
    with col1:
        if st.button("⪻ Previous", disabled=(current == 0), key='previousbutton'):
            st.session_state.step_index -= 1
            st.rerun()
    with col2:
        if current < len(steps) - 1:
            if  st.button("Next ⪼", key='nextbutton'):
                st.session_state.step_index += 1
                st.rerun()
        else:
            if st.button("Finish!", key='finishbutton'):
                st.balloons()
                st.success("You finished cooking!")

    #button home
    if st.button("🏠 Home"):
        st.session_state.page = "home"
        st.session_state.step_index = None
        st.session_state.PickedMenu = None
        st.rerun()

if st.session_state.page == "home":
    HomePage()
elif st.session_state.page == "recipe":
    RecipeStep(st.session_state.PickedMenu)
elif st.session_state.page == "cooking":
    CookingMode()
