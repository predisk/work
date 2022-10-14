from dash import Dash, dcc, html, Input, Output
import plotly.express as px

import pandas as pd
print('test')
df = pd.read_csv('data.csv')
data = df
data_chart1 = data.groupby('LaunchSite')['LaunchSite'].count()
chart1 = px.pie(data,
            values=data.groupby('LaunchSite')['LaunchSite'].count(),
            names=data.groupby('LaunchSite')['LaunchSite'].count().index,
            title='Launch Times for Each Site'
        )
chart1.update(layout =dict(title=dict(x=0.5)))
site_cs = data[data['LaunchSite']== 'CCSFS SLC 40']
site_cs.replace({True:'Success'},regex=True, inplace=True)
site_cs.replace({False:'Fail'},regex=True, inplace=True)
site_cs = site_cs.groupby(['LaunchSite','Outcome']).size().reset_index(name='count')
chart2 = px.pie(site_cs,
            values = site_cs['count'],
            names = site_cs['Outcome'],
            title='Launch Times for Each Site'
        )
chart2.update(layout =dict(title=dict(x=0.5)))
chart2.update_traces(textposition='inside', textinfo='percent')


data3 = data
data3.replace({True:'Success'},regex=True, inplace=True)
data3.replace({False:'Fail'},regex=True, inplace=True)
chart3 = px.histogram(data3, y="Orbit", color="Outcome")
chart3.update(layout =dict(title=dict(x=0.5)))
chart4 = px.histogram(data3, y="LandingPad", color="Outcome")
chart4.update(layout =dict(title=dict(x=0.5)))
graph3 = dcc.Graph(
        id='graph3',
        figure=chart3,
        className="four columns"
    )
graph4 = dcc.Graph(
        id='graph4',
        figure=chart4,
        className="four columns"
    )
row4 = html.Div(children=[graph3,graph4])

app = Dash(__name__)
row2 = html.Div(children=[html.Iframe(id = 'map',srcDoc=open('site_location.html','r').read(), width='100%',height='500')])
header = html.H1('Interactive Dashboard')
header2 = html.H3('Launch Site Location Info')
header3 = html.H3('Different Payload Distribution')
header4 = html.H3('Launch Outcome')
# header4 = html.H3('Launch Outcome for Different Orbit')
# header5 = html.H3('Launch Outcome for Different LandingPad')
app.layout = html.Div([
    header,
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'Sites', 'value': 'overview'},
                     {'label': 'CCSFS SLC 40', 'value': 'CCSFS SLC 40'},
                     {'label': 'KSC LC 39A', 'value': 'KSC LC 39A'},
                     {'label': 'VAFB SLC 4E', 'value': 'VAFB SLC 4E'}
                 ],
                 value='overview',
                 placeholder='Select a Launch Site here',
                 searchable=True

                 ),

    html.Div(dcc.Graph(id='success_rate_of_site')),
    header2,
    row2,
    header3,
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        df['Year'].min(),
        df['Year'].max(),
        step=None,
        value=df['Year'].min(),
        marks={str(Year): str(Year) for Year in df['Year'].unique()},
        id='year-slider'
    ),
    header4,
    row4
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.Year == selected_year]

    fig = px.scatter(filtered_df, x="Orbit", y="PayloadMass")

    fig.update_layout(transition_duration=500)

    return fig


@app.callback(
    Output('success_rate_of_site', 'figure'),
    Input('site-dropdown', 'value'))
def get_pie_chart(entered_site):
    filtered_df = df
    if entered_site == 'overview':
        fig = chart1
        return fig
    else:
        site_cs = data[data['LaunchSite'] == entered_site]
        site_cs.replace({True: 'Success'}, regex=True, inplace=True)
        site_cs.replace({False: 'Fail'}, regex=True, inplace=True)
        site_cs = site_cs.groupby(['LaunchSite', 'Outcome']).size().reset_index(name='count')
        chart2 = px.pie(site_cs,
                        values=site_cs['count'],
                        names=site_cs['Outcome'],
                        title='Launch Times for Each Site'
                        )
        chart2.update(layout=dict(title=dict(x=0.5)))
        chart2.update_traces(textposition='inside', textinfo='percent')
        fig = chart2

        return fig


if __name__ == '__main__':
    app.run_server(debug=True)