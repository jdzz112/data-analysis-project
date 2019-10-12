import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    city=input_mod('Which city do you want to explore,chicago,new york ciy or washington:\n',['chicago','new york city','washington'])
    # TO DO: get user input for month (all, january, february, ... , june)
    month=input_mod('which month do you want to explore,january, february, march, april,may or june:\n',['january', 'february', 'march', 'april', 'may', 'june','all'])
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day=input_mod('which day do you want to explore:\n',['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday'])
    
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
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['month']=df['Start Time'].dt.month
    df['day_of_week']=df['Start Time'].dt.weekday_name
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('The most frequen times of month:{}:'.format(df['month'].mode()[0]))
    # TO DO: display the most common day of week
    print('The most frequen times of day:{}'.format(df['day_of_week'].mode()[0]))
    # TO DO: display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    print('The most frequen times of hour:{}:'.format(df['hour'].mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # TO DO: display most commonly used start station
    print('The most commonly used start station:{}'.format(df['Start Station'].mode()[0]))
    # TO DO: display most commonly used end station
    print('The most commonly used end station:{}'.format(df['End Station'].mode()[0]))
    # TO DO: display most frequent combination of start station and end station trip
    df['Start_End']='Start: '+df['Start Station']+'\n End: '+df['End Station']
    print('The most frequent combination of start and end station trip:\n {}'.format(df['Start_End'].mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # TO DO: display total travel time
    print('Total travel time:%.2f min'% (df['Trip Duration'].sum()/60))
    # TO DO: display mean travel time
    print('The mean travel time:%.2f min'% (df['Trip Duration'].mean()/60))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # TO DO: Display counts of user types
    print('The counts of user types:{}'.format(df['User Type'].groupby(df['User Type']).count()))
    # TO DO: Display counts of gender
    try:
        print('The counts of gender:{}'.format(df['Gender'].groupby(df['Gender']).count()))
    except:
        print('Data missing')
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        print('The earliest year of birth:{}\n The most recent year of birth:{}\n The most common year of birth:{}'.format(df['Birth Year'].min(),df['Birth Year'].max(),df['Birth Year'].mode()))
    except:
        print('Data missing')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def input_mod(input_print,enterable_list):
    """
    input_print: information of input, enterable_list: data
    """
    while True:
        ret = input(input_print).lower()
        if ret in enterable_list:
            return ret
            break
        else:
            print('Invalid input') 
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print('Let\'s see the data head')
        print(df.head(10))
        go_on=input('Go on ? yes or no ?\n')
        if go_on.lower() != 'yes':
              break
        describe_df= input('\nWould you like to check the describe data? Enter yes or no.\n')
        if describe_df.lower() != 'yes':
            continue
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
