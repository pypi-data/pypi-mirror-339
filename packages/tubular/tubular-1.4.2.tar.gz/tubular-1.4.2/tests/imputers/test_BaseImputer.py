from copy import deepcopy

import narwhals as nw
import pandas as pd
import polars as pl
import pytest
from sklearn.exceptions import NotFittedError

import tests.test_data as d
from tests import utils as u
from tests.base_tests import (
    ColumnStrListInitTests,
    GenericFitTests,
    OtherBaseBehaviourTests,
)

# Categorical columns created under the same global string cache have the same underlying
# physical value when string values are equal.
# there is an efficiency cost, but not an issue for tests
pl.enable_string_cache()


class GenericImputerTransformTests:
    @pytest.fixture()
    def test_fit_df(self, request):
        library = request.param
        df_dict = {
            "a": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
            "b": ["a", "b", "c", "d", "e", "f", None],
            "c": ["a", "b", "c", "d", "e", "f", None],
        }

        return u.dataframe_init_dispatch(df_dict, library)

    @pytest.fixture()
    def expected_df_1(self, request):
        library = request.param
        df1_dict = {
            "a": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
            "b": ["a", "b", "c", "d", "e", "f", None],
            "c": ["a", "b", "c", "d", "e", "f", None],
        }

        df1 = u.dataframe_init_dispatch(df1_dict, library)

        narwhals_df = nw.from_native(df1)
        narwhals_df = narwhals_df.with_columns(nw.col("c").cast(nw.dtypes.Categorical))

        return narwhals_df.to_native()

    @pytest.fixture()
    def expected_df_2(self, request):
        library = request.param
        df2_dict = {
            "a": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None],
            "b": ["a", "b", "c", "d", "e", "f", "g"],
            "c": ["a", "b", "c", "d", "e", "f", None],
        }
        df2 = u.dataframe_init_dispatch(df2_dict, library)
        narwhals_df = nw.from_native(df2)
        narwhals_df = narwhals_df.with_columns(nw.col("c").cast(nw.dtypes.Categorical))

        return narwhals_df.to_native()

    @pytest.fixture()
    def expected_df_3(self, request):
        library = request.param
        df3_dict = {
            "a": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None],
            "b": ["a", "b", "c", "d", "e", "f", "g"],
            "c": ["a", "b", "c", "d", "e", "f", "f"],
        }

        df3 = u.dataframe_init_dispatch(dataframe_dict=df3_dict, library=library)

        narwhals_df = nw.from_native(df3)
        narwhals_df = narwhals_df.with_columns(nw.col("c").cast(nw.dtypes.Categorical))

        return narwhals_df.to_native()

    @pytest.mark.parametrize("test_fit_df", ["pandas", "polars"], indirect=True)
    def test_not_fitted_error_raised(self, test_fit_df, initialized_transformers):
        transformer = initialized_transformers[self.transformer_name]
        # if transformer is not yet polars compatible, skip this test
        if not transformer.polars_compatible and isinstance(test_fit_df, pl.DataFrame):
            return
        if initialized_transformers[self.transformer_name].FITS:
            with pytest.raises(NotFittedError):
                initialized_transformers[self.transformer_name].transform(test_fit_df)

    @pytest.mark.parametrize("library", ["pandas", "polars"])
    def test_impute_value_unchanged(self, library, initialized_transformers):
        """Test that self.impute_value is unchanged after transform."""
        df1 = d.create_df_1(library=library)
        transformer = initialized_transformers[self.transformer_name]
        # if transformer is not yet polars compatible, skip this test
        if not transformer.polars_compatible and isinstance(df1, pl.DataFrame):
            return
        transformer.impute_values_ = {"b": 1}
        impute_values = deepcopy(transformer.impute_values_)

        transformer.transform(df1)

        assert (
            transformer.impute_values_ == impute_values
        ), "impute_values_ changed in transform"

    @pytest.mark.parametrize(
        ("library", "expected_df_1"),
        [("pandas", "pandas"), ("polars", "polars")],
        indirect=["expected_df_1"],
    )
    def test_expected_output_1(self, library, expected_df_1, initialized_transformers):
        """Test that transform is giving the expected output when applied to float column."""
        # Create the DataFrame using the library parameter
        df2 = d.create_df_2(library=library)

        # Initialize the transformer
        transformer = initialized_transformers[self.transformer_name]
        # if transformer is not yet polars compatible, skip this test
        if not transformer.polars_compatible and isinstance(df2, pl.DataFrame):
            return
        transformer.impute_values_ = {"a": 7}
        transformer.columns = ["a"]

        df_transformed = transformer.transform(df2)

        # Convert both DataFrames to a common format using Narwhals
        df_transformed_common = nw.from_native(df_transformed)
        expected_df_1_common = nw.from_native(expected_df_1)

        # Check outcomes for single rows
        for i in range(len(df_transformed_common)):
            df_transformed_row = df_transformed_common[[i]].to_native()
            df_expected_row = expected_df_1_common[[i]].to_native()

            u.assert_frame_equal_dispatch(
                df_transformed_row,
                df_expected_row,
            )

        # Check whole dataframes
        u.assert_frame_equal_dispatch(
            df_transformed_common.to_native(),
            expected_df_1_common.to_native(),
        )

    @pytest.mark.parametrize(
        ("library", "expected_df_2"),
        [("pandas", "pandas"), ("polars", "polars")],
        indirect=["expected_df_2"],
    )
    def test_expected_output_2(self, library, expected_df_2, initialized_transformers):
        """Test that transform is giving the expected output when applied to object column."""
        # Create the DataFrame using the library parameter
        df2 = d.create_df_2(library=library)

        # Initialize the transformer
        transformer = initialized_transformers[self.transformer_name]

        # if transformer is not yet polars compatible, skip this test
        if not transformer.polars_compatible and isinstance(df2, pl.DataFrame):
            return

        transformer.impute_values_ = {"b": "g"}
        transformer.columns = ["b"]

        # Transform the DataFrame
        df_transformed = transformer.transform(df2)

        # Convert both DataFrames to a common format using Narwhals
        df_transformed_common = nw.from_native(df_transformed)
        expected_df_2_common = nw.from_native(expected_df_2)

        # Check outcomes for single rows
        for i in range(len(df_transformed_common)):
            df_transformed_row = df_transformed_common[[i]].to_native()
            df_expected_row = expected_df_2_common[[i]].to_native()

            u.assert_frame_equal_dispatch(
                df_transformed_row,
                df_expected_row,
            )

        # Check whole dataframes
        u.assert_frame_equal_dispatch(
            df_transformed_common.to_native(),
            expected_df_2_common.to_native(),
        )

    @pytest.mark.parametrize(
        ("library", "expected_df_3"),
        [("pandas", "pandas"), ("polars", "polars")],
        indirect=["expected_df_3"],
    )
    def test_expected_output_3(self, library, expected_df_3, initialized_transformers):
        """Test that transform is giving the expected output when applied to object and categorical columns."""
        # Create the DataFrame using the library parameter
        df2 = d.create_df_2(library=library)

        # Initialize the transformer
        transformer = initialized_transformers[self.transformer_name]

        # if transformer is not yet polars compatible, skip this test
        if not transformer.polars_compatible and isinstance(df2, pl.DataFrame):
            return

        transformer.impute_values_ = {"b": "g", "c": "f"}
        transformer.columns = ["b", "c"]

        # Transform the DataFrame
        df_transformed = transformer.transform(df2)
        df_transformed["c"]

        # ArbitraryImputer will add a new categorical level to cat columns,
        # make sure expected takes this into account
        if self.transformer_name == "ArbitraryImputer" and isinstance(
            expected_df_3,
            pd.DataFrame,
        ):
            expected_df_3["c"] = expected_df_3["c"].cat.add_categories(
                transformer.impute_value,
            )

        # Convert both DataFrames to a common format using Narwhals
        df_transformed_common = nw.from_native(df_transformed)
        expected_df_3_common = nw.from_native(expected_df_3)

        # Check outcomes for single rows
        for i in range(len(df_transformed_common)):
            df_transformed_row = df_transformed_common[[i]].to_native()
            df_expected_row = expected_df_3_common[[i]].to_native()

            u.assert_frame_equal_dispatch(
                df_transformed_row,
                df_expected_row,
            )

        # Check whole dataframes
        u.assert_frame_equal_dispatch(
            df_transformed_common.to_native(),
            expected_df_3_common.to_native(),
        )

    @pytest.mark.parametrize(
        "library",
        ["pandas", "polars"],
    )
    def test_imputation_with_falsey_values(self, library, initialized_transformers):
        """Test that transform is giving the expected output when applied to object and categorical columns."""
        # Create the DataFrame using the library parameter
        df_dict = {
            "b": [1, 2, None],
        }

        df = u.dataframe_init_dispatch(dataframe_dict=df_dict, library=library)

        # Initialize the transformer
        transformer = initialized_transformers[self.transformer_name]

        # if transformer is not yet polars compatible, skip this test
        if not transformer.polars_compatible and isinstance(df, pl.DataFrame):
            return

        transformer.impute_values_ = {"b": 0}
        transformer.columns = ["b"]

        expected_df_dict = {
            "b": [1.0, 2.0, 0.0],
        }

        expected_df = u.dataframe_init_dispatch(
            dataframe_dict=expected_df_dict,
            library=library,
        )

        # Transform the DataFrame
        df_transformed = transformer.transform(df)

        u.assert_frame_equal_dispatch(
            df_transformed,
            expected_df,
        )


class GenericImputerTransformTestsWeight:
    @pytest.fixture()
    def expected_df_weights(self, request):
        """Expected output for test_nulls_imputed_correctly_weights."""
        library = request.param
        df = d.create_df_9(library=library)

        df = nw.from_native(df)

        df = df.with_columns(df["b"].fill_null(4))

        return df.to_native()

    @pytest.mark.parametrize(
        ("library", "expected_df_weights"),
        [("pandas", "pandas"), ("polars", "polars")],
        indirect=["expected_df_weights"],
    )
    def test_nulls_imputed_correctly_weights(
        self,
        library,
        expected_df_weights,
        minimal_attribute_dict,
        uninitialized_transformers,
    ):
        """Test missing values are filled with the correct values - and unrelated columns are not changed
        (when weight is used).
        """
        # Create the DataFrame using the library parameter
        df = d.create_df_9(library=library)

        args = minimal_attribute_dict[self.transformer_name].copy()
        args["weights_column"] = "c"

        transformer = uninitialized_transformers[self.transformer_name](**args)

        # if transformer is not yet polars compatible, skip this test
        if not transformer.polars_compatible and isinstance(df, pl.DataFrame):
            return

        # Set the impute values dict directly rather than fitting x on df so test works with helpers
        transformer.impute_values_ = {"b": 4}

        df_transformed = transformer.transform(df)

        # Convert both DataFrames to a common format using Narwhals
        df_transformed_common = nw.from_native(df_transformed)
        expected_df_weights_common = nw.from_native(expected_df_weights)

        # Check outcomes for single rows
        for i in range(len(df_transformed_common)):
            df_transformed_row = df_transformed_common[[i]].to_native()
            df_expected_row = expected_df_weights_common[[i]].to_native()

            u.assert_frame_equal_dispatch(
                df_transformed_row,
                df_expected_row,
            )

        # Check whole dataframes
        u.assert_frame_equal_dispatch(
            df_transformed_common.to_native(),
            expected_df_weights_common.to_native(),
        )

    @pytest.mark.parametrize("library", ["pandas", "polars"])
    def test_learnt_values_not_modified_weights(
        self,
        library,
        minimal_attribute_dict,
        uninitialized_transformers,
    ):
        """Test that the impute_values_ from fit are not changed in transform - when using weights."""
        df = d.create_df_9(library=library)

        args = minimal_attribute_dict[self.transformer_name].copy()
        args["columns"] = ["a", "b"]
        args["weights_column"] = "c"

        transformer1 = uninitialized_transformers[self.transformer_name](**args)

        # if transformer is not yet polars compatible, skip this test
        if not transformer1.polars_compatible and isinstance(df, pl.DataFrame):
            return

        transformer1.fit(df)

        transformer2 = uninitialized_transformers[self.transformer_name](**args)

        transformer2.fit_transform(df)

        # Check if the impute_values_ are the same
        assert (
            transformer1.impute_values_ == transformer2.impute_values_
        ), f"Impute values changed in transform for {self.transformer_name}"


class TestInit(ColumnStrListInitTests):
    """Generic tests for transformer.init()."""

    @classmethod
    def setup_class(cls):
        cls.transformer_name = "BaseImputer"


class TestFit(GenericFitTests):
    """Generic tests for transformer.fit()"""

    @classmethod
    def setup_class(cls):
        cls.transformer_name = "BaseImputer"


class TestTransform(GenericImputerTransformTests):
    """Tests for BaseImputer.transform."""

    @classmethod
    def setup_class(cls):
        cls.transformer_name = "BaseImputer"


class TestOtherBaseBehaviour(OtherBaseBehaviourTests):
    """
    Class to run tests for BaseTransformerBehaviour outside the three standard methods.

    May need to overwite specific tests in this class if the tested transformer modifies this behaviour.
    """

    @classmethod
    def setup_class(cls):
        cls.transformer_name = "BaseImputer"
