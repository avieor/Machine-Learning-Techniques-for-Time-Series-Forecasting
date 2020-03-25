import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from datetime import datetime
from dash.dependencies import Input, Output
from Log_Entry_Class import Log_Entry

from Log_Book_Class import Log_Book
from Log_Entry_Request_Class import Log_Entry_Request

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#DICTIONARIES AND ARRAYS

#colours that will be used throughout the UI
colors = {
    'main' : '#1a1c23',
    'log_book': '#22252b',
    'text': '#b2b2af',
    'graph':  '#21252c',
    'green': '#3d9970',
    'red': '#fc4136',
    'black': '#000000',
    'white' : '#FFFFFF'
}

styles = {
    'grey_text_on_black_background': {
        'color': colors['text'],
        'background-color': colors['main']
    }
}

dataset_choices = [
    'Data\Appliances Energy Usage Prediction\energydata_complete.csv',
    'Demonstrations\monthly-sunspots.csv'
]

model_choices = [
    'Linear Regression'
]

#FUNCTIONS

#creates a log_book and fills it
def create_and_fill_log_book():
    log_book =create_log_book()
    return fill_log_book(log_book)

#this class will create log entries for the purpose of demonstration
def fill_log_book(log_book):
    log_book.append_log_entry(create_log_entry(Log_Entry_Request(dataset_choices[0], 'Linear Regression', 1/2 )))
    log_book.append_log_entry(create_log_entry(Log_Entry_Request(dataset_choices[1], 'Linear Regression', 1/2 )))
    log_book.append_log_entry(create_log_entry(Log_Entry_Request(dataset_choices[0], 'Linear Regression', 1/2 )))
    log_book.append_log_entry(create_log_entry(Log_Entry_Request(dataset_choices[1], 'Linear Regression', 1/2 )))
    return log_book


#this class will create log entrie for the purpose of demonstration
def create_log_book():
    log_book = Log_Book()
    return log_book

#creates a log entry from a log_entry_request and returns it
def create_log_entry(log_entry_request):
    #If dropdown selected is a valid data
    if log_entry_request.dataset in dataset_choices and log_entry_request.model in model_choices and log_entry_request.check_valid_ratio():
        #Create a Log Entry
        log_entry = Log_Entry(log_entry_request.model, log_entry_request.dataset, datetime.now().date(), log_entry_request.ratio)
        return log_entry
    else:
        print('log entry could not be created at create_log_entry(log_entry_request)', flush=True)

#return either the log entry request page or the log entry page
def return_left_hand_side(log_book):
    if log_book.selected_log_entry in  log_book.log_entry_array:
        return  log_entry_layout()
    else:
        return log_entry_request_layout()


def print_log_book():
    print('LOGBOOK:')
    for i in range(len(log_book.button_array)):
        print(log_book.log_entry_array[i].dataset, flush=True)

#HTML LAYOUT

#html layout for the header
def header_layout():
    return html.Div(
        style = {'width': '100%', 'background-color': colors['white'], 'color': colors['black']},
        children = [
            #Heading 1
            html.H1(children='Machine Learning Techniques for Time Series Forecasting',
                style={
                    'display': 'block',
                    'text-align': 'center',
                    'font-size': 35
                },
            ),
            #Heading 2
            html.H2(children='Microsoft Project Group 6',
                style={
                    'text-align': 'center',
                    'font-size': 15
                },
            )
        ]
    )


#Html Layout for logbook
def log_book_layout(log_book):
    return html.Div(
        children = [
            html.H2(children='Logbook',
                style={
                'text-align': 'center',
                'font-size': 35,
                'color': colors['black'],
                'padding': 0
                }
            ),
            html.Table(
                className="table-news",
                children=[
                    html.Tr(
                        children=[
                            log_book.button_array[i]
                        ]
                    )
                    for i in range(len(log_book.button_array))
                ],
            )
        ]
    )


#html layout for log Entry
def log_entry_layout():
    return html.Div(
        style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'},
        children = [

            #Training Data Graph and div
            html.Div(style={'width': '50%', 'display': 'inline-block', 'padding': '5'},
                children = [
                    #Title
                    html.H3('Training data graph', style={'text-align': 'center'}),
                    #Graph
                    dcc.Loading(
                        children = [dcc.Graph(id='training-data-graph')],
                        type = 'circle',
                    ),
                ]
            ),

            #Forecasting Data Graph
            html.Div(style={'width': '50%', 'display': 'inline-block', 'padding': '0 20'},
                children = [
                    # Forecasting data graph
                    html.H3('Forecast data graph',style={'text-align': 'center'}),
                    dcc.Loading(
                        children = [
                            dcc.Graph(id='forecast-data-graph'),
                        ],
                        type = 'circle',
                    )
                ]
            ),
        ]
    )


def log_entry_request_layout():
    return html.Div(
        children = [
            html.H3('Enter log entry request details',style={'text-align': 'center'}),
            #dataset dropdown + label div
            html.Div(style={'width': '50%', 'display': 'inline-block', 'padding': '5'},
                children = [
                    html.Label(['Dataset']),
                    dcc.Dropdown(
                        id='Dataset-dropdown',
                        options=[
                            {'label': 'Energy Data', 'value': dataset_choices[0]},
                            {'label': 'Sunspots', 'value': dataset_choices[1]}
                        ],
                        placeholder='Select a Dataset',
                        value='None',
                    ),
                ]
            ),

            #Model dropdown label + dropdown div
            html.Div(style={'width': '50%', 'display': 'inline-block', 'padding': '5'},
                children = [
                    #label
                    html.Label(['Model']),
                    #dropdown
                    dcc.Dropdown(
                        id='Model-dropdown',
                        options=[
                            {'label': 'Linear Regression', 'value': model_choices[0]},
                        ],
                        placeholder='Select a Model',
                        value='None',
                    ),
                ]
            ),
            html.Div([
                html.Label(['Dataset']),
                html.Div(dcc.Input(id='input-box', type='text')),
                dcc.Loading(
                    children = [
                        html.Button('Submit', id='button'),
                        html.Div(id='output-container-button',
                                children=['Enter a bottom heavy fraction or a decimal less than one but greater than 0 and press submit'])
                    ]
                )
                ]
            )
        ]
    )

#create log book
log_book = create_and_fill_log_book()
#log_book = create_log_book()

#APP LAYOUT

app.layout = html.Div(style={'background-color': colors['white'], 'color': colors['black'], 'margin-bottom': '50px', 'margin-top': '25px'},
    children = [
        #Top Bar
        html.Div(
            id="top_bar",children = [header_layout()],
        ),
        #log book
        html.Div(
            id="log_book",children = [log_book_layout(log_book)],
            style={
                'width': '100%',
                'display': 'inline-block',
                'background-color': colors['white']
                }
        ),
        #left hand side of screen (either log entry request page or log entry page)
        html.Div(
            id="log_entry",
            children = [return_left_hand_side(log_book)],
            style={'width': '100%', 'display': 'inline-block'}
        )
    ]
)

#CALLBACKS

#Called when the submit button is pressed
@app.callback(dash.dependencies.Output('output-container-button', 'children'),
            [dash.dependencies.Input('button', 'n_clicks')],
            [dash.dependencies.State('Dataset-dropdown', 'value'),
            dash.dependencies.State('Model-dropdown', 'value'),
            dash.dependencies.State('input-box', 'value')])
def submit_log_entry_request(button_value, dataset_dropdown_value, model_dropdown_value, input_box_value  ):
    if input_box_value is not None :
        log_entry_request = Log_Entry_Request(dataset_dropdown_value, model_dropdown_value, input_box_value)
        if log_entry_request.dataset in dataset_choices and log_entry_request.model in model_choices and log_entry_request.check_valid_ratio():
            print('log entry request is valid', flush=True)
            log_entry = create_log_entry(log_entry_request)
            log_book.append_log_entry(log_entry)
            print_log_book()
        else:
            print('***log entry could not be created at submit_log_entry_request(button_value, dataset_dropdown_value, model_dropdown_value, input_box_value  )***', flush=True)
            print('dataset',log_entry_request.dataset,'model', log_entry_request.model, 'ratio', log_entry_request.check_valid_ratio())
    else:
        print('Request input type was none', flush=True)

if __name__ == '__main__':
    app.run_server(debug=True)
