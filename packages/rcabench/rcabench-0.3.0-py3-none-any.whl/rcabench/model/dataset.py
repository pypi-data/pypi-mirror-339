from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class DeleteResult(BaseModel):
    """
    数据集批量删除操作结果

    Attributes:
        success_count: 成功删除的数据集数量
        failed_names: 删除失败的数据集名称列表
    """

    success_count: int = Field(
        default=0,
        ge=0,
        description="Number of successfully deleted datasets",
        example=2,
    )

    failed_names: List[str] = Field(
        default_factory=list,
        description="List of dataset names that failed to delete",
        examples=["ts-ts-preserve-service-cpu-exhaustion-znzxcn"],
    )


class DatasetItem(BaseModel):
    """
    数据集元数据信息

    Attributes:
        name: 数据集的唯一标识符
        param: 数据集的配置参数
        start_time: 注入窗口的开始时间戳
        end_time: 注入窗口的结束时间戳
    """

    name: str = Field(
        ...,
        description="Unique identifier for the dataset",
        examples="ts-ts-preserve-service-cpu-exhaustion-znzxcn",
        max_length=64,
    )

    param: Dict[str, Any] = Field(
        ...,
        description="Configuration parameters for dataset",
    )

    start_time: datetime = Field(
        ...,
        description="Start timestamp of injection window",
        examples="2025-03-23T12:05:42+08:00",
    )

    end_time: datetime = Field(
        ...,
        description="End timestamp of injection window",
        examples="2025-03-23T12:06:42+08:00",
    )


class DetectorRecord(BaseModel):
    """
    detector 算法指标记录

    Attributes:
        span_name: 存在问题的Span名称
        issue: 检测到的异常描述
        avg_duration: 平均持续时间指标（分钟）
        succ_rate: 成功率百分比（0-1范围）
        p90: 90分位延迟测量值
        p95: 95分位延迟测量值
        p99: 99分位延迟测量值
    """

    span_name: str = Field(
        ...,
        description="Identified span name with issues",
    )

    issue: str = Field(
        ...,
        description="Description of detected anomaly",
    )

    avg_duration: Optional[float] = Field(
        None,
        description="Average duration metric (seconds)",
    )

    succ_rate: Optional[float] = Field(
        None,
        description="Success rate percentage (0-1 scale)",
        ge=0,
        le=1,
    )

    p90: Optional[float] = Field(
        None,
        description="90th percentile latency measurement",
        ge=0,
        le=1,
        alias="P90",
    )

    p95: Optional[float] = Field(
        None,
        description="95th percentile latency measurement",
        ge=0,
        le=1,
        alias="P95",
    )

    p99: Optional[float] = Field(
        None,
        description="99th percentile latency measurement",
        ge=0,
        le=1,
        alias="P99",
    )


class GranularityRecord(BaseModel):
    """
    粒度分析结果记录

    Attributes:
        level: 分析粒度级别（service/pod/span/metric）
        result: 识别到的根因描述
        rank: 问题严重性排名
        confidence: 分析结果的置信度评分
    """

    level: str = Field(
        ...,
        description="Analysis granularity level (service/pod/span/metric)",
        examples="service",
        max_length=32,
    )

    result: str = Field(
        ...,
        description="Identified root cause description",
        examples="ts-preserve-service",
    )

    rank: int = Field(
        ..., gt=0, description="Severity ranking of the issue", examples=1
    )

    confidence: float = Field(
        ...,
        ge=0,
        le=1,
        description="Confidence score of the analysis result",
        examples=0.8,
    )


class ExecutionRecord(BaseModel):
    """
    根因分析执行记录

    Attributes:
        algorithm: 根因分析算法名称
        granularity_results: 不同粒度层级的分析结果
    """

    algorithm: str = Field(
        ...,
        description="Root cause analysis algorithm name",
        examples="e-diagnose",
    )

    granularity_results: List[GranularityRecord] = Field(
        default_factory=list,
        description="Analysis results across different granularity levels",
    )


class ListResult(BaseModel):
    """
    分页数据集查询结果

    Attributes:
        total: 数据集总数
        datasets: 数据集条目列表
    """

    total: int = Field(
        default=0,
        ge=0,
        description="Total number of datasets",
        examples=20,
    )

    datasets: List[DatasetItem] = Field(
        default_factory=list,
        description="List of datasets",
    )


class QueryResult(DatasetItem):
    """
    包含诊断信息的扩展数据集查询结果

    Attributes:
        detector_result: 详细的异常检测指标
        execution_results: 多算法根因分析结果集合
    """

    detector_result: DetectorRecord = Field(
        ..., description="Detailed anomaly detection metrics"
    )

    execution_results: List[ExecutionRecord] = Field(
        default_factory=list,
        description="Collection of root cause analysis results from multiple algorithms",
    )
