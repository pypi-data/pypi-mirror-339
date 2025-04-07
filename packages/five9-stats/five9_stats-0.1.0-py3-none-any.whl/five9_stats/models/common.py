"""
Common models shared between both Five9 Statistics APIs.

This module contains Pydantic models that are common to both the
Interval Statistics API and the Real-time Stats Snapshot API.
"""

from datetime import datetime
from typing import List, Optional, Any, Dict

from pydantic import BaseModel, Field


class HttpErrorDetail(BaseModel):
    """Error detail information."""
    
    code: Optional[str] = None
    message: Optional[str] = None
    localized_message: Optional[str] = Field(None, alias="localizedMessage")


class TraceableHttpError(BaseModel):
    """Traceable HTTP error response."""
    
    code: Optional[int] = None
    message: Optional[str] = None
    trace_id: Optional[str] = Field(None, alias="traceId")
    details: Optional[List[HttpErrorDetail]] = None
    
    # Allow extra fields for flexibility with different API error formats
    class Config:
        extra = "allow"
        
    @classmethod
    def parse_error(cls, data: Dict[str, Any]) -> 'TraceableHttpError':
        """
        Parse error data with flexible field mapping to handle different error formats.
        
        Args:
            data: Error response data
            
        Returns:
            Parsed TraceableHttpError
        """
        # Try to map common error fields from different formats
        error_data = {}
        
        # Handle code field
        if "code" in data:
            error_data["code"] = data["code"]
        elif "statusCode" in data:
            error_data["code"] = data["statusCode"]
        elif "status" in data:
            error_data["code"] = data["status"]
            
        # Handle message field
        if "message" in data:
            error_data["message"] = data["message"]
        elif "error" in data:
            error_data["message"] = data["error"]
        elif "errorMessage" in data:
            error_data["message"] = data["errorMessage"]
            
        # Handle trace ID field
        if "traceId" in data:
            error_data["traceId"] = data["traceId"]
        elif "trace_id" in data:
            error_data["traceId"] = data["trace_id"]
        elif "requestId" in data:
            error_data["traceId"] = data["requestId"]
            
        # Include all original data for reference
        error_data.update(data)
        
        return cls.parse_obj(error_data)


class AggregationExtraFieldSchema(BaseModel):
    """Additional aggregation field included in statistic data."""
    
    field: Optional[str] = None
    description: Optional[str] = None


class AggregationSchema(BaseModel):
    """Defines the aggregation applied to specified statistic type."""
    
    field: Optional[str] = None
    description: Optional[str] = None
    extra_fields: Optional[List[AggregationExtraFieldSchema]] = Field(None, alias="extraFields")


class FilterSchema(BaseModel):
    """Defines a field eligible for filtering."""
    
    field: Optional[str] = None
    description: Optional[str] = None


class FieldSchema(BaseModel):
    """Describes a field or metric."""
    
    name: Optional[str] = None
    title: Optional[str] = None
    type: Optional[str] = None
    format: Optional[str] = None
    display_format: Optional[str] = Field(None, alias="displayFormat")
    description: Optional[str] = None


class MetadataSchema(BaseModel):
    """Contains information about statistics types."""
    
    statistics_type: Optional[str] = Field(None, alias="statisticsType")
    statistics_class: Optional[str] = Field(None, alias="statisticsClass")
    fields: Optional[List[FieldSchema]] = None
    filters: Optional[List[FilterSchema]] = None
    aggregations: Optional[List[AggregationSchema]] = None
    default_aggregation: Optional[AggregationSchema] = Field(None, alias="defaultAggregation")


class SubscriptionMetadata(BaseModel):
    """Metadata for each subscription statistics type."""
    
    items: List[MetadataSchema]


class PageDetails(BaseModel):
    """Pagination details."""
    
    next: Optional[str] = None
    limit: Optional[int] = None


class DomainRef(BaseModel):
    """Reference to a domain."""
    
    domain_id: Optional[str] = Field(None, alias="domainId")
    uri: Optional[str] = None