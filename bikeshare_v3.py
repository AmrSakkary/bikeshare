import time
import pandas as pd
import numpy as np

#Global data
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_dict={'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6, 'all':""}
day_dict={'mon':0,'tue':1,'wed':2,'thu':3,'fri':4,'sat':5,'sun':6, 'all':""}

# A function to change the month value to month name for a better raw data view
def change_month_value(month):
    for key,value in month_dict.items():
        if month == value:
            month_name=key.title()
            return month_name
# A function to change the day value to day name for a better raw data view
def change_day_value(day):
    for key,value in day_dict.items():
        if day == value:
            day_name=key.title()
            return day_name

# A function to extract the days,hours,minutes and seconds based on a given number expresses the number of seconds
def get_time(total_time):
    """Loads time number in seconds.

    Args:
        (int) total_time - a variable contains a number that expresses the number of seconds.
    Returns:
        tot_days -  the number of days available on the total time.
        rem_hours - the number of remaining days available on the total time after calculating total days.
        rem_min -   the number of remaining minutes available on the total time after calculating total days and remaining hours.
        rem_sec -   the number of remaining seconds available on the total time after calculating total days, remaining hours, and remaining minutes.
    """
    # Total Days in the total time
    tot_days=int(total_time/24/60/60)
    
    # Remaining Hours
    rem_hours=int(((total_time/60/60/24)-tot_days)*24)
    
    # Remaining Minutes
    rem_min=(total_time//60)%60
    
    # Remaining Seconds
    rem_sec=total_time%60
    
    return tot_days,rem_hours,rem_min,rem_sec


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    #city - name of the city to analyze
    print('Hello! Let\'s explore some US bikeshare data!\n')
    while True:
        print("We provide data for three cites (New York City), (Washington), and (Chicago)\n")
        print("If you want info about New York city enter (ny)\nIf you want info about Washington city enter (wa)\nIf you want Chicago city enter (ch) \n ")
        c=(input("Kindly enter your preferred city: ")).lower()
        print()
        if c == "ny":
            city=CITY_DATA['new york city']
            break
        elif c == "ch":
            city=CITY_DATA['chicago']
            break
        elif c == "wa":
            city=CITY_DATA['washington']
            break
        else:
            print("Please enter a valid city input\n")
#     month - name of the month to filter by, or "all" to apply no month filter
    while True:
        print("We provide data of the first six months of the year\n")
        m=(input("Kindly enter your preferred month full name or first three letters or enter (all) if you want full months data: ")).lower()
        print()
        if m in month_dict or m[0:3] in month_dict or m.lower()== 'all':
            month=m[:3]
            break
        else:
            print('Please enter a valid month name\n')
    #name of the day to analyze
    while True:
        d=(input("Kindly enter your preferred day full name or first three letters or enter (all) if you want full days data: ")).lower()
        if d in day_dict or d[:3] in day_dict or d== 'all':
            day=d[:3]
            break
        else:
            print('Please enter a valid day name\n')
    print('-'*40)
    return city,month,day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df=pd.read_csv(city)

    
    #rename first column to ID
    df=df.rename(columns={'Unnamed: 0':'Trip Code'})
    
    #changing (Start Time) column type to datetime
    df['Start Time']=pd.to_datetime(df['Start Time'])
    
    #creating (Month) column
    df['Month']=df['Start Time'].dt.month
    
    
    #creating (Day) column
    df['Day']=df['Start Time'].dt.weekday
    
    #creating (Hour) column
    df['Hour']=df['Start Time'].dt.hour
    
    #filter with months
    if month != "":
        df=df[df["Month"]==month]
    else:
        df=df
      
    #filter with days
    if day != "":
        df=df[df["Day"]==day]
        
    #changing the month value to month name for a better raw data view
    df['Month']=df['Month'].apply(lambda x:change_month_value(x))
    
    #changing the day value to day name for a better raw data view
    df['Day']=df['Day'].apply(lambda x:change_day_value(x))
    


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # most common month
    most_c_month=df['Month'].mode()[0]
    m_count=df[df['Month']==df['Month'].mode()[0]]['Month'].count()
    print("most common month is: {} ,and occurred with count of: {}".format(most_c_month,m_count))
    
    # most common day of week
    most_c_day=df['Day'].mode()[0]
    d_count=df[df['Day']==df['Day'].mode()[0]]['Day'].count()
    print("most common day is: {} ,and occurred with count of: {}".format(most_c_day,d_count))
    
    # most common hour of day
    most_c_hour=df['Hour'].mode()[0]
    h_count=df[df['Hour']==df['Hour'].mode()[0]]['Hour'].count()
    print("most common hour is: {} ,and occurred with count of: {}".format(most_c_hour,h_count))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # most common Start Station
    most_c_s_station=df['Start Station'].mode()[0]
    s_count=df[df['Start Station']==df['Start Station'].mode()[0]]['Start Station'].count()
    print("Most common start station is: ({}), and occurred with count of: {}".format(most_c_s_station,s_count))
    
    # most common End Station
    most_c_e_station=df['End Station'].mode()[0]
    e_count=df[df['End Station']==df['End Station'].mode()[0]]['End Station'].count()
    print("Most common end station is: ({}) ,and occurred with count of: {}".format(most_c_e_station,e_count))
    
    # most common trip from start to end (i.e., most frequent combination of start station and end station)
    #creating a column that contains start and end stations together 
    df['Start_to_end']= '('+df['Start Station'] +') And ('+ df['End Station'] + ')'
    
    most_c_se_station=df['Start_to_end'].mode()[0]
    se_count=df[df['Start_to_end']==df['Start_to_end'].mode()[0]]['Start_to_end'].count()
    print("Most common Start to End Station is: {}, and occurred with count of: {}".format(most_c_se_station,se_count))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Total travel time
    total_time=df['Trip Duration'].sum()
    
    #Extracting days, hours, minutes, and seconds in total_time var
    tot_days,rem_hours,rem_min,rem_sec= get_time(total_time)
    
    # Average travel time
    avg_time=df['Trip Duration'].mean()
    
    #Extracting days, hours, minutes, and seconds in avg_time var
    avg_days,avg_rem_hours,avg_rem_min,avg_rem_sec= get_time(avg_time)
    
#     print('Total trip duration is: {}, with average of: {}'. format(total_time,avg_time))

    print("Total trip duration is {} Days, {} Hours, {} Minutes, and {} Seconds.\n".format(tot_days,rem_hours,rem_min,rem_sec))
    
    print("Average trip duration is {} Days, {} Hours, {} Minutes, and {} Seconds.".format(avg_days,avg_rem_hours,avg_rem_min,avg_rem_sec))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    users_count=df['User Type'].value_counts()
    print('Count of each user type\n')
    print(users_count,"\n")
    
    if city == 'chicago.csv' or city == 'new_york_city.csv':
        
        # counts of each gender (only available for NYC and Chicago)
        gender_count=df['Gender'].value_counts()
        
        print('Count of each user gender\n')
        print(gender_count,"\n")
        
        # earliest year of birth
        old=df['Birth Year'].min()
        
        # most recent year of birth
        young=df['Birth Year'].max()
        
        # most common year of birth
        common=df['Birth Year'].mode()[0]
        
        print('Earliest year of birth is: {}, most recent year of birth is: {}, and most common year of birth is: {}'.format(old,young,common))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_more_data(df):

	"""Displays raw data based on user request."""

	start=0
	end=5
	get_raw=input("Do you want to see some raw data? Enter yes or no.\n")
	if get_raw.lower() == 'yes':
		while True:
			print(df.iloc[start:end])
			start=end
			end+=5
			get_more=input("Do you want to more raw data? Enter yes or no.\n")
			print()
			if get_more.lower() != 'yes':
			    break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month_dict[month], day_dict[day])
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        get_more_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
