import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_log_error
from house_prices.preprocess import drop_missing_columns, preprocess_features


def compute_rmsle(
        y_true: np.ndarray,
        y_pred: np.ndarray,
        precision: int = 2
        ) -> float:
    """Compute Root Mean Squared Logarithmic
    Error between true and predicted values.

    Args:
        y_true: Array of actual target values.
        y_pred: Array of predicted target values.
        precision: Number of decimal places to round the result.

    Returns:
        Rounded RMSLE value.
    """
    rmsle = np.sqrt(mean_squared_log_error(y_true, y_pred))
    return round(rmsle, precision)


def load_and_split_data(
        file_path: str
        ) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Load CSV data and split into training and validation sets.

    Args:
        file_path: Path to the CSV file.

    Returns:
        Tuple of (X_train, X_val, y_train, y_val).
    """
    df = pd.read_csv(file_path)
    X = df.drop(columns=['SalePrice'])
    y = df['SalePrice']
    return train_test_split(X, y, test_size=0.2, random_state=42)


def build_model(data: pd.DataFrame) -> dict[str, float]:
    """Model building and evaluation.

    Args:
        data: Input DataFrame (unused, kept for API consistency).

    Returns:
        Dictionary with model performance metrics.
    """
    X_train, X_val, y_train, y_val = load_and_split_data('../data/train.csv')
    X_train = drop_missing_columns(X_train, 0.8)
    X_val = X_val[X_train.columns]
    cont_cols = ['LotArea', 'GrLivArea']
    cat_cols = ['Neighborhood', 'MSZoning']

    scaler = StandardScaler()
    encoder = OneHotEncoder(
        sparse_output=False,
        handle_unknown='ignore',
        drop='first'
        )

    scaler.fit(X_train[cont_cols])
    encoder.fit(X_train[cat_cols])

    X_train_proc = preprocess_features(
        X_train,
        cont_cols,
        cat_cols,
        scaler,
        encoder
        )
    X_val_proc = preprocess_features(
        X_val,
        cont_cols,
        cat_cols,
        scaler,
        encoder
        )

    model = LinearRegression()
    model.fit(X_train_proc, y_train)

    joblib.dump(model, '../models/model.joblib')
    joblib.dump(scaler, '../models/scaler.joblib')
    joblib.dump(encoder, '../models/encoder.joblib')

    y_pred_val = model.predict(X_val_proc)
    y_pred_val = np.clip(y_pred_val, a_min=1, a_max=None)
    rmsle = compute_rmsle(y_val, y_pred_val)
    return {'rmsle': rmsle}
