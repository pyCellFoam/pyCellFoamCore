import pickle
import numpy as np
import pandas as pd
import plotly.graph_objects as go

with open('simulation_roi2_results.pkl', 'rb') as f:
    data = pickle.load(f)


time = data['time']
TiS = data['TiS']

# Create new time array with 200 points
time_resampled = np.linspace(0, 30, 200)

# Interpolate TiS to match the new time points
TiS_resampled = np.array([np.interp(time_resampled, time, TiS[i, :]) for i in range(TiS.shape[0])])

# Update the arrays
time = time_resampled
TiS = TiS_resampled


fig = go.Figure()
for i in range(TiS.shape[0]):
    fig.add_trace(go.Scatter(x=time, y=TiS[i, :], mode='lines', name=f'Row {i}'))

fig.update_layout(
    xaxis_title='Time in s',
    yaxis_title='Temperature in K',
    showlegend=False
)

fig.show()

# Create DataFrame with time and TiS data
df_data = {'time': time}
for i in range(TiS.shape[0]):
    df_data[f'TiS_row_{i}'] = TiS[i, :]

df = pd.DataFrame(df_data)
df.to_csv('simulation_roi2_results.csv', index=False)
