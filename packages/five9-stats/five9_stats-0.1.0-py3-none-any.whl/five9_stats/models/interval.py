"""
Models for the Five9 Interval Statistics API.

This module contains Pydantic models for the Interval Statistics API,
which provides historical statistics for domains, agents, campaigns, and ACD.
"""

from datetime import datetime
from typing import List, Optional, Any, Dict

from pydantic import BaseModel, Field

from five9_stats.models.common import PageDetails


class AcdStatistics(BaseModel):
    """Interval metrics aggregated by skill Ids for ACD statistics."""
    
    id: Optional[str] = None
    abandon_chat_rate: Optional[float] = Field(None, alias="abandonChatRate")
    abandon_rate: Optional[float] = Field(None, alias="abandonRate")
    average_abandon_time: Optional[int] = Field(None, alias="averageAbandonTime")
    average_active_talk_time: Optional[int] = Field(None, alias="averageActiveTalkTime")
    average_after_call_work_time: Optional[int] = Field(None, alias="averageAfterCallWorkTime")
    average_after_chat_work_time: Optional[int] = Field(None, alias="averageAfterChatWorkTime")
    average_call_time: Optional[int] = Field(None, alias="averageCallTime")
    average_chat_time: Optional[int] = Field(None, alias="averageChatTime")
    average_email_time: Optional[int] = Field(None, alias="averageEmailTime")
    average_first_response_time_for_chat: Optional[int] = Field(None, alias="averageFirstResponseTimeForChat")
    average_first_response_time_for_email: Optional[int] = Field(None, alias="averageFirstResponseTimeForEmail")
    average_handle_time: Optional[int] = Field(None, alias="averageHandleTime")
    average_handle_time_for_chat: Optional[int] = Field(None, alias="averageHandleTimeForChat")
    average_handle_time_for_email: Optional[int] = Field(None, alias="averageHandleTimeForEmail")
    average_queue_time: Optional[int] = Field(None, alias="averageQueueTime")
    average_queue_time_for_chat: Optional[int] = Field(None, alias="averageQueueTimeForChat")
    average_queue_time_for_email: Optional[int] = Field(None, alias="averageQueueTimeForEmail")
    average_speed_of_answer: Optional[int] = Field(None, alias="averageSpeedOfAnswer")
    average_talk_time: Optional[int] = Field(None, alias="averageTalkTime")
    calls_in_service_level: Optional[int] = Field(None, alias="callsInServiceLevel")
    calls_out_of_service_level: Optional[int] = Field(None, alias="callsOutOfServiceLevel")
    inbound_abandon_rate: Optional[float] = Field(None, alias="inboundAbandonRate")
    inbound_calls_abandoned: Optional[int] = Field(None, alias="inboundCallsAbandoned")
    inbound_calls_answered: Optional[int] = Field(None, alias="inboundCallsAnswered")
    inbound_calls_answered_percentage: Optional[float] = Field(None, alias="inboundCallsAnsweredPercentage")
    inbound_calls_offered: Optional[int] = Field(None, alias="inboundCallsOffered")
    longest_queue_time: Optional[int] = Field(None, alias="longestQueueTime")
    longest_queue_time_for_chat: Optional[int] = Field(None, alias="longestQueueTimeForChat")
    longest_queue_time_for_email: Optional[int] = Field(None, alias="longestQueueTimeForEmail")
    outbound_calls_abandoned: Optional[int] = Field(None, alias="outboundCallsAbandoned")
    outbound_abandon_rate: Optional[float] = Field(None, alias="outboundAbandonRate")
    service_level_percentage: Optional[float] = Field(None, alias="serviceLevelPercentage")
    total_calls_count: Optional[int] = Field(None, alias="totalCallsCount")
    total_calls_handled: Optional[int] = Field(None, alias="totalCallsHandled")
    total_cases_handled: Optional[int] = Field(None, alias="totalCasesHandled")
    total_chats_abandoned: Optional[int] = Field(None, alias="totalChatsAbandoned")
    total_chats_closed: Optional[int] = Field(None, alias="totalChatsClosed")
    total_chats_handled: Optional[int] = Field(None, alias="totalChatsHandled")
    total_emails_closed: Optional[int] = Field(None, alias="totalEmailsClosed")
    total_emails_handled: Optional[int] = Field(None, alias="totalEmailsHandled")
    total_emails_parked: Optional[int] = Field(None, alias="totalEmailsParked")
    # Additional fields can be added as needed


class AcdStatisticsResponse(BaseModel):
    """Response containing interval statistics supported under ACD statistics."""
    
    domain_id: Optional[str] = Field(None, alias="domainId")
    data: Optional[List[AcdStatistics]] = None
    paging: Optional[PageDetails] = None


class AgentStatistics(BaseModel):
    """Interval metrics aggregated by agent Ids for agent statistics."""
    
    id: Optional[str] = None
    average_active_talk_time: Optional[int] = Field(None, alias="averageActiveTalkTime")
    average_after_call_work_time: Optional[int] = Field(None, alias="averageAfterCallWorkTime")
    average_after_chat_work_time: Optional[int] = Field(None, alias="averageAfterChatWorkTime")
    average_chat_interaction_time: Optional[int] = Field(None, alias="averageChatInteractionTime")
    average_chat_time: Optional[int] = Field(None, alias="averageChatTime")
    average_email_time: Optional[int] = Field(None, alias="averageEmailTime")
    average_call_time: Optional[int] = Field(None, alias="averageCallTime")
    average_handle_time: Optional[int] = Field(None, alias="averageHandleTime")
    average_handle_time_for_chat: Optional[int] = Field(None, alias="averageHandleTimeForChat")
    average_handle_time_for_email: Optional[int] = Field(None, alias="averageHandleTimeForEmail")
    average_hold_time: Optional[int] = Field(None, alias="averageHoldTime")
    average_not_ready_time: Optional[int] = Field(None, alias="averageNotReadyTime")
    average_ready_time: Optional[int] = Field(None, alias="averageReadyTime")
    average_response_time_for_chat: Optional[int] = Field(None, alias="averageResponseTimeForChat")
    average_response_time_for_email: Optional[int] = Field(None, alias="averageResponseTimeForEmail")
    average_talk_time: Optional[int] = Field(None, alias="averageTalkTime")
    first_call_resolution: Optional[float] = Field(None, alias="firstCallResolution")
    inbound_calls_count: Optional[int] = Field(None, alias="inboundCallsCount")
    internal_calls_count: Optional[int] = Field(None, alias="internalCallsCount")
    occupancy_rate: Optional[float] = Field(None, alias="occupancyRate")
    total_active_talk_time: Optional[int] = Field(None, alias="totalActiveTalkTime")
    total_after_call_work_time: Optional[int] = Field(None, alias="totalAfterCallWorkTime")
    total_after_chat_work_time: Optional[int] = Field(None, alias="totalAfterChatWorkTime")
    total_calls_abandoned: Optional[int] = Field(None, alias="totalCallsAbandoned")
    total_calls_count: Optional[int] = Field(None, alias="totalCallsCount")
    total_calls_handled: Optional[int] = Field(None, alias="totalCallsHandled")
    total_cases_handled: Optional[int] = Field(None, alias="totalCasesHandled")
    total_chats_abandoned: Optional[int] = Field(None, alias="totalChatsAbandoned")
    total_chats_assigned: Optional[int] = Field(None, alias="totalChatsAssigned")
    total_chats_closed: Optional[int] = Field(None, alias="totalChatsClosed")
    total_chats_handled: Optional[int] = Field(None, alias="totalChatsHandled")
    total_chat_time: Optional[int] = Field(None, alias="totalChatTime")
    total_emails_assigned: Optional[int] = Field(None, alias="totalEmailsAssigned")
    total_emails_closed: Optional[int] = Field(None, alias="totalEmailsClosed")
    total_emails_handled: Optional[int] = Field(None, alias="totalEmailsHandled")
    total_emails_parked: Optional[int] = Field(None, alias="totalEmailsParked")
    total_hold_time: Optional[int] = Field(None, alias="totalHoldTime")
    total_login_time: Optional[int] = Field(None, alias="totalLoginTime")
    total_not_ready_time: Optional[int] = Field(None, alias="totalNotReadyTime")
    total_ready_time: Optional[int] = Field(None, alias="totalReadyTime")
    # Additional fields can be added as needed


class AgentStatisticsResponse(BaseModel):
    """Response containing interval statistics supported under agent statistics."""
    
    domain_id: Optional[str] = Field(None, alias="domainId")
    data: Optional[List[AgentStatistics]] = None
    paging: Optional[PageDetails] = None


class CampaignStatistics(BaseModel):
    """Interval metrics aggregated by campaign Ids for campaign statistics."""
    
    id: Optional[str] = None
    abandon_call_rate: Optional[float] = Field(None, alias="abandonCallRate")
    average_abandon_time: Optional[int] = Field(None, alias="averageAbandonTime")
    average_active_talk_time: Optional[int] = Field(None, alias="averageActiveTalkTime")
    average_after_call_work_time: Optional[int] = Field(None, alias="averageAfterCallWorkTime")
    average_after_chat_work_time: Optional[int] = Field(None, alias="averageAfterChatWorkTime")
    average_call_time: Optional[int] = Field(None, alias="averageCallTime")
    average_first_response_time_for_chat: Optional[int] = Field(None, alias="averageFirstResponseTimeForChat")
    average_first_response_time_for_email: Optional[int] = Field(None, alias="averageFirstResponseTimeForEmail")
    average_handle_time: Optional[int] = Field(None, alias="averageHandleTime")
    average_handle_time_for_chat: Optional[int] = Field(None, alias="averageHandleTimeForChat")
    average_handle_time_for_email: Optional[int] = Field(None, alias="averageHandleTimeForEmail")
    average_hold_time: Optional[int] = Field(None, alias="averageHoldTime")
    average_queue_wait_time: Optional[int] = Field(None, alias="averageQueueWaitTime")
    average_queue_wait_time_for_chat: Optional[int] = Field(None, alias="averageQueueWaitTimeForChat")
    average_queue_wait_time_for_email: Optional[int] = Field(None, alias="averageQueueWaitTimeForEmail")
    average_service_level: Optional[int] = Field(None, alias="averageServiceLevel")
    average_speed_of_answer: Optional[int] = Field(None, alias="averageSpeedOfAnswer")
    average_talk_time: Optional[int] = Field(None, alias="averageTalkTime")
    calls_abandoned: Optional[int] = Field(None, alias="callsAbandoned")
    calls_connected: Optional[int] = Field(None, alias="callsConnected")
    calls_in_service_level: Optional[int] = Field(None, alias="callsInServiceLevel")
    calls_out_of_service_level: Optional[int] = Field(None, alias="callsOutOfServiceLevel")
    first_call_resolution: Optional[float] = Field(None, alias="firstCallResolution")
    longest_queue_wait_time: Optional[int] = Field(None, alias="longestQueueWaitTime")
    service_level_queue: Optional[float] = Field(None, alias="serviceLevelQueue")
    total_calls_count: Optional[int] = Field(None, alias="totalCallsCount")
    total_calls_handled: Optional[int] = Field(None, alias="totalCallsHandled")
    total_cases_handled: Optional[int] = Field(None, alias="totalCasesHandled")
    total_chats_abandoned: Optional[int] = Field(None, alias="totalChatsAbandoned")
    total_chats_closed: Optional[int] = Field(None, alias="totalChatsClosed")
    total_chats_handled: Optional[int] = Field(None, alias="totalChatsHandled")
    total_emails_closed: Optional[int] = Field(None, alias="totalEmailsClosed")
    total_emails_handled: Optional[int] = Field(None, alias="totalEmailsHandled")
    total_emails_parked: Optional[int] = Field(None, alias="totalEmailsParked")
    # Additional fields can be added as needed


class CampaignStatisticsResponse(BaseModel):
    """Response containing interval statistics supported under campaign statistics."""
    
    domain_id: Optional[str] = Field(None, alias="domainId")
    data: Optional[List[CampaignStatistics]] = None
    paging: Optional[PageDetails] = None


class QueueStatistics(BaseModel):
    """Queue statistics provides interval metrics aggregated by queue Ids."""
    
    id: Optional[str] = None
    abandon_rate: Optional[float] = Field(None, alias="abandonRate")
    average_abandon_time: Optional[int] = Field(None, alias="averageAbandonTime")
    average_active_talk_time: Optional[int] = Field(None, alias="averageActiveTalkTime")
    average_after_chat_work_time: Optional[int] = Field(None, alias="averageAfterChatWorkTime")
    average_handle_time: Optional[int] = Field(None, alias="averageHandleTime")
    average_queue_time: Optional[int] = Field(None, alias="averageQueueTime")
    average_speed_of_answer: Optional[int] = Field(None, alias="averageSpeedOfAnswer")
    calls_in_service_level: Optional[int] = Field(None, alias="callsInServiceLevel")
    calls_out_of_service_level: Optional[int] = Field(None, alias="callsOutOfServiceLevel")
    inbound_abandon_rate: Optional[float] = Field(None, alias="inboundAbandonRate")
    inbound_calls_abandoned: Optional[int] = Field(None, alias="inboundCallsAbandoned")
    outbound_abandon_rate: Optional[float] = Field(None, alias="outboundAbandonRate")
    outbound_calls_abandoned: Optional[int] = Field(None, alias="outboundCallsAbandoned")
    service_level_percentage: Optional[float] = Field(None, alias="serviceLevelPercentage")
    total_calls_abandoned: Optional[int] = Field(None, alias="totalCallsAbandoned")
    total_calls_count: Optional[int] = Field(None, alias="totalCallsCount")
    total_calls_handled: Optional[int] = Field(None, alias="totalCallsHandled")


class QueueStatisticsResponse(BaseModel):
    """Response containing all the interval statistics supported under Queue Statistics."""
    
    domain_id: Optional[str] = Field(None, alias="domainId")
    data: Optional[List[QueueStatistics]] = None
    paging: Optional[PageDetails] = None