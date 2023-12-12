import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os  
import streamlit as st

st.set_page_config(layout="wide")
st.markdown("""<style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}</style>""", unsafe_allow_html=True) 

if os.path.exists('./debt.csv'): 
    debt = pd.read_csv('debt.csv')

# ---------------------------------------------------------------------------- #
#               The Functions for the exercises are defined here.
# ---------------------------------------------------------------------------- #

# Exercise 1
debt_long = debt.melt(id_vars=['Country Name', 'Country Code', 'Series Name', 'Series Code'], var_name='Date', value_name='Debt')
debt_long.dropna(subset = 'Debt', inplace=True)
debt_long = debt_long[debt_long['Debt'] != 0]
debt_long.loc[:, 'Date'] = debt_long['Date'].str.split(' ').str[0]
debt_long.reset_index(drop=True, inplace=True)

# Exercise 2
def extract_data(country, date):
    df = debt_long[(debt_long['Country Name'] == country) & (debt_long['Date'] == date)]
    if not df.empty:
        series_mapping = {
            'Total Internal': 'DP.DOD.DECD.CR.PS.CD',
            'Total External': 'DP.DOD.DECX.CR.PS.CD',
            'Local Currency': 'DP.DOD.DECN.CR.PS.CD',
            'Foreign Currency': 'DP.DOD.DECF.CR.PS.CD',
            'Short Term Debt': 'DP.DOD.DSTC.CR.PS.CD',
            'Long Term Debt': 'DP.DOD.DLTC.CR.PS.CD'}

        dictionary = {}

        for key, series_code in series_mapping.items():
            series_data = df[df['Series Code'] == series_code]
            if not series_data.empty:
                dictionary[key] = series_data['Debt'].iloc[0]
            else:
                dictionary[key] = None
        
        return dictionary

    else:
        return {'Error': 'No data available for the selected country and date.'}

# Exercise 3
def get_countries(debt_type, date):
    df = debt_long[(debt_long['Series Code'] == debt_type) & (debt_long['Date'] == date)]
    df.dropna(subset='Debt')
    dict_countries = {}
    for index, row in df.iterrows():
        dict_countries[row['Country Name']] = row['Debt']
    if not dict_countries:
        return {'Error': 'No data available for the selected debt type and date.'}
    else:
        return dict_countries

# Exercise 4
def pie_chart_internal_external(country, date):
    df = debt_long[(debt_long['Country Name'] == country) & (debt_long['Date'] == date)]
    internal_debt_data  = df[df['Series Code'] == 'DP.DOD.DECD.CR.PS.CD']
    external_debt_data =  df[df['Series Code'] == 'DP.DOD.DECX.CR.PS.CD']

    if internal_debt_data.empty and external_debt_data.empty:
        st.error(f'No data available for Internal and External Debt for {country} in {date}.')
        return
    else:
        internal_debt = internal_debt_data['Debt'].iloc[0]
        external_debt = external_debt_data['Debt'].iloc[0]
        labels = ['Internal Debt', 'External Debt']
        sizes = [internal_debt, external_debt]

        fig, ax = plt.subplots(figsize=(6, 6))
        sns.set(style="whitegrid")
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['lightblue', 'lightcoral'])
        plt.title(f'Debt Composition for {country} in {date[:4]} in {date[-2:]}')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), shadow=True, ncol=1)
        plt.show()
        st.pyplot(fig)
        return 

# Exercise 5
def barchart_all(country, date):
    df = debt_long[(debt_long['Country Name'] == country) & (debt_long['Date'] == date)]
    if df.empty:
        st.error(f'No data available for {country} on {date}.')
        return
    else:
        sizes = df['Debt'].tolist()
        labels = df['Series Code'].tolist()
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.bar(labels, sizes, color=sns.color_palette("muted"))
        plt.title(f'Debt Composition for {country} in {date[:4]} in {date[-2:]}', fontsize=16)
        plt.xlabel('Debt Category', fontsize=12)
        plt.ylabel('Debt Amount', fontsize=12)
        plt.yscale('log')
        plt.xticks(rotation=90, ha='center', fontsize=7)
        plt.grid(axis='y', linestyle='', alpha=0.7)
        sns.despine(left=True, bottom=True)
        plt.show()
        st.pyplot(fig)
        return

# Exercise 6
def line_chart_countries(countries, debt_type):

    # Filter data for the selected countries and debt type
    debt_type_df = debt_long[debt_long['Series Code'] == debt_type]
    countries_with_debt = debt_type_df['Country Name'].tolist()

    # Check if one country form the list is in the list of countries with debt
    countries_available = [country for country in countries if country in countries_with_debt]
    if not countries_available:
        countries_str = ", ".join(countries)
        st.warning(f"No data available for the debt type {debt_type} in {countries_str}")
        return

    # Check if the selected countries are available for the selected debt type
    countries_not_available = [country for country in countries if country not in countries_with_debt]
    if countries_not_available:
        not_available_str = ', '.join(countries_not_available)
        st.warning(f"The debt type is not available for the following countries: {not_available_str}")

    fig, ax = plt.subplots(figsize=(12, 8))
    plt.title(f'Evolution of {debt_type} for {", ".join(countries)}', fontsize=16)
    sns.set(style="whitegrid")
    country_data = debt_long[(debt_long['Country Name'].isin(countries)) & debt_long['Series Code'].str.contains(debt_type)]
    sns.lineplot(x='Date', y='Debt',hue = 'Country Name', data=country_data, palette='muted')
    plt.xticks(rotation=90)
    plt.xlabel('Date')
    plt.ylabel('Debt')
    plt.yscale('log')
    plt.xlim(country_data['Date'].iloc[0], country_data['Date'].iloc[-1])
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(4))
    plt.legend()
    plt.show()
    st.pyplot(fig)

# Exercise 7
def line_chart_debt_types(country, debt_types):

    # Filter data for the selected country and debt types
    country_df = debt_long[debt_long['Country Name'] == country]
    debt_types_available = country_df['Series Code'].tolist()

    # Check if one debt type form the list is in the list of debts types with the given country
    debt_types_available = [debt_type for debt_type in debt_types if debt_type in debt_types_available]
    if not debt_types_available:
        st.warning(f"No data available for {country} and the debt types {debt_types_str}")
        return

    # Check if the selected debt types are available for the selected country
    debt_types_not_available = [debt_type for debt_type in debt_types if debt_type not in debt_types_available]
    if debt_types_not_available:
        not_available_str = ', '.join(debt_types_not_available)
        st.warning(f"{country} does not have the following debt types: {not_available_str}")

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.set(style="whitegrid")
    plt.title(f'Evolution of Debt Types for {country}', fontsize=16)
    country_data = debt_long[(debt_long['Country Name'] == country) & debt_long['Series Code'].isin(debt_types)]
    sns.lineplot(x='Date', y='Debt', hue='Series Code', data=country_data, palette='muted')
    plt.xticks(rotation=90)
    plt.xlabel('Date')
    plt.ylabel('Debt')
    plt.yscale('log')
    plt.xlim(country_data['Date'].iloc[0], country_data['Date'].iloc[-1])
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(4))
    plt.legend(title='Debt Types')
    plt.show()
    st.pyplot(fig)

# Exercise 8
def box_plot_countries(countries, debt_types):

    # Get unique countries and debt types in the entire DataFrame, for the selected other value
    debt_df = debt_long[debt_long['Country Name'].isin(countries)]
    country_df = debt_long[debt_long['Series Code'].isin(debt_types)]
    available_countries = country_df['Country Name'].unique()
    available_debt = debt_long['Series Code'].unique()

    # Check if there are selected countries or debt types that do not have a match in the DataFrame
    missing_countries = [country for country in countries if country not in available_countries]
    missing_debt_types = [debt_type for debt_type in debt_types if debt_type not in available_debt]

    # Check if there is data available for the selected debt types and countries
    filtered_data = debt_long[(debt_long['Country Name'].isin(countries)) & (debt_long['Series Code'].isin(debt_types))]
    if filtered_data.empty:
        countries_str = ', '.join(countries)
        debt_types_str = ', '.join(debt_types)
        st.warning(f"The combination of {countries_str} and {debt_types_str} does not have any data available.")
        return

    # Optionally, you can display a warning message for missing countries or debt types
    if missing_countries:
        missing_countries_str = ', '.join(missing_countries)
        st.warning(f"The following countries are not in the data: {missing_countries_str}")
    if missing_debt_types:
        missing_debt_types_str = ', '.join(missing_debt_types)
        st.warning(f"The following debt types are not in the data: {missing_debt_types_str}")

    fig, ax = plt.subplots(figsize=(12, 8))
    plt.title(f'Box Plot of Debt for {", ".join(countries)}', fontsize=16)
    sns.boxplot(x='Country Name', y='Debt', hue='Series Code', data=filtered_data, palette='muted')
    plt.xlabel('Country')
    plt.ylabel('Debt')
    plt.yscale('log')
    plt.legend(title='Debt Type')
    plt.show()
    st.pyplot(fig)



# ---------------------------------------------------------------------------- #
#       The following Code provides a Streamlit interface for the project.
#                       Every exercise gets a seperate page.
# ---------------------------------------------------------------------------- #



# Set the page layout
st.markdown(
    """
    <style>
        .sidebar-image {
            position: absolute;
            top: -4rem;
            left: 2rem;
            max-height: 100px;
            max-width: 100px;
        }
        span[data-baseweb="tag"] {
            background-color: grey !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
with st.sidebar:
    st.markdown(
        """
        <img class="sidebar-image" src="https://s3-us-west-2.amazonaws.com/lcdevelopment/c7f416/site_files/bac608ef2e_national-debt-icon.png" alt="Sidebar Image">
        """,
        unsafe_allow_html=True,
    )    
    
    st.title("Goverment Debt")
    choice = st.radio("Navigation", ['Exercise 1', 'Exercise 2', 'Exercise 3', 'Exercise 4', 'Exercise 5', 'Exercise 6', 'Exercise 7', 'Exercise 8'])
    st.info("This project displayes govermental debt.")




# Create the pages for the different exercises#
if choice == 'Exercise 1':
    st.subheader("Exercise 1")
    # Display Exercise 1 result
    st.write(debt_long)
    
if choice == 'Exercise 2':
    st.subheader("Exercise 2")
    # Get countries
    unique_countries = debt_long['Country Name'].unique()
    country_input = st.selectbox("Select country:", unique_countries)
    # Get dates
    unique_dates_for_country = debt_long[debt_long['Country Name'] == country_input]['Date'].unique()
    date_input = st.selectbox("Select date:", unique_dates_for_country)
    # Display Exercise 2 result
    result = extract_data(country_input, date_input)
    if 'error' in result:
        st.error(result['error'])
    else:
        st.write(result)

if choice == 'Exercise 3':
    st.subheader("Exercise 3")
    # Get countries
    unique_debt_type = debt_long['Series Code'].unique()
    debt_type = st.selectbox("Select Debt Type:", unique_debt_type)
    # Get dates
    unique_dates_for_debt = debt_long[debt_long['Series Code'] == debt_type]['Date'].unique()
    date_input = st.selectbox("Select date:", unique_dates_for_debt)
    # Display Exercise 3 result
    result = get_countries(debt_type, date_input)
    st.write(result)

# Exercise 4
if choice == 'Exercise 4':
    st.subheader("Exercise 4")
    # Get  countries
    unique_countries = debt_long['Country Name'].unique()
    country_input = st.selectbox("Select Country:", unique_countries)
    # Get unique dates for the selected country
    unique_dates_for_country = debt_long[debt_long['Country Name'] == country_input]['Date'].unique()
    date_input = st.selectbox("Select date:", unique_dates_for_country)
    # Display Exercise 4 result
    pie_chart_internal_external(country_input, date_input)



if choice == 'Exercise 5':
    st.subheader("Exercise 5")
    # Get  countries
    unique_countries = debt_long['Country Name'].unique()
    country_input = st.selectbox("Select Country:", unique_countries)
    # Get unique dates for the selected country
    unique_dates_for_country = debt_long[debt_long['Country Name'] == country_input]['Date'].unique()
    date_input = st.selectbox("Select date:", unique_dates_for_country)
    # Display Exercise 5 result
    barchart_all(country_input, date_input)


if choice == 'Exercise 6':
    st.subheader("Exercise 6")
    # Get countries
    unique_countries = debt_long['Country Name'].unique()
    default_countries = ['Australia']
    countries_list = st.multiselect("Select countries:", unique_countries, default=default_countries)
    # Get debt with available data for at least one of the selected countries
    countries_df = debt_long[debt_long['Country Name'].isin(countries_list)]
    available_debt_types = countries_df['Series Code'].unique()
    debt_type_input = st.selectbox("Select debt type:", available_debt_types, index=0)
    # Display Exercise 6 result
    line_chart_countries(countries_list, debt_type_input)



if choice == 'Exercise 7':
    st.subheader("Exercise 7")
    # Get debt
    unique_debt_type = debt_long['Series Code'].unique()
    default_debt = ['DP.DOD.DECD.CR.PS.CD']
    debt_types_list = st.multiselect("Select debt:", unique_debt_type, default=default_debt)
    # Get countries with available data for at least one of the selected debt types
    countries_df = debt_long[debt_long['Series Code'].isin(debt_types_list)]
    available_contries = countries_df['Country Name'].unique()
    country_input = st.selectbox("Select Country:", available_contries, index=0)
    # Display Exercise 7 result
    line_chart_debt_types(country_input, debt_types_list)


if choice == 'Exercise 8':
    st.subheader("Exercise 8")
    # Get countries
    unique_countries = debt_long['Country Name'].unique()
    default_countries = ['Australia']
    countries_list = st.multiselect("Select countries:", unique_countries, default=default_countries)
    # Get debt with available data for at least one of the selected countries
    countries_df = debt_long[debt_long['Country Name'].isin(countries_list)]
    available_debt_types = countries_df['Series Code'].unique()
    default_debt = available_debt_types[0]
    debt_types_list = st.multiselect("Select debt:", available_debt_types, default=default_debt)
    # Display Exercise 8 result
    box_plot_countries(countries_list, debt_types_list)


