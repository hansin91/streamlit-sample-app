import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from numerize import numerize

st.set_page_config(
    page_title= "Superstore dashboard",
    layout="wide"
)

df = pd.read_csv('data/superstore.csv')
df['order_date'] = pd.to_datetime(df['order_date'])
df['ship_date'] = pd.to_datetime(df['ship_date'])

st.title('Superstore')

df['order_year'] = df['order_date'].dt.year
CURR_YEAR  = df['order_year'].max()
PREV_YEAR = CURR_YEAR - 1
# st.dataframe(df, use_container_width=True)

mx_data = pd.pivot_table(
    data=df,
    index='order_year',
    aggfunc={
        'sales': np.sum,
        'profit': np.sum,
        'order_id': pd.Series.nunique,
        'customer_id': pd.Series.nunique
    }
).reset_index()

mx_data['profit_ratio'] = 100.0 * mx_data['profit'] / mx_data['sales']
st.dataframe(mx_data, use_container_width=True)

mx_sales, mx_order, mx_customer, mx_profit = st.columns(4)
with mx_sales:
    curr_sales = mx_data.loc[mx_data['order_year'] == CURR_YEAR, 'sales'].values[0]
    prev_sales = mx_data.loc[mx_data['order_year'] == PREV_YEAR, 'sales'].values[0]

    sales_diff_pct = 100.0 * (curr_sales - prev_sales) / prev_sales
    st.metric(
        label='Sales',
        value=f"{numerize.numerize(curr_sales)}",
        delta=f"{sales_diff_pct:.2f}%"
    )

with mx_order:
    curr_orders = mx_data.loc[mx_data['order_year'] == CURR_YEAR, 'order_id'].values[0]
    prev_orders = mx_data.loc[mx_data['order_year'] == PREV_YEAR, 'order_id'].values[0]

    orders_diff_pct = 100.0 * (curr_orders - prev_orders) / prev_orders
    st.metric(
        label='Orders',
        value=curr_orders,
        delta=f"{orders_diff_pct:.2f}%"
    )

with mx_customer:
    curr_customers = mx_data.loc[mx_data['order_year'] == CURR_YEAR, 'customer_id'].values[0]
    prev_customers = mx_data.loc[mx_data['order_year'] == PREV_YEAR, 'customer_id'].values[0]

    customers_diff_pct = 100.0 * (curr_customers - prev_customers) / prev_customers
    st.metric(
        label='Customers',
        value=curr_customers,
        delta=f"{customers_diff_pct:.2f}%"
    )

with mx_profit:
    curr_profit = mx_data.loc[mx_data['order_year'] == CURR_YEAR, 'profit_ratio'].values[0]
    prev_profit = mx_data.loc[mx_data['order_year'] == PREV_YEAR, 'profit_ratio'].values[0]

    profit_diff_pct = curr_profit - prev_profit
    st.metric(
        label='Profit',
        value=f"{curr_profit:.2f}%",
        delta=f"{profit_diff_pct:.2f}%"
    )

st.header("Daily Sales")
sales_line = alt.Chart(df[df['order_year'] == CURR_YEAR]).mark_line().encode(
    alt.X('order_date', title='Order date'),
    alt.Y('sales', title= 'Sales', aggregate='sum')
)
st.altair_chart(sales_line, use_container_width=True)

st.header("Monthly Sales")
sales_monthly = alt.Chart(df[df['order_year'] == CURR_YEAR]).mark_line().encode(
    alt.X('order_date', title='Order date', timeUnit='yearmonth'),
    alt.Y('sales', title= 'Sales', aggregate='sum')
)
st.altair_chart(sales_monthly, use_container_width=True)

st.header('Sales')
freqOption = st.selectbox(
  "Choose frequency",
  options=("Daily", "Monthly")
)

timeUnit = {
    'Daily': 'yearmonthdate',
    'Monthly': 'yearmonth'
}

aggregateOption = st.selectbox(
    "Choose aggregate",
    options=('Sum', 'Max', 'Mean', 'Average')
)
aggreggate = {
    'Sum': 'sum',
    'Max': 'max',
    'Mean': 'mean',
    'Average': 'average'
}

sales_custom = alt.Chart(df[df['order_year'] == CURR_YEAR]).mark_line().encode(
    alt.X('order_date', title='Order date', timeUnit=timeUnit[freqOption]),
    alt.Y('sales', title= 'Sales', aggregate=aggreggate[aggregateOption])
)
st.altair_chart(sales_custom, use_container_width=True)

west, east, south, central = st.columns(4)
with west:
    st.header('West')
    sales_cat = alt.Chart(df[(df['order_year'] == CURR_YEAR) & (df['region'] == 'West')]).mark_bar().encode(
        alt.X('category', title='Category', axis=alt.Axis(labelAngle=0)),
        alt.Y('sales', title='Sales', aggregate='sum')
    )
    st.altair_chart(sales_cat, use_container_width=True)

with east:
    st.header('East')
    sales_cat = alt.Chart(df[(df['order_year'] == CURR_YEAR) & (df['region'] == 'East')]).mark_bar().encode(
        alt.X('category', title='Category', axis=alt.Axis(labelAngle=0)),
        alt.Y('sales', title='Sales', aggregate='sum')
    )
    st.altair_chart(sales_cat, use_container_width=True)

with south:
    st.header('South')
    sales_cat = alt.Chart(df[(df['order_year'] == CURR_YEAR) & (df['region'] == 'South')]).mark_bar().encode(
        alt.X('category', title='Category', axis=alt.Axis(labelAngle=0)),
        alt.Y('sales', title='Sales', aggregate='sum')
    )
    st.altair_chart(sales_cat, use_container_width=True)

with central:
    st.header('Central')
    sales_cat = alt.Chart(df[(df['order_year'] == CURR_YEAR) & (df['region'] == 'Central')]).mark_bar().encode(
        alt.X('category', title='Category', axis=alt.Axis(labelAngle=0)),
        alt.Y('sales', title='Sales', aggregate='sum')
    )
    st.altair_chart(sales_cat, use_container_width=True)

region_point = alt.Chart(df[df['order_year']==CURR_YEAR]).mark_point(filled=True).encode(
    alt.X('customer_id', aggregate='distinct'),
    alt.Y('order_id', aggregate='distinct'),
    color='region',
    size='sum(sales)'
)

st.altair_chart(region_point, use_container_width=True)