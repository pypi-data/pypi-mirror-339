"""Arctic client."""
import aiohttp
import asyncio
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
from .utils import generate_headers


@dataclass
class BusLine:
    id: str
    name: str
    title: str
    description: str
    detail: Optional[str]
    brand_name: Optional[str]
    logo: Optional[str]
    start_date: str
    end_date: str


@dataclass
class Location:
    type: str
    coordinates: List[float]  # [longitude, latitude]


@dataclass
class BusStop:
    id: str
    common_name: str
    stop_type: Optional[str]
    indicator: Optional[str]
    bearing: Optional[str]
    location: Location
    lines: List[BusLine] = field(default_factory=list)


@dataclass
class Visit:
    direction: str
    destination_name: str
    aimed_arrival_time: datetime
    aimed_departure_time: datetime
    is_real_time: bool
    cancelled: bool
    expected_arrival_time: Optional[datetime]
    expected_departure_time: Optional[datetime]
    display_time: str
    line: str
    journey_id: str
    journey_href: str
    journey_date: str


class ArcticClient:
    """
    Async client for interacting with Arctic API bus service data.
    """

    def __init__(self, tenant: str, session: Optional[aiohttp.ClientSession] = None):
        """
        Initialize the client with a tenant name (e.g., 'bluestar').
        """
        self.tenant = tenant
        self.base_url = f"https://{tenant}.arcticapi.com"
        self.session = session

        self._close_session = False
        self._timeout = 5

    async def _get(self, url):
        """Make a GET request."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
            self._close_session = True

        async with asyncio.timeout(self._timeout):
            async with self.session.get(
                f"{self.base_url}/{url}", headers=generate_headers()
            ) as resp:
                return await resp.json()

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self):
        """
        Enter async context and create an aiohttp session.
        """
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """
        Exit async context and close the aiohttp session.
        """
        await self.session.close()

    async def search_stops(self, query: str) -> List[BusStop]:
        """
        Search for bus stops matching a query string.

        Args:
            query: The text to search for (e.g., stop name).

        Returns:
            A list of dicts representing stop places.
        """
        data = await self._get(f"places?search={query}")
        places = data.get("_embedded", {}).get("place", [])
        stops = []

        for data in places:
            if data.get("type") != "stop":
                continue

            stops.append(self._process_stop(data))

        return stops

    async def get_stop_info(self, stop_id: str) -> BusStop:
        """
        Retrieve detailed information for a given stop.

        Args:
            stop_id: The unique identifier for the bus stop.

        Returns:
            A `BusStop` instance populated with metadata and bus lines.
        """
        data = await self._get(f"network/stops/{stop_id}")
        return self._process_stop(data)

    def _process_stop(self, data: dict) -> BusStop:
        """
        Process API response for stop and return BusStop object.

        Args:
            data: API object.

        Returns:
            A `BusStop` instance populated with metadata and bus lines.
        """
        loc = Location(**data["location"])
        lines_raw = data.get("_embedded", {}).get("lines", [])

        lines = []
        for l in lines_raw:
            lines.append(
                BusLine(
                    id=l["id"],
                    name=l["name"],
                    title=l["title"],
                    description=l["description"],
                    detail=l.get("detail"),
                    brand_name=l.get("brandName"),
                    logo=l.get("logo"),
                    start_date=l["startDate"],
                    end_date=l["endDate"],
                )
            )
        return BusStop(
            id=data.get("id") or data.get("atcoCode") or "",
            common_name=data.get("commonName", ""),
            stop_type=data.get("stopType"),
            indicator=data.get("indicator"),
            bearing=data.get("bearing"),
            location=loc,
            lines=lines,
        )

    async def get_stop_visits(
        self, stop_id: str, line_filter: Optional[str] = None
    ) -> List[Visit]:
        """
        Get upcoming visit times for a specific stop.

        Args:
            stop_id: The unique identifier for the stop.
            line_filter: Optional name of a bus line to filter visits.

        Returns:
            A list of `Visit` objects representing expected bus arrivals,
            sorted by expected arrival time.
        """
        data = await self._get(
            f"network/stops/{stop_id}/visits?filter%5Bcancelled%5D=%2A"
        )
        visits_raw = data.get("_embedded", {}).get("timetable:visit", [])
        visits = []
        for v in visits_raw:
            line_data = v["_links"]["transmodel:line"]
            line = line_data["name"]

            if line_filter and line.lower() != line_filter.lower():
                continue

            journey = v["_links"]["timetable:journey"]
            visits.append(
                Visit(
                    direction=v["direction"],
                    destination_name=v["destinationName"],
                    aimed_arrival_time=datetime.fromisoformat(v["aimedArrivalTime"]),
                    aimed_departure_time=datetime.fromisoformat(
                        v["aimedDepartureTime"]
                    ),
                    is_real_time=v["isRealTime"],
                    cancelled=v["cancelled"],
                    expected_arrival_time=datetime.fromisoformat(
                        v["expectedArrivalTime"]
                    )
                    if v.get("expectedArrivalTime")
                    else None,
                    expected_departure_time=datetime.fromisoformat(
                        v["expectedDepartureTime"]
                    )
                    if v.get("expectedDepartureTime")
                    else None,
                    display_time=v["displayTime"],
                    line=line,
                    journey_id=journey["id"],
                    journey_href=journey["href"],
                    journey_date=journey["date"],
                )
            )
        visits.sort(key=lambda v: v.expected_arrival_time or v.aimed_arrival_time)
        return visits

    async def get_next_bus(
        self, stop_id: str, line_filter: Optional[str] = None
    ) -> Optional[Visit]:
        """
        Get the next bus visit from a stop, optionally filtering by line.

        Args:
            stop_id: The stop ID to check.
            line_filter: Optional name of the line to filter.

        Returns:
            The next upcoming `Visit` or None if none are found.
        """
        visits = await self.get_stop_visits(stop_id, line_filter)
        return visits[0] if visits else None
