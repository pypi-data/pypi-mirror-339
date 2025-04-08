import io
import logging
from collections import OrderedDict
from typing import List, NamedTuple, Any, Dict

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime

from synthera.protocols import SyntheraClientProtocol

_logger: logging.Logger = logging.getLogger(__name__)


class SimulationPastDateRequest(BaseModel):
    yield_curve_names: List[str] = Field(
        ...,  # Make it required
        description="List of yield curve names",
        examples=["USD_Z0", "EUR_Z0", "GBP_Z0"],
        min_length=1,  # Ensure at least one curve name is provided
    )
    no_of_samples: int = Field(
        ...,  # Make it required
        description="Number of samples",
        examples=[100, 1000, 10000],
        gt=0,
    )
    no_of_days: int = Field(
        ...,  # Make it required
        description="Number of days",
        examples=[3, 30, 120],
        gt=0,
    )
    reference_date: str = Field(
        ...,  # Make it required
        description="Reference date in YYYY-MM-DD format",
        pattern=r"^\d{4}-\d{2}-\d{2}$",  # Regex pattern for YYYY-MM-DD
    )
    model_label: str = Field(
        ...,  # Make it required
        description="Model label",
        examples=["model-v28", "model-v29"],
        min_length=1,
    )
    return_conditional: bool = Field(
        default=False,  # Provide default value
        description="Return conditional flag",
    )

    @field_validator("reference_date")
    def validate_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Must be YYYY-MM-DD")
        return v

    @model_validator(mode="after")
    def validate_model(self) -> "SimulationPastDateRequest":
        # Ensure reference date is not in the future
        if datetime.strptime(self.reference_date, "%Y-%m-%d") > datetime.now():
            raise ValueError("reference_date cannot be in the future")

        # Validate total data points don't exceed reasonable limit
        total_points = (
            self.no_of_samples * self.no_of_days * len(self.yield_curve_names)
        )
        if total_points > 100_000_000:  # 100 million points limit
            raise ValueError(
                f"Total data points ({total_points}) exceeds maximum limit"
            )

        return self


class SimulationPastDateOutput(BaseModel):
    label: str
    data: str


class SimulationPastDateMetadata(BaseModel):
    reference_date: str
    universe_available: List[str]
    models_available: List[str]


class SimulationPastDateResponse(BaseModel):
    outputs: List[SimulationPastDateOutput]
    metadata: SimulationPastDateMetadata


class SimulationPastDateResults(NamedTuple):
    dataframes: OrderedDict[str, pd.DataFrame]
    names: List[str]
    column_names: List[str]
    ndarray: np.ndarray
    metadata: Dict[str, Any]


class FixedIncome:
    fixed_income_endpoint: str = "fixed-income"
    simulation_past_date_endpoint: str = f"{fixed_income_endpoint}/simulation/past-date"

    def __init__(self, client: SyntheraClientProtocol) -> None:
        self.client: SyntheraClientProtocol = client

    def _decode_to_df(self, encoded_data: str) -> pd.DataFrame:
        """Decode a hex-encoded parquet file string into a pandas DataFrame."""
        try:
            parquet_bytes: bytes = bytes.fromhex(encoded_data)
            buffer: io.BytesIO = io.BytesIO(parquet_bytes)
            df: pd.DataFrame = pd.read_parquet(buffer, engine="pyarrow")
        except Exception as e:
            raise ValueError(f"Failed to decode data: {e}")
        return df

    def simulation_past_date(self, params: dict) -> SimulationPastDateResults:
        """Simulate yield curves for past dates."""
        # pre-processing
        request: SimulationPastDateRequest = SimulationPastDateRequest.model_validate(
            params
        )

        _logger.info(
            f"Requesting simulation of yield curves for past dates: {request.model_dump()}"
        )

        # make request
        response: dict = self.client.make_post_request(
            endpoint=self.simulation_past_date_endpoint,
            payload=request.model_dump(),
        )

        response: SimulationPastDateResponse = (
            SimulationPastDateResponse.model_validate(response)
        )

        # post-processing
        dataframes: OrderedDict[str, pd.DataFrame] = OrderedDict()
        for output in response.outputs:
            df: pd.DataFrame = self._decode_to_df(output.data)
            df["IDX"] = pd.to_datetime(df["IDX"], unit="s")
            df["SAMPLE"] = df["SAMPLE"].astype(int)
            dataframes.update({output.label: df})

        array: np.ndarray = np.concatenate(
            [
                df.values.reshape(request.no_of_samples, 1, -1, df.values.shape[1])
                for key, df in dataframes.items()
            ],
            axis=1,
        )

        return SimulationPastDateResults(
            dataframes=dataframes,
            names=list(dataframes.keys()),
            ndarray=array,
            column_names=list(list(dataframes.values())[0].columns),
            metadata=response.metadata.model_dump(),
        )
