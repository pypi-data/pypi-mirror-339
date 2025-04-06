import pandas as pd
import numpy as np
import joblib
from house_prices.preprocess import preprocess_features


def make_predictions(input_data: pd.DataFrame) -> np.ndarray:
    """Generate predictions from input data using a trained model.

    Args:
        input_data: Input DataFrame with features.

    Returns:
        Array of predicted house prices.
    """
    cont_cols = ['LotArea', 'GrLivArea']
    cat_cols = ['Neighborhood', 'MSZoning']

    scaler = joblib.load('../models/scaler.joblib')
    encoder = joblib.load('../models/encoder.joblib')
    model = joblib.load('../models/model.joblib')

    X_proc = preprocess_features(
        input_data,
        cont_cols,
        cat_cols,
        scaler,
        encoder
        )
    y_pred = model.predict(X_proc)
    return np.clip(y_pred, a_min=1, a_max=None)
