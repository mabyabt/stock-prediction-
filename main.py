# import
import streamlit as st
from datetime import date

import yfinances as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from  plotly import graph_obj as go


START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")


st.title("I Stocke prediction appication")


stocks = ("AAPL", "GOOG", "MSFT", "TSLA")
selected_stocks = st.selectbox("Select stocks fro prediction", stocks)

n_years = st.slider("Yers of prediction: ", 1,4)
period = n_years * 365


def load_data(ticker):
    data = yf.download(ticker,START,TODAY)
    data.reset_index(inplace=True)
    return data


data_load_state = st.text("load data...")

data = load_data(selected_stocks)
data_load_state.text("loadin done")

