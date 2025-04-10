import dataclasses
import typing
from typing import Literal

# Import gridspec
from matplotlib import font_manager
import matplotlib.axes
import matplotlib.colors
import matplotlib.figure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Import the squarify library
import squarify


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
    background_color: str = "#D0DDE6"
    figsize: tuple[int, int] = (10, 8)
    fontsize: int = 16
    small_fontsize: int = 10
    fontname: str | None = "serif"
    colors: dict[str, str] = dataclasses.field(default_factory=dict)


# No change needed here, it will use the new defaults from the class

# Helper function type hints
T = typing.TypeVar("T")
Axes = matplotlib.axes.Axes
Figure = matplotlib.figure.Figure
Series = pd.Series
DataFrame = pd.DataFrame
default_color_palette = plt.get_cmap("Dark2")


def _prepare_data(
    df: DataFrame, category_col: str, subcategory_col: str, value_col: str, total_col: str
) -> tuple[Series, DataFrame]:
    """Aggregates totals, pivots values, and sorts categories."""
    # Ensure consistent sorting for categories and subcategories
    df[category_col] = pd.Categorical(df[category_col], categories=df[category_col].unique(), ordered=True)
    df[subcategory_col] = pd.Categorical(df[subcategory_col], categories=df[subcategory_col].unique(), ordered=True)
    df = df.sort_values(by=[category_col, subcategory_col])

    totals_agg = df.groupby(category_col, observed=False)[total_col].first()  # Use observed=False with Categorical
    values_pivot = df.pivot_table(
        index=category_col,
        columns=subcategory_col,
        values=value_col,
        fill_value=0,
        observed=False,  # Use observed=False
    )
    # Reindex necessary if some categories have no subcategory data after pivot
    values_pivot = values_pivot.reindex(totals_agg.index, fill_value=0)
    return totals_agg, values_pivot


def _setup_plot(style: BarinbarStyle) -> tuple[Figure, Axes]:
    """Initializes the matplotlib figure and axes."""
    fig, ax = plt.subplots(figsize=style.figsize)
    return fig, ax


def _plot_bars(
    ax: Axes, totals_agg: Series, values_pivot: DataFrame, style: BarinbarStyle, back_ground_width: str
) -> None:
    """Plots the background and inner bars with consistent width."""
    unique_categories = totals_agg.index
    unique_subcategories = values_pivot.columns
    n_categories = len(unique_categories)
    n_subcategories = len(unique_subcategories)
    index = np.arange(n_categories)

    default_colors = [default_color_palette(i) for i in range(min(n_subcategories, 10))]

    # --- Bar Width Calculations ---
    # Define a single width for all bars (background and inner)
    bar_width = 0.6 / n_subcategories  # Adjust base width as needed, divided for spacing
    inner_gap = bar_width * 0.1  # Small gap between inner bars

    # --- Plot Background ---
    # Background bar centered at index, with the standard bar_width
    total_width = n_subcategories * bar_width + max(0, n_subcategories - 1) * inner_gap
    ax.bar(
        index,
        totals_agg,
        total_width if back_ground_width == "total" else bar_width,
        color=style.background_color,
        label="_nolegend_",
        zorder=1,
        alpha=0.7,
    )

    # --- Plot Inner Bars ---
    # Calculate the total span of the inner bars group
    total_inner_span = n_subcategories * bar_width + max(0, n_subcategories - 1) * inner_gap
    # Calculate the offset for the center of the *first* inner bar relative to the category index
    start_offset = -total_inner_span / 2 + bar_width / 2

    for i, subcat in enumerate(unique_subcategories):
        subcat_values = values_pivot[subcat]
        # Calculate the center position for this specific inner bar
        current_offset = start_offset + i * (bar_width + inner_gap)

        bar_color = style.colors.get(subcat, default_colors[i % len(default_colors)])
        ax.bar(
            index + current_offset,  # Apply the calculated offset
            subcat_values,
            bar_width,  # Use the standard bar_width
            label=subcat,
            color=bar_color,
            alpha=0.85,
            edgecolor="grey",
            linewidth=0.6,
            zorder=2,
        )


def _add_labels(fig: Figure, ax: Axes, totals_agg: Series, values_pivot: DataFrame, style: BarinbarStyle) -> None:
    """Adds numeric, subcategory (rotated), and category labels to the bars."""
    unique_categories = totals_agg.index
    unique_subcategories = values_pivot.columns
    n_categories = len(unique_categories)
    n_subcategories = len(unique_subcategories)
    index = np.arange(n_categories)

    value_label_padding = 3
    subcategory_label_padding = 4  # Padding between numeric and subcategory label
    vertical_offset_for_total_label = 2  # Padding above highest label for category/total

    # --- Reusing width calculations from _plot_bars ---
    bar_width = 0.6 / n_subcategories
    inner_gap = bar_width * 0.1
    total_inner_span = n_subcategories * bar_width + max(0, n_subcategories - 1) * inner_gap
    start_offset = -total_inner_span / 2 + bar_width / 2
    # --- End width calculations ---

    # --- Store Labels Temporarily ---
    all_placed_labels = []  # Store all text objects added

    # Add labels to inner bars
    container_offset = 1  # Background bar is container 0
    for i, subcat in enumerate(unique_subcategories):
        if i + container_offset >= len(ax.containers):
            continue
        bars = ax.containers[i + container_offset]

        # Add numeric labels
        numeric_labels = ax.bar_label(
            bars, fmt="$%gK", padding=value_label_padding, fontsize=style.small_fontsize, fontname=style.fontname
        )
        all_placed_labels.extend(numeric_labels)

        # Add rotated subcategory labels above numeric labels
        for bar_idx, (bar, numeric_label) in enumerate(zip(bars, numeric_labels, strict=False)):
            height = bar.get_height()
            if height == 0:
                continue

            # Get the top position of the numeric label in data coordinates *after drawing*
            fig.canvas.draw()  # Ensure layout is computed
            numeric_label_bbox = numeric_label.get_window_extent()  # Use default renderer
            numeric_label_bbox_data = ax.transData.inverted().transform(numeric_label_bbox)
            numeric_label_top_y = numeric_label_bbox_data[1, 1]

            # Add rotated subcategory label
            rotated_label = ax.text(
                bar.get_x() + bar.get_width() / 2,
                numeric_label_top_y + subcategory_label_padding,
                subcat,
                ha="center",
                va="bottom",
                rotation=90,
                fontsize=style.small_fontsize,
                fontname=style.fontname,
            )
            all_placed_labels.append(rotated_label)

    # --- Add category/total labels above all other labels ---
    fig.canvas.draw()  # Crucial: Ensure all label positions are finalized before getting extents
    max_label_y_per_category_idx = {}  # Stores max Y extent for each category index

    # Find the highest point reached by any label within each category's vertical space
    for label_obj in all_placed_labels:
        label_bbox = label_obj.get_window_extent()
        label_bbox_data = ax.transData.inverted().transform(label_bbox)
        label_top_y = label_bbox_data[1, 1]
        label_x_center = label_bbox_data[0, 0] + (label_bbox_data[1, 0] - label_bbox_data[0, 0]) / 2  # Center X

        # Find the closest category index based on x position
        closest_category_idx = np.argmin(np.abs(index - label_x_center))

        # Update the max Y for this category index
        current_max_y = max_label_y_per_category_idx.get(closest_category_idx, -np.inf)  # Initialize with -inf
        max_label_y_per_category_idx[closest_category_idx] = max(current_max_y, label_top_y)

    # Now place the category/total labels
    for i, (cat, total_val) in enumerate(totals_agg.items()):
        # Determine base Y from the highest bar (background or inner)
        background_bar_height = 0
        if len(ax.containers) > 0 and len(ax.containers[0]) > i:
            background_bar_height = ax.containers[0][i].get_height()

        max_inner_bar_height = 0
        heights_in_containers = []
        for container_idx, c in enumerate(ax.containers):
            if container_idx < container_offset:
                continue
            if len(c) > i:
                heights_in_containers.append(c[i].get_height())
        max_inner_bar_height = max(heights_in_containers) if heights_in_containers else 0

        bar_top_y = max(background_bar_height, max_inner_bar_height)

        # Use the max Y extent found for this category, or the bar top if no labels exist
        max_existing_label_y = max_label_y_per_category_idx.get(i, bar_top_y)

        # Ensure the final label position is at least above the bar top
        final_y_pos = max(max_existing_label_y, bar_top_y) + vertical_offset_for_total_label

        ax.text(
            index[i],  # Center the category label on the category index
            final_y_pos,
            f"{cat}\n${total_val:g}K",
            ha="center",
            va="bottom",
            fontsize=style.small_fontsize,
            fontname=style.fontname,
            linespacing=1.5,
        )


def _format_plot(ax: Axes, totals_agg: Series, values_pivot: DataFrame, title: str, style: BarinbarStyle) -> None:
    """Applies final formatting to the plot."""
    unique_categories = totals_agg.index
    # unique_subcategories = values_pivot.columns # Not needed here anymore
    n_categories = len(unique_categories)
    # n_subcategories = len(unique_subcategories) # Not needed here anymore
    index = np.arange(n_categories)

    ax.set_xticks(index)
    # ax.set_xticklabels(unique_categories, fontname=style.fontname) # Labels now added above bars
    ax.set_xticklabels([])  # Remove category names from x-axis ticks
    ax.tick_params(axis="x", which="both", bottom=False, top=False, labelbottom=False)  # Hide x-axis labels and ticks

    for side in ["top", "right", "left", "bottom"]:
        ax.spines[side].set_visible(False)
    ax.get_yaxis().set_visible(False)

    ax.set_title(title, loc="left", fontsize=style.fontsize, fontweight="bold", fontname=style.fontname)

    # Improve legend handling
    handles, labels = ax.get_legend_handles_labels()
    # Ensure correct order based on original subcategory order from pivot table
    ordered_handles_labels = []
    subcat_order = values_pivot.columns.tolist()
    label_map = dict(zip(labels, handles, strict=False))
    for subcat in subcat_order:
        if subcat in label_map and not subcat.startswith("_nolegend_"):
            ordered_handles_labels.append((label_map[subcat], subcat))

    # Filter out potential '_nolegend_' entries if any slipped through
    # filtered_handles_labels = [(h, l) for h, l in zip(handles, labels, strict=False) if not l.startswith("_nolegend_")]
    if ordered_handles_labels:
        handles, labels = zip(*ordered_handles_labels, strict=False)
        ax.legend(
            handles,
            labels,
            loc="upper right",
            frameon=False,
            ncol=len(labels),  # Use actual number of labels for ncol
            fontsize=style.small_fontsize,
            prop=font_manager.FontProperties(family=style.fontname, size=style.small_fontsize),
        )
    elif ax.get_legend() is not None:
        ax.get_legend().remove()  # Remove legend if no valid entries

    # Adjust layout slightly more generously
    plt.tight_layout(rect=(0.0, 0.05, 1.0, 0.92))


def plot_bar_in_bar(
    df: DataFrame,
    category_col: str,
    subcategory_col: str,
    value_col: str,
    total_col: str,
    title: str,
    style: BarinbarStyle,
    back_ground_width: Literal["total", "single"],
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
    _plot_bars(ax, totals_agg, values_pivot, style, back_ground_width)
    fig.canvas.draw()
    _add_labels(fig, ax, totals_agg, values_pivot, style)
    _format_plot(ax, totals_agg, values_pivot, title, style)
    plt.show()


def plot_treemap_bars(
    df: DataFrame,
    category_col: str,
    group_col: str,
    value_col: str,
    title: str,
    figsize: tuple[int, int] = (12, 6),
    value_format_str: str = "${value}K",
    fontname: str | None = "serif",
    base_palette: str = "Dark2",  # Added palette option
):
    """Generates horizontally arranged treemaps with consistent widths
      and heights proportional to the total value of each group.

    Args:
        df: DataFrame containing the data.
        category_col: Column with categories within each treemap (e.g., 'Region').
        group_col: Column used to group data into separate treemaps (e.g., 'Segment').
        value_col: Column with values determining rectangle size and subplot height.
        title: Overall chart title.
        figsize: Size of the figure (width, base_height). Height scales automatically.
        value_format_str: F-string format for labels (use {value}).
        fontname: Font name for labels and titles.
        base_palette: Matplotlib colormap name for coloring categories consistently.
    """
    # --- Data Preparation ---
    # Ensure correct data types and ordering for reliable grouping/sorting
    df[group_col] = pd.Categorical(df[group_col])
    df[category_col] = pd.Categorical(df[category_col])
    df = df.sort_values(by=[group_col, category_col])

    # Calculate Total Value per Group for height ratios and SORTING
    group_totals = df.groupby(group_col, observed=True)[value_col].sum()
    if group_totals.empty:
        print(f"Warning: No data found after grouping by '{group_col}'. Cannot plot.")
        return
    # Sort groups by total value, descending (highest first)
    group_totals = group_totals.sort_values(ascending=False)

    # --- Color Mapping for Categories ---
    unique_categories = df[category_col].cat.categories.tolist()
    palette = plt.get_cmap(base_palette)
    category_colors = {
        cat: palette(i / max(1, len(unique_categories) - 1))  # Normalize index for cmap
        for i, cat in enumerate(unique_categories)
    }

    # --- Treemap Plotting with Manual Positioning ---
    groups = group_totals.index  # Use the sorted index
    n_groups = len(groups)

    # --- Manual Layout Calculations ---
    max_total = group_totals.max()
    # Avoid division by zero if max_total is 0
    height_ratios = group_totals / max_total if max_total > 0 else pd.Series(1, index=group_totals.index)

    total_fig_width, base_fig_height = figsize
    fig = plt.figure(figsize=(total_fig_width, base_fig_height))

    # --- Adjust width allocation (using previous "thinner" settings) ---
    total_plot_width_fraction = 0.7
    total_gap_width_fraction = 1.0 - total_plot_width_fraction
    subplot_width_norm = total_plot_width_fraction / n_groups if n_groups > 0 else 0
    horizontal_gap_norm = total_gap_width_fraction / (n_groups + 1) if n_groups > 0 else 0

    # --- Plotting Loop ---
    for i, group in enumerate(groups):  # Iterate through SORTED groups
        # Calculate position and size for this subplot's Axes
        left = ((i + 1) * horizontal_gap_norm) + (i * subplot_width_norm)
        width = subplot_width_norm
        height = height_ratios[group] * 0.85  # Scale height proportionally, leave top margin
        bottom = 0.05

        ax = fig.add_axes([left, bottom, width, height])

        # Filter data for the current group
        group_data = df[df[group_col] == group].copy()
        # Sort *within* the treemap (optional but good)
        group_data = group_data.sort_values(value_col, ascending=False)

        # Prepare data for squarify
        sizes = group_data[value_col].values
        current_categories = group_data[category_col].values
        labels = [
            f"{cat}\n{value_format_str.format(value=rev)}" for cat, rev in zip(current_categories, sizes, strict=False)
        ]
        colors = [category_colors.get(cat, "#808080") for cat in current_categories]

        if len(sizes) > 0:
            squarify.plot(
                sizes=sizes,
                label=labels,
                color=colors,
                alpha=0.8,
                ax=ax,
                text_kwargs={"fontsize": 9, "fontname": fontname},
            )
        # Add group total to the title
        ax.set_title(
            f"{group}\n(Total: {value_format_str.format(value=group_totals[group])})",
            fontsize=10,
            fontname=fontname,
            pad=5,
        )
        ax.axis("off")

    # Add suptitle above the manually placed axes
    fig.suptitle(title, fontsize=16, fontweight="bold", fontname=fontname, y=0.98)

    plt.show()


if __name__ == "__main__":
    # --- Data Preparation (same as before) ---
    data = {
        "Region": ["West"] * 3 + ["East"] * 3 + ["Central"] * 3 + ["South"] * 3,
        "Segment": ["Consumer", "Corporate", "Home Office"] * 4,
        "Revenue": [364, 232, 143, 357, 204, 131, 254, 158, 91, 196, 122, 74],
    }
    revenues = pd.DataFrame(data)
    # Calculate TotalRevenue dynamically
    region_totals = revenues.groupby("Region")["Revenue"].sum().reset_index()
    region_totals = region_totals.rename(columns={"Revenue": "TotalRevenue"})
    revenues = pd.merge(revenues, region_totals, on="Region")

    # Note: Explicit sorting with pd.Categorical is now handled within _prepare_data

    # --- Call the new treemap function ---
    plot_treemap_bars(
        df=revenues.copy(),  # Pass a copy to avoid modifying original df
        category_col="Segment",  # Swapped group/category for better visual
        group_col="Region",
        value_col="Revenue",
        title="Regional Revenue Distribution by Segment (Treemap)",
        value_format_str="${value}K",
        base_palette="tab10",
    )

    # --- Bar-in-bar calls ---
    pastel_colors_bar = {
        "Consumer": default_color_palette(0),
        "Corporate": default_color_palette(1),
        "Home Office": default_color_palette(2),
    }
    serif_style = BarinbarStyle(fontname="serif", colors=pastel_colors_bar)

    print("Plotting Bar-in-Bar (Total Background)...")
    plot_bar_in_bar(
        df=revenues.copy(),  # Pass a copy
        category_col="Region",
        subcategory_col="Segment",
        value_col="Revenue",
        total_col="TotalRevenue",
        title="Regions-Revenue by Segment (Background=Total Width)",
        style=serif_style,
        back_ground_width="total",
    )
    print("Plotting Bar-in-Bar (Single Background)...")
    plot_bar_in_bar(
        df=revenues.copy(),  # Pass a copy
        category_col="Region",
        subcategory_col="Segment",
        value_col="Revenue",
        total_col="TotalRevenue",
        title="Regions-Revenue by Segment (Background=Single Width)",
        style=serif_style,
        back_ground_width="single",
    )

    # --- Old treemap code within __main__ is now removed ---
