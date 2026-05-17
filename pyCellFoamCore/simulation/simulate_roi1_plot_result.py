import pickle
import numpy as np
import pandas as pd
import plotly.graph_objects as go

with open('simulation_roi1_results.pkl', 'rb') as f:
    data = pickle.load(f)


time = data['time']
TiS = data['TiS']

select_rows = [120, 131, 142, 154, 160]
# select_rows = range(TiS.shape[0])  # Select all rows

# Create new time array with 200 points
time_resampled = np.linspace(0, 45, 2000)

# Interpolate TiS to match the new time points
TiS_resampled = np.array([np.interp(time_resampled, time, TiS[i, :]) for i in range(TiS.shape[0])])

# Update the arrays
time = time_resampled
TiS = TiS_resampled




fig = go.Figure()
for i in select_rows:
    fig.add_trace(go.Scatter(x=time, y=TiS[i, :], mode='lines', name=f'Row {i}'))

fig.update_layout(
    xaxis_title='Time in s',
    yaxis_title='Temperature in K',
    showlegend=False
)

fig.show()

# Create DataFrame with time and TiS data
df_data = {'time': time}
for i in select_rows:
    df_data[f'TiS_row_{i}'] = TiS[i, :]

df = pd.DataFrame(df_data)
df.to_csv('simulation_roi1_results.csv', index=False)

for select_row in select_rows:
    print(f"n_{{{select_row}}}\,[{','.join(map(lambda x: f'{x:.1f}', data['coordinates'][select_row]))}]")