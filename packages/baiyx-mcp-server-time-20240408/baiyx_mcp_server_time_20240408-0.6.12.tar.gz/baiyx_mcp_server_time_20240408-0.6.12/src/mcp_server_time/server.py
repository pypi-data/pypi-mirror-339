import asyncio
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from zoneinfo import ZoneInfo
import importlib.metadata
import anyio

from mcp.server.fastmcp.server import FastMCP
from mcp.shared.exceptions import McpError
from pydantic import BaseModel


class TimeResult(BaseModel):
    timezone: str
    datetime: str
    is_dst: bool


class TimeConversionResult(BaseModel):
    source: TimeResult
    target: TimeResult
    time_difference: str
    version: str 

def get_local_tz(local_tz_override: str | None = None) -> ZoneInfo:
    if local_tz_override:
        return ZoneInfo(local_tz_override)

    # Get local timezone from datetime.now()
    tzinfo = datetime.now().astimezone(tz=None).tzinfo
    if tzinfo is not None:
        return ZoneInfo(str(tzinfo))
    raise McpError("Could not determine local timezone - tzinfo is None")


def get_zoneinfo(timezone_name: str) -> ZoneInfo:
    try:
        return ZoneInfo(timezone_name)
    except Exception as e:
        raise McpError(f"Invalid timezone: {str(e)}")


class TimeServer:
    def __init__(self, local_timezone: Optional[str] = None):
        self.mcp = FastMCP("mcp-time")
        self.local_tz = str(get_local_tz(local_timezone))
        self.setup_tools()
        
        version = importlib.metadata.version("baiyx-mcp-server-time-20240408")
        print(f"\n🕒 MCP Time Server v{version} starting...")
        print(f"📍 Using timezone: {self.local_tz}")
        print("✨ Server is ready to handle requests!\n")

    def setup_tools(self):
        @self.mcp.tool()
        def get_current_time(timezone: str = None) -> TimeResult:
            """Get current time in specified timezone"""
            timezone_name = timezone or self.local_tz
            timezone = get_zoneinfo(timezone_name)
            current_time = datetime.now(timezone)

            return TimeResult(
                timezone=timezone_name,
                datetime=current_time.isoformat(timespec="seconds"),
                is_dst=bool(current_time.dst()),
                version= importlib.metadata.version("baiyx-mcp-server-time-20240408"),
            )

        @self.mcp.tool()
        def convert_time(
            source_timezone: str,
            time: str,
            target_timezone: str
        ) -> TimeConversionResult:
            """Convert time between timezones"""
            source_timezone = source_timezone or self.local_tz
            target_timezone = target_timezone or self.local_tz
            
            source_tz = get_zoneinfo(source_timezone)
            target_tz = get_zoneinfo(target_timezone)

            try:
                parsed_time = datetime.strptime(time, "%H:%M").time()
            except ValueError:
                raise ValueError("Invalid time format. Expected HH:MM [24-hour format]")

            now = datetime.now(source_tz)
            source_time = datetime(
                now.year,
                now.month,
                now.day,
                parsed_time.hour,
                parsed_time.minute,
                tzinfo=source_tz,
            )

            target_time = source_time.astimezone(target_tz)
            source_offset = source_time.utcoffset() or timedelta()
            target_offset = target_time.utcoffset() or timedelta()
            hours_difference = (target_offset - source_offset).total_seconds() / 3600

            if hours_difference.is_integer():
                time_diff_str = f"{hours_difference:+.1f}h"
            else:
                time_diff_str = f"{hours_difference:+.2f}".rstrip("0").rstrip(".") + "h"

            return TimeConversionResult(
                source=TimeResult(
                    timezone=source_timezone,
                    datetime=source_time.isoformat(timespec="seconds"),
                    is_dst=bool(source_time.dst()),
                ),
                target=TimeResult(
                    timezone=target_timezone,
                    datetime=target_time.isoformat(timespec="seconds"),
                    is_dst=bool(target_time.dst()),
                ),
                time_difference=time_diff_str,
                version= importlib.metadata.version("baiyx-mcp-server-time-20240408"),
            )


async def serve(local_timezone: str | None = None) -> None:
    server = TimeServer(local_timezone)
    await server.mcp.run_stdio_async()
