#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 12:17:00 2021

@author: emicervantes
"""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# import peter's image
from PIL import Image
image = Image.open('anteater.jpg')

# 1. Show app's title
st.title("Peter's Data Plot")

# 2. Group members' names and thier link to GitHub
st.markdown("Emi Cervantes: [Github Link](https://github.com/emicervantes?tab=repositories)")
st.markdown("Grace Lee: [Github Link](https://github.com/GraceLeeUCI?tab=repositories)")
st.markdown("Yuzhen Lang [Github Link](https://github.com/Langyuzhen?tab=repositories)")

# 3. File uploader widget
# forcing the file to have extension csv
file  = st.file_uploader(label = "Upload file", type = 'csv')

st.image(image)


# 4. Make a pandas DataFrame from the file   
# show an error if there is no file 
if file is not None:
    df = pd.read_csv(file)
    
    
    # 5. using applymap and lambda, replace alls tring entries consisting blank
    # with Numpy's not-a-number
    df = df.applymap(lambda x: np.nan if x == " " else x) #question 5
    
    # 6. using list comprehension, make a list containing the names of all 
    # columns of the DataFrame which can be made numeric
    def can_be_numeric(c):
        try:
            pd.to_numeric(df[c])
            return True
        except:
            return False
        
    # make a lit of all the columns tht can be made numeric
    good_cols = [c for c in df.columns if can_be_numeric(c)]
    

    # 7. replace dataframe with another version, where all those columns are
    # made numeric 
    df[good_cols] = df[good_cols].apply(pd.to_numeric, axis = 0)
    
    # 8. use st.selectbox to let the user choose any numeric column for the 
    # x-axis and y-axis
    x_axis = st.selectbox("Choose an X-value", good_cols)
    y_axis = st.selectbox("Choose a Y-value", good_cols)
    
    # 9. use the range slider version of st.slider to allow the user to select 
    # the rows they want plotted. 
    # Have the minimum be 0 and the maximum be the number of rows in the file
    rows = st.slider("Choose the range ", min_value = 0, max_value = len(df.index)-1)
    
    # 10. Use f-string and st.write to display some information about the 
    # chosen data
    st.write("You chose: ")
    st.write()
    st.write(f"X axis: {x_axis}")
    st.write(f"Y-axis: {y_axis}")
    st.write(f"Rows range: 0 ~ {rows}")
    
    # 11.  Use st.altair_chart to display the chart with the chosen x-axis,
    # y-axis, and rows
    chart = alt.Chart(df.loc[0:rows,:]).mark_circle().encode(
        x = x_axis,
        y = y_axis  
    )
    
    st.altair_chart(chart, use_container_width=True)


    # 12. Include at least one extra element in the app
    # picture in the beginning

else:
    st.write("Peter wants to see your data! Give him a csv file!!")
