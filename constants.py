# Column Names 
# Dataset columns
CRASH_ID = 'Collision_Id'
CRASH_DATE = 'Crash Date'
CRASH_TIME = 'Crash Time'
BOROUGH = 'Borough'
LATITUDE = 'Latitude'
LONGITUDE = 'Longitude'
ZIP_CODE = 'Zip Code'
ON_STREET = 'On Street Name'
CROSS_STREET = 'Cross Street Name'
OFF_STREET = 'Off Street Name'
NUM_PEOPLE_INJURED = 'Number Of Persons Injured'
NUM_PEOPLE_KILLED = 'Number Of Persons Killed' 
VEHICLE_1_FACTOR = 'Contributing Factor Vehicle 1'
VEHICLE_2_FACTOR = 'Contributing Factor Vehicle 2'
VEHICLE_1_TYPE = 'Vehicle Type Code 1' 
VEHICLE_2_TYPE = 'Vehicle Type Code 2'

# Derived columns
DATETIME = "Crash_Datetime"
DAY_OF_WEEK = "Day Of Week"
MONTH = "Month"
HOUR_OF_DAY = "Crash Time (Hour Of Day)"
FATAL = "Fatal"
INJURY_CAUSING = "Injurious"
SEVERITY = "Severity"
NUM_ACCIDENTS = "Number of Accidents"

IMPORTANT_RAW_DATA_COLUMNS = [
    CRASH_DATE, CRASH_TIME, LATITUDE, LONGITUDE, ZIP_CODE, 
    BOROUGH, ON_STREET, CROSS_STREET, OFF_STREET, 
    NUM_PEOPLE_INJURED, NUM_PEOPLE_KILLED, 
    VEHICLE_1_FACTOR, VEHICLE_2_FACTOR, 
    VEHICLE_1_TYPE, VEHICLE_2_TYPE, 
    CRASH_ID
]
OUTPUT_COLUMNS = [
    CRASH_DATE, CRASH_TIME, MONTH, DAY_OF_WEEK, HOUR_OF_DAY, LATITUDE, LONGITUDE, 
    SEVERITY, NUM_ACCIDENTS, NUM_PEOPLE_INJURED, NUM_PEOPLE_KILLED, 
    BOROUGH, ZIP_CODE, ON_STREET, CROSS_STREET, OFF_STREET, 
    VEHICLE_1_FACTOR, VEHICLE_2_FACTOR, VEHICLE_1_TYPE, VEHICLE_2_TYPE, 
    CRASH_ID
]

WEEKDAY_SORT_KEY = {  # to fix sort order for weekdays in the time series chart
    "Monday": 0, 
    "Tuesday": 1, 
    "Wednesday": 2, 
    "Thursday": 3, 
    "Friday": 4, 
    "Saturday": 5, 
    "Sunday": 6, 
}