# 1 Goals of This Project 
A city's road transport system and traffic law enforcement are important aspects of a well-planned city where its residents can feel safe to go out on the road. Vehicular collisions often happen due to systematic reasons that can be studied and identified in advance, such that traffic police can be given these insights to prepare for mitigating and ideally preventing potential mishaps.

With this idea in mind, this interactive application allows its user to answer questions about vehicular collisions in New York with 3 different visualizations: 
- Part 1 contains a time series visualization that can interactively be modified to plot on date, day of week, hour of day, and month. It helps answer at what times of a day, or what day of a week, or what months in a year do accidents occur most often. 
- Part 2 contains a geographic map view of where accidents occur most frequently in the city of New York. This can help identify streets and intersections that need infrastructural uplifts or more traffic police patrolling.
- Part 3 answers questions about what the top contributing factors behind the accidents are using a stacked bar chart visualization. 
- Finally, Part 4 allows a user to export and download the underlying data to an Excel file should they want to do further analysis of their own.

The web application is hosted at: [https://share.streamlit.io/idsf21/assignment-2-specteross/main/app.py](https://share.streamlit.io/idsf21/assignment-2-specteross/main/app.py)

# 2 Design Choices
## 2.1 Dataset Selection Process
I chose this dataset on accidents in New York City because:
- It contained both timestamps for time series analysis and longitudes & latitudes for geospatial analsysis.
- I like driving and road transport systems, and was thus immediately interested in exploring this dataset of driving patterns in the city of New York after seeing it posted on Kaggle.

I looked at multiple other datasets as well, like Carbon Emmissions, Power Plant Energy Generation, and Covid Vaccinations, but these either didn't have both time series and location coordinate columns in the same data while I was interested in creating both visualizations, or they felt they were often studied well, both historically and in terms on other students in this class taking them up.

## 2.2 Visual Encodings Used 
### When?
For answering questions on WHEN do traffic accidents occur most frequently in New York, I used an interactive line chart as my visual encoding because it allows a user to easily observe changes in a quantity over time. 
- The chart allows multiple layers of interaction, for instance, you can zoom, pan, move around on the chart, or double click on the legend items to isolate on them. 
- The chart also allows further interaction by allowing a user to change x-axis between Crash Date, Day of Week, or Hour of Day, change y-axis to look at number of accidents, injuries, or fatalities, and change the legend to look at the data by area or by their severity level.
- Finally, the chart shows the absolute values of accidents on hovering over a bar.

### Where?
For answering questions about where collistion happen most frequently, I used an interactive cartographic map as my visual encoding because it intuitively allows a user to look at the big picture and zoom in on a particular are for a closer look as desired.
- The map allows a user to easily zoom in and out and pan around as desired. 
- The map also shows the number of accidents on hovering over a bar for clarity.

### Why? 
For answering questions on the top contributing factors behind these vehicular collisions, I used a stacked bar chart because these stacks show different areas or different severity levels (as per user's choice of legend) in different colors on a single bar for each contributing factor, thus allowing an easy visual comparison in between these categories as well as in between different contributing factors.
- As before, this chart allows zooming, panning, and isolating a single area or a set of areas or accident severity levels by simply clicking on the categories in the legend.
- This chart also allows the user to interactively select and change the x and y axes, and the legend as per their choice using the catetgorical and numerical columns available in the underlying data.

## 2.3 Other Visual Encodings Considered
I also considered the following visual encodings: 
- Using a heatmap in Part 1 for showing accidents by hour of day on one axis and crash date on the other axis, but didn't use this as variations in frequency of hour of day by date or by month is not that high. Accidents commonly occur during high traffic times like 2-5pm and not as much in the wee hours of the night like 2-5am. Thus, a time series line chart that allows viewing the data by any of date, day of week, or hour of day (as per user's choice) felt more useful.
- Using grouped bar charts instead of stacked bar charts in Part 2 for showing accidents. However, I decided stacked bar charts are more useful as I am comparing absolute numbers not percentages of different categories. For instance, in a grouped bar chart, Fatal accidents will always be a meek small bar on the side of all accidents, and it makes more sense to show them as "a part" of all accidents rather than comparing them.
- Using pie charts to display percentages of accidents of various types, which I didn't include as I made three other visualizations and didn't want to make the application too complex.

## 2.4 Data Export
I read in one of our IDS required readings (Sharing Data in Process & Provenance section of Week 5 Visualization Reading) that good data science application should allow useres to export the underlying data for their own further analysis. Hence, I  worked on adding an Export to Excel functionality that lazily exports the data when a user clicks on export, as per user selected filters on the sidebar. The process does not happen at startup and does not affect application load time.

# 3 Development Process
This was a **solo project**.

I spent ~18 hours in total on this homework.
- ~2 hours on browsing different datasets on Kaggle and data.gov and selecting this dataset
- ~12 hours on coding up this application. I am new to Streamlit so there was a bit of a learning curve. Among these 12, spent:
    - ~1 hour on reading up on Streamlit documentation and browsing it's gallery and cheatsheet \[2\], 
    - ~3 hours on the geospatial view creation \[3\] and adding the filters on the Sidebar, 
    - ~2 hours on the time series and bar plots with plotly, 
    - ~1 hour on figuring out how to cache the cleaned/processed data as the application was becoming slow without it.
    - ~2 hours on figuring out how to efficiently export data to an Excel file without hanging up the whole application (the application was freezing for ~20 seconds in my first attempt at it), 
    - and the rest on debugging various issues as they cropped up.
    
- ~2 hours on writing in-application questions and related answers/insights for all 4 parts
- ~1 hour on figuring out how to deploy the application on a public URL
- ~1 hour on giving finishing touches and writing up this README.md

Overall, I really liked the experience of this homework and I think Streamlit is an awesome library. I am surprised I didn't know about it before - I could create a web appplication this easily with just Python code. :)

## 3.1 Disclaimer: 
The application is based on vehicular collision data claimed to be reported by the New York City Police Department, made available publicly on Kaggle [\[1\]](https://www.kaggle.com/mysarahmadbhat/nyc-traffic-accidents). I, as the author of this web application, do not take guarantees for its authenticity and completeness, as that is out of scope for this project. I have studied the dataset for patterns and buiding interactive visualizations on top of it, but underlying accuracy and completeness has been assumed. That said, the insights drawn from the presented visualizations do line up with intuition on when and where accidents would be expected to happen based on factors like rush hours, busy streets, etc. which suggests that the quality of the dataset has merit and is good enough to study for the scope of this project.

## 3.2 Limitations: 
The dataset is limited to the date range of January 2020 through August 2020, as that is the full dataset found on Kaggle for this task, however, the presented visualizations do showcase a proof of concept for a longer horizon and more complete dataset.


# 4 Citations 
\[1\] The dataset was taken from [this page](https://www.kaggle.com/mysarahmadbhat/nyc-traffic-accidents) on Kaggle.\
\[2\] I used this [streamlit cheatsheet](https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py) and Streamlit API docs to learn and code up this application.\
\[3\] [This demo app](https://github.com/streamlit/demo-uber-nyc-pickups/blob/master/streamlit_app.py) helped me understand how to build the map view in Part 2, and I took snippets of code from it (present in map_helper.py).\
\[4\] [This thread](https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/16) was useful in adding the Export to Excel functionality in Part 4.\
\[5\] [Interactive Dynamics for Visual Analysis](https://canvas.cmu.edu/courses/25299/pages/reading-for-week-5-visualization?module_item_id=4937648), Week 5 Readings, IDS Fall 2021 
