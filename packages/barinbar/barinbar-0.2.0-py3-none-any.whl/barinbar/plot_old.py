import dataclasses
import typing

import matplotlib.axes
import matplotlib.figure
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np
import pandas as pd
from matplotlib.cm import get_cmap
from matplotlib import font_manager


@dataclasses.dataclass
class BarinbarStyle:
    """Style for the bar-in-bar chart.
    background_color: Color for the background total bar.
    figsize: Size of the figure.
    fontsize: Fontsize for the main title.
    small_fontsize: Fontsize for the labels.
    fontname: Elegant font for the chart.
    colors: Dictionary mapping sub-categories to colors.
    """

    # Updated defaults based on .mplstyle
    background_color: str = "#E8EEF2"
    figsize: tuple[int, int] = (10, 8)
    fontsize: int = 16
    small_fontsize: int = 10
    fontname: str | None = "serif"
    colors: dict[str, str] = dataclasses.field(default_factory=dict)


# No change needed here, it will use the new defaults from the class

# Helper function type hints
T = typing.TypeVar('T')
Axes = matplotlib.axes.Axes
Figure = matplotlib.figure.Figure
Series = pd.Series
DataFrame = pd.DataFrame
default_color_palette = plt.get_cmap("Dark2")

def _prepare_data(
    df: DataFrame, category_col: str, subcategory_col: str, value_col: str, total_col: str
) -> tuple[Series, DataFrame]:
    """Aggregates totals and pivots values."""
    totals_agg = df.groupby(category_col)[total_col].first()
    values_pivot = df.pivot_table(
        index=category_col, columns=subcategory_col, values=value_col, fill_value=0
    )
    values_pivot = values_pivot.reindex(totals_agg.index)
    return totals_agg, values_pivot

def _setup_plot(style: BarinbarStyle) -> tuple[Figure, Axes]:
    """Initializes the matplotlib figure and axes."""
    fig, ax = plt.subplots(figsize=style.figsize)
    return fig, ax

def _plot_bars(
    ax: Axes,
    totals_agg: Series,
    values_pivot: DataFrame,
    style: BarinbarStyle
) -> None:
    """Plots the background and inner bars."""
    unique_categories = totals_agg.index
    unique_subcategories = values_pivot.columns
    n_categories = len(unique_categories)
    n_subcategories = len(unique_subcategories)
    index = np.arange(n_categories)

    default_colors = [default_color_palette(i) for i in range(min(n_subcategories, 10))]

    # --- Bar Width Calculations ---
    bar_width_total = 0.6
    gap_fraction = 0.1
    total_inner_width = bar_width_total * (1 - gap_fraction)
    bar_width_inner = total_inner_width / n_subcategories
    gap_width = (bar_width_total * gap_fraction) / (n_subcategories -1) if n_subcategories > 1 else 0

    # --- Plot Background ---
    ax.bar(index, totals_agg, bar_width_total*1.1, color=style.background_color, label="_nolegend_")

    # --- Plot Inner Bars ---
    for i, subcat in enumerate(unique_subcategories):
        subcat_values = values_pivot[subcat]
        offset = (i - (n_subcategories - 1) / 2) * (bar_width_inner + gap_width) - (gap_width/2 * (n_subcategories > 1))
        bar_color = style.colors.get(subcat, default_colors[i % len(default_colors)])
        ax.bar(
            index + offset,
            subcat_values,
            bar_width_inner,
            label=subcat,
            color=bar_color,
        )

def _add_labels(
    fig: Figure,
    ax: Axes,
    totals_agg: Series,
    values_pivot: DataFrame,
    style: BarinbarStyle
) -> None:
    """Adds numeric, subcategory, and category labels to the bars."""
    unique_categories = totals_agg.index
    unique_subcategories = values_pivot.columns
    n_categories = len(unique_categories)
    n_subcategories = len(unique_subcategories)
    index = np.arange(n_categories)

    value_label_padding = 3
    subcategory_label_padding = 4
    vertical_offset_for_total_label = 2

    bar_width_total = 0.6
    gap_fraction = 0.1
    total_inner_width = bar_width_total * (1 - gap_fraction)
    bar_width_inner = total_inner_width / n_subcategories

    # Add labels to inner bars
    container_offset = 1 # Background bar is container 0
    for i, subcat in enumerate(unique_subcategories):
        bars = ax.containers[i + container_offset] # Get the correct container
        numeric_labels = ax.bar_label(
            bars,
            fmt="$%gK",
            padding=value_label_padding,
            fontsize=style.small_fontsize,
            fontname=style.fontname
        )

        # Add rotated subcategory labels
        for bar, numeric_label in zip(bars, numeric_labels):
            height = bar.get_height()
            if height == 0: continue

            numeric_label_bbox = numeric_label.get_window_extent(renderer=fig.canvas.get_renderer())
            numeric_label_bbox_data = ax.transData.inverted().transform(numeric_label_bbox)
            numeric_label_top_y = numeric_label_bbox_data[1, 1]

            ax.text(
                bar.get_x() + bar.get_width() / 2,
                numeric_label_top_y + subcategory_label_padding,
                subcat,
                ha="center", va="bottom", rotation=90,
                fontsize=style.small_fontsize,
                fontname=style.fontname
            )

    # Add category/total labels above bars
    for i, (cat, total_val) in enumerate(totals_agg.items()):
        max_inner_bar_height = 0
        if len(ax.containers) > i + container_offset: # Ensure container exists
             # Access heights directly from the correct container for this category index 'i'
             # This assumes bars within a container correspond directly to category indices
             heights_in_containers = [c[i].get_height() for c in ax.containers[container_offset:] if len(c) > i]
             max_inner_bar_height = max(heights_in_containers) if heights_in_containers else 0


        label_base_y_pos = max(total_val, max_inner_bar_height)
        max_label_y = label_base_y_pos

        # Estimate highest point reached by labels
        for container_idx, container in enumerate(ax.containers):
             if container_idx < container_offset: continue # Skip background
             if len(container) <= i: continue # Ensure bar exists at this index

             bar = container[i] # Bar corresponding to category i in this container

             for txt in ax.texts:
                 text_x, text_y = txt.get_position()
                 # Check if text is associated with the current category's bars
                 if abs(text_x - (index[i])) < bar_width_total / 2:
                     potential_top = text_y # Approximation
                     max_label_y = max(max_label_y, potential_top)


        ax.text(
            index[i],
            max_label_y + vertical_offset_for_total_label,
            f"{cat}\n${total_val:g}K",
            ha="center", va="bottom",
            fontsize=style.small_fontsize,
            fontname=style.fontname,
            linespacing=1.5,
        )


def _format_plot(
    ax: Axes,
    totals_agg: Series,
    values_pivot: DataFrame,
    title: str,
    style: BarinbarStyle
) -> None:
    """Applies final formatting to the plot."""
    unique_categories = totals_agg.index
    unique_subcategories = values_pivot.columns
    n_categories = len(unique_categories)
    n_subcategories = len(unique_subcategories)
    index = np.arange(n_categories)

    ax.set_xticks(index)
    ax.set_xticklabels(unique_categories, fontname=style.fontname)
    ax.tick_params(axis="x", which="both", bottom=False, top=False, labelsize=style.small_fontsize)

    for side in ["top", "right", "left", "bottom"]:
        ax.spines[side].set_visible(False)
    ax.get_yaxis().set_visible(False)

    ax.set_title(title, loc="left", fontsize=style.fontsize, fontweight="bold", fontname=style.fontname)
    ax.legend(
        loc="upper right", frameon=False, ncol=n_subcategories,
        fontsize=style.small_fontsize, prop = font_manager.FontProperties(family=style.fontname, size=style.small_fontsize)
    )

    plt.tight_layout(rect=(0.0, 0.05, 1.0, 0.90))


def plot_bar_in_bar(
    df: DataFrame,
    category_col: str,
    subcategory_col: str,
    value_col: str,
    total_col: str,
    title: str,
    style: BarinbarStyle, # Removed default value here
):
    """Generates a bar-in-bar chart from a pandas DataFrame.

    Args:
        df: DataFrame containing the data.
        category_col: Column with main categories.
        subcategory_col: Column with sub-categories.
        value_col: Column with segment values.
        total_col: Column with total category values.
        title: Chart title.
        style: Styling options object.
    """
    # --- Workflow ---
    totals_agg, values_pivot = _prepare_data(df, category_col, subcategory_col, value_col, total_col)
    fig, ax = _setup_plot(style)
    _plot_bars(ax, totals_agg, values_pivot, style)
    fig.canvas.draw()
    _add_labels(fig, ax, totals_agg, values_pivot, style)
    _format_plot(ax, totals_agg, values_pivot, title, style)
    plt.show()


if __name__ == "__main__":
    data = {
        "Region": ["West"]*3 + ["East"]*3 + ["Central"]*3 + ["South"]*3,
        "Segment": ["Consumer", "Corporate", "Home Office"] * 4,
        "Revenue": [364, 232, 143, 357, 204, 131, 254, 158, 91, 196, 122, 74],
    }
    revenues = pd.DataFrame(data)
    region_totals = revenues.groupby("Region")["Revenue"].sum().reset_index()
    region_totals = region_totals.rename(columns={"Revenue": "TotalRevenue"})
    revenues = pd.merge(revenues, region_totals, on="Region")
    region_order = ["West", "East", "Central", "South"]
    segment_order = ["Consumer", "Corporate", "Home Office"]
    revenues["Region"] = pd.Categorical(revenues["Region"], categories=region_order, ordered=True)
    revenues["Segment"] = pd.Categorical(revenues["Segment"], categories=segment_order, ordered=True)
    revenues = revenues.sort_values(by=["Region", "Segment"])

    # Define explicit styles
    pastel_colors = {
        "Consumer": default_color_palette(0),
        "Corporate": default_color_palette(1),
        "Home Office": default_color_palette(2),
    }

    serif_style = BarinbarStyle(fontname='serif',colors=pastel_colors) # Example: Minimal style override


    plot_bar_in_bar(
        df=revenues,
        category_col="Region",
        subcategory_col="Segment",
        value_col="Revenue",
        total_col="TotalRevenue",
        title="Regions-Revenue by Segment (Serif)",
        style=serif_style, # Pass a different explicit style
    )
