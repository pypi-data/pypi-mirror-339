"""
Models for the Five9 Real-time Stats Snapshot API.

This module contains Pydantic models for the Real-time Stats Snapshot API,
which provides real-time statistics for domains, agents, interactions, campaigns, and utilization thresholds.
"""

from datetime import datetime
from typing import List, Optional, Any, Dict

from pydantic import BaseModel, Field

from five9_stats.models.common import PageDetails, DomainRef


class AcdStatus(BaseModel):
    """ACD Status provides snapshot metrics aggregated by skillId."""
    
    id: Optional[str] = None
    active_calls: Optional[int] = Field(None, alias="activeCalls")
    agents_active: Optional[int] = Field(None, alias="agentsActive")
    agents_logged_in: Optional[int] = Field(None, alias="agentsLoggedIn")
    agents_not_ready_for_chats: Optional[int] = Field(None, alias="agentsNotReadyForChats")
    agents_not_ready_for_emails: Optional[int] = Field(None, alias="agentsNotReadyForEmails")
    agents_not_ready_for_voice: Optional[int] = Field(None, alias="agentsNotReadyForVoice")
    agents_not_ready_for_voicemails: Optional[int] = Field(None, alias="agentsNotReadyForVoicemails")
    agents_on_acw: Optional[int] = Field(None, alias="agentsOnAcw")
    agents_on_call: Optional[int] = Field(None, alias="agentsOnCall")
    agents_on_case: Optional[int] = Field(None, alias="agentsOnCase")
    agents_on_chat: Optional[int] = Field(None, alias="agentsOnChat")
    agents_on_email: Optional[int] = Field(None, alias="agentsOnEmail")
    agents_on_parked_email: Optional[int] = Field(None, alias="agentsOnParkedEmail")
    agents_on_vm: Optional[int] = Field(None, alias="agentsOnVM")
    agents_ready_for_chat: Optional[int] = Field(None, alias="agentsReadyForChat")
    agents_ready_for_emails: Optional[int] = Field(None, alias="agentsReadyForEmails")
    agents_ready_for_voice: Optional[int] = Field(None, alias="agentsReadyForVoice")
    agents_ready_for_voicemail: Optional[int] = Field(None, alias="agentsReadyForVoicemail")
    available_agents: Optional[int] = Field(None, alias="availableAgents")
    callbacks_in_queue: Optional[int] = Field(None, alias="callbacksInQueue")
    calls_in_queue: Optional[int] = Field(None, alias="callsInQueue")
    calls_on_hold: Optional[int] = Field(None, alias="callsOnHold")
    cases_in_queue: Optional[int] = Field(None, alias="casesInQueue")
    chats_in_queue: Optional[int] = Field(None, alias="chatsInQueue")
    cumulative_longest_queue_time: Optional[datetime] = Field(None, alias="cumulativeLongestQueueTime")
    cumulative_current_longest_queue_time: Optional[datetime] = Field(None, alias="cumulativeCurrentLongestQueueTime")
    current_longest_active_call: Optional[datetime] = Field(None, alias="currentLongestActiveCall")
    longest_available_agent: Optional[datetime] = Field(None, alias="longestAvailableAgent")
    current_longest_call_in_queue: Optional[datetime] = Field(None, alias="currentLongestCallInQueue")
    current_longest_call_on_hold: Optional[datetime] = Field(None, alias="currentLongestCallOnHold")
    current_longest_queue_time_for_case: Optional[datetime] = Field(None, alias="currentLongestQueueTimeForCase")
    current_longest_queue_time_for_chat: Optional[datetime] = Field(None, alias="currentLongestQueueTimeForChat")
    current_longest_queue_time_for_email: Optional[datetime] = Field(None, alias="currentLongestQueueTimeForEmail")
    emails_in_queue: Optional[int] = Field(None, alias="emailsInQueue")
    total_text_interactions_in_queue: Optional[int] = Field(None, alias="totalTextInteractionsInQueue")
    voicemails_in_progress: Optional[int] = Field(None, alias="voicemailsInProgress")
    voicemails_in_queue: Optional[int] = Field(None, alias="voicemailsInQueue")
    voicemails_total: Optional[int] = Field(None, alias="voicemailsTotal")


class AcdStatusResponse(BaseModel):
    """Response containing all the snapshot statistics supported under ACD Status."""
    
    domain_id: Optional[str] = Field(None, alias="domainId")
    data: Optional[List[AcdStatus]] = None
    paging: Optional[PageDetails] = None


class QueueStatus(BaseModel):
    """Queue Status provides snapshot metrics aggregated by queueId."""
    
    id: Optional[str] = None
    callbacks_in_queue: Optional[int] = Field(None, alias="callbacksInQueue")
    calls_in_queue: Optional[int] = Field(None, alias="callsInQueue")
    current_longest_call_in_queue: Optional[datetime] = Field(None, alias="currentLongestCallInQueue")
    cumulative_current_longest_queue_time: Optional[datetime] = Field(None, alias="cumulativeCurrentLongestQueueTime")


class QueueStatusResponse(BaseModel):
    """Response containing all the snapshot statistics supported under Queue Status."""
    
    domain_id: Optional[str] = Field(None, alias="domainId")
    data: Optional[List[QueueStatus]] = None
    paging: Optional[PageDetails] = None


class AgentState(BaseModel):
    """Agent state provides snapshot metrics aggregated by agent IDs."""
    
    id: Optional[str] = None
    presence_state: Optional[str] = Field(None, alias="presenceState")
    state_since: Optional[datetime] = Field(None, alias="stateSince")
    call_type: Optional[str] = Field(None, alias="callType")
    chat_interaction_state: Optional[str] = Field(None, alias="chatInteractionState")
    email_interaction_state: Optional[str] = Field(None, alias="emailInteractionState")
    media_availability: Optional[List[str]] = Field(None, alias="mediaAvailability")
    reason_code: Optional[str] = Field(None, alias="reasonCode")
    reason_since: Optional[datetime] = Field(None, alias="reasonSince")
    aid_mode: Optional[List[str]] = Field(None, alias="aidMode")
    voice_interaction_state: Optional[str] = Field(None, alias="voiceInteractionState")
    voicemail_interaction_state: Optional[str] = Field(None, alias="voicemailInteractionState")
    customer_name: Optional[str] = Field(None, alias="customerName")
    campaign_ids: Optional[List[str]] = Field(None, alias="campaignIds")
    skill_id: Optional[List[str]] = Field(None, alias="skillId")
    skill_availability: Optional[List[str]] = Field(None, alias="skillAvailability")
    on_hold_state_since: Optional[datetime] = Field(None, alias="onHoldStateSince")
    on_park_state_since: Optional[datetime] = Field(None, alias="onParkStateSince")
    after_call_work_state_since: Optional[datetime] = Field(None, alias="afterCallWorkStateSince")
    logged_out_state_since: Optional[datetime] = Field(None, alias="loggedOutStateSince")
    ready_state_since: Optional[datetime] = Field(None, alias="readyStateSince")
    not_ready_state_since: Optional[datetime] = Field(None, alias="notReadyStateSince")
    on_call_state_since: Optional[datetime] = Field(None, alias="onCallStateSince")
    on_chat_state_since: Optional[datetime] = Field(None, alias="onChatStateSince")
    parked_email_state_since: Optional[datetime] = Field(None, alias="parkedEmailStateSince")
    current_chats_count: Optional[int] = Field(None, alias="currentChatsCount")
    current_video_chats_count: Optional[int] = Field(None, alias="currentVideoChatsCount")
    current_emails_count: Optional[int] = Field(None, alias="currentEmailsCount")
    current_cases_count: Optional[int] = Field(None, alias="currentCasesCount")
    current_parked_calls_count: Optional[int] = Field(None, alias="currentParkedCallsCount")
    current_parked_emails_count: Optional[int] = Field(None, alias="currentParkedEmailsCount")
    voice_cap: Optional[float] = Field(None, alias="voiceCAP")
    voicemail_cap: Optional[float] = Field(None, alias="voicemailCAP")
    chat_cap: Optional[float] = Field(None, alias="chatCAP")
    email_cap: Optional[float] = Field(None, alias="emailCAP")
    video_cap: Optional[float] = Field(None, alias="videoCAP")
    total_cap: Optional[float] = Field(None, alias="totalCAP")
    voice_wl: Optional[str] = Field(None, alias="voiceWL")
    voicemail_wl: Optional[str] = Field(None, alias="voicemailWL")
    chat_wl: Optional[str] = Field(None, alias="chatWL")
    email_wl: Optional[str] = Field(None, alias="emailWL")
    video_wl: Optional[str] = Field(None, alias="videoWL")
    total_wl: Optional[str] = Field(None, alias="totalWL")
    parked_email_wl: Optional[str] = Field(None, alias="parkedEmailWL")


class AgentStateResponse(BaseModel):
    """Response containing all the snapshot statistics supported under Agent State."""
    
    domain_id: Optional[str] = Field(None, alias="domainId")
    data: Optional[List[AgentState]] = None
    paging: Optional[PageDetails] = None


class AgentInteractions(BaseModel):
    """Agent Interactions provides snapshot of active interaction details for an agent."""
    
    id: Optional[str] = None
    skill_id: Optional[str] = Field(None, alias="skillId")
    campaign_id: Optional[str] = Field(None, alias="campaignId")
    contact_id: Optional[str] = Field(None, alias="contactId")
    customer_name: Optional[str] = Field(None, alias="customerName")
    customer_email: Optional[str] = Field(None, alias="customerEmail")
    media: Optional[str] = None
    media_type: Optional[str] = Field(None, alias="mediaType")
    vendor: Optional[str] = None
    acd_mode: Optional[str] = Field(None, alias="acdMode")
    to: Optional[str] = None
    from_: Optional[str] = Field(None, alias="from")
    subject: Optional[str] = None
    priority: Optional[str] = None
    transfer_count: Optional[int] = Field(None, alias="transferCount")
    state: Optional[str] = None
    create_timestamp: Optional[datetime] = Field(None, alias="createTimestamp")
    assign_timestamp: Optional[datetime] = Field(None, alias="assignTimestamp")
    first_response_timestamp: Optional[datetime] = Field(None, alias="firstResponseTimestamp")
    disposition_timestamp: Optional[datetime] = Field(None, alias="dispositionTimestamp")
    offer_expiration_timestamp: Optional[datetime] = Field(None, alias="offerExpirationTimestamp")
    agent_first_response_timestamp: Optional[datetime] = Field(None, alias="agentFirstResponseTimestamp")
    queued_timestamp: Optional[datetime] = Field(None, alias="queuedTimestamp")
    requeue_timestamp: Optional[datetime] = Field(None, alias="requeueTimestamp")
    parked_timestamp: Optional[datetime] = Field(None, alias="parkedTimestamp")
    parked_expiration: Optional[datetime] = Field(None, alias="parkedExpiration")
    open_disposition_id: Optional[str] = Field(None, alias="openDispositionId")


class AgentInteractionsResponse(BaseModel):
    """Response containing all the snapshot statistics supported under Agent Interactions."""
    
    domain_id: Optional[str] = Field(None, alias="domainId")
    data: Optional[List[AgentInteractions]] = None


class AcdInteractions(BaseModel):
    """ACD Interactions provides snapshot of active interaction details for a skill."""
    
    id: Optional[str] = None
    skill_id: Optional[str] = Field(None, alias="skillId")
    campaign_id: Optional[str] = Field(None, alias="campaignId")
    contact_id: Optional[str] = Field(None, alias="contactId")
    customer_name: Optional[str] = Field(None, alias="customerName")
    customer_number: Optional[str] = Field(None, alias="customerNumber")
    customer_email: Optional[str] = Field(None, alias="customerEmail")
    media: Optional[str] = None
    media_type: Optional[str] = Field(None, alias="mediaType")
    priority: Optional[str] = None
    subject: Optional[str] = None
    to: Optional[str] = None
    transfer_count: Optional[int] = Field(None, alias="transferCount")
    queued_timestamp: Optional[datetime] = Field(None, alias="queuedTimestamp")
    in_queue_callback: Optional[bool] = Field(None, alias="inQueueCallback")
    create_timestamp: Optional[datetime] = Field(None, alias="createTimestamp")


class AcdInteractionsResponse(BaseModel):
    """Response containing all the snapshot statistics supported under ACD Interactions for a given skill."""
    
    domain_id: Optional[str] = Field(None, alias="domainId")
    data: Optional[List[AcdInteractions]] = None


class DispositionReference(BaseModel):
    """The URI reference to a disposition."""
    
    disposition_id: str = Field(..., alias="dispositionId")
    uri: Optional[str] = None


class DispositionCount(BaseModel):
    """Disposition count for campaign profile."""
    
    count: int
    dispositions: List[DispositionReference]


class CampaignProfileDispositionCriteria(BaseModel):
    """Campaign profile disposition criteria."""
    
    criteria: Optional[List[DispositionCount]] = None


class UtilizationThresholdSettings(BaseModel):
    """Utilization threshold settings for inbound campaign notifications."""
    
    alerting_threshold: Optional[int] = Field(None, alias="alertingThreshold")
    alerting_recipients: Optional[str] = Field(None, alias="alertingRecipients")
    domain: Optional[DomainRef] = None
    campaign_id: Optional[str] = Field(None, alias="campaignId")


class CampaignResourceLimits(BaseModel):
    """Resource limits for inbound campaigns."""
    
    max_num_of_voice_lines: Optional[int] = Field(None, alias="maxNumOfVoiceLines")
    max_num_of_vivr_sessions: Optional[int] = Field(None, alias="maxNumOfVivrSessions")
    max_num_of_text_interactions: Optional[int] = Field(None, alias="maxNumOfTextInteractions")
    domain: Optional[DomainRef] = None
    campaign_id: Optional[str] = Field(None, alias="campaignId")


class EmailUtilizationThresholdSettings(BaseModel):
    """Utilization threshold settings for domain emails."""
    
    alerting_threshold: Optional[int] = Field(None, alias="alertingThreshold")
    alerting_recipients: Optional[str] = Field(None, alias="alertingRecipients")
    domain: Optional[DomainRef] = None