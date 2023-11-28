import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os  
import streamlit as st

st.set_page_config(layout="wide")
st.markdown("""<style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}</style>""", unsafe_allow_html=True) 

if os.path.exists('./debt.csv'): 
    df = pd.read_csv('debt.csv', index_col=None)

########################################
# The Functions for the exercises are defined here.
########################################

# Exercise 1
debt_long = df.melt(id_vars=['Country Name', 'Country Code', 'Series Name', 'Series Code'], var_name='Date', value_name='Debt')
debt_long = debt_long.dropna(subset = 'Debt')
debt_long.loc[:, 'Date'] = debt_long['Date'].str.split(' ').str[0]
debt_long.reset_index(drop=True, inplace=True)
# TODO More cleaning needed?

# Exercise 2
def extract_data(country, date):
    df = debt_long[(debt_long['Country Name'] == country) & (debt_long['Date'] == date)]
    dictionary = {
        'Total  Internal': df[df['Series Code'] == 'DP.DOD.DECD.CR.PS.CD']['Debt'].iloc[0],
        'Total External': df[df['Series Code'] == 'DP.DOD.DECX.CR.PS.CD']['Debt'].iloc[0],
        'Local Currency': df[df['Series Code'] == 'DP.DOD.DECN.CR.PS.CD']['Debt'].iloc[0],
        'Foreign Currency': df[df['Series Code'] == 'DP.DOD.DECF.CR.PS.CD']['Debt'].iloc[0],
        'Short Term Debt': df[df['Series Code'] == 'DP.DOD.DSTC.CR.PS.CD']['Debt'].iloc[0],
        'Long Term Debt': df[df['Series Code'] == 'DP.DOD.DLTC.CR.PS.CD']['Debt'].iloc[0]
    }
    return dictionary

# Exercise 3
def get_countries(debt_type, date):
    df = debt_long[(debt_long['Series Code'] == debt_type) & (debt_long['Date'] == date)]
    df.dropna(subset='Debt')
    dict_countries = {}
    for index, row in df.iterrows():
        dict_countries[row['Country Name']] = row['Debt']
    return dict_countries

# Exercise 4
def pie_cart_internal_external(country, date):
    df = debt_long[(debt_long['Country Name'] == country) & (debt_long['Date'] == date)]
    internal_debt  = df[df['Series Code'] == 'DP.DOD.DECD.CR.PS.CD']['Debt'].iloc[0]
    external_debt =  df[df['Series Code'] == 'DP.DOD.DECX.CR.PS.CD']['Debt'].iloc[0]
    labels = ['Internal Debt', 'External Debt']
    sizes = [internal_debt, external_debt]

    fig, ax = plt.subplots(figsize=(6, 6))
    sns.set(style="whitegrid")
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['lightblue', 'lightcoral'])
    plt.title(f'Debt Composition for {country} in {date[:4]} in {date[-2:]}')
    # Show the legend at the bottom with the amount of debt
    plt.legend(loc='lower right', shadow=True, ncol=1)
    plt.show()
    st.pyplot(fig)

# Exercise 5
def pie_chart_all_debt(country, date):
    df = debt_long[(debt_long['Country Name'] == country) & (debt_long['Date'] == date)]

   # TODO Create Function, what should we display?

# Exercise 6
def line_chart_countries(countries, debt_type):
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
    plt.legend(title='Debt Types', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()
    st.pyplot(fig)


# Exercise 8
def box_plot_countries(countries, debt_types):
    # Filter data for the selected countries and debt types
    filtered_data = debt_long[(debt_long['Country Name'].isin(countries)) & (debt_long['Series Code'].isin(debt_types))]
    # Create a box plot
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.set(style="whitegrid")
    palette = sns.color_palette("muted")
    plt.title(f'Box Plot of Debt for {", ".join(countries)}', fontsize=16)
    sns.boxplot(x='Country Name', y='Debt', hue='Series Code', data=filtered_data, palette=palette)
    plt.xticks(rotation=90)
    plt.xlabel('Country')
    plt.ylabel('Debt')
    plt.yscale('log')
    plt.legend(title='Debt Type')
    plt.show()
    st.pyplot(fig)



########################################
# The following Code provides a Streamlit interface for the project.
# Every exercise gets a seperate page.
########################################

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


if choice == 'Excersice 1':
    st.subheader("Exercise 1")
    # Display Exercise 1 result
    print(2)
    st.write(debt_long)
    print(2)
    
if choice == 'Exercise 2':
    st.subheader("Exercise 2")
    # Get user input for Exercise 2
    country_input = st.text_input("Enter country:", "Uganda")
    date_input = st.text_input("Enter date (e.g. 2019Q3):", "2019Q3")
    # Display Exercise 2 result
    result = extract_data(country_input, date_input)
    st.write(result)
    print(extract_data('Uganda', '2019Q3'))

if choice == 'Exercise 3':
    st.subheader("Exercise 3")
    # Get user input for Exercise 3
    country_input = st.text_input("Enter Debt type:", "DP.DOD.DECD.CR.PS.CD")
    date_input = st.text_input("Enter date (e.g. 2019Q3):", "2019Q3")
    # Display Exercise 2 result
    result = get_countries(country_input, date_input)
    st.write(result)

if choice == 'Exercise 4':
    st.subheader("Exercise 4")
    # Get user input for Exercise 4
    country_input = st.text_input("Enter country:", "Uganda")
    date_input = st.text_input("Enter date (e.g., 2019Q3):", "2019Q3")

    # Display Exercise 4 result
    pie_cart_internal_external(country_input, date_input)

if choice == 'Exercise 5':
    st.subheader("Exercise 5")
    # Get user input for Exercise 5

    # Display Exercise 5 result
    pie_chart_all_debt()

if choice == 'Exercise 6':
    st.subheader("Exercise 6")
    # Get user input for Exercise 6
    countries_input = st.text_input("Enter countries (comma-separated):", "Mexico,Canada,St. Lucia")
    debt_type_input = st.text_input("Enter debt type:", "DP.DOD.DECD.CR.PS.CD")
    countries_list = [country.strip() for country in countries_input.split(',')]

    # Display Exercise 6 result
    line_chart_countries(countries_list, debt_type_input)

    # TODO look at 'Australia' or 'Mexico' do we need to clean the data or those just strange spikes?


if choice == 'Exercise 7':
    st.subheader("Exercise 7")
    # Get user input for Exercise 7
    country_input = st.text_input("Enter country:", "Canada")
    debt_types_input = st.text_input("Enter debt types (comma-separated):", "DP.DOD.DECD.CR.PS.CD,DP.DOD.DECX.CR.PS.CD,DP.DOD.DECT.CR.PS.CD")
    debt_types_list = [debt_type.strip() for debt_type in debt_types_input.split(',')]
    # Display Exercise 7 result
    line_chart_debt_types(country_input, debt_types_list)

if choice == 'Exercise 8':
    st.subheader("Exercise 8")
    # Get user input for Exercise 8
    countries_input = st.text_input("Enter countries (comma-separated):", "Mexico,Canada")
    debt_types_input = st.text_input("Enter debt types (comma-separated):", "DP.DOD.DECD.CR.PS.CD,DP.DOD.DECX.CR.PS.CD,DP.DOD.DECT.CR.PS.CD")
    countries_to_plot = [country.strip() for country in countries_input.split(',')]
    debt_types_to_plot = [debt_type.strip() for debt_type in debt_types_input.split(',')]
    # Display Exercise 8 result
    box_plot_countries(countries_to_plot, debt_types_to_plot)


