# import necessary libraries
import plotly.graph_objs as go

# route for dashboard (requires login)
@app.route(‘/dashboard’)
@login_required
def dashboard():
    # sample data for demonstration
    x_values = [1, 2, 3, 4, 5]
    y_values = [10, 15, 13, 17, 18]

    # create a bar chart
    bar_chart = go.bar(x=x_values, y=y_values, marker=dict(color=’rgb(26, 118, 255)’))

    # create a layout for the chart
    layout = go.layout(title=’sample bar chart’, xaxis=dict(title=’x axis’), yaxis=dict(title=’y axis’))

    # create a figure and add the chart and layout
    fig = go.figure(data=[bar_chart], layout=layout)

    # convert the figure to json format for rendering in html
    chart_json = fig.to_json()

    return render_template(‘dashboard.html’, chart_json=chart_json)
