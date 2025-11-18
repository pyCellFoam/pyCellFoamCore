"""
Dash app for interactive 3D visualization of nodes and their dual volumes.
Run this script to start the interactive web application.
"""
import logging
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from pyCellFoamCore.k_cells.edge.baseEdge import EdgePlotly
from pyCellFoamCore.tools.logging_formatter import set_logging_format
_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)

# Execute the roi2_modified.py file to get all the data
print("Loading 3D complex data...")
exec(open('export/roi2_modified.py').read(), globals())
print("Data loaded successfully!")

# Now we have access to all variables from roi2_modified.py including:
# nodes, dc (dual complex), NodePlotly, VolumePlotly

# Create the Dash app
app = dash.Dash(__name__)

# Create dropdown options for nodes
node_options = [{'label': 'None (no node selected)', 'value': -1}]
for i, node in enumerate(nodes):
    label = (f'Node {node}: '
             f'({node.xCoordinate:.2f}, '
             f'{node.yCoordinate:.2f}, '
             f'{node.zCoordinate:.2f})')
    node_options.append({
        'label': label,
        'value': i
    })

# Define the app layout
app.layout = html.Div([
    html.H1("3D Node and Dual Volume Visualization",
            style={'textAlign': 'center', 'marginBottom': 30}),

    html.Div([
        html.Div([
            html.Label("Select a Node:",
                       style={'marginBottom': 10, 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='node-dropdown',
                options=node_options,
                value=-1,  # Default to no node selected
                style={'marginBottom': 20}
            )
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            html.Label("Display Options:",
                       style={'marginBottom': 10, 'fontWeight': 'bold'}),
            dcc.Checklist(
                id='display-options',
                options=[
                    {'label': 'Primal Nodes', 'value': 'primal_nodes'},
                    {'label': 'Dual Nodes', 'value': 'dual_nodes'},
                    {'label': 'Primal Edges', 'value': 'primal_edges'},
                    {'label': 'Dual Edges', 'value': 'dual_edges'}
                ],
                value=['primal_nodes', 'dual_nodes', 'primal_edges', 'dual_edges'],  # All selected by default
                style={'marginBottom': 20},
                labelStyle={'display': 'block', 'marginBottom': 5}
            )
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'})
    ]),

    dcc.Graph(id='3d-plot', style={'height': '80vh'})
])


# Callback to update the plot when dropdown selection changes
@app.callback(
    Output('3d-plot', 'figure'),
    [Input('node-dropdown', 'value'),
     Input('display-options', 'value')]
)
def update_plot(selected_node_index, display_options):
    """Update the 3D plot based on selected node and display options."""
    # Create base figure
    fig = go.Figure()

    # Add selected node and its dual volume if a node is selected
    if selected_node_index is not None and selected_node_index >= 0:
        # Get the selected node
        selected_node = nodes[selected_node_index]
        _log.info("Selected Node: %s", {selected_node})

        # Create a figure for the selected node
        selected_node_plotly = NodePlotly([selected_node])
        fig = selected_node_plotly.plot_nodes_plotly(show_label=True)

        # Find the corresponding dual volume for this node
        # In a dual complex, each primal node corresponds to a dual volume
        dual_volume = selected_node.dualCell3D
        dual_volume_plotly = VolumePlotly([dual_volume])

        # Add the dual volume to the same figure
        dual_volume_plotly.plot_volumes_plotly(fig, show_label=True,
                                              show_normal_vec=False)

    # Add optional elements based on checkbox selection
    if 'primal_nodes' in display_options:
        primal_node_plotly = NodePlotly(pc.nodes)
        primal_node_plotly.plot_nodes_plotly(fig, show_label=False)

    if 'dual_nodes' in display_options:
        dual_node_plotly = NodePlotly(dc.nodes)
        dual_node_plotly.plot_nodes_plotly(fig, show_label=False)

    if 'primal_edges' in display_options:
        primal_edge_plotly = EdgePlotly(pc.edges)
        primal_edge_plotly.plot_edges_plotly(fig, show_label=False,
                                           show_direction=False,
                                           show_barycenter=False)

    if 'dual_edges' in display_options:
        dual_edge_plotly = EdgePlotly(dc.edges)
        dual_edge_plotly.plot_edges_plotly(fig, show_label=False,
                                         show_direction=False,
                                         show_barycenter=False)

    # Update layout for better visualization
    title = "3D Complex Visualization"
    if selected_node_index is not None and selected_node_index >= 0:
        selected_node = nodes[selected_node_index]
        title = f"Node {selected_node.num} and its Dual Volume"

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X Coordinate',
            yaxis_title='Y Coordinate',
            zaxis_title='Z Coordinate',
            aspectmode='cube'
        ),
        showlegend=True,
        margin=dict(l=0, r=0, b=0, t=40)
    )

    return fig


if __name__ == '__main__':
    _log.info("Starting Dash app...")
    _log.info("Open your browser and go to: http://127.0.0.1:8050")
    app.run(debug=True, port=8050)