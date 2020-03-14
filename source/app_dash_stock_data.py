import dash
import dash_core_components as core
import dash_bootstrap_components as boots
from dash_html_components import H1, Div, Span
from dash.dependencies import Input, Output
from pandas_datareader import data as pdr
import yfinance as yfi


class Context:

    stock_context = None

    @classmethod
    def set_stock_context(cls, context):
        cls.stock_context = context

    @classmethod
    def get_stock_context(cls):
        return cls.stock_context


my_app = dash.Dash('Stock Data', external_stylesheets=[boots.themes.BOOTSTRAP])

nav = boots.NavbarSimple(
    children=[
        boots.NavItem(boots.NavLink("Link for Company's Website", href="#", id="stock-web-link")),
        boots.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                boots.DropdownMenuItem("What are you lookin at?"),
                boots.DropdownMenuItem("Nothing to see here"),
                boots.DropdownMenuItem(divider=True),
                boots.DropdownMenuItem("ugh"),
            ],
        ),
    ],
    brand="Stock Data",
    brand_href="#",
    sticky="top",
)

body = boots.Container(
    [
        boots.Row(
            [
                boots.Col(
                    [
                        H1(
                            'Search Stocks',
                            className='',
                            id=''
                          ),
                        Span(
                            'Examples: COKE, TSLA, MSFT, CYH.'
                        ),
                        core.Input(
                            id='ticker_input',
                            value='MSFT',
                            className='input'
                        )
                    ],
                    className='col-4 mb-4'
                ),
                boots.Col(
                    [
                        H1(
                            'Stock Data',
                            className='',
                            id='stock-name'
                        ),
                        core.Graph(
                            # type='dash.Output',
                            id='graph_out',
                            figure={}
                        )
                    ],
                    className='mb-4'
                )
            ],
        )
    ],
    className='mt-4'
)

my_app.layout = Div([nav, body])


@my_app.callback(Output('stock-name', 'children'), [Input('graph_out', 'figure')])
def update_stock_name(figure):
    return "{}".format(Context.get_stock_context().get('shortName'))


@my_app.callback(Output('stock-web-link', 'href'), [Input('graph_out', 'figure')])
def update_stock_link(figure):
    return "{}".format(Context.get_stock_context().get('website'))


@my_app.callback(Output('graph_out', 'figure'), [Input('ticker_input', "value")])
def update_graph(stock_ticker_input):
    stock_info = yfi.Ticker(stock_ticker_input)
    stock_ticker = pdr.get_data_yahoo(stock_ticker_input)
    figure = {
        'data': [
            {
                'x': stock_ticker.index,
                'y': stock_ticker.Open
            }
        ]
    }
    Context.set_stock_context(stock_info.info)
    return figure


my_app.server.run(debug=True)