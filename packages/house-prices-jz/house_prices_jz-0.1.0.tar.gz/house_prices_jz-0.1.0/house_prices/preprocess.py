import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder


def drop_missing_columns(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """Drop columns with more than a threshold percentage of missing values.

    Args:
        df: Input DataFrame to clean.
        threshold: Fraction of rows that must be non-null to keep a column.

    Returns:
        DataFrame with columns having >threshold% missing values dropped.
    """
    thresh = threshold * len(df)
    return df.dropna(thresh=thresh, axis=1)


def preprocess_features(
        X: pd.DataFrame,
        cont_cols: list[str],
        cat_cols: list[str],
        scaler: StandardScaler,
        encoder: OneHotEncoder
        ) -> np.ndarray:
    """Preprocess continuous and categorical features into a single array.

    Args:
        X: Input DataFrame with features.
        cont_cols: List of continuous column names.
        cat_cols: List of categorical column names.
        scaler: Fitted StandardScaler for continuous features.
        encoder: Fitted OneHotEncoder for categorical features.

    Returns:
        NumPy array with scaled continuous and encoded categorical features.
    """
    X_cont_scaled = scaler.transform(X[cont_cols])
    X_cat_encoded = encoder.transform(X[cat_cols])
    return np.hstack((X_cont_scaled, X_cat_encoded))
