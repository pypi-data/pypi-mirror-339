"""
Client for the Five9 Interval Statistics API.

This module provides a client for the Interval Statistics API, which offers
historical statistics for domains, agents, campaigns, and ACD.
"""

from typing import Dict, Any, Optional, List, Union

from five9_stats.api.client import Five9StatsClient
from five9_stats.models.common import SubscriptionMetadata
from five9_stats.models.interval import (
    AcdStatisticsResponse,
    AgentStatisticsResponse,
    CampaignStatisticsResponse,
    QueueStatisticsResponse,
)


class IntervalStatsClient(Five9StatsClient):
    """Client for the Five9 Interval Statistics API."""
    
    def __init__(
        self,
        username: str,
        password: str,
        base_url: str = "https://api.prod.us.five9.net",
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: int = 1,
    ):
        """
        Initialize the Interval Statistics API client.
        
        Args:
            username: Five9 username
            password: Five9 password
            base_url: Base URL for the Five9 API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            retry_delay: Delay between retries in seconds
        """
        super().__init__(username, password, base_url, timeout, max_retries, retry_delay)
    
    async def get_statistics_metadata(self, domain_id: str) -> SubscriptionMetadata:
        """
        Retrieve statistics and metadata.
        
        Args:
            domain_id: Unique ID of the domain
            
        Returns:
            Metadata for statistics
        """
        path = f"/interval-stats/v1/domains/{domain_id}/statistics"
        return await self.get(path, response_model=SubscriptionMetadata)
    
    async def get_agent_statistics(
        self,
        domain_id: str,
        media_types: Optional[str] = None,
        filters: Optional[str] = None,
        time_zone: Optional[str] = None,
        time_period: Optional[str] = None,
        shift_start_hour: Optional[int] = None,
        shift_start_minute: Optional[int] = None,
        shift_duration: Optional[int] = None,
        page_limit: Optional[int] = None,
        page_cursor: Optional[str] = None,
        interval_start_time: Optional[str] = None,
        interval_end_time: Optional[str] = None,
        search_by_metrics: Optional[str] = None,
        agent_groups: Optional[str] = None,
        disposition_ids: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> AgentStatisticsResponse:
        """
        Retrieve agent statistics.
        
        Args:
            domain_id: Unique ID of the domain
            media_types: Comma separated media types (e.g., "VOICE,CHAT,EMAIL")
            filters: Comma separated agent/campaign/skill Ids
            time_zone: Time zone (default: UTC)
            time_period: Time period (e.g., LAST_15_MINUTES, DAY, WEEK, MONTH, SHIFT)
            shift_start_hour: Start hour of the time range for SHIFT time period (0-23)
            shift_start_minute: Start minute of the time range for SHIFT time period (0-59)
            shift_duration: Length of the time range in minutes for SHIFT time period (1-1440)
            page_limit: The page limit (max 100)
            page_cursor: The page cursor to retrieve a particular page of results
            interval_start_time: Start time for custom interval (ISO 8601 format)
            interval_end_time: End time for custom interval (ISO 8601 format)
            search_by_metrics: Comma separated metrics to search by
            agent_groups: Comma separated agent group ids
            disposition_ids: Comma separated disposition ids
            sort: Field to sort the result order (use '-' to indicate descending order)
            
        Returns:
            Agent statistics response
        """
        path = f"/interval-stats/v1/domains/{domain_id}/statistics/agent-statistics"
        params = {
            "mediaTypes": media_types,
            "filters": filters,
            "timeZone": time_zone,
            "timePeriod": time_period,
            "shiftStartHour": shift_start_hour,
            "shiftStartMinute": shift_start_minute,
            "shiftDuration": shift_duration,
            "pageLimit": page_limit,
            "pageCursor": page_cursor,
            "intervalStartTime": interval_start_time,
            "intervalEndTime": interval_end_time,
            "searchByMetrics": search_by_metrics,
            "agentGroups": agent_groups,
            "dispositionIds": disposition_ids,
            "sort": sort,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return await self.get(path, params=params, response_model=AgentStatisticsResponse)
    
    async def get_campaign_statistics(
        self,
        domain_id: str,
        campaign_type: str,
        media_types: Optional[str] = None,
        filters: Optional[str] = None,
        disposition_ids: Optional[str] = None,
        time_zone: Optional[str] = None,
        time_period: Optional[str] = None,
        shift_start_hour: Optional[int] = None,
        shift_start_minute: Optional[int] = None,
        shift_duration: Optional[int] = None,
        page_limit: Optional[int] = None,
        page_cursor: Optional[str] = None,
        interval_start_time: Optional[str] = None,
        interval_end_time: Optional[str] = None,
        search_by_metrics: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> CampaignStatisticsResponse:
        """
        Retrieve campaign statistics.
        
        Args:
            domain_id: Unique ID of the domain
            campaign_type: Campaign Type (INBOUND/OUTBOUND/AUTODIAL)
            media_types: Comma separated media types (e.g., "VOICE,CHAT,EMAIL")
            filters: Comma separated agent/campaign/skill Ids
            disposition_ids: Comma separated disposition ids
            time_zone: Time zone (default: UTC)
            time_period: Time period (e.g., LAST_15_MINUTES, DAY, WEEK, MONTH, SHIFT)
            shift_start_hour: Start hour of the time range for SHIFT time period (0-23)
            shift_start_minute: Start minute of the time range for SHIFT time period (0-59)
            shift_duration: Length of the time range in minutes for SHIFT time period (1-1440)
            page_limit: The page limit (max 100)
            page_cursor: The page cursor to retrieve a particular page of results
            interval_start_time: Start time for custom interval (ISO 8601 format)
            interval_end_time: End time for custom interval (ISO 8601 format)
            search_by_metrics: Comma separated metrics to search by
            sort: Field to sort the result order (use '-' to indicate descending order)
            
        Returns:
            Campaign statistics response
        """
        path = f"/interval-stats/v1/domains/{domain_id}/statistics/campaign-statistics"
        params = {
            "campaignType": campaign_type,
            "mediaTypes": media_types,
            "filters": filters,
            "dispositionIds": disposition_ids,
            "timeZone": time_zone,
            "timePeriod": time_period,
            "shiftStartHour": shift_start_hour,
            "shiftStartMinute": shift_start_minute,
            "shiftDuration": shift_duration,
            "pageLimit": page_limit,
            "pageCursor": page_cursor,
            "intervalStartTime": interval_start_time,
            "intervalEndTime": interval_end_time,
            "searchByMetrics": search_by_metrics,
            "sort": sort,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return await self.get(path, params=params, response_model=CampaignStatisticsResponse)
    
    async def get_acd_statistics(
        self,
        domain_id: str,
        media_types: Optional[str] = None,
        filters: Optional[str] = None,
        time_zone: Optional[str] = None,
        time_period: Optional[str] = None,
        shift_start_hour: Optional[int] = None,
        shift_start_minute: Optional[int] = None,
        shift_duration: Optional[int] = None,
        page_limit: Optional[int] = None,
        page_cursor: Optional[str] = None,
        interval_start_time: Optional[str] = None,
        interval_end_time: Optional[str] = None,
        search_by_metrics: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> AcdStatisticsResponse:
        """
        Retrieve ACD statistics.
        
        Args:
            domain_id: Unique ID of the domain
            media_types: Comma separated media types (e.g., "VOICE,CHAT,EMAIL")
            filters: Comma separated agent/campaign/skill Ids
            time_zone: Time zone (default: UTC)
            time_period: Time period (e.g., LAST_15_MINUTES, DAY, WEEK, MONTH, SHIFT)
            shift_start_hour: Start hour of the time range for SHIFT time period (0-23)
            shift_start_minute: Start minute of the time range for SHIFT time period (0-59)
            shift_duration: Length of the time range in minutes for SHIFT time period (1-1440)
            page_limit: The page limit (max 100)
            page_cursor: The page cursor to retrieve a particular page of results
            interval_start_time: Start time for custom interval (ISO 8601 format)
            interval_end_time: End time for custom interval (ISO 8601 format)
            search_by_metrics: Comma separated metrics to search by
            sort: Field to sort the result order (use '-' to indicate descending order)
            
        Returns:
            ACD statistics response
        """
        path = f"/interval-stats/v1/domains/{domain_id}/statistics/acd-statistics"
        params = {
            "mediaTypes": media_types,
            "filters": filters,
            "timeZone": time_zone,
            "timePeriod": time_period,
            "shiftStartHour": shift_start_hour,
            "shiftStartMinute": shift_start_minute,
            "shiftDuration": shift_duration,
            "pageLimit": page_limit,
            "pageCursor": page_cursor,
            "intervalStartTime": interval_start_time,
            "intervalEndTime": interval_end_time,
            "searchByMetrics": search_by_metrics,
            "sort": sort,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return await self.get(path, params=params, response_model=AcdStatisticsResponse)
    
    async def get_queue_statistics(
        self,
        domain_id: str,
        media_types: Optional[str] = None,
        filters: Optional[str] = None,
        time_zone: Optional[str] = None,
        time_period: Optional[str] = None,
        shift_start_hour: Optional[int] = None,
        shift_start_minute: Optional[int] = None,
        shift_duration: Optional[int] = None,
        page_limit: Optional[int] = None,
        page_cursor: Optional[str] = None,
        interval_start_time: Optional[str] = None,
        interval_end_time: Optional[str] = None,
        search_by_metrics: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> QueueStatisticsResponse:
        """
        Retrieve Queue statistics.
        
        Args:
            domain_id: Unique ID of the domain
            media_types: Comma separated media types (e.g., "VOICE,CHAT,EMAIL")
            filters: Comma separated agent/campaign/skill Ids
            time_zone: Time zone (default: UTC)
            time_period: Time period (e.g., LAST_15_MINUTES, DAY, WEEK, MONTH, SHIFT)
            shift_start_hour: Start hour of the time range for SHIFT time period (0-23)
            shift_start_minute: Start minute of the time range for SHIFT time period (0-59)
            shift_duration: Length of the time range in minutes for SHIFT time period (1-1440)
            page_limit: The page limit (max 100)
            page_cursor: The page cursor to retrieve a particular page of results
            interval_start_time: Start time for custom interval (ISO 8601 format)
            interval_end_time: End time for custom interval (ISO 8601 format)
            search_by_metrics: Comma separated metrics to search by
            sort: Field to sort the result order (use '-' to indicate descending order)
            
        Returns:
            Queue statistics response
        """
        path = f"/interval-stats/v1/domains/{domain_id}/statistics/queue-statistics"
        params = {
            "mediaTypes": media_types,
            "filters": filters,
            "timeZone": time_zone,
            "timePeriod": time_period,
            "shiftStartHour": shift_start_hour,
            "shiftStartMinute": shift_start_minute,
            "shiftDuration": shift_duration,
            "pageLimit": page_limit,
            "pageCursor": page_cursor,
            "intervalStartTime": interval_start_time,
            "intervalEndTime": interval_end_time,
            "searchByMetrics": search_by_metrics,
            "sort": sort,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return await self.get(path, params=params, response_model=QueueStatisticsResponse)