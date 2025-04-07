import io
import math
from copy import deepcopy
from typing import Optional, Sequence, Union

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import shap
from PIL import Image
from scipy.stats import gaussian_kde
from sklearn.metrics import roc_auc_score, roc_curve


def fig_to_image(fig: plt.Figure) -> Image.Image:
    """
    Converts a Matplotlib figure to a PIL Image.

    This function captures a Matplotlib figure (`plt.Figure`) in memory,
    saves it as a PNG, and returns it as a PIL Image object.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The Matplotlib figure to convert.

    Returns
    -------
    PIL.Image.Image
        A deep-copied PIL image of the rendered figure.

    Notes
    -----
    - The function uses an in-memory buffer (`io.BytesIO`) to avoid writing to disk.
    - The image is returned as a deep copy to ensure the buffer is not needed afterward.
    - Useful for exporting plots into reports, GUIs, or storing images in datasets.
    """
    with io.BytesIO() as bytes_io:
        fig.savefig(bytes_io, format="png")
        bytes_io.seek(0)
        return deepcopy(Image.open(bytes_io))


def plot_bar(
    df: pd.DataFrame,
    key: str,
    bins: Optional[int] = 30,
    figsize: Optional[tuple[int, int]] = (6, 6),
    kde: Optional[bool] = True,
) -> None:
    """
    Plots a histogram for a numerical column.

    This function visualizes the distribution of a numerical variable using a histogram
    with an optional Kernel Density Estimate (KDE) curve.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing numerical data.
    key : str
        The column to plot.
    bins : int, optional
        The number of bins for the histogram (default: 30).
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    kde : bool, optional
        Whether to display the Kernel Density Estimate (KDE) curve (default: True).

    Returns
    -------
    None
        The function displays the histogram but does not return a value.

    Notes
    -----
    - KDE helps visualize the distribution shape more smoothly.
    - The x-axis represents the numerical values of the selected column.
    - The y-axis represents the frequency of occurrences.
    """
    # Create the histogram
    plt.figure(figsize=figsize)

    sns.histplot(df[key], bins=bins, kde=kde)

    plt.xlabel(f"{key} (units)")
    plt.ylabel("Frequency")

    plt.title(f"Histogram of {key}")

    plt.show()


def plot_bar_missings(
    df: pd.DataFrame,
    bin_width: Optional[int] = 5,
    figsize: Optional[tuple[int, int]] = (6, 6),
) -> None:
    """
    Plots a bar chart showing the distribution of missing values across columns.

    This function groups columns into bins based on their percentage of missing values
    and visualizes the distribution.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing missing values.
    bin_width : int, optional
        The bin width for grouping missing value percentages (default: 5%).
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).

    Returns
    -------
    None
        The function displays the bar chart but does not return a value.

    Notes
    -----
    - Missing values are computed as a percentage of total rows per column.
    - Columns are grouped into bins (default: 5% intervals).
    - Helps identify the distribution of missing values across columns.
    """
    # Compute the percentage of missing values per column
    missing_percentage = df.isnull().mean() * 100

    # Create bins (default: 0% to 100% in 5% increments)
    bins = range(0, 101, bin_width)
    missing_binned = pd.cut(missing_percentage, bins=bins, right=False)

    # Count the number of columns in each bin
    missing_distribution = missing_binned.value_counts().sort_index()

    # Plot the histogram
    plt.figure(figsize=figsize)

    sns.barplot(
        x=missing_distribution.index.astype(str),
        y=missing_distribution.values,
        color="royalblue",
    )

    plt.xticks(rotation=90)
    plt.xlabel("Filling Rate (%)")
    plt.ylabel("Number of Columns")
    plt.title("Column Filling Rate Distribution (5% bins)")

    plt.show()


def plot_bar_unique_classes(
    df: pd.DataFrame,
    figsize: Optional[tuple[int, int]] = (6, 6),
) -> None:
    """
    Plots a bar chart showing the number of unique values per categorical column.

    This function selects categorical (object-type) columns from the DataFrame,
    counts the number of unique values for each, and visualizes the distribution
    using a bar chart with annotations and a dynamic color scale.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing categorical data.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).

    Returns
    -------
    None
        The function displays the bar chart but does not return a value.

    Notes
    -----
    - Only categorical (`object` dtype) columns are analyzed.
    - Columns are sorted in descending order of unique value counts.
    - The number of unique values is displayed on top of each bar.
    """
    # Select categorical (object) columns
    qualitative_columns = df.select_dtypes("object")

    # Count unique values per categorical column
    unique_counts = qualitative_columns.apply(pd.Series.nunique, axis=0)

    # Sort columns by the number of unique values
    unique_counts = unique_counts.sort_values(ascending=False)

    # Normalize the color scale based on unique value counts
    norm = plt.Normalize(unique_counts.min(), unique_counts.max())
    colors = plt.cm.coolwarm(norm(unique_counts.values))

    x = unique_counts.index
    y = unique_counts.values

    # Plot the bar chart with color mapping
    plt.figure(figsize=figsize)
    ax = sns.barplot(
        x=x,
        y=y,
        hue=x,  # Assign hue for different colors
        legend=False,
        palette=list(colors),
    )

    # Annotate each bar with the unique value count
    for index, value in enumerate(unique_counts.values):
        ax.text(
            index,
            value + 1,
            str(value),
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color="black",
        )

    plt.xticks(rotation=90)
    plt.xlabel("Categorical Columns")
    plt.ylabel("Number of Unique Values")
    plt.title("Unique Values per Categorical Column")

    plt.show()


def plot_boxplot(
    df: pd.DataFrame,
    column: str,
    figsize: Optional[tuple[int, int]] = (6, 6),
) -> None:
    """
    Displays a boxplot for a specified column.

    This function generates a boxplot to visualize the distribution,
    central tendency, and potential outliers in the given column.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    column : str
        The column to visualize.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).

    Returns
    -------
    None
        The function displays the plot but does not return a value.

    Notes
    -----
    - NaN values are ignored in the boxplot.
    - The boxplot is colored orange for better visibility.
    """
    _tmp_df = df[~df[column].isna()].copy()[[column]]

    plt.figure(figsize=figsize)

    sns.boxplot(x=_tmp_df[column], color="orange")

    plt.xlabel("Nombre d'éléments")
    plt.title(f"Boxplot de {column}")

    plt.show()


def plot_pie(
    df: pd.DataFrame,
    key: str,
    figsize: Optional[tuple[int, int]] = (6, 6),
) -> None:
    """
    Plots a pie chart showing the distribution of a categorical variable.

    This function visualizes the proportion of unique values in the specified column
    as a pie chart.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing the data.
    key : str
        The categorical column to visualize.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).

    Returns
    -------
    None
        The function displays the pie chart but does not return a value.

    Notes
    -----
    - Uses a pastel color palette for better readability.
    - Displays percentages with one decimal place.
    - The pie chart starts at a 90-degree angle for alignment.
    """
    # Count occurrences of unique values in the column
    target_counts = df[key].value_counts()

    # Define a pastel color palette
    colors = sns.color_palette("pastel")[0 : len(target_counts)]

    # Create the pie chart
    plt.figure(figsize=figsize)

    plt.pie(
        target_counts,
        labels=target_counts.index,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
    )

    plt.title(f"Distribution of {key}")

    plt.show()


def plot_pie_column_types(
    df: pd.DataFrame,
    figsize: Optional[tuple[int, int]] = (6, 6),
) -> None:
    """
    Plots a pie chart showing the distribution of column data types in a DataFrame.

    This function visualizes the proportion of different data types present in the DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).

    Returns
    -------
    None
        The function displays the pie chart but does not return a value.

    Notes
    -----
    - Uses a pastel color palette for better readability.
    - Displays percentages with one decimal place.
    - Helps understand the data structure by visualizing the distribution of types.
    """
    # Count the number of columns by data type
    dtype_counts = df.dtypes.value_counts()

    # Define a pastel color palette
    colors = sns.color_palette("pastel")[0 : len(dtype_counts)]

    # Prepare labels with types and number of columns
    labels = [
        f"{dtype} ({count})"
        for dtype, count in zip(dtype_counts.index, dtype_counts.values)
    ]

    # Create the pie chart
    plt.figure(figsize=figsize)

    plt.pie(
        dtype_counts,
        autopct="%1.1f%%",
        colors=colors,
        labels=labels,
        startangle=90,
    )

    plt.title("Distribution of Columns by Data Type")

    plt.show()


def plot_heatmap_chi2(
    df: pd.DataFrame,
    X: str,
    Y: str,
    figsize: Optional[tuple[int, int]] = (6, 6),
) -> float:
    """
    Displays a chi-squared (χ²) contingency heatmap between two categorical variables.

    This function computes a contingency table, calculates the expected frequencies
    under independence, and visualizes the relative contribution of each cell to
    the chi-squared statistic.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing categorical variables.
    X : str
        The first categorical variable (rows of the contingency table).
    Y : str, optional
        The second categorical variable (columns of the contingency table.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).

    Returns
    -------
    None
        The function displays a heatmap but does not return a value.

    Notes
    -----
    - The chi-squared test measures the association between categorical variables.
    - The heatmap colors represent the relative contribution of each cell to the
      chi-squared statistic.
    - The table is normalized by the total chi-squared value for interpretability.
    """
    cont = df[[X, Y]].pivot_table(
        aggfunc=len,
        index=X,
        columns=Y,
        margins=True,
        margins_name="total",
    )

    tx = cont.loc[:, ["total"]]
    ty = cont.loc[["total"], :]

    c = cont.fillna(0)  # On remplace les valeurs nulles par 0
    n = len(df)

    indep = tx.dot(ty) / n
    measure = (c - indep) ** 2 / indep
    xi_n = measure.sum().sum()
    table = measure / xi_n

    plt.figure(figsize=figsize)

    sns.heatmap(
        table.iloc[:-1, :-1],
        annot=c.iloc[:-1, :-1],
        cbar=False,
        cmap="Oranges",
        fmt="d",
        linewidths=0.5,
    )

    plt.title(f"Heatmap des catégories '{X}' et '{Y}'")

    plt.xlabel(Y)
    plt.ylabel(X)

    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)

    plt.show()


def plot_heatmap_corr(
    df: pd.DataFrame,
    target: str,
    ascending: Optional[bool] = True,
    columns: Optional[Sequence[str]] = None,
    figsize: Optional[tuple[int, int]] = (6, 6),
    limit: Optional[int] = 10,
) -> None:
    """
    Plots a Pearson correlation heatmap for the most correlated numerical features with a target variable.

    This function selects the top correlated numerical columns (by absolute correlation)
    with the target variable and displays a heatmap.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing numerical and categorical data.
    target : str
        The target variable to compute correlations against.
    ascending : bool, optional
        Whether to sort correlations in ascending order (default: True).
    columns : Sequence[str], optional
        A list of specific numerical columns to include. If None, selects the most correlated columns.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    limit : int, optional
        The number of top correlated features to display (default: 10).

    Returns
    -------
    None
        The function displays the correlation heatmap but does not return a value.

    Notes
    -----
    - Only numerical columns are considered for correlation calculations.
    - If `columns=None`, the function selects the top correlated features with the target.
    - Uses Pearson correlation for linear relationships.
    - The heatmap masks the upper triangle for better readability.
    """
    # Select only numerical columns
    df_numeric = df.select_dtypes(include=["number"])

    if columns is None:
        # Compute correlation with target and drop NaN values
        tmp_corr = df_numeric.corr()[target].dropna()
        # Sort by absolute correlation and select the top features
        tmp_cols = tmp_corr.sort_values(ascending=ascending)

        if target in tmp_cols:
            tmp_cols = tmp_cols.drop(target)

        columns = list(tmp_cols.iloc[0:limit].index) + [target]

    # Compute the Pearson correlation matrix
    corr_matrix = df_numeric[columns].corr(method="pearson")

    # Create a mask to hide the upper triangle
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

    plt.figure(figsize=figsize)

    sns.heatmap(
        corr_matrix,
        annot=True,
        mask=mask,
        cbar=False,
        cmap="Oranges",
        fmt=".2f",
        linewidths=0.5,
    )

    plt.title("Pearson Correlation Matrix")

    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)

    plt.show()


def plot_by_categories(
    df: pd.DataFrame,
    column: str,
    target: str,
    figsize: Optional[tuple[int, int]] = (6, 6),
    palette: Optional[str] = "tab10",
) -> None:
    """
    Plots the distribution of a numerical variable by categories in a target column.

    This function generates a Kernel Density Estimate (KDE) plot for a numerical column,
    grouped by categories in the target column. Each category is visualized with a
    distinct color.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing categorical and numerical data.
    column : str
        The numerical column to visualize.
    target : str
        The categorical column used to group the KDE plots.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    palette : str, optional
        The color palette used for the categories (default: "tab10").

    Returns
    -------
    None
        The function displays the KDE plot but does not return a value.

    Notes
    -----
    - Each category in the target column gets a unique color from the palette.
    - The KDE plot shows the density distribution of the numerical variable.
    - A legend is added to indicate which color corresponds to each category.
    """
    plt.figure(figsize=figsize)

    categories = df[target].unique()

    # Generate a dynamic color palette
    colors = sns.color_palette(palette, len(categories))

    legends = []

    # KDE plot for each category
    for i, val in enumerate(categories):
        color = colors[i]
        label = f"{target} == {val}"

        sns.kdeplot(
            df.loc[df[target] == val, column], color=color, fill=True, label=label
        )

        legends.append(mpatches.Patch(color=color, label=label))

    # Add legend
    plt.legend(handles=legends)

    # Labeling of the plot
    plt.xlabel(column)
    plt.ylabel("Density")

    plt.title(f"Distribution of {column} by {target}")

    plt.show()


def plot_bar_by_target(
    df: pd.DataFrame,
    column: str,
    target: str,
    figsize: Optional[tuple[int, int]] = (6, 6),
    num_bins: Optional[int] = 10,
    target_coef: Optional[int] = 100,
) -> None:
    """
    Plots a bar chart showing the relationship between a numerical variable and a target.

    This function bins the numerical column into equal-width intervals, then calculates
    the mean value of the target variable for each bin and visualizes the result as a bar plot.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing numerical and categorical data.
    column : str
        The numerical column to bin and analyze.
    target : str
        The target variable whose mean is calculated per bin.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    num_bins : int, optional
        The number of bins to divide the numerical column into (default: 10).
    target_coef : int, optional
        A scaling factor to adjust the target values in the plot (default: 100).

    Returns
    -------
    None
        The function displays the bar chart but does not return a value.

    Notes
    -----
    - The numerical column is divided into `num_bins` equally spaced bins.
    - The mean of the target variable is computed for each bin.
    - The y-axis represents the scaled mean value of the target.
    - Binned labels on the x-axis are rotated for better readability.
    """
    plt.figure(figsize=figsize)

    # Copy necessary columns
    bar_data = df.copy()[[column, target]]

    # Define bin range
    _min = math.floor(bar_data[column].min())
    _max = math.ceil(bar_data[column].max())

    # Bin the numerical column
    bar_data[f"{column}_BINNED"] = pd.cut(
        bar_data[column], bins=np.linspace(_min, _max, num=(num_bins + 1))
    )

    # Compute mean target value for each bin
    bar_groups = bar_data.groupby(f"{column}_BINNED", observed=False).mean()

    # Plot the bar chart
    plt.bar(bar_groups.index.astype(str), bar_groups[target] * target_coef)

    # Formatting
    plt.xticks(rotation=75)
    plt.xlabel(column)
    plt.ylabel(target)
    plt.title(f"{target} by {column}")

    plt.show()


def plot_scatter_corr(
    df: pd.DataFrame,
    v1: str,
    v2: str,
    color_line: Optional[str] = "darkorange",
    color_map: Optional[str] = "plasma",
    figsize: Optional[tuple[int, int]] = (6, 6),
    limit: Optional[int] = 100000,
) -> None:
    """
    Plots a scatter plot with density-based coloring and a regression line.

    This function visualizes the relationship between two numerical variables
    with a scatter plot where point colors reflect density, and a regression
    line is added for trend analysis.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing numerical data.
    v1 : str
        The first numerical variable (x-axis).
    v2 : str
        The second numerical variable (y-axis).
    color_line : str, optional
        The color of the regression line (default: "darkorange").
    color_map : str, optional
        The colormap used to color points based on density (default: "plasma").
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    limit : int, optional
        The maximum number of rows to use from the dataset (default: 100000).

    Returns
    -------
    None
        The function displays the scatter plot but does not return a value.

    Notes
    -----
    - Missing values in `v1` and `v2` are dropped before plotting.
    - Point colors are determined based on density estimation using `gaussian_kde`.
    - A regression line is added using Seaborn's `regplot`.
    """
    # Remove missing values and limit the number of rows
    df_clean = df.dropna(subset=[v1, v2]).iloc[:limit, :]

    # Compute density for each point
    xy = np.vstack([df_clean[v1], df_clean[v2]])
    density = gaussian_kde(xy)(xy)

    # Create the figure
    plt.figure(figsize=figsize)

    # Plot scatter points colored by density
    plt.scatter(
        df_clean[v1],
        df_clean[v2],
        c=density,
        cmap=color_map,
        alpha=0.6,
    )

    # Add regression line
    sns.regplot(
        data=df_clean,
        x=v1,
        y=v2,
        scatter=False,
        line_kws={"linewidth": 3, "color": color_line},
    )

    # Add labels and title
    plt.xlabel(v1)
    plt.ylabel(v2)
    plt.title(f"Relationship between {v1} and {v2} with Density-based Coloring")

    # Show the plot
    plt.show()


def plot_probability_distribution_per_prediction_type(
    X: pd.DataFrame,
    binwidth: Optional[float] = 0.025,
    categories_to_include: Optional[Sequence[str]] = None,
    figsize: Optional[tuple[int, int]] = (6, 6),
    title: Optional[str] = "Distribution des probabilités par type de prédiction",
    palette: Optional[str] = "tab10",
    show: Optional[bool] = True,
) -> None:
    """
    Plots the distribution of prediction probabilities by prediction type.

    This function displays a histogram of predicted probabilities grouped by
    prediction type (e.g., true_positive, false_negative, etc.). Useful for
    analyzing model confidence by classification outcome.

    Parameters
    ----------
    X : pandas.DataFrame
        A DataFrame containing at least the following columns:
        - 'prediction_type': classification of each prediction.
        - 'probality_score': predicted probability for the positive class.
    binwidth : float, optional
        The width of the histogram bins (default: 0.025).
    categories_to_include : Sequence[str], optional
        A list of prediction types to include (e.g., ["true_positive", "false_positive"]).
        If None, all available types are included.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    title : str, optional
        Title of the plot (default: "Distribution des probabilités par type de prédiction").
    palette : str, optional
        Seaborn color palette for the histogram bars (default: "tab10").
    show : bool, optional
        Whether to display the plot immediately with `plt.show()` (default: True).

    Returns
    -------
    None
        Displays a Seaborn histogram grouped by prediction type.

    Raises
    ------
    ValueError
        If required columns are missing from the input DataFrame.
    """
    # Vérification de la présence des colonnes nécessaires
    required_columns = {"prediction_type", "probality_score"}
    missing_columns = required_columns - set(X.columns)
    if missing_columns:
        raise ValueError(
            f"Les colonnes suivantes sont absentes de X: {missing_columns}"
        )

    # Inclure les catégories spécifiées
    if categories_to_include is None:
        x_filtered = X
    else:
        x_filtered = X[X["prediction_type"].isin(categories_to_include)]

    # Vérifier que les données ne sont pas vides après filtrage
    if x_filtered.empty:
        print("Toutes les lignes ont été filtrées, il n'y a rien à tracer.")
        return

    # Créer la figure
    plt.figure(figsize=figsize)

    # Tracer l'histogramme
    sns.histplot(
        data=x_filtered,
        x="probality_score",
        hue="prediction_type",
        binwidth=binwidth,
        legend=True,
        palette=palette,
    )

    plt.title(title)

    if show:
        plt.show()


def plot_roc_curve(
    y: Union[pd.Series, np.ndarray],
    y_proba: Union[pd.Series, np.ndarray],
    figsize: Optional[tuple[int, int]] = (6, 6),
    show: Optional[bool] = True,
) -> None:
    """
    Plots the ROC curve and displays the AUC score.

    This function computes and plots the Receiver Operating Characteristic (ROC)
    curve for a binary classifier, based on the true labels and predicted probabilities.

    Parameters
    ----------
    y : array-like (pandas.Series or numpy.ndarray)
        True binary labels.
    y_proba : array-like (pandas.Series or numpy.ndarray)
        Predicted probabilities for the positive class.
    figsize : tuple of int, optional
        Size of the matplotlib figure (default: (6, 6)).
    show : bool, optional
        Whether to immediately display the plot using plt.show() (default: True).

    Returns
    -------
    None
        Displays the ROC curve.

    Notes
    -----
    - The diagonal line represents a random classifier (AUC = 0.5).
    - AUC (Area Under the Curve) is shown in the legend for model evaluation.
    """
    fpr, tpr, _ = roc_curve(y, y_proba)
    auc = roc_auc_score(y, y_proba)

    plt.figure(figsize=figsize)

    plt.plot(fpr, tpr, label=f"AUC = {auc:.2f}")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray")

    plt.xlabel("Taux de faux positifs (FPR)")
    plt.ylabel("Taux de vrais positifs (TPR)")
    plt.title("Courbe ROC")
    plt.legend()

    if show:
        plt.show()


def plot_shap_waterfall(shap_values: shap.Explanation, vars_to_show) -> None:
    if not vars_to_show:
        raise ValueError("Veuillez spécifier les variables à afficher.")

    # Filtrer les valeurs
    mask = [feature in vars_to_show for feature in shap_values.feature_names]

    filtered_sv = shap.Explanation(
        values=shap_values.values[mask],
        base_values=shap_values.base_values,
        data=shap_values.data[mask],
        feature_names=[
            name for name in shap_values.feature_names if name in vars_to_show
        ],
    )

    # Affichage waterfall custom
    shap.plots.waterfall(filtered_sv)
