# Citations
# [0] The dataset was taken from Kaggle
#     https://www.kaggle.com/mysarahmadbhat/nyc-traffic-accidents
# [1] Streamlit cheatsheet to learn and code this application 
#     https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py
# [2] This demo app helped me understand how to build the map view in Part 2, and I took snippets of code from it (present in map_helper.py)
#     https://github.com/streamlit/demo-uber-nyc-pickups/blob/master/streamlit_app.py
# [3] This thread was useful to add the Export to Excel functionality in Part 4 
#     https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/16

# Import external libraries
from datetime import datetime
import io
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Import required files from this repository
from constants import *
from map_helper import *

MIN_DATE = datetime(2020, 1, 1, 0, 0, 0)
MAX_DATE = datetime(2020, 8, 29, 0, 0, 0)

def list_of_values_for_attribute(df, attribute):
    attribute_df = df[(~df[attribute].isna())]
    attrs = sorted(list(set(attribute_df[attribute])))
    return attrs

@st.cache()
def load_and_clean_data():
    accidents_df = pd.read_csv("NYC Accidents 2020.csv")

    # Data Cleaning - 
    # Rename shouting all caps to more reasonable sentence-cased columns. 
    # (Maybe my personal OCD, but I don't like all caps anywhere except python constants LOL)
    accidents_df.rename(columns=str.title, inplace=True)  
    accidents_df = accidents_df[IMPORTANT_RAW_DATA_COLUMNS]

    # Augment new derived columns
    accidents_df[NUM_ACCIDENTS] = 1
    accidents_df[DATETIME] = pd.to_datetime(accidents_df[CRASH_DATE] + ' ' + accidents_df[CRASH_TIME])
    accidents_df[DAY_OF_WEEK] = accidents_df[DATETIME].dt.strftime('%A')
    accidents_df[HOUR_OF_DAY] = accidents_df[DATETIME].dt.hour
    accidents_df[MONTH] = accidents_df[DATETIME].dt.month
    accidents_df[FATAL] = (accidents_df[NUM_PEOPLE_KILLED] > 0)
    accidents_df[INJURY_CAUSING] = (accidents_df[NUM_PEOPLE_INJURED] > 0)

    def severity_level(row): 
        if row[FATAL]: 
            return "Fatal"
        elif row[INJURY_CAUSING]:
            return "Injurious"
        else: 
            return "Safe"

    accidents_df[SEVERITY] = accidents_df.apply(lambda x: severity_level(x), axis=1)
    return accidents_df

with st.spinner():
    accidents_df = load_and_clean_data()

st.title("Traffic Accidents in New York City")
st.write("""
    This interactive application is designed to help you visually explore where and how often vehicular accidents occurred 
    in the city of New York in January through August of 2020, as reported by the NYPD.
""")

# Take interactive imputs from end user
st.sidebar.markdown("""
    NOTE: The filters presented in this sidebar affect all of Parts 1-4 **_together_**. \n
    If you'd like to change only one part instead, please use the interactive controls provided _within the individual visualizations_."""
)
# DATE RANGE
date_to_datetime = lambda x: datetime.combine(x, datetime.min.time())
date_input = st.sidebar.date_input('Select Date Range', 
    value=(MIN_DATE, MAX_DATE), min_value=MIN_DATE, max_value=MAX_DATE, help="Data Availability: 1Jan20 - 29Aug20")
try: 
    start_date, end_date = date_input
except: 
    start_date, end_date = MIN_DATE, MAX_DATE
start_datetime, end_datetime = date_to_datetime(start_date), date_to_datetime(end_date)
selected_date_string = f"""Date Range: {start_datetime.strftime("%d%b%y")} - {end_date.strftime("%d%b%y")}"""

# AREA
areas = st.sidebar.multiselect('Select City Areas', list_of_values_for_attribute(accidents_df, BOROUGH), help="You can select multiple areas")
selected_areas_string = f"""Areas: {", ".join([i.title() for i in areas])}"""

# SEVERITY
selected_severities = st.sidebar.multiselect('Select Accident Severity', list_of_values_for_attribute(accidents_df, SEVERITY))

# DAYS OF WEEK
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
selected_days_of_week = st.sidebar.multiselect('Select Day of Week', days_of_week, help="You can select multiple days")

# HOUR OF ACCIDENT
start_hour, end_hour = st.sidebar.slider("Select hour range of accident", 0, 23, (0, 23))

# Build filtered dataframe based on user selected filters
filtered_df = accidents_df.copy()
filtered_df = filtered_df[(filtered_df[DATETIME] >= start_datetime) & (filtered_df[DATETIME] <= end_datetime)]
if len(areas):
    filtered_df = filtered_df[filtered_df[BOROUGH].isin(areas)]
if len(selected_severities):
    filtered_df = filtered_df[filtered_df[SEVERITY].isin(selected_severities)]
if len(selected_days_of_week):
    filtered_df = filtered_df[filtered_df[DAY_OF_WEEK].isin(selected_days_of_week)]
filtered_df = filtered_df[(filtered_df[HOUR_OF_DAY] >= start_hour) & (filtered_df[HOUR_OF_DAY] <= end_hour)]
st.markdown("---")
st.write("For your selected filters (see sidebar):")
col1, col2, col3 = st.columns((1, 1, 1))
with col1: 
    st.metric("Total Vehicular Collisions", f"{len(filtered_df):,}")
with col2: 
    num_injurious_accidents = len(filtered_df[filtered_df[SEVERITY] == "Injurious"])
    st.metric("Of which Injurious (but not Fatal)", f"{num_injurious_accidents:,}")
with col3: 
    num_fatal_accidents = len(filtered_df[filtered_df[SEVERITY] == "Fatal"])
    st.metric("Of which Fatal", f"{num_fatal_accidents:,}")    

# If there are no accidents for the selected filters, show the user an error and cleanly stop execution
if not len(filtered_df):
    st.write(f"We currently have no data for the selected filters!")
    st.stop()

# Visualizations
st.markdown("""---""")
col1, col2 = st.columns((1, 4))
with col1:
    st.header("Part 1")
with col2:
    st.header("""Seasonality and Patterns""")
st.markdown("""
    ### _When_ do vehicular collisions occur most often? 
    Let's take a look at a time series of accidents. This can help us discover seasonality and patterns in rash driving behavior. 
    You can double-click on the legend categories to isolate to accidents of that type. 
""")

col1, col2, col3 = st.columns((1, 1, 1))
with col1: 
    x_attrs = [CRASH_DATE, HOUR_OF_DAY, DAY_OF_WEEK, MONTH]
    if len(selected_days_of_week) == 1:  # No use of plotting by week if user has selected a single weekday in the common filters
        x_attrs.remove(DAY_OF_WEEK)
    if len(set(list(filtered_df[MONTH]))) == 1:
        x_attrs.remove(MONTH)
    x_attr = st.selectbox("Select x-axis: ", x_attrs)
with col2: 
    y_attr = st.selectbox("Select y-axis: ", [NUM_ACCIDENTS, NUM_PEOPLE_INJURED, NUM_PEOPLE_KILLED], key="Part1")
with col3: 
    legend_entries = ["Area", SEVERITY, "No Legend"]
    if len(areas) == 1:  # No use of categorizing by area if user has selected a single area in the common filters
        legend_entries = [SEVERITY, "No Legend"]
    if len(selected_severities) == 1:  # No use of categorizing by severity if user has selected a single severity in the common filters
        legend_entries = ["No Legend", "Area"]
    color = st.selectbox("Select legend: ", legend_entries)
    if color == "Area":
        color = BOROUGH

if color != "No Legend":
    time_series_df = filtered_df[[x_attr, y_attr, color]]
    time_series_df = time_series_df.groupby([x_attr, color]).sum().reset_index()
    if x_attr == DAY_OF_WEEK:
        time_series_df[DAY_OF_WEEK + "SORT_HELPER"] = time_series_df[DAY_OF_WEEK].apply(lambda x: WEEKDAY_SORT_KEY[x])
        time_series_df = time_series_df.sort_values([DAY_OF_WEEK + "SORT_HELPER"])
        st.plotly_chart(px.line(time_series_df, x=x_attr, y=y_attr, color=color))
    else: 
        st.plotly_chart(px.line(time_series_df, x=x_attr, y=y_attr, color=color))
else: 
    time_series_df = filtered_df[[x_attr, y_attr]]
    time_series_df = time_series_df.groupby([x_attr]).sum().reset_index()
    if x_attr == DAY_OF_WEEK:
        time_series_df[DAY_OF_WEEK + "SORT_HELPER"] = time_series_df[DAY_OF_WEEK].apply(lambda x: WEEKDAY_SORT_KEY[x])
        time_series_df = time_series_df.sort_values([DAY_OF_WEEK + "SORT_HELPER"])
        st.plotly_chart(px.line(time_series_df, x=x_attr, y=y_attr))
    else: 
        st.plotly_chart(px.line(time_series_df, x=x_attr, y=y_attr))

st.markdown("""
    #### Insights on Patterns
    The above chart answers the 'when' question in multiple ways. For instance: 
    
    1. If you select `Crash Date` or `Month` on the x-axis, we see that most accidents occur in the months of January through March, 
    which can perhaps be attributed to slippery winter roads. There is a sharp dip in the numbers in the summer months of April and May, 
    while a slight increase is seen in the higher rainfall months of June though August.

    2. Interestingly, the average `Number of Persons Injured` (select it on y-axis) is about the same in autumn months vs winter months , 
    even though almost double the accidents happen per day in windter months on average. 
    This can perhaps be attributed to lesser pedestrians and cyclists on the road in winter months.
    
    3. Pivoting the chart by `Day Of Week` shows that most accidents occur on Fridays, perhaps attributable to higher traffic and pedestrians 
    on the road coming out for parties and perhaps driving after a few drinks.

    4. Finally, selecting `Hour of Day` on x-axis shows us that most accidents occur in the afternoon, between 2-4pm. This insight can be used to enforce
    stricter traffic police patroling or speedblocks during these rush hours.
    ---
""")

# Part 2: Map
col1, col2 = st.columns((1,4))
with col1:
    st.write("## Part 2")
with col2:
    st.header("Geospatial View")
st.markdown("""
    ### _Where_ do vehicular collisions occur most often? 
    Below, you can use an interactive map view to explore on what streets and localities accidents happen most often in NYC.
    Please use the sidebar on the left to select different filters on the map. You can hover over a bar to view the number of accidents that occured in that area.
""")

# Remove the accidents we don't have a longitude and latitude for. 
# This removes about ~8% accidents (74,881 down to 68,935)
location_df = filtered_df[(~filtered_df[LONGITUDE].isna() & ~filtered_df[LATITUDE].isna())]
location_df = location_df[[CRASH_DATE, CRASH_TIME, LATITUDE, LONGITUDE, NUM_PEOPLE_INJURED, NUM_PEOPLE_KILLED]]
midpoint = (np.median(location_df[LATITUDE]), np.median(location_df[LONGITUDE]))
map(location_df, midpoint[0], midpoint[1], 11)   # \cite{[2]}
st.markdown("""
    #### Geospatial Insights
    1. We can see from the above map that accidents commonly occur on the peripheries of the city and on intersections of bridges, 
    likely due to higher average speed on broader outer circuit expressways.
    2. They are also more common in the Manhattan Wall street area, likely due to denser populations of pedestrians, cyclists, and cars all heading to or from their offices.
""")
# PART 3: Contributing factors
st.markdown("""---""")
col1, col2 = st.columns((1,4))
with col1:
    st.header("Part 3")
with col2:
    st.header("Top Contributing Factors")
st.markdown("""
    ### _What_ are the top reasons vehicular collisions happen? 
    Next, let's examine the top 10 contributing factors behind vehicular collisions in NYC. This can help answer why accidents commonly occur. 
    You can double-click on the categories in the legend to isolate to accidents of that type. \n
    And as before, you can use the sidebar on the left to select filters that apply to all parts 1 through 4. \n
""")

col1, col2, col3 = st.columns((1, 1, 1))
with col1: 
    x_attr = st.selectbox("Select x-axis: ", [VEHICLE_1_FACTOR, VEHICLE_2_FACTOR])
with col2: 
    y_attr = st.selectbox("Select y-axis: ", [NUM_ACCIDENTS, NUM_PEOPLE_INJURED, NUM_PEOPLE_KILLED], key="Part3")
with col3: 
    color = st.selectbox("Select legend: ", ["Area", SEVERITY])
    if color == "Area":
        color = BOROUGH
filter_unspecified = st.checkbox('Filter out Unspecified Contributing Factors', True)
contributing_factors_1 = list_of_values_for_attribute(accidents_df, VEHICLE_1_FACTOR)
contributing_factors_2 = list_of_values_for_attribute(accidents_df, VEHICLE_2_FACTOR)
contributing_factors = list(set(contributing_factors_1 + contributing_factors_2))
contributing_factors_df = filtered_df[filtered_df[x_attr].isin(contributing_factors)]
if filter_unspecified:
    contributing_factors_df = contributing_factors_df[contributing_factors_df[x_attr] != "Unspecified"]

top_contributing_factors = list(contributing_factors_df.groupby(
    [x_attr]).sum().reset_index().sort_values(by=[y_attr], ascending=False).head(10)[x_attr])
contributing_factors_df_with_severity = contributing_factors_df.groupby([x_attr, color]).sum().reset_index()
contributing_factors_df_with_severity = contributing_factors_df_with_severity.sort_values(by=[y_attr], ascending=False)
top_contributing_factors_df = contributing_factors_df_with_severity[
    contributing_factors_df_with_severity[x_attr].isin(top_contributing_factors)]
st.plotly_chart(px.bar(top_contributing_factors_df, x=x_attr, y=y_attr, color=color))
st.markdown("""
    #### Insights from Contributing Factors: 
    1. We see from the above chart that `Driver Inattention` comes out on top, followed by 
    `Failure to Yield Right of Way` for all areas except Manhattan. 
    2. Furthermore, isolating to Manhattan shows that it is the only area where `Following Too Closely` 
    is the second highest contributing factor. This makes intuitive sense because of a denser workforce 
    population and a higher number of pedestrians walking to office.
    3. Finally, deselecting the "Filter out Unspecified Contributing Factors" checkbox, we see that 
    often the police do not report the contributing factors in collisions. This insight can be used by 
    law enforcement agencies to strengthen onsite accident reporting.
""")
st.markdown("""---""")
# Part 4: Data Export to Excel \cite{[3]}   
col1, col2 = st.columns((1,4))
with col1:
    st.write("## Part 4")
with col2:
    st.header("""Export/Download Data""")
st.write("Below, you can download the underlying data with your selected filters to an Excel file if you'd like to.")
download = st.button("Click here to export filtered data")
export_df = filtered_df.sort_values(by=[CRASH_DATE]).reset_index().drop(columns=["index"])
export_df = export_df[OUTPUT_COLUMNS]
if download: 
    with st.spinner():
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # Write each dataframe to a different worksheet.
            export_df.to_excel(writer, index=False, sheet_name='NYC Accidents Report')

            # Close the Pandas Excel writer and output the Excel file to the buffer
            writer.save()
            st.text("File export is ready!")
            st.download_button(
                label="Click here to Download", 
                data=buffer,
                file_name="NYCAccidents.xlsx",
                mime="application/vnd.ms-excel"
            )
        download=False

st.write("Here's a small sample of the data you'll get on downloading: ")
st.dataframe(export_df.head())
