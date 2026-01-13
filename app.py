import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Path to your CSV
FILE_PATH = "formatted_data.csv"

def load_data():
    """Load and prepare the data"""
    df = pd.read_csv(FILE_PATH)
    df['date'] = pd.to_datetime(df['date'])  # ensure date column is datetime
    df = df.sort_values('date')
    # Filter only Pink Morsel if needed
    pink_morsel_df = df
    return pink_morsel_df

def create_sales_chart(dataset, selected_region='all'):
    """Function to generate the line chart"""
    if selected_region != 'all':
        dataset = dataset[dataset['region'].str.lower() == selected_region]
    
    region_display = selected_region.capitalize() if selected_region != 'all' else 'All Regions'
    
    fig = px.line(
        dataset,
        x='date',
        y='sales',
        title=f'Pink Morsel Sales Over Time - {region_display}',
        labels={'date': 'Date', 'sales': 'Sales ($)'},
        color_discrete_sequence=['#FF6B9D']  # Pink color for the line
    )
    
    # Add vertical line for price increase
    fig.add_vline(
        x=pd.Timestamp('2021-01-15'),
        line_dash="dash",
        line_color="#FF3333",
        line_width=2,
        opacity=0.8
    )

    # Add annotation for price increase
    fig.add_annotation(
        x=pd.Timestamp('2021-01-15'),
        y=dataset['sales'].max(),
        text="Price Increase<br>Jan 15, 2021",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#FF3333",
        arrowsize=1.5,
        arrowwidth=2,
        ax=0,
        ay=-60,
        font=dict(color="#FF3333", size=12, family="Arial"),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#FF3333",
        borderwidth=1,
        borderpad=4
    )

    fig.update_layout(
        plot_bgcolor='rgba(255, 245, 250, 0.9)',
        paper_bgcolor='#FFF5FA',
        font=dict(family="Arial, sans-serif", color='#333333'),
        title_font=dict(size=22, color='#D6336C', family="Arial Black"),
        xaxis=dict(
            title_font=dict(size=14, color='#666666'),
            tickfont=dict(size=12, color='#666666'),
            gridcolor='rgba(200, 200, 200, 0.3)',
            linecolor='#CCCCCC',
            showgrid=True
        ),
        yaxis=dict(
            title_font=dict(size=14, color='#666666'),
            tickfont=dict(size=12, color='#666666'),
            gridcolor='rgba(200, 200, 200, 0.3)',
            linecolor='#CCCCCC',
            showgrid=True
        ),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='white',
            font_size=12,
            font_family="Arial"
        ),
        margin=dict(l=60, r=30, t=80, b=60),
        showlegend=False
    )
    
    # Update line style
    fig.update_traces(
        line=dict(width=3),
        hovertemplate='Date: %{x|%b %d, %Y}<br>Sales: $%{y:,.2f}<extra></extra>'
    )
    
    return fig

def create_app():
    """Create and return the Dash app instance"""
    app = Dash(__name__)
    
    # Load data
    pink_morsel_df = load_data()
    
    # Layout of the app with enhanced styling
    app.layout = html.Div(
        style={
            'backgroundColor': '#FFF5FA',
            'minHeight': '100vh',
            'padding': '20px',
            'fontFamily': 'Arial, sans-serif'
        },
        children=[
            # Header Section
            html.Div(
                style={
                    'background': 'linear-gradient(135deg, #FF6B9D 0%, #D6336C 100%)',
                    'padding': '30px',
                    'borderRadius': '15px',
                    'boxShadow': '0 4px 20px rgba(214, 51, 108, 0.3)',
                    'marginBottom': '30px',
                    'color': 'white'
                },
                children=[
                    html.H1(
                        "Pink Morsel Sales Visualizer",
                        style={
                            'textAlign': 'center',
                            'color': 'white',
                            'fontSize': '36px',
                            'fontWeight': 'bold',
                            'marginBottom': '10px',
                            'textShadow': '2px 2px 4px rgba(0,0,0,0.2)'
                        },
                        id='header'
                    ),
                    html.P(
                        "Analyze sales trends across different regions. Compare performance before and after the January 15, 2021 price increase.",
                        style={
                            'textAlign': 'center',
                            'fontSize': '18px',
                            'color': 'rgba(255, 255, 255, 0.9)',
                            'maxWidth': '800px',
                            'margin': '0 auto',
                            'lineHeight': '1.6'
                        }
                    )
                ]
            ),
            
            # Control Panel
            html.Div(
                style={
                    'backgroundColor': 'white',
                    'padding': '25px',
                    'borderRadius': '12px',
                    'boxShadow': '0 2px 15px rgba(0, 0, 0, 0.1)',
                    'marginBottom': '30px'
                },
                children=[
                    html.H2(
                        "Region Filter",
                        style={
                            'color': '#D6336C',
                            'marginBottom': '20px',
                            'fontSize': '22px',
                            'textAlign': 'center'
                        }
                    ),
                    html.P(
                        "Select a region to view specific sales data, or choose 'All' to see the complete picture:",
                        style={
                            'textAlign': 'center',
                            'color': '#666666',
                            'marginBottom': '20px',
                            'fontSize': '16px'
                        }
                    ),
                    
                    # Region filter radio buttons with enhanced styling
                    html.Div(
                        dcc.RadioItems(
                            id='region_selector',
                            options=[
                                {'label': 'All Regions', 'value': 'all'},
                                {'label': 'North', 'value': 'north'},
                                {'label': 'East', 'value': 'east'},
                                {'label': 'South', 'value': 'south'},
                                {'label': 'West', 'value': 'west'}
                            ],
                            value='all',
                            inline=True,
                            labelStyle={
                                'display': 'inline-block',
                                'margin': '10px 15px',
                                'padding': '12px 25px',
                                'backgroundColor': '#FFF5FA',
                                'borderRadius': '8px',
                                'border': '2px solid #FFD1DC',
                                'cursor': 'pointer',
                                'transition': 'all 0.3s ease',
                                'fontSize': '16px',
                                'fontWeight': '500'
                            },
                            inputStyle={
                                'marginRight': '8px',
                                'transform': 'scale(1.2)'
                            },
                            style={'textAlign': 'center', 'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap'}
                        ),
                        style={'marginBottom': '10px'}
                    ),
                    
                    # Key Insight Box
                    html.Div(
                        style={
                            'backgroundColor': '#FFF0F5',
                            'borderLeft': '4px solid #FF6B9D',
                            'padding': '15px',
                            'marginTop': '20px',
                            'borderRadius': '8px'
                        },
                        children=[
                            html.H4(
                                "📈 Key Insight:",
                                style={'color': '#D6336C', 'marginBottom': '8px'}
                            ),
                            html.P(
                                "The red dashed line marks the price increase on January 15, 2021. "
                                "Use the region filters to see how different areas responded to the price change.",
                                style={'color': '#666666', 'margin': '0', 'fontSize': '14px'}
                            )
                        ]
                    )
                ]
            ),
            
            # Graph Container
            html.Div(
                style={
                    'backgroundColor': 'white',
                    'padding': '25px',
                    'borderRadius': '12px',
                    'boxShadow': '0 2px 15px rgba(0, 0, 0, 0.1)'
                },
                children=[
                    dcc.Graph(
                        id='sales_graph',
                        figure=create_sales_chart(pink_morsel_df),
                        config={'displayModeBar': True, 'displaylogo': False},
                        style={'height': '600px'}
                    )
                ]
            ),
            
            # Footer
            html.Div(
                style={
                    'marginTop': '40px',
                    'padding': '20px',
                    'textAlign': 'center',
                    'color': '#999999',
                    'fontSize': '14px',
                    'borderTop': '1px solid #FFD1DC'
                },
                children=[
                    html.P("Soul Foods Analytics Dashboard • Created with Plotly Dash"),
                    html.P("Data Source: Pink Morsel Sales Records (2020-2022)")
                ]
            )
        ]
    )
    
    # Callback to update the chart based on region
    @app.callback(
        Output('sales_graph', 'figure'),
        Input('region_selector', 'value')
    )
    def update_chart(selected_region):
        return create_sales_chart(pink_morsel_df, selected_region)
    
    return app

# Run the app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)