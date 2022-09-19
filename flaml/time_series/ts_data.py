import copy
import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Callable, Dict, Generator, Union

import pandas as pd
import numpy as np
from pandas import DataFrame, Series

from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer

from .feature import monthly_fourier_features


@dataclass
class TimeSeriesDataset:
    train_data: pd.DataFrame
    time_idx: str
    time_col: str
    target_names: List[str]
    frequency: str
    test_data: pd.DataFrame
    time_varying_known_categoricals: List[str] = field(default_factory=lambda: [])
    time_varying_known_reals: List[str] = field(default_factory=lambda: [])
    time_varying_unknown_categoricals: List[str] = field(default_factory=lambda: [])
    time_varying_unknown_reals: List[str] = field(default_factory=lambda: [])

    def __init__(
        self,
        train_data: pd.DataFrame,
        time_col: str,
        target_names: Union[str, List[str]],
        time_idx: str = "index",
        test_data: Optional[pd.DataFrame] = None,
    ):
        self.train_data = train_data
        self.time_col = time_col
        self.time_idx = time_idx
        self.target_names = (
            [target_names] if isinstance(target_names, str) else list(target_names)
        )
        assert isinstance(self.target_names, list)
        assert len(self.target_names)

        self.frequency = pd.infer_freq(train_data[time_col].unique())
        assert (
            self.frequency is not None
        ), "Only time series of regular frequency are currently supported."

        float_cols = list(train_data.select_dtypes(include=["floating"]).columns)
        self.time_varying_known_reals = list(set(float_cols) - set(self.target_names))

        self.time_varying_known_categoricals = list(
            set(train_data.columns)
            - set(self.time_varying_known_reals)
            - set(self.target_names)
            - {time_col}
        )
        if test_data is not None:
            self.test_data = test_data
        else:
            self.test_data = pd.DataFrame(columns=self.train_data.columns)

    def add_test_data(self, X: pd.DataFrame) -> "TimeSeriesDataset":
        assert self.time_col in X.columns
        train_data = self.all_data[
            self.all_data[self.time_col] < X[self.time_col].min()
        ]
        return TimeSeriesDataset(
            train_data, self.time_col, self.target_names, self.time_idx, X
        )

    @property
    def all_data(self):
        return pd.concat([self.train_data, self.test_data], axis=0)

    @property
    def regressors(self):
        return self.time_varying_known_categoricals + self.time_varying_known_reals

    @property
    def end_date(self):
        test_len = 0 if self.test_data is None else len(self.test_data)
        data = self.test_data if test_len else self.train_data
        return data.iloc[-1][self.time_col]

    def _X(self, df: pd.DataFrame):
        features = [col for col in df.columns if col not in self.target_names]
        return df[features]

    def _y(self, df: pd.DataFrame):
        if len(self.target_names) > 1:
            return df[self.target_names]
        else:
            out = df[self.target_names[0]]
            if out.dtype == object:
                out = out.astype(str)
            return out

    @property
    def X_train(self) -> pd.DataFrame:
        return self._X(self.train_data)

    @property
    def X_val(self) -> pd.DataFrame:
        return self._X(self.test_data)

    @property
    def y_train(self) -> pd.DataFrame:
        return self._y(self.train_data)

    @property
    def y_val(self) -> pd.DataFrame:
        return self._y(self.test_data)

    def next_scale(self) -> int:
        scale_map = {"D": 7, "MS": 12}
        return scale_map.get(self.frequency, 8)

    def known_features_to_floats(
        self, train: bool, drop_first: bool = True
    ) -> np.ndarray:
        # this is a bit tricky as shapes for train and test data must match, so need to encode together
        combined = pd.concat(
            [
                self.train_data,
                self.test_data,
            ],
            ignore_index=True,
        )

        cat_one_hots = pd.get_dummies(
            combined[self.time_varying_known_categoricals],
            columns=self.time_varying_known_categoricals,
            drop_first=drop_first,
        ).values.astype(float)

        reals = combined[self.time_varying_known_reals].values.astype(float)
        both = np.concatenate([reals, cat_one_hots], axis=1)

        if train:
            return both[: len(self.train_data)]
        else:
            return both[len(self.train_data) :]

    def unique_dimension_values(self) -> np.ndarray:
        # this is the same set for train and test data, by construction
        return self.combine_dims(self.train_data).unique()

    def combine_dims(self, df):
        return df.apply(lambda row: tuple([row[d] for d in self.dimensions]), axis=1)

    def to_univariate(self) -> Dict[str, "TimeSeriesDataset"]:
        """
        Convert a multivariate TrainingData  to a dict of univariate ones
        @param df:
        @return:
        """

        train_dims = self.combine_dims(self.train_data)
        test_dims = self.combine_dims(self.test_data)

        out = {}
        for d in train_dims.unique():
            out[d] = copy.copy(self)
            out[d].train_data = self.train_data[train_dims == d]
            out[d].test_data = self.test_data[test_dims == d]
        return out

    def move_validation_boundary(self, steps: int) -> "TimeSeriesDataset":
        out = copy.copy(self)
        if steps > 0:
            out.train_data = pd.concat([self.train_data, self.test_data[:steps]])
            out.test_data = self.test_data[steps:]
        elif steps < 0:
            out.train_data = self.train_data[:steps]
            out.test_data = pd.concat([self.train_data[steps:], self.test_data])

        return out

    def cv_train_val_sets(
        self, n_splits: int, val_length: int, step_size: int
    ) -> Generator["TimeSeriesDataset", None, None]:
        max_index = len(self.train_data) - 1
        for i in range(n_splits):
            out = copy.copy(self)
            val_start = max_index - (n_splits - i - 1) * step_size - val_length
            out.train_data = self.train_data[:val_start]
            out.test_data = self.train_data[val_start : val_start + val_length]
            yield out

    def filter(self, filter_fun: Callable) -> "TimeSeriesDataset":
        if filter_fun is None:
            return self
        out = copy.copy(self)
        out.train_data = self.train_data[filter_fun]
        out.test_data = self.test_data[filter_fun]
        return out

    def prettify_prediction(self, y_pred: Union[pd.DataFrame, pd.Series, np.ndarray]):
        if self.test_data is not None and len(self.test_data):
            assert len(y_pred) == len(self.test_data)

            if isinstance(y_pred, np.ndarray):
                y_pred = pd.DataFrame(
                    data=y_pred, columns=self.target_names, index=self.test_data.index
                )
            elif isinstance(y_pred, pd.Series):
                assert len(self.target_names) == 1, "Not enough columns in y_pred"
                y_pred.name = self.target_names[0]
                y_pred = pd.DataFrame(y_pred)
                y_pred.index = self.test_data.index
            elif isinstance(y_pred, pd.DataFrame):
                y_pred.index = self.test_data.index

            if self.time_col not in y_pred.columns:
                y_pred[self.time_col] = self.test_data[self.time_col]

        else:
            if isinstance(y_pred, np.ndarray):
                raise ValueError("Can't enrich np.ndarray as self.test_data is None")
            elif isinstance(y_pred, pd.Series):
                assert len(self.target_names) == 1, "Not enough columns in y_pred"
                y_pred = pd.DataFrame({self.target_names[0]: y_pred})
            # TODO auto-create the timestamps for the time column instead of throwing
            raise NotImplementedError(
                "Need a non-None test_data for this to work, for now"
            )

        assert isinstance(y_pred, pd.DataFrame)
        assert self.time_col in y_pred.columns
        assert all([t in y_pred.columns for t in self.target_names])
        return y_pred

    def merge_prediction_with_target(
        self, y_pred: Union[pd.DataFrame, pd.Series, np.ndarray]
    ):
        y_pred = self.prettify_prediction(y_pred)
        return pd.concat(
            [self.train_data[[self.time_col] + self.target_names], y_pred], axis=0
        )


def enrich(
    X: Union[int, TimeSeriesDataset, pd.DataFrame],
    fourier_degree: Optional[int],
    time_col: str,
    frequency: Optional[str] = None,
    test_end_date: Optional[datetime.datetime] = None,
    remove_constants: bool = False,
):
    if isinstance(X, int):
        X = create_forward_frame(frequency, X, test_end_date, time_col)

    if fourier_degree is None:
        fourier_degree = 4

    if isinstance(X, TimeSeriesDataset):
        return enrich_dataset(X, fourier_degree, remove_constants)

    return enrich_dataframe(X, fourier_degree, remove_constants)


def enrich_dataframe(
    df: Union[pd.DataFrame, pd.Series],
    fourier_degree: int,
    remove_constants: bool = False,
) -> pd.DataFrame:

    if isinstance(df, pd.Series):
        df = pd.DataFrame(df)

    new_cols = []
    for col in df.columns:
        if df[col].dtype.name == "datetime64[ns]":
            extras = monthly_fourier_features(df[col], fourier_degree)
            extras.columns = [f"{col}_{c}" for c in extras.columns]
            extras.index = df.index
            new_cols.append(extras)
            date_feat = date_feature_dict(df[col])
            if remove_constants:
                re_date_feat = {
                    k: v for k, v in date_feat.items() if v.nunique(dropna=False) >= 2
                }
            else:
                re_date_feat = date_feat

            date_feat = pd.DataFrame(re_date_feat, index=df.index)
            new_cols.append(date_feat)

    return pd.concat([df] + new_cols, axis=1, verify_integrity=True)


def enrich_dataset(
    X: TimeSeriesDataset, fourier_degree: int = 0, remove_constants: bool = False
) -> TimeSeriesDataset:
    new_train = enrich_dataframe(X.train_data, fourier_degree, remove_constants)
    new_test = (
        None
        if X.test_data is None
        else enrich_dataframe(X.test_data, fourier_degree, remove_constants)
    )
    return TimeSeriesDataset(
        train_data=new_train,
        time_col=X.time_col,
        target_names=X.target_names,
        time_idx=X.time_idx,
        test_data=new_test,
    )


def date_feature_dict(timestamps: pd.Series) -> dict:
    tmp_dt = timestamps.dt
    column = timestamps.name
    new_columns_dict = {
        f"{column}_year": tmp_dt.year,
        f"{column}_month": tmp_dt.month,
        f"{column}_day": tmp_dt.day,
        f"{column}_hour": tmp_dt.hour,
        f"{column}_minute": tmp_dt.minute,
        f"{column}_second": tmp_dt.second,
        f"{column}_dayofweek": tmp_dt.dayofweek,
        f"{column}_dayofyear": tmp_dt.dayofyear,
        f"{column}_quarter": tmp_dt.quarter,
    }

    return new_columns_dict


class DataTransformerTS:
    """Transform input time series training data."""

    def __init__(self, time_col: str, label: Union[str, List[str]]):
        self.time_col = time_col
        self.label = label
        self.cat_columns = []
        self.num_columns = []
        self.datetime_columns = []
        self.drop_columns = []

    @property
    def _drop(self):
        return len(self.drop_columns)

    def fit(self, X: Union[DataFrame, np.array], y):
        """Fit transformer.

        Args:
            X: A numpy array or a pandas dataframe of training data.
            y: A numpy array or a pandas series of labels.

        Returns:
            X: Processed numpy array or pandas dataframe of training data.
            y: Processed numpy array or pandas series of labels.
        """
        assert isinstance(X, DataFrame)
        X = X.copy()
        n = X.shape[0]
        # drop = False

        # ds_col = X[self.time_col]

        if isinstance(y, Series):
            y = y.rename(self.label)

        for column in X.columns:
            # sklearn/utils/validation.py needs int/float values
            if X[column].dtype.name in ("object", "category"):
                if (
                    # drop columns where all values are the same
                    X[column].nunique() == 1
                    # this drops UID-type cols
                    or X[column].nunique(dropna=True) == n - X[column].isnull().sum()
                ):
                    self.drop_columns.append(column)
                else:
                    self.cat_columns.append(column)
            elif X[column].nunique(dropna=True) < 2:
                self.drop_columns.append(column)
                # drop = True
            elif X[column].dtype.name == "datetime64[ns]":
                pass  # these will be processed at model level,
                # so they can also be done in the predict method

                # self.datetime_columns.append(column)
                # new_columns_dict = date_feature_dict(X[column])
                # for key, value in new_columns_dict.items():
                #     if key not in X.columns and value.nunique(dropna=False) >= 2:
                #         self.num_columns.append(key)
                #         X[key] = value
                # if column != self.time_col:
                #     X[column] = X[column].map(lambda x: x.toordinal())
                #     self.num_columns.append(column)
                # else:
                #     X[column + "_ord"] = X[column].map(lambda x: x.toordinal())
                #     self.num_columns.append(column + "_ord")
            else:
                self.num_columns.append(column)

        if self.num_columns:
            # TODO: what does this do???
            # X_num = X[num_columns]
            # if np.issubdtype(X_num.columns.dtype, np.integer) and (
            #     drop
            #     or min(X_num.columns) != 0
            #     or max(X_num.columns) != X_num.shape[1] - 1
            # ):
            #     X_num.columns = range(X_num.shape[1])
            #     drop = True
            # else:
            #     drop = False

            self.transformer = ColumnTransformer(
                [
                    (
                        "continuous",
                        SimpleImputer(missing_values=np.nan, strategy="median"),
                        self.num_columns,
                    )
                ]
            )

            self.transformer.fit(X[self.num_columns])
        else:
            self.transformer = None

        # TODO: want to generate datetime features for time_col, too!
        # X.insert(0, self.time_col, ds_col)

        # TODO: revisit for multivariate series, and recast for a single df input anyway
        ycol = y[y.columns[0]]
        if not pd.api.types.is_numeric_dtype(ycol):
            self.label_transformer = LabelEncoder()
            self.label_transformer.fit(ycol)
        else:
            self.label_transformer = None

    def transform(self, X: Union[DataFrame, np.array], y=None):
        # TODO: revisit for multivariate series, and recast for a single df input anyway
        if self.label_transformer is not None and y is not None:
            ycol = y[y.columns[0]]
            y_tr = self.label_transformer.transform(ycol)
            y.iloc[:] = y_tr.reshape(y.shape)

        X.drop(columns=self.drop_columns, inplace=True)

        for col in self.cat_columns:
            if X[col].dtype.name == "category":
                if "__NAN__" not in X[col].cat.categories:
                    X[col] = X[col].cat.add_categories("__NAN__").fillna("__NAN__")
            else:
                X[col] = X[col].fillna("__NAN__")
                X[col] = X[col].astype("category")

        # for column in self.datetime_columns:
        #     # as of now, don't do it to time_col? Why?
        #     new_columns_dict = date_feature_dict(X[column])
        #     for key, value in new_columns_dict.items():
        #         if key in self.num_columns:
        #             X[key] = value
        #     if column != self.time_col:
        #         X[column] = X[column].map(lambda x: x.toordinal())
        #     else:
        #         X[column + "_ord"] = X[column].map(lambda x: x.toordinal())

        for column in self.num_columns:
            X[column] = X[column].fillna(np.nan)

        if self.transformer is not None:
            X[self.num_columns] = self.transformer.transform(X[self.num_columns])

        return X, y

    def fit_transform(self, X: Union[DataFrame, np.array], y):
        self.fit(X, y)
        return self.transform(X, y)

    # def _transform(self, X: Union[DataFrame, np.array]):
    #     """Process data using fit transformer.
    #
    #     Args:
    #         X: A numpy array or a pandas dataframe of training data.
    #
    #     Returns:
    #         X: Processed numpy array or pandas dataframe of training data.
    #     """
    #     X = X.copy()
    #     if isinstance(X, np.ndarray):
    #         array_order = len(X.shape)
    #         feature_labels = []
    #         if array_order > 1:
    #             feature_labels = [f"x{i}" for i in range(X.shape[1] - 1)]
    #         X = pd.DataFrame(X, columns=[self.time_col] + feature_labels)
    #
    #     if isinstance(X, DataFrame):
    #         cat_columns, num_columns, datetime_columns = (
    #             self._cat_columns,
    #             self._num_columns,
    #             self._datetime_columns,
    #         )
    #         ds_col = X.pop(self.time_col)
    #         for column in datetime_columns:
    #             tmp_dt = X[column].dt
    #             new_columns_dict = {
    #                 f"year_{column}": tmp_dt.year,
    #                 f"month_{column}": tmp_dt.month,
    #                 f"day_{column}": tmp_dt.day,
    #                 f"hour_{column}": tmp_dt.hour,
    #                 f"minute_{column}": tmp_dt.minute,
    #                 f"second_{column}": tmp_dt.second,
    #                 f"dayofweek_{column}": tmp_dt.dayofweek,
    #                 f"dayofyear_{column}": tmp_dt.dayofyear,
    #                 f"quarter_{column}": tmp_dt.quarter,
    #             }
    #             for new_col_name, new_col_value in new_columns_dict.items():
    #                 if new_col_name not in X.columns and new_col_name in num_columns:
    #                     X[new_col_name] = new_col_value
    #             X[column] = X[column].map(datetime.toordinal)
    #             del tmp_dt
    #         X = X[cat_columns + num_columns].copy()
    #         X.insert(0, self.time_col, ds_col)
    #         for column in cat_columns:
    #             if X[column].dtype.name == "object":
    #                 X[column] = X[column].fillna("__NAN__")
    #             elif X[column].dtype.name == "category":
    #                 current_categories = X[column].cat.categories
    #                 if "__NAN__" not in current_categories:
    #                     X[column] = (
    #                         X[column].cat.add_categories("__NAN__").fillna("__NAN__")
    #                     )
    #         if cat_columns:
    #             X[cat_columns] = X[cat_columns].astype("category")
    #         if num_columns:
    #             X_num = X[num_columns].fillna(np.nan)
    #             if self._drop:
    #                 X_num.columns = range(X_num.shape[1])
    #             X[num_columns] = self.transformer.transform(X_num)
    #     return X


def create_forward_frame(
    frequency: str,
    steps: int,
    test_end_date: datetime.datetime,
    time_col: str,
):
    start_date = test_end_date + pd.Timedelta(1, frequency)
    times = pd.date_range(
        start=start_date,
        periods=steps,
        freq=frequency,
    )
    return pd.DataFrame({time_col: times})
