import time
import pandas as pd
import numpy as np


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = str(input("Please enter the city of interest: Chicago, New York City, Washington: \n")).lower()
    while (city.lower() != 'chicago') and (city.lower() != 'new york city') and (city.lower() != 'washington'):
        city = input("Please choose your city among Chicago, New York city or Washington: \n").lower()
    print('\n You have chosen', city)
    print('-' * 10)

    # get user input for month (all, january, february, ... , june)
    month = str(input("Please choose the month of interest: January, February, March, April, May, June "
                      "or All \n")).lower()
    while (month.lower() != 'january') and (month.lower() != 'february') and (month.lower() != 'march') and \
            (month.lower() != 'april') and (month.lower() != 'may') and (month.lower() != 'june') and \
            (month.lower() != 'all'):
        month = input("Please enter a valid month from January to June or All, please write the full word: \n").lower()
    print('\n You have chosen', month)
    print('-' * 10)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = str(input("Choose the day of the week: Monday, Tuesday, Wednesday, Thursday, Friday or All \n")).lower()
    while (day.lower() != 'monday') and (day.lower() != 'tuesday') and (day.lower() != 'wednesday') and (
            day.lower() != 'thursday') and (day.lower() != 'friday') and (
            day.lower() != 'all'):
        day = input("Please enter a valid day of week from monday to sunday or All, please write the full "
                    "word \n").lower()
    print('\n You have chosen', day)

    print('-' * 40)
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
    df = pd.read_csv(CITY_DATA[city])

    # make month and day seprate from start time column
    df['month'] = pd.to_datetime(df['Start Time']).dt.month_name()
    if month != 'all':
        df = df.loc[df['month'] == month.title()]

    df['day'] = pd.to_datetime(df['Start Time']).dt.day_name()

    if day != 'all':
        df = df.loc[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    mode_month = df['month'].mode()
    print('The most common month:', mode_month[0])

    # display the most common day of week
    mode_day = df['day'].mode()
    print('The most common day:', mode_day[0])

    # display the most common start hour
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    mode_hour = df['hour'].mode()
    print('The most common start hour:', mode_hour[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mode_start_station = df['Start Station'].mode()
    print('The most common start station:', mode_start_station[0])

    # display most commonly used end station
    mode_end_station = df['End Station'].mode()
    print('The most common end station:', mode_end_station[0])

    # display most frequent combination of start station and end station trip
    mode_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('The most frequent combination of start to end station:', mode_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    total_travel_time = time.strftime("%H:%M:%S", time.gmtime(total_travel))
    print('The total travel time (HH:mm:ss):', total_travel_time)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    mean_travel_time = time.strftime("%H:%M:%S", time.gmtime(mean_travel))
    print('The average travel time (HH:mm:ss):', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user = df['User Type'].value_counts(ascending=True).to_frame()
    print('The users type is as follows:\n', count_user)

    # Display counts of gender
    if (city == 'chicago') or (city == 'new york city'):
        count_gender = df['Gender'].value_counts(ascending=True).to_frame()
        print('The distribution of gender is as follows:\n', count_gender)
    else:
        print('Unfortunately Washington city doesn\'t have information about gender')

    # Display earliest, most recent, and most common year of birth
    if (city == 'chicago') or (city == 'new york city'):
        min_birth = int(df['Birth Year'].min())
        max_birth = int(df['Birth Year'].max())
        mean_birth = int(df['Birth Year'].mode()[0])
        print('The earliest year of birth is', min_birth, '\nThe most recent year of birth is:', max_birth,
              '\nThe most common year of birth is:', mean_birth)
    else:
        print('Unfortunately Washington city doesn\'t have information about year of birth')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """
    Request for seeing raw data. Possibility of showing 5 full rows each time.
    #x = pd.read_csv('./chicago.csv')
    #y = pd.read_csv('./new_york_city.csv')
    #z = pd.read_csv('./washington.csv')
    """
    row_count = df.shape[0]

    raw_material = str(input('\nWould you like to see the first 5 row of raw material according to your city, month and'
                             ' day filter? Enter Yes or No.\n')).lower()
    if raw_material.lower() == 'yes':
        pd.options.display.max_columns = 1000
        print(df.head())
        for i in range(10, row_count, 5):
            raw_material_new = input('\nWould you like to see the next 5 row? Enter Yes or No.\n')
            if raw_material_new.lower() == 'yes':
                pd.options.display.max_columns = 1000
                print(df[i-5:i])
            elif raw_material.lower() == 'no':
                print('Sure, we move on!')
            else:
                print('Not a valid input')
                break

    elif raw_material.lower() == 'no':
        print('Sure, we move on!')
    else:
        print('Not a valid input')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print ('you have entered No or invalid input')
            break


if __name__ == "__main__":
    main()
