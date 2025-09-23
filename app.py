import streamlit as st

#อาหารกับวัตถุดิบที่ใช้
Pad_Thai = {"Flat rice noodles", "Eggs", "Garlic", "Shallots", "Dried shrimp", "Bean sprouts", "Chinese chives", "Lime"}
Tom_Yum = {"Lemongrass", "Galangal", "Kaffir lime leaves", "Chili", "Fish sauce", "Lime", "Shrimp"}

Food = [Pad_Thai, Tom_Yum]

Ingredients = set.union(*Food)

st.multiselect("What do you have in your fridge?", Ingredients)
