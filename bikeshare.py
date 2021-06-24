import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # loop that takes user input for city
    while True:
        try:
            city = input('Would you like to see data from Chicago, New York, or Washington?\n').lower()
            if city not in ('chicago','new york', 'washington'):
                print('Please Enter a valid city\n')
            else:
                    break
        except: 
            print('Please Enter a valid city\n')


    # loop that takes user input for month
    while True:
        try:
            month = input('From wich month? January, February, March, April, May, or June? (type "all" to see data from all months)\n').lower()
            if month not in ('all','january','february','march','april','may','june'):
            
                print('Please Enter a valid month\n')
                
            else:
                   
                   break
                   
        except: 
            print('Please Enter a valid month\n')
     
    # loop that takes user input for day of week
    while True:
        try:
            day = input('From wich day of the week?(type "all" to see data from all days)\n').lower()
            if day not in ('all','sunday','monday','tuesday','wednesday','thursday','friday','saturday'):
                print('Please enter a valid day\n')
                
            else:
            
                break
                
        except: 
            print('Please Enter a valid day\n')
    
    print('-'*40)
    return city, month, day



def load_data(city, month, day):

    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_list = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = month_list [(df['month'].mode()[0]) - 1]

    # display the most common day of week
    
    popular_day = df['day_of_week'].mode()[0]
    
    # display the most common start hour
    
    df['hour'] = df['Start Time'].dt.hour
    
    popular_hour = df['hour'].mode()[0]
    
    print(' Most popular month of travel: {}\n Most popular day of travel: {}\n Most popular hour of travel: {}\n'.format(popular_month, popular_day, popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
  
  
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    fq_start = df['Start Station'].mode()[0]

    # display most commonly used end station
    fq_end = df['End Station'].mode()[0]
    
    # display most frequent combination of start station and end station trip
    fq_trip = df.groupby(['Start Station','End Station']).size().idxmax()
    
    print('The most frequent start station was: {}\nThe most frequent end station was: {}\n'.format(fq_start, fq_end))
     
    print('The most popular trip was from {} to {}'.format(fq_trip[0], fq_trip[1]))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum().round()

    # display mean travel time
    mean = df['Trip Duration'].mean().round()
    
    print('Total trip duration time was {} seconds\nAverage trip duration was: {} seconds'.format(total_time,mean))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    utypes = df['User Type'].value_counts()
    
    print(utypes)

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
    
        print('\nUsers Gender:\n',gender)
    except:
    
        print('\nNo gender data available\n')
        
    # Display oldest and youngest year of birth
    try:
        oldest = int(df['Birth Year'].min())
    
        youngest = int(df['Birth Year'].max())
    
        print('\nOldest year of birth: {}\nYoungest year of birth: {}\n'.format(oldest,youngest))
    
        #Display the most common year of birth
        frequent_year = int(df['Birth Year'].value_counts().keys().tolist()[0])
    
        times_ocurred = df['Birth Year'].value_counts().tolist()[0]
    
        print('\nMost Frequent year of birth: {}. Occurred {} times\n'.format(frequent_year, times_ocurred))
    except:
    
        print('\nNo birth year data available\n')

    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
    
def display_raw_data(df):
    """ Your docstring here """
    i = 0
    raw = input("Would you like to see raw data from the first 5 row?(type 'yes' or 'no')").lower() 
    pd.set_option('display.max_columns',200)

    while True:            
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df[i:5+i]) # TO DO: appropriately subset/slice your dataframe to display next five rows
            raw = input("Would you like to see the next 5 rows(type 'yes' or no')?").lower() # TO DO: convert the user input to lower case using lower() function
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()
            
            
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()       
            if restart == 'no':
                break
            elif restart == 'yes':
                break
            else:
                print("\nYour input is invalid. Please enter only 'yes' or 'no'\n")
            
        if restart == 'no':             
            break

if __name__ == "__main__":
	main()