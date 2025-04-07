"""
Client for the Five9 Real-time Stats Snapshot API.

This module provides a client for the Real-time Stats Snapshot API, which offers
real-time statistics for domains, agents, interactions, campaigns, and utilization thresholds.
"""

from typing import Dict, Any, Optional, List, Union

from five9_stats.api.client import Five9StatsClient
from five9_stats.models.common import SubscriptionMetadata
from five9_stats.models.snapshot import (
    AcdStatusResponse,
    QueueStatusResponse,
    AgentStateResponse,
    AgentInteractionsResponse,
    AcdInteractionsResponse,
    CampaignProfileDispositionCriteria,
    UtilizationThresholdSettings,
    CampaignResourceLimits,
    EmailUtilizationThresholdSettings,
)


class SnapshotStatsClient(Five9StatsClient):
    """Client for the Five9 Real-time Stats Snapshot API."""
    
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
        Initialize the Real-time Stats Snapshot API client.
        
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
        Retrieve statistics by domain.
        
        Args:
            domain_id: Unique ID of the domain
            
        Returns:
            Metadata for statistics
        """
        path = f"/snapshot-stats/v1/domains/{domain_id}/statistics"
        return await self.get(path, response_model=SubscriptionMetadata)
    
    async def get_acd_status(
        self,
        domain_id: str,
        media_types: Optional[str] = None,
        filters: Optional[str] = None,
        page_limit: Optional[int] = None,
        page_cursor: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> AcdStatusResponse:
        """
        Retrieve the ACD status for a domain.
        
        Args:
            domain_id: Unique ID of the domain
            media_types: Comma separated media types (e.g., "VOICE,CHAT,EMAIL")
            filters: Comma separated agent/campaign/skill IDs
            page_limit: The page limit (max 100)
            page_cursor: The page cursor to retrieve a specified page of results
            sort: Field to sort the result order (use '-' to indicate descending order)
            
        Returns:
            ACD status response
        """
        path = f"/snapshot-stats/v1/domains/{domain_id}/statistics/acd-status"
        params = {
            "mediaTypes": media_types,
            "filters": filters,
            "pageLimit": page_limit,
            "pageCursor": page_cursor,
            "sort": sort,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return await self.get(path, params=params, response_model=AcdStatusResponse)
    
    async def get_agent_state(
        self,
        domain_id: str,
        media_types: Optional[str] = None,
        filters: Optional[str] = None,
        page_limit: Optional[int] = None,
        page_cursor: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> AgentStateResponse:
        """
        Retrieve agent states for a domain.
        
        Args:
            domain_id: Unique ID of the domain
            media_types: Comma separated media types (e.g., "VOICE,CHAT,EMAIL")
            filters: Comma separated agent/campaign/skill IDs
            page_limit: The page limit (max 100)
            page_cursor: The page cursor to retrieve a specified page of results
            sort: Field to sort the result order (use '-' to indicate descending order)
            
        Returns:
            Agent state response
        """
        path = f"/snapshot-stats/v1/domains/{domain_id}/statistics/agent-state"
        params = {
            "mediaTypes": media_types,
            "filters": filters,
            "pageLimit": page_limit,
            "pageCursor": page_cursor,
            "sort": sort,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return await self.get(path, params=params, response_model=AgentStateResponse)
    
    async def get_queue_status(
        self,
        domain_id: str,
        media_types: Optional[str] = None,
        filters: Optional[str] = None,
        page_limit: Optional[int] = None,
        page_cursor: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> QueueStatusResponse:
        """
        Retrieve the Queue status for a domain.
        
        Args:
            domain_id: Unique ID of the domain
            media_types: Comma separated media types (e.g., "VOICE,CHAT,EMAIL")
            filters: Comma separated agent/campaign/skill IDs
            page_limit: The page limit (max 100)
            page_cursor: The page cursor to retrieve a specified page of results
            sort: Field to sort the result order (use '-' to indicate descending order)
            
        Returns:
            Queue status response
        """
        path = f"/snapshot-stats/v1/domains/{domain_id}/statistics/queue-status"
        params = {
            "mediaTypes": media_types,
            "filters": filters,
            "pageLimit": page_limit,
            "pageCursor": page_cursor,
            "sort": sort,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return await self.get(path, params=params, response_model=QueueStatusResponse)
    
    async def get_agent_interactions(
        self,
        domain_id: str,
        user_uid: str,
        media_types: Optional[str] = None,
    ) -> AgentInteractionsResponse:
        """
        Retrieve user interactions.
        
        Args:
            domain_id: Unique ID of the domain
            user_uid: User UID
            media_types: Comma separated media types (e.g., "VOICE,CHAT,EMAIL")
            
        Returns:
            Agent interactions response
        """
        path = f"/snapshot-stats/v1/domains/{domain_id}/statistics/interactions/user/{user_uid}"
        params = {
            "mediaTypes": media_types,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return await self.get(path, params=params, response_model=AgentInteractionsResponse)
    
    async def get_acd_interactions(
        self,
        domain_id: str,
        skill_id: str,
        media_types: Optional[str] = None,
        in_queue: Optional[bool] = None,
    ) -> AcdInteractionsResponse:
        """
        Retrieve ACD interaction details by skill.
        
        Args:
            domain_id: Unique ID of the domain
            skill_id: Skill Id
            media_types: Comma separated media types (e.g., "VOICE,CHAT,EMAIL")
            in_queue: If true, retrieves interactions in queue; otherwise, retrieves voicemails in progress
            
        Returns:
            ACD interactions response
        """
        path = f"/snapshot-stats/v1/domains/{domain_id}/statistics/acd-interactions/skill/{skill_id}"
        params = {
            "mediaTypes": media_types,
            "inQueue": in_queue,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return await self.get(path, params=params, response_model=AcdInteractionsResponse)
    
    async def get_campaign_profile_disposition_counts(
        self,
        domain_id: str,
        campaign_profile_id: str,
    ) -> CampaignProfileDispositionCriteria:
        """
        Return the campaign profile disposition counts.
        
        Args:
            domain_id: Domain ID
            campaign_profile_id: Campaign profile ID
            
        Returns:
            Campaign profile disposition criteria
        """
        path = f"/snapshot-stats/v1/domains/{domain_id}/campaign-profiles/{campaign_profile_id}/disposition-counts"
        return await self.get(path, response_model=CampaignProfileDispositionCriteria)
    
    async def update_campaign_profile_disposition_counts(
        self,
        domain_id: str,
        campaign_profile_id: str,
        criteria: CampaignProfileDispositionCriteria,
        if_match: Optional[str] = None,
    ) -> CampaignProfileDispositionCriteria:
        """
        Update the campaign profile disposition count.
        
        Args:
            domain_id: Domain ID
            campaign_profile_id: Campaign profile ID
            criteria: Campaign profile disposition criteria
            if_match: If-Match header for conditional requests
            
        Returns:
            Updated campaign profile disposition criteria
        """
        path = f"/snapshot-stats/v1/domains/{domain_id}/campaign-profiles/{campaign_profile_id}/disposition-counts"
        headers = {}
        if if_match:
            headers["If-Match"] = if_match
        
        return await self.put(
            path,
            json_data=criteria.dict(by_alias=True),
            headers=headers,
            response_model=CampaignProfileDispositionCriteria,
        )
    
    async def get_inbound_campaign_utilization_threshold(
        self,
        domain_id: str,
        campaign_id: str,
    ) -> UtilizationThresholdSettings:
        """
        Retrieve the utilization threshold for inbound campaign notifications.
        
        Args:
            domain_id: Domain ID
            campaign_id: Campaign ID
            
        Returns:
            Utilization threshold settings
        """
        path = f"/snapshot-stats/v1/domains/{domain_id}/campaigns/{campaign_id}/utilization-thresholds"
        return await self.get(path, response_model=UtilizationThresholdSettings)
    
    async def update_inbound_campaign_utilization_threshold(
        self,
        domain_id: str,
        campaign_id: str,
        settings: UtilizationThresholdSettings,
    ) -> UtilizationThresholdSettings:
        """
        Update the utilization threshold for inbound campaign notifications.
        
        Args:
            domain_id: Domain ID
            campaign_id: Campaign ID
            settings: Utilization threshold settings
            
        Returns:
            Updated utilization threshold settings
        """
        path = f"/snapshot-stats/v1/domains/{domain_id}/campaigns/{campaign_id}/utilization-thresholds"
        return await self.put(
            path,
            json_data=settings.dict(by_alias=True),
            response_model=UtilizationThresholdSettings,
        )
    
    async def get_inbound_campaign_resource_limits(
        self,
        domain_id: str,
        campaign_id: str,
    ) -> CampaignResourceLimits:
        """
        Retrieve the inbound campaign resource limits.
        
        Args:
            domain_id: Domain ID
            campaign_id: Campaign ID
            
        Returns:
            Campaign resource limits
        """
        path = f"/snapshot-stats/v1/domains/{domain_id}/campaigns/{campaign_id}/resource-limits"
        return await self.get(path, response_model=CampaignResourceLimits)
    
    async def update_inbound_campaign_resource_limits(
        self,
        domain_id: str,
        campaign_id: str,
        limits: CampaignResourceLimits,
    ) -> CampaignResourceLimits:
        """
        Update the inbound campaign resource limits.
        
        Args:
            domain_id: Domain ID
            campaign_id: Campaign ID
            limits: Campaign resource limits
            
        Returns:
            Updated campaign resource limits
        """
        path = f"/snapshot-stats/v1/domains/{domain_id}/campaigns/{campaign_id}/resource-limits"
        return await self.put(
            path,
            json_data=limits.dict(by_alias=True),
            response_model=CampaignResourceLimits,
        )
    
    async def get_email_utilization_thresholds(
        self,
        domain_id: str,
    ) -> EmailUtilizationThresholdSettings:
        """
        Retrieve the domain utilization threshold for emails.
        
        Args:
            domain_id: Domain ID
            
        Returns:
            Email utilization threshold settings
        """
        path = f"/snapshot-stats/v1/domains/{domain_id}/domain-settings/email"
        return await self.get(path, response_model=EmailUtilizationThresholdSettings)
    
    async def update_email_utilization_thresholds(
        self,
        domain_id: str,
        settings: EmailUtilizationThresholdSettings,
    ) -> EmailUtilizationThresholdSettings:
        """
        Update the domain utilization threshold for emails.
        
        Args:
            domain_id: Domain ID
            settings: Email utilization threshold settings
            
        Returns:
            Updated email utilization threshold settings
        """
        path = f"/snapshot-stats/v1/domains/{domain_id}/domain-settings/email"
        return await self.put(
            path,
            json_data=settings.dict(by_alias=True),
            response_model=EmailUtilizationThresholdSettings,
        )