import plotly.graph_objects as go
import pandas as pd

class Plotter:
    def __init__(self, title="Zn Values Over Time"):
        self.title = title

    def create_plot(self, df: pd.DataFrame, y1_column: str, y2_column: str = None, real_time= None):
        ...

        if not pd.api.types.is_datetime64_any_dtype(df['timestamps']):
            df['timestamps'] = pd.to_datetime(df['timestamps'], utc=True)

        if y2_column:
            mode = 'lines'
            line = dict(width=1)
        else:
            mode = 'lines'
            line = dict(width=3)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df['timestamps'],
            y=df[y1_column],
            mode=mode,
            name=y1_column.replace('_', ' ').title(),
            line=line,
            yaxis='y1'
        ))

        if y2_column:
            fig.add_trace(go.Scatter(
                x=df['timestamps'],
                y=df[y2_column],
                mode=mode,
                name=y2_column.replace('_', ' ').title(),
                line=line,
                yaxis='y2'
            ))

        if not y2_column:
            fig.add_shape(
                type="line",
                x0=df['timestamps'].min(),
                x1=df['timestamps'].max(),
                y0=7.6,
                y1=7.6,
                line=dict(color="red", width=2, dash="dash"),
                yref="y",
                xref="x"
            )

            fig.add_shape(
                type="line",
                x0=df['timestamps'].min(),
                x1=df['timestamps'].max(),
                y0=-7.6,
                y1=-7.6,
                line=dict(color="green", width=2, dash="dash"),
                yref="y",
                xref="x"
            )

        total_days = max((df['timestamps'].max() - df['timestamps'].min()).days, 1)

        if real_time:
                layout = dict(
                height= 250,
                xaxis_title='Timestamp',
                yaxis=dict(
                    title=y1_column.replace('_', ' ').title(),
                    side='left'
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,       
                    xanchor="right",
                    x=1,
                    font=dict(size=10),
                    bgcolor="rgba(0,0,0,0)"
                ),
                legend_title='',
                hovermode='x unified',
                xaxis=dict(
                    range=[df['timestamps'].min(), df['timestamps'].max()],
                    type="date",
                    autorange=True
                ),
            )
        else:
            layout = dict(
                title=self.title if not y2_column else "Fluctuations Over Time",
                xaxis_title='Timestamp',
                yaxis=dict(
                    title=y1_column.replace('_', ' ').title(),
                    side='left'
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,       
                    xanchor="right",
                    x=1,
                    font=dict(size=10),
                    bgcolor="rgba(0,0,0,0)"
                ),
                legend_title='Legend',
                hovermode='x unified',
                xaxis=dict(
                    range=[df['timestamps'].min(), df['timestamps'].max()],
                    rangeselector=dict(
                        buttons=list([
                            dict(count=5, label="5m", step="minute", stepmode="backward"),
                            dict(count=10, label="10m", step="minute", stepmode="backward"),
                            dict(count=1, label="1h", step="hour", stepmode="backward"),
                            dict(count=1, label="1d", step="day", stepmode="backward"),
                            dict(count=total_days, label="All", step="day", stepmode="backward")
                        ])
                    ),
                    rangeslider=dict(visible=True,
                                    thickness=0.05,
                                    bgcolor='rgba(200, 200, 200, 0.2)', 
                                    bordercolor='rgba(0, 0, 0, 0.2)',
                                    borderwidth=1),
                    type="date",
                    autorange=False
                )
            )

        if y2_column:
            layout['yaxis2'] = dict(
                title=y2_column.replace('_', ' ').title(),
                overlaying='y',
                side='right'
            )

        fig.update_layout(**layout)

        return fig




if __name__=="__main__":
    file= "processed_output.csv"
    df= pd.read_csv(file)
    zn_plot= Plotter()
    fig= zn_plot.create_plot(df, 'outlet_volume', "inlet_volume")
    fig.show()