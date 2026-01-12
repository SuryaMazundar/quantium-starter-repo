import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Path to your CSV
FILE_PATH = "C:/Users/0wner/Downloads/GIT_Folder/quantium-starter-repo-main/quantium-starter-repo/formatted_data.csv"

# Load and prepare the data
df = pd.read_csv(FILE_PATH)
df['date'] = pd.to_datetime(df['date'])  # ensure date column is datetime
df = df.sort_values('date')

# Filter only Pink Morsel if needed
pink_morsel_df = df[df['morsel'] == 'Pink Morsel'] if 'morsel' in df.columns else df

# Initialize the Dash app
app = Dash(__name__)

# Function to generate the line chart
def create_sales_chart(dataset, selected_region='all'):
    if selected_region != 'all':
        dataset = dataset[dataset['region'].str.lower() == selected_region]
    fig = px.line(
        dataset,
        x='date',
        y='sales',
        title=f'Pink Morsel Sales Over Time ({selected_region.capitalize()})',
        labels={'date': 'Date', 'sales': 'Quantity Sold'}
    )
    
    # Add vertical line for price increase
    fig.add_vline(
        x=pd.Timestamp('2021-01-15'),
        line_dash="dash",
        line_color="red"
    )

    # Add annotation at top of chart
    fig.add_annotation(
        x=pd.Timestamp('2021-01-15'),
        y=dataset['sales'].max(),  # top of chart
        text="Price Increase",
        showarrow=True,
        arrowhead=3,
        ax=0,
        ay=-40,
        font=dict(color="red")
    )

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='whitesmoke',
        font=dict(color='#333')
    )
    return fig


# Layout of the app
app.layout = html.Div(children=[
    html.H1("Pink Morsel Sales Visualizer", style={'textAlign': 'center', 'color': '#D6336C'}),
    html.P(
        "Filter sales by region to explore trends. Observe the effect of the 15 Jan 2021 price increase.",
        style={'textAlign': 'center', 'fontSize': '16px'}
    ),

    # Region filter radio buttons
    html.Div(
        dcc.RadioItems(
            id='region_selector',
            options=[
                {'label': 'All', 'value': 'all'},
                {'label': 'North', 'value': 'north'},
                {'label': 'East', 'value': 'east'},
                {'label': 'South', 'value': 'south'},
                {'label': 'West', 'value': 'west'}
            ],
            value='all',
            inline=True,
            style={'fontSize': '16px', 'margin': '10px'}
        ),
        style={'textAlign': 'center', 'marginBottom': '20px'}
    ),

    # Graph
    dcc.Graph(
        id='sales_graph',
        figure=create_sales_chart(pink_morsel_df)
    )
])

# Callback to update the chart based on region
@app.callback(
    Output('sales_graph', 'figure'),
    Input('region_selector', 'value')
)
def update_chart(selected_region):
    return create_sales_chart(pink_morsel_df, selected_region)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
