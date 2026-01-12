import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# Path to your CSV
FILE_PATH = "C:/Users/0wner/Downloads/GIT_Folder/quantium-starter-repo-main/quantium-starter-repo/formatted_data.csv"

# Load and prepare the data
df = pd.read_csv(FILE_PATH)
df['date'] = pd.to_datetime(df['date'])  # ensure date column is datetime
df = df.sort_values('date')

# Filter only Pink Morsel if needed
pink_morsel_df = df[df['morsel'] == 'Pink Morsel'] if 'morsel' in df.columns else df

# Create the line chart
sales_fig = px.line(
    pink_morsel_df,
    x='date',
    y='sales',
    title='Pink Morsel Sales Over Time',
    labels={'date': 'Date', 'sales': 'Quantity Sold'}
)

# Initialize the Dash app
app = Dash(__name__)

# Layout of the app
app.layout = html.Div(children=[
    html.H1("Pink Morsel Sales Visualizer", style={'textAlign': 'center'}),
    html.P(
        "This dashboard shows Pink Morsel sales over time. "
        "Observe the trend before and after the price increase on 15th Jan 2021.",
        style={'textAlign': 'center'}
    ),
    dcc.Graph(
        id='sales_graph',
        figure=sales_fig
    )
])

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
