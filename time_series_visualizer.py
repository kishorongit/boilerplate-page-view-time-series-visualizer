import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"]).set_index("date")

# Clean data
mask = (
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
)
df = df[mask]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(16, 5))
    
    df["value"].plot(ax=ax, color="red")
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.xticks(rotation = 0, horizontalalignment="center")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Create a new DataFrame for grouping by year and month
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Group by year and month, calculate average page views
    df_bar = df_bar.groupby(['year', 'month'])["value"].mean().unstack()
    df_bar = df_bar[['January', 'February', 'March', 'April', 'May',
                                'June', 'July', 'August', 'September', 'October', 'November', 'December']]

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(8, 7))
    df_bar.plot(kind='bar', ax=ax)
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    with plt.rc_context({'font.family': 'sans serif','font.size': 9, 'font.weight': 'ultralight'}):
        fig, axes = plt.subplots(1, 2, figsize=(16, 6), dpi=300)
        
        # Yearly boxplot
        sns.boxplot(data=df_box, x="year", y="value", hue="year", palette="tab10", 
            legend=False, flierprops={"marker": "+", "markersize": 3}, ax=axes[0])
        axes[0].set_title("Year-wise Box Plot (Trend)")
        axes[0].set_xlabel("Year")
        axes[0].set_ylabel("Page Views")
        axes[0].set_yticks(range(0, 200_001, 20_000))
        
        # Monthly boxplot
        month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        month_colors = ["#EA96A3", "#E19154", "#B89C49", "#98A246", "#60AE47", "#4AAE8A", 
            "#4BABA4", "#4FABBC", "#6DAEE2", "#B6A8EB", "#DF8FE7", "#E890C6"]
        sns.set_palette( month_colors ) 
        sns.boxplot(data=df_box, x="month", y="value", hue="month", hue_order=month_order, 
            order=month_order, flierprops={"marker": "+", "markersize":3}, ax=axes[1])
        axes[1].set_title("Month-wise Box Plot (Seasonality)")
        axes[1].set_xlabel("Month")
        axes[1].set_ylabel("Page Views")
        axes[1].set_yticks(range(0, 200_001, 20_000))

        fig.tight_layout(pad=3)

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
