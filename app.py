import streamlit as st
import pandas as pd

st.set_page_config(page_title="CheckWatthudip", page_icon=":pizza:")

Food = [
    {"Name":"แกงฮังเล",
     "Ingredients":{"เนื้อหมู":"เนื้อหมู 1000 กรัม", "พริกแกงฮังเล":"พริกแกงฮังเล 3-5 ช้อนโต๊ะ (ถ้าไม่มี พอใช้น้ำพริกแกงเผ็ด แทนได้)",
                    "ผงฮังเล":"ผงฮังเล 1-2 ช้อนโต๊ะ (ถ้าไม่มี พอใช้ผงกะหรี่แทนได้)", "ซิอิ๊วดำ":"ซิอิ๊วดำ 1 ช้อนโต๊ะ",
                    "น้ำตาลปี๊บ":"น้ำตาลปี๊บ 2 ช้อนโต๊ะ", "น้ำปลา":"น้ำปลา 2 ช้อนโต๊ะ", "น้ำมะขามเปียก":"น้ำมะขามเปียก 2-4 ช้อนโต๊ะ",
                    "ขิงซอย":"ขิงซอย 1/2 ถ้วย", "กระเทียมโทนดอง":"กระเทียมโทนดอง 2 ช้อนโต๊ะ", "ถั่วลิสงคั่ว":"ถั่วลิสงคั่ว 2 ช้อนโต๊ะ"},
     "Recipe":["หมักหมู โดยนำหมูที่หั่นเตรียมไว้ ผสมกับพริกแกงฮังเล และซิอิ๊วดำ คลุกเข้ากันให้ทั่ว หมักทิ้งไว้ 1 ชั่วโมง",
               "ตั้งน้ำมันในกระทะบนไฟร้อนปานกลาง ใส่เนื้อหมูที่หมักไว้ลงไปผัด พอให้ผิวด้านนอกสุก จากนั้นจึงใส่น้ำเปล่าลงไปพอท่วม คนให้ส่วนผสมเข้ากัน และเคี่ยวด้วยไฟอ่อนทิ้งไว้อย่างน้อย 1 ชั่วโมง หมั่นคนเรื่อยๆระหว่างเคี่ยว ถ้าน้ำแห้งสามารถเติมน้ำเพิ่มได้",
               "เมื่อเเคี่ยวจนครบหนึ่งชั่วโมง หรือเนื้อหมูนุ่มดีแล้ว ปรุงรสด้วยน้ำตาลมะพร้าว, น้ำมะขามเปียก และน้ำปลา จากนั้นจึงใส่ขิงซอย, กระเทียมโทน และถั่วลิสงคั่ว",
               "คนให้ส่วนผสมเข้ากัน และเคี่ยวต่อไปอีกสักพัก จึงปิดไฟ ตักใส่ถ้วยและเสิร์ฟ"]},  
]

df = pd.DataFrame(Food)

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
