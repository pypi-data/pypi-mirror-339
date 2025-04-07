from typing import Any, Optional, Sequence, Type, Union

import numpy as np
import pandas as pd
from sklearn.base import ClassifierMixin, RegressorMixin
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    mean_absolute_error,
    r2_score,
    root_mean_squared_error,
)
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures


def classification_report_to_df(
    y: Union[pd.Series, np.ndarray], y_pred: Union[pd.Series, np.ndarray]
) -> pd.DataFrame:
    """
    Converts a classification report into a DataFrame.

    This function generates a classification report (precision, recall, f1-score, support)
    using scikit-learn and returns it as a pandas DataFrame for easier inspection and formatting.

    Parameters
    ----------
    y : array-like (pandas.Series or numpy.ndarray)
        True class labels.
    y_pred : array-like (pandas.Series or numpy.ndarray)
        Predicted class labels.

    Returns
    -------
    pandas.DataFrame
        A DataFrame version of the classification report with metrics per class and averages.

    Notes
    -----
    - Useful for saving classification metrics or visualizing them in tabular format.
    - Includes weighted, macro, and micro averages.
    """
    # Generate the classification report as a dictionary
    report_dict = classification_report(y, y_pred, output_dict=True)

    # Convert to a pandas DataFrame
    df_report = pd.DataFrame(report_dict).transpose()

    return df_report


def confusion_matrix_to_df(
    y: Union[pd.Series, np.ndarray], y_pred: Union[pd.Series, np.ndarray]
) -> pd.DataFrame:
    """
    Converts a confusion matrix into a readable pandas DataFrame.

    This function computes the confusion matrix from true and predicted labels,
    then formats it as a DataFrame with understandable row and column labels.

    Parameters
    ----------
    y : array-like (pandas.Series or numpy.ndarray)
        True class labels.
    y_pred : array-like (pandas.Series or numpy.ndarray)
        Predicted class labels.

    Returns
    -------
    pandas.DataFrame
        A formatted confusion matrix with labels like 'expected-<class>' and 'predicted-<class>'.

    Notes
    -----
    - Automatically handles multi-class classification.
    - Replaces periods in class names with underscores for cleaner labels.
    """
    cm = confusion_matrix(y, y_pred)
    labels = np.unique(y)

    df_cm = pd.DataFrame(
        cm,
        index=[f"expected-{str(label).replace('.', '_')}" for label in labels],
        columns=[f"predicted-{str(label).replace('.', '_')}" for label in labels],
    )

    return df_cm


def create_polynomial_features(
    df: pd.DataFrame,
    columns: Optional[Sequence[str]] = None,
    degree: int = 3,
    skip: Optional[Sequence[str]] = None,
) -> pd.DataFrame:
    """
    Generates polynomial features from selected numerical columns in a DataFrame,
    while optionally skipping certain columns (e.g., target variables or IDs).

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing numerical data.
    columns : Sequence[str], optional
        A list of column names to use for generating polynomial features.
        If None, all columns are used (default: None).
    degree : int, optional
        The degree of polynomial features to generate (default: 3).
    skip : Sequence[str], optional
        List of column names to exclude from transformation but keep in the output (default: None).

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the generated polynomial features, along with skipped columns.

    Notes
    -----
    - Skipped columns (e.g., target, ID) are excluded from the transformation
      and reattached to the result.
    - Column names in the output are sanitized to remove spaces.
    - Uses scikit-learn's `PolynomialFeatures` under the hood.
    """
    # Copy the original DataFrame
    poly_features = df.copy()

    # Determine which columns to use
    if columns:
        poly_features = poly_features[columns]
    else:
        columns = list(poly_features.columns)

    # Store skipped columns
    skip_dict = {col: [] for col in skip or []}

    for col in skip or []:
        if col in columns:
            skip_dict[col] = poly_features[col]
            poly_features = poly_features.drop(columns=[col])
            columns.remove(col)

    # Generate polynomial features
    poly_transformer = PolynomialFeatures(degree=degree)
    poly_array = poly_transformer.fit_transform(poly_features)

    # Convert to DataFrame with generated feature names
    poly_features = pd.DataFrame(
        poly_array, columns=poly_transformer.get_feature_names_out(columns)
    )

    # Reattach skipped columns
    for col, poly_skip in skip_dict.items():
        poly_features[col] = poly_skip

    # Clean column names
    poly_features.columns = poly_features.columns.str.replace(" ", "_")

    return poly_features


def encode_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Encodes categorical variables using label encoding for binary categories
    and one-hot encoding for all other categorical variables.

    This function applies label encoding to categorical columns with two or fewer unique values
    and one-hot encoding to all other categorical variables.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing categorical and numerical data.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with categorical variables encoded.

    Notes
    -----
    - Label encoding is applied to columns with 2 or fewer unique values.
    - One-hot encoding is applied to all other categorical variables.
    - The function ensures that categorical values are transformed properly without data leakage.
    """
    tmp_df = df.copy()
    le = LabelEncoder()

    # Iterate through the columns
    for col in tmp_df:
        if tmp_df[col].dtype == "object":
            # Apply Label Encoding if the column has 2 or fewer unique categories
            if tmp_df[col].nunique() <= 2:
                tmp_df[col] = le.fit_transform(tmp_df[col])

    # Apply one-hot encoding for remaining categorical variables
    return pd.get_dummies(tmp_df)


def get_predict_proba_df(
    model: ClassifierMixin,
    X: Union[pd.DataFrame, np.ndarray],
    y: Union[pd.Series, np.ndarray],
    y_pred: Union[pd.Series, np.ndarray],
    label: int = 1,
) -> pd.DataFrame:
    """
    Constructs a DataFrame containing prediction results, including probability scores
    and classification types (true positive, false positive, etc.).

    Parameters
    ----------
    model : ClassifierMixin
        A trained classification model that implements `predict_proba`.
    X : pandas.DataFrame or numpy.ndarray
        Feature matrix used for prediction.
    y : pandas.Series or numpy.ndarray
        True labels.
    y_pred : pandas.Series or numpy.ndarray
        Predicted labels.
    label : int, optional
        Class label index for which to extract predicted probabilities (default: 1).

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the following columns:
        - "TARGET": actual class labels.
        - "prediction": predicted class labels.
        - "probality_score": predicted probability for the selected label.
        - "prediction_type": classification type ("TP", "FP", "FN", "TN", etc.).

    Notes
    -----
    - Assumes a helper function `get_prediction_type(pred, true)` is available to classify outcomes.
    - Can be useful for inspecting prediction confidence and building calibration plots.
    """
    predict_proba = model.predict_proba(X)[:, label]

    predict_proba_df = pd.DataFrame()
    predict_proba_df["TARGET"] = y.to_numpy()
    predict_proba_df["prediction"] = y_pred
    predict_proba_df["probality_score"] = predict_proba
    predict_proba_df["prediction_type"] = predict_proba_df.apply(
        lambda row: get_prediction_type(row["prediction"], row["TARGET"]), axis=1
    )

    return predict_proba_df


def get_metrics_df(
    model: RegressorMixin,
    X_train: Union[pd.DataFrame, np.ndarray],
    y_train: Union[pd.Series, np.ndarray],
    y_train_pred: Union[pd.Series, np.ndarray],
    X_test: Union[pd.DataFrame, np.ndarray],
    y_test: Union[pd.Series, np.ndarray],
    y_test_pred: Union[pd.Series, np.ndarray],
) -> pd.DataFrame:
    """
    Computes key regression metrics for training and testing sets.

    This function evaluates a model's performance on both training and testing sets
    and returns a summary DataFrame containing common regression metrics.

    Parameters
    ----------
    model : RegressorMixin
        A trained regression model implementing the `score` method.
    X_train : array-like
        Features used for training.
    y_train : array-like
        Ground truth labels for training.
    y_train_pred : array-like
        Predicted labels for the training set.
    X_test : array-like
        Features used for testing.
    y_test : array-like
        Ground truth labels for testing.
    y_test_pred : array-like
        Predicted labels for the testing set.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with metrics for both Train and Test sets, including:
        - Model Score (R² by default)
        - Accuracy (for classification tasks)
        - RMSE
        - MAE
        - R² Score

    Notes
    -----
    - Accuracy is included, but only relevant for classification tasks.
    - RMSE is computed via a custom helper function.
    - All values are rounded to 2 decimal places.
    """
    metrics_dict = {
        "Model Score": [
            round(model.score(X_train, y_train), 2),
            round(model.score(X_test, y_test), 2),
        ],
        "Accuracy": [
            round(accuracy_score(y_train, y_train_pred), 2),
            round(accuracy_score(y_test, y_test_pred), 2),
        ],
        "RMSE": [
            round(root_mean_squared_error(y_train, y_train_pred), 2),
            round(root_mean_squared_error(y_test, y_test_pred), 2),
        ],
        "MAE": [
            round(mean_absolute_error(y_train, y_train_pred), 2),
            round(mean_absolute_error(y_test, y_test_pred), 2),
        ],
        "R² Score": [
            round(r2_score(y_train, y_train_pred), 2),
            round(r2_score(y_test, y_test_pred), 2),
        ],
    }

    return pd.DataFrame(metrics_dict, index=["Train", "Test"])


def get_prediction_type(prediction: int, target: int) -> str:
    """
    Determines the classification outcome type for a binary prediction.

    This function compares a predicted label and the true label (target)
    and returns a string indicating whether the result is:
    - true_positive
    - true_negative
    - false_positive
    - false_negative

    Parameters
    ----------
    prediction : int
        The predicted label (usually 0 or 1).
    target : int
        The true label (usually 0 or 1).

    Returns
    -------
    str
        A string indicating the prediction type:
        - "true_positive"
        - "true_negative"
        - "false_positive"
        - "false_negative"
        - "unknown" (in case of invalid input)

    Notes
    -----
    - This function assumes binary classification with values in {0, 1}.
    - It returns "unknown" if the inputs are not in expected form.
    """
    if prediction and target:
        return "true_positive"
    elif not prediction and not target:
        return "true_negative"
    elif prediction and not target:
        return "false_positive"
    elif not prediction and target:
        return "false_negative"
    else:
        return "unknown"


def get_stats(
    df: pd.DataFrame,
    ascending: Optional[bool] = True,
    columns: Optional[Sequence[str]] = None,
    missing_only: Optional[bool] = False,
    with_outliers: Optional[bool] = False,
) -> pd.DataFrame:
    """
    Computes statistical summaries for numerical columns in a DataFrame.

    This function analyzes numerical columns and computes missing values,
    outlier statistics, and descriptive statistics.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing numerical and categorical data.
    ascending : bool, optional
        Whether to sort the output DataFrame in ascending order of missing values (default: True).
    columns : Sequence[str], optional
        A list of specific numerical columns to analyze. If not provided, all numerical columns are used.
    missing_only : bool, optional
        If True, only numerical columns with missing values are included in the output (default: False).
    with_outliers : bool, optional
        If True, calculates outlier statistics using the IQR method (default: False).

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing:
        - Percentage of missing values.
        - (Optional) Outlier statistics.
        - (Optional) Descriptive statistics (min, max, mean, median, variance, etc.).

    Notes
    -----
    - Only numerical columns are analyzed (categorical columns are excluded).
    - If `missing_only=True`, columns without missing values are excluded.
    - If `with_outliers=True`, outliers are detected using the IQR method:
      * Lower bound = Q1 - 1.5 * IQR
      * Upper bound = Q3 + 1.5 * IQR
      * Counts of values below and above these bounds are recorded.
    - If `with_metrics=True`, additional statistics such as mean, variance, and skewness are included.
    - Results are sorted by percentage of missing values.
    """
    bound_lower_list = []
    bound_upper_list = []
    nb_outliers_list = []

    # Select only numerical columns
    num_df = df.drop(columns=df.select_dtypes(include=["object"]).columns)

    if missing_only:
        # Identify and drop columns without missing values
        num_df = num_df.drop(columns=num_df.columns[num_df.isna().sum() == 0])

    if columns is None:
        columns = num_df.columns

    # Compute outlier statistics if requested
    for col in columns:
        if with_outliers:
            q1 = num_df[col].quantile(0.25)
            q3 = num_df[col].quantile(0.75)
            iqr = q3 - q1

            _bound_lower = q1 - 1.5 * iqr
            _bound_upper = q3 + 1.5 * iqr

            _nb_of_lower = len(num_df[num_df[col] < _bound_lower])
            _nb_of_upper = len(num_df[num_df[col] > _bound_upper])

            bound_lower_list.append(_bound_lower)
            bound_upper_list.append(_bound_upper)
            nb_outliers_list.append(f"{_nb_of_lower} - {_nb_of_upper}")

    # Compute missing value percentages
    data = {
        "% Missing Values": round(
            (num_df[columns].isna().sum() / len(num_df)) * 100, 2
        ),
    }

    # Add outlier statistics if requested
    if with_outliers:
        data.update(
            {
                "Nb. Outliers": nb_outliers_list,
                "Lower Outlier Bound": bound_lower_list,
                "Upper Outlier Bound": bound_upper_list,
            }
        )

    # Compute descriptive statistics if requested
    data.update(
        {
            "% Null Values": round(
                (num_df[columns].eq(0).sum() / len(num_df)) * 100, 2
            ),
            "Minimum": num_df[columns].min(),
            "Maximum": num_df[columns].max(),
            "Mean": num_df[columns].mean(),
            "Median": num_df[columns].median(),
            "Mode": [num_df[c].mode()[0] for c in columns],
            "Variance": num_df[columns].var(),
            "Standard Deviation": num_df[columns].std(),
            "Skewness": num_df[columns].skew(),
            "Kurtosis": num_df[columns].kurtosis(),
        }
    )

    return pd.DataFrame(data).sort_values(by="% Missing Values", ascending=ascending)


def get_missing_stats(
    df: pd.DataFrame,
    ascending: Optional[bool] = True,
    columns: Optional[Sequence[str]] = None,
    missing_only: Optional[bool] = False,
) -> pd.DataFrame:
    """
    Computes missing value statistics for categorical (object-type) columns in a DataFrame.

    This function analyzes categorical columns and computes the percentage of missing values.
    It can optionally exclude columns without missing values.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing categorical and numerical data.
    ascending : bool, optional
        Whether to sort the output DataFrame in ascending order of missing values (default: True).
    columns : Sequence[str], optional
        A list of specific categorical columns to analyze. If not provided, all categorical columns are used.
    missing_only : bool, optional
        If True, only categorical columns with missing values are included in the output (default: False).

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing:
        - Percentage of missing values per categorical column.

    Notes
    -----
    - If `missing_only=True`, columns without missing values are excluded from the results.
    - Results are sorted by percentage of missing values.
    """
    # Select only categorical columns
    tmp_df = df.copy()

    if missing_only:
        # Identify columns without missing values and drop them
        tmp_df = tmp_df.drop(columns=tmp_df.columns[tmp_df.isna().sum() == 0])

    # Use specified columns or default to all remaining categorical columns
    if columns is None:
        columns = tmp_df.columns

    # Compute missing value percentages
    data = {
        "% Missing Values": round((tmp_df[columns].isna().sum() / len(tmp_df)) * 100, 2)
    }

    return pd.DataFrame(data).sort_values(by="% Missing Values", ascending=ascending)


def impute_missing_values(
    df: pd.DataFrame,
    columns: Sequence[str],
    na_threshold: float = 0.1,
    imputer_cls: Type[SimpleImputer] = SimpleImputer,
    **kwargs: Any,
) -> pd.DataFrame:
    """
    Imputes missing values in selected columns of a DataFrame using a specified imputer.

    This function first removes rows where the percentage of missing values in a column
    exceeds a given threshold, then applies an imputer to fill the remaining missing values.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing numerical and/or categorical data.
    columns : Sequence[str]
        The list of column names to be imputed.
    na_threshold : float, optional
        The maximum allowed percentage of missing values per column before
        dropping rows containing those missing values (default: 0.1, i.e., 10%).
    imputer_cls : Type[SimpleImputer], optional
        The imputer class to use for missing value imputation (default: `SimpleImputer`).
    **kwargs : Any
        Additional keyword arguments passed to the imputer's constructor.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the same column names as the original selection,
        but with missing values imputed.

    Notes
    -----
    - If a column has more than `na_threshold` fraction of missing values,
      all rows with missing values in that column are dropped before imputation.
    - The imputer is instantiated dynamically using `imputer_cls(**kwargs)`,
      allowing flexibility in choosing different imputation strategies.
    - The function returns a DataFrame with the same column names but without missing values.
    """
    # Create a new DataFrame with the selected columns
    tmp_df = df.copy()[columns]

    # Identify columns where NaN proportion exceeds the threshold
    na_columns = tmp_df.columns[tmp_df.isna().mean() > na_threshold]

    # Drop rows with NaN values in these columns
    tmp_df = tmp_df.dropna(subset=na_columns)

    # Impute missing values and return as a DataFrame with the same column names
    return pd.DataFrame(
        imputer_cls(**kwargs).fit_transform(tmp_df),
        columns=tmp_df.columns,
    )


def list_unique_modalities_by_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Lists unique modalities (categories) for each categorical column in the DataFrame.

    This function inspects all columns of type 'object' or 'category' and returns a
    summary table listing the unique non-null values for each such column.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing categorical and/or numerical variables.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with two columns:
        - 'column': Name of the categorical column.
        - 'modalities': A comma-separated string of unique values (sorted).

    Notes
    -----
    - Null values are excluded from the modality list.
    - The values are converted to strings and sorted alphabetically.
    - Useful for exploring and auditing categorical variables.
    """
    cols = df.select_dtypes(include=["object", "category"]).columns
    summary = []

    for col in cols:
        values = sorted(df[col].dropna().unique())
        summary.append({"column": col, "modalities": ", ".join(map(str, values))})

    summary_df = pd.DataFrame(summary)

    if not summary:
        summary_df = pd.DataFrame(columns=["column", "modalities"])

    return summary_df.sort_values(by="column").set_index("column")


def sort_columns_by_filled_ratio(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Sorts a DataFrame's columns by the percentage of non-missing values.

    Columns with the highest proportion of filled values appear first.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with columns sorted by completeness (non-NaN ratio).
    """
    # Calculer le taux de remplissage (valeurs non NaN) pour chaque colonne
    ratio_filled = df.notna().mean()

    # Trier les colonnes par taux de remplissage décroissant
    columns_sorted_list = ratio_filled.sort_values(ascending=False).index

    # Réorganiser le DataFrame avec ces colonnes triées
    return df[columns_sorted_list]


def summarize_columns_by_prefix(
    df: pd.DataFrame, prefixes: Sequence[str]
) -> pd.DataFrame:
    """
    Summarizes columns in a DataFrame that start with given prefixes.

    This function scans all column names in the DataFrame and groups them
    by the specified prefixes, returning a summary of matching columns per prefix.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing column names to be analyzed.
    prefixes : Sequence[str]
        A list or sequence of string prefixes to match against column names.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with two columns:
        - 'prefix': The prefix string being matched.
        - 'matching_columns': A comma-separated string of all matching column names.

    Notes
    -----
    - If no columns match a prefix, the 'matching_columns' field will be an empty string.
    - This is useful for exploring grouped variable sets (e.g., "EXT_SOURCE", "DAYS_", "FLAG_").
    """
    summary = []

    for prefix in prefixes:
        matching = [col for col in df.columns if col.startswith(prefix)]
        summary.append(
            {
                "prefix": prefix,
                "matching_columns": ", ".join(matching) if matching else "",
            }
        )

    return pd.DataFrame(summary).set_index("prefix")
