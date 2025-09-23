import streamlit as st

Food = {
    "Pad Thai": {"Flat rice noodles", "Eggs", "Garlic", "Shallots", 
                 "Dried shrimp", "Bean sprouts", "Chinese chives", "Lime"},
    "Tom Yum": {"Lemongrass", "Galangal", "Kaffir lime leaves", 
                "Chili", "Fish sauce", "Lime", "Shrimp"}
}

Ingredients = set.union(*Food.values())

st.title("เช็ควัตถุดิบ")
st.subheader("What do you have in your fridge?")

selected = st.multiselect("", Ingredients)

if selected:
    for name, ingredients in Food.items():
        if set(selected) & ingredients:
            st.write(name)
