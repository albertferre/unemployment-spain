import streamlit as st
import pandas as pd
import plotly.express as px
from src.utils import download_file, parse_excel_file
import statsmodels.api as sm
import plotly.graph_objects as go
import numpy as np



# Load the data from the parsed Excel file
data = parse_excel_file([
    "data/evolparoseries2001.xls",
    "data/evolparoseries.xlsx"
]).sort_values("date_time")




def forecast_unemployment():

    data_forecast = data.copy()

    data_forecast = data_forecast[data_forecast.date_time<"2011-05-01"].reset_index()
    # Set the date_time column as the index
    data_forecast.set_index('date_time', inplace=True,drop=False)

    # Fit the ARIMA model
    # model = sm.tsa.ARIMA(np.asarray(data_forecast['total']), order=(3,1,2))
    # results = model.fit()

    # Fit the Holt-Winters model
    model = sm.tsa.ExponentialSmoothing(data_forecast['total'], seasonal='add', seasonal_periods=12)
    results = model.fit()

    print(results.summary())

    # Forecast the next 12 months
    forecast_steps = 12
    forecast = results.forecast(steps=forecast_steps)


    # Create a new DataFrame to store the forecast
    forecast_index = pd.date_range(data_forecast.index[-1], periods=forecast_steps+1, freq='MS')
    forecast_df = pd.DataFrame(forecast, index=forecast_index[1:], columns=['forecast'])


    #####################################################
    # Perform seasonal decomposition
    decomposition = sm.tsa.seasonal_decompose(data_forecast['total'], model='mul', extrapolate_trend='freq')

    # Extract the trend, seasonal, and residual components
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    print(trend)
    pendiente = (trend[-1] - trend[-12])/12
    pendiente_trend = range(12)*pendiente
    print(seasonal[-12:].values)

    # Forecast the next 12 months using the seasonal component
    forecast_steps = 12
    forecast_seasonal = (seasonal[-12:].values * data_forecast.total[-1]) + pendiente_trend
    forecast_index = pd.date_range(data_forecast.index[-1], periods=forecast_steps + 1, freq='MS')[1:]

    # Create a new DataFrame to store the forecast
    forecast_df = pd.DataFrame({'forecast': forecast_seasonal}, index=forecast_index)
    ###################################################


    return forecast_df

def forecast_page():
    st.title("Unemployment Data Dashboard")

    # Create a line chart using Plotly Express
    fig = px.line(data, x='date_time', y='total', title='Unemployment Evolution',
                  labels={'date_time': 'Date', 'total': 'Total Unemployment'})


    forecast_df = forecast_unemployment()
    # Add the forecast to the plot
    fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df['forecast'], mode='lines',
                            name='Forecast', line=dict(color='red')))

    # Display the chart using Streamlit
    st.plotly_chart(fig)

# Streamlit App
def main():
    forecast_page()

if __name__ == '__main__':
    main()
