import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def checking(word,key):
    while True:
        check=input(word).strip().lower()
        if check in ['chicago', 'new york city', 'washington'] and key=='city':
            break
        elif check in ['all', 'january', 'february', 'march','april','may', 'june'] and key=='month':
            break
        elif check in [ 'all', 'monday', 'tuesday','wednesday', 'thursday','friday','saturday', 'sunday'] and key=='day':
            break
        else:
            if key=='city':
                print('Sorry, the city you choosed is not available in our City Data. Please choose one of the available cities from this list (Chicago, New York City, Washington) ')
            if key=='month':
                print("Sorry, the data for the month you choosed is not available . Please choose one of  the available months from this list('all', 'January', 'February', 'March','April','May', 'June') ")
            if key=='day':
                print("Sorry, enter the correct name of the day")
    return check

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\t\tHello! Let\'s explore some US bikeshare data!')
    print('\t Note!, You Can Enter The Words As You Want, Small Case or Upper Case ')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=checking(" Please choose The Name Of The City From The Following Cities (Chicago, New York City, Washington ) :",'city')   
    # get user input for month (all, january, february, ... , june)
    month=checking(" In which month ? (all, January, February, March, April, May, June) would you like to analysis :",'month')    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=checking("In Which day ? (all, Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday) would you like to see data about :",'day')
   
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
        df - Pandas DataFrame containing city data filtered by month and day
    """
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

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
    most_common_month=df['month'].mode()[0]
    print("The Most Common Month : ",most_common_month)

    # display the most common day of week
    most_common_day=df['day_of_week'].mode()[0]
    print("The Most Common Day of the Week :",most_common_day)

    # display the most common start hour
    most_common_start_hour=df['hour'].mode()[0]
    print("The Most Common Hour of day is :",most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station=df['Start Station'].mode()[0]
    print("The Most Common Start Station is :",start_station)

    # display most commonly used end station
    end_station=df['End Station'].mode()[0]
    print("The Most Common End Station is :",end_station)

    # display most frequent combination of start station and end station trip
    start_end=df.groupby(['Start Station','End Station'])
    start_end_station=start_end.size().sort_values(ascending =False).head(1)
    print(" the most common trip from start station to end station is :\n",start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()
    print("The Total Travel Time is :",travel_time," second.")


    # display mean travel time
    mean_travel_time=df['Trip Duration'].mean()
    print("The Average Travel Time is :",mean_travel_time," second.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type=df['User Type'].value_counts()
    print("The Number Of Each User Type is :\n",user_type)

    # Display counts of gender
    if city!="washington":
        
        gender= df['Gender'].value_counts()
        print("The Number Of Each Gender is :\n",gender)


    # Display earliest, most recent, and most common year of birth


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
