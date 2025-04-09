"""
Leneda API client for accessing energy consumption and production data.

This module provides a client for the Leneda API, which allows access to
energy consumption and production data for electricity and gas.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, Union

import requests

from .models import AggregatedMeteringData, MeteringData

# Set up logging
logger = logging.getLogger("leneda.client")


class LenedaClient:
    """Client for the Leneda API."""

    BASE_URL = "https://api.leneda.lu/api"

    def __init__(self, api_key: str, energy_id: str, debug: bool = False):
        """
        Initialize the Leneda API client.

        Args:
            api_key: Your Leneda API key
            energy_id: Your Energy ID
            debug: Enable debug logging
        """
        self.api_key = api_key
        self.energy_id = energy_id

        # Set up headers for API requests
        self.headers = {
            "X-API-KEY": api_key,
            "X-ENERGY-ID": energy_id,
            "Content-Type": "application/json",
        }

        # Set up debug logging if requested
        if debug:
            logging.getLogger("leneda").setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug logging enabled for Leneda client")

    def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: Dict[str, Any] = None,
        data: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Make a request to the Leneda API.

        Args:
            endpoint: API endpoint to call
            method: HTTP method to use
            params: Query parameters
            data: Request body data

        Returns:
            API response as a dictionary
        """
        url = f"{self.BASE_URL}/{endpoint}"

        # Log the request details
        logger.debug(f"Making {method} request to {url}")
        if params:
            logger.debug(f"Query parameters: {params}")
        if data:
            logger.debug(f"Request data: {data}")

        try:
            # Make the request
            response = requests.request(
                method=method, url=url, headers=self.headers, params=params, json=data
            )

            # Check for HTTP errors
            response.raise_for_status()

            # Parse the response
            if response.content:
                response_data = response.json()
                logger.debug(f"Response status: {response.status_code}")
                logger.debug(f"Response data: {json.dumps(response_data, indent=2)}")
                return response_data
            else:
                logger.debug(f"Response status: {response.status_code} (no content)")
                return {}

        except requests.exceptions.HTTPError as e:
            # Handle HTTP errors
            logger.error(f"HTTP error: {e}")
            if hasattr(e, "response") and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response body: {e.response.text}")
            raise

        except requests.exceptions.RequestException as e:
            # Handle other request errors
            logger.error(f"Request error: {e}")
            raise

        except json.JSONDecodeError as e:
            # Handle JSON parsing errors
            logger.error(f"JSON decode error: {e}")
            logger.error(f"Response text: {response.text}")
            raise

    def get_metering_data(
        self,
        metering_point_code: str,
        obis_code: str,
        start_date_time: Union[str, datetime],
        end_date_time: Union[str, datetime],
    ) -> MeteringData:
        """
        Get time series data for a specific metering point and OBIS code.

        Args:
            metering_point_code: The metering point code
            obis_code: The OBIS code
            start_date_time: Start date and time (ISO format string or datetime object)
            end_date_time: End date and time (ISO format string or datetime object)

        Returns:
            MeteringData object containing the time series data
        """
        # Convert datetime objects to ISO format strings if needed
        if isinstance(start_date_time, datetime):
            start_date_time = start_date_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        if isinstance(end_date_time, datetime):
            end_date_time = end_date_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Set up the endpoint and parameters
        endpoint = f"metering-points/{metering_point_code}/time-series"
        params = {
            "obisCode": obis_code,
            "startDateTime": start_date_time,
            "endDateTime": end_date_time,
        }

        # Make the request
        response_data = self._make_request(endpoint, params=params)

        # Parse the response into a MeteringData object
        return MeteringData.from_dict(
            response_data, metering_point_code=metering_point_code, obis_code=obis_code
        )

    def get_aggregated_metering_data(
        self,
        metering_point_code: str,
        obis_code: str,
        start_date: Union[str, datetime],
        end_date: Union[str, datetime],
        aggregation_level: str = "Day",
        transformation_mode: str = "Accumulation",
    ) -> AggregatedMeteringData:
        """
        Get aggregated time series data for a specific metering point and OBIS code.

        Args:
            metering_point_code: The metering point code
            obis_code: The OBIS code
            start_date: Start date (ISO format string or datetime object)
            end_date: End date (ISO format string or datetime object)
            aggregation_level: Aggregation level (Day, Week, Month, Quarter, Year)
            transformation_mode: Transformation mode (Accumulation, Average, Maximum, Minimum)

        Returns:
            AggregatedMeteringData object containing the aggregated time series data
        """
        # Convert datetime objects to ISO format strings if needed
        if isinstance(start_date, datetime):
            start_date = start_date.strftime("%Y-%m-%d")
        if isinstance(end_date, datetime):
            end_date = end_date.strftime("%Y-%m-%d")

        # Set up the endpoint and parameters
        endpoint = f"metering-points/{metering_point_code}/time-series/aggregated"
        params = {
            "obisCode": obis_code,
            "startDate": start_date,
            "endDate": end_date,
            "aggregationLevel": aggregation_level,
            "transformationMode": transformation_mode,
        }

        # Make the request
        response_data = self._make_request(endpoint, params=params)

        # Parse the response into an AggregatedMeteringData object
        return AggregatedMeteringData.from_dict(
            response_data,
            metering_point_code=metering_point_code,
            obis_code=obis_code,
            aggregation_level=aggregation_level,
            transformation_mode=transformation_mode,
        )

    def request_metering_data_access(self, metering_point_code: str) -> Dict[str, Any]:
        """
        Request access to metering data for a specific metering point.

        Args:
            metering_point_code: The metering point code

        Returns:
            Response data from the API
        """
        # Set up the endpoint and data
        endpoint = "metering-data-access-request"
        data = {"meteringPointCode": metering_point_code}

        # Make the request
        response_data = self._make_request(endpoint, method="POST", data=data)

        return response_data
