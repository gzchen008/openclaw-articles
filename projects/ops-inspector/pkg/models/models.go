package models

import (
	"database/sql/driver"
	"encoding/json"
	"errors"
	"time"

	"github.com/google/uuid"
)

// Inspection 巡检任务定义
type Inspection struct {
	ID             uuid.UUID      `gorm:"type:char(36);primary_key" json:"id"`
	Name           string         `gorm:"type:varchar(255);not null;uniqueIndex" json:"name"`
	Description    string         `gorm:"type:text" json:"description"`
	Type           InspectionType `gorm:"type:varchar(50);not null" json:"type"`
	Schedule       string         `gorm:"type:varchar(100)" json:"schedule"` // Cron表达式
	Config         JSONMap        `gorm:"type:json" json:"config"`
	NotifyChannels StringArray    `gorm:"type:json" json:"notify_channels"`
	SOPID          *uuid.UUID     `gorm:"type:char(36)" json:"sop_id,omitempty"`
	Enabled        bool           `gorm:"default:true" json:"enabled"`
	SuppressWindow int            `gorm:"default:0" json:"suppress_window"` // 抑制窗口(秒)
	Timeout        int            `gorm:"default:300" json:"timeout"`       // 超时时间(秒)
	Retries        int            `gorm:"default:3" json:"retries"`
	CreatedAt      time.Time      `json:"created_at"`
	UpdatedAt      time.Time      `json:"updated_at"`
	DeletedAt      *time.Time     `gorm:"index" json:"deleted_at,omitempty"`
}

// TableName 指定表名
func (Inspection) TableName() string {
	return "inspections"
}

// BeforeCreate 创建前生成UUID
func (i *Inspection) BeforeCreate() error {
	if i.ID == uuid.Nil {
		i.ID = uuid.New()
	}
	return nil
}

// InspectionType 巡检类型
type InspectionType string

const (
	InspectionTypeCron   InspectionType = "cron"
	InspectionTypeEvent  InspectionType = "event"
	InspectionTypeManual InspectionType = "manual"
)

// InspectionRun 巡检执行记录
type InspectionRun struct {
	ID           uuid.UUID       `gorm:"type:char(36);primary_key" json:"id"`
	InspectionID uuid.UUID       `gorm:"type:char(36);index" json:"inspection_id"`
	Status       RunStatus       `gorm:"type:varchar(50);not null" json:"status"`
	TriggeredBy  string          `gorm:"type:varchar(100)" json:"triggered_by"`
	StartedAt    time.Time       `json:"started_at"`
	CompletedAt  *time.Time      `json:"completed_at,omitempty"`
	Duration     int             `json:"duration"` // 执行时长(毫秒)
	Result       *InspectionResult `gorm:"type:json" json:"result,omitempty"`
	ErrorMessage string          `gorm:"type:text" json:"error_message,omitempty"`
	CreatedAt    time.Time       `json:"created_at"`
}

// TableName 指定表名
func (InspectionRun) TableName() string {
	return "inspection_runs"
}

// BeforeCreate 创建前生成UUID
func (r *InspectionRun) BeforeCreate() error {
	if r.ID == uuid.Nil {
		r.ID = uuid.New()
	}
	return nil
}

// RunStatus 执行状态
type RunStatus string

const (
	RunStatusPending   RunStatus = "pending"
	RunStatusRunning   RunStatus = "running"
	RunStatusSuccess   RunStatus = "success"
	RunStatusWarning   RunStatus = "warning"
	RunStatusFailed    RunStatus = "failed"
	RunStatusCancelled RunStatus = "cancelled"
	RunStatusTimeout   RunStatus = "timeout"
)

// InspectionResult 巡检结果
type InspectionResult struct {
	Status   ResultStatus     `json:"status"`
	Level    ResultLevel      `json:"level"`
	Summary  string           `json:"summary"`
	Details  []InspectionDetail `json:"details"`
	Metrics  map[string]Metric `json:"metrics"`
	Output   string           `json:"output"`
}

// ResultStatus 结果状态
type ResultStatus string

const (
	ResultStatusSuccess ResultStatus = "success"
	ResultStatusWarning ResultStatus = "warning"
	ResultStatusFailed  ResultStatus = "failed"
	ResultStatusError   ResultStatus = "error"
)

// ResultLevel 严重程度
type ResultLevel string

const (
	ResultLevelNormal   ResultLevel = "normal"
	ResultLevelWarning  ResultLevel = "warning"
	ResultLevelCritical ResultLevel = "critical"
)

// InspectionDetail 检查项详情
type InspectionDetail struct {
	Name            string      `json:"name"`
	Status          ResultStatus `json:"status"`
	Message         string      `json:"message"`
	Value           interface{} `json:"value"`
	Threshold       interface{} `json:"threshold,omitempty"`
	SuggestedAction string      `json:"suggested_action,omitempty"`
}

// Metric 指标数据
type Metric struct {
	Name   string            `json:"name"`
	Value  float64           `json:"value"`
	Labels map[string]string `json:"labels,omitempty"`
	Unit   string            `json:"unit,omitempty"`
}

// SOP 标准操作流程
type SOP struct {
	ID          uuid.UUID   `gorm:"type:char(36);primary_key" json:"id"`
	Name        string      `gorm:"type:varchar(255);not null;uniqueIndex" json:"name"`
	Description string      `gorm:"type:text" json:"description"`
	Version     string      `gorm:"type:varchar(20)" json:"version"`
	Definition  JSONMap     `gorm:"type:json" json:"definition"`
	Enabled     bool        `gorm:"default:true" json:"enabled"`
	CreatedAt   time.Time   `json:"created_at"`
	UpdatedAt   time.Time   `json:"updated_at"`
}

// TableName 指定表名
func (SOP) TableName() string {
	return "sops"
}

// SOPInstance SOP执行实例
type SOPInstance struct {
	ID          uuid.UUID     `gorm:"type:char(36);primary_key" json:"id"`
	SOPID       uuid.UUID     `gorm:"type:char(36);index" json:"sop_id"`
	RunID       uuid.UUID     `gorm:"type:char(36);index" json:"run_id"`
	Status      SOPStatus     `gorm:"type:varchar(50)" json:"status"`
	Variables   JSONMap       `gorm:"type:json" json:"variables"`
	StartedAt   time.Time     `json:"started_at"`
	CompletedAt *time.Time    `json:"completed_at,omitempty"`
	CreatedAt   time.Time     `json:"created_at"`
}

// TableName 指定表名
func (SOPInstance) TableName() string {
	return "sop_instances"
}

// SOPStatus SOP状态
type SOPStatus string

const (
	SOPStatusPending   SOPStatus = "pending"
	SOPStatusRunning   SOPStatus = "running"
	SOPStatusWaiting   SOPStatus = "waiting"
	SOPStatusPaused    SOPStatus = "paused"
	SOPStatusCompleted SOPStatus = "completed"
	SOPStatusFailed    SOPStatus = "failed"
	SOPStatusCancelled SOPStatus = "cancelled"
)

// NotificationChannel 通知渠道配置
type NotificationChannel struct {
	ID       uuid.UUID `gorm:"type:char(36);primary_key" json:"id"`
	Name     string    `gorm:"type:varchar(100);not null;uniqueIndex" json:"name"`
	Type     string    `gorm:"type:varchar(50);not null" json:"type"` // dingtalk/lark/email/webhook
	Config   JSONMap   `gorm:"type:json" json:"config"`
	Enabled  bool      `gorm:"default:true" json:"enabled"`
	Priority int       `gorm:"default:0" json:"priority"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// TableName 指定表名
func (NotificationChannel) TableName() string {
	return "notification_channels"
}

// NotificationRecord 通知记录
type NotificationRecord struct {
	ID        uuid.UUID `gorm:"type:char(36);primary_key" json:"id"`
	RunID     uuid.UUID `gorm:"type:char(36);index" json:"run_id"`
	ChannelID uuid.UUID `gorm:"type:char(36)" json:"channel_id"`
	Status    string    `gorm:"type:varchar(50)" json:"status"` // pending/sent/failed
	Content   string    `gorm:"type:text" json:"content"`
	Error     string    `gorm:"type:text" json:"error"`
	SentAt    *time.Time `json:"sent_at,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

// TableName 指定表名
func (NotificationRecord) TableName() string {
	return "notification_records"
}

// JSONMap JSON字段类型
type JSONMap map[string]interface{}

// Value 实现driver.Valuer接口
func (j JSONMap) Value() (driver.Value, error) {
	if j == nil {
		return nil, nil
	}
	return json.Marshal(j)
}

// Scan 实现sql.Scanner接口
func (j *JSONMap) Scan(value interface{}) error {
	if value == nil {
		*j = nil
		return nil
	}
	bytes, ok := value.([]byte)
	if !ok {
		return errors.New("type assertion to []byte failed")
	}
	return json.Unmarshal(bytes, j)
}

// StringArray 字符串数组类型
type StringArray []string

// Value 实现driver.Valuer接口
func (s StringArray) Value() (driver.Value, error) {
	if s == nil {
		return nil, nil
	}
	return json.Marshal(s)
}

// Scan 实现sql.Scanner接口
func (s *StringArray) Scan(value interface{}) error {
	if value == nil {
		*s = nil
		return nil
	}
	bytes, ok := value.([]byte)
	if !ok {
		return errors.New("type assertion to []byte failed")
	}
	return json.Unmarshal(bytes, s)
}

// InspectionResult Value 实现driver.Valuer接口
func (r InspectionResult) Value() (driver.Value, error) {
	return json.Marshal(r)
}

// Scan 实现sql.Scanner接口
func (r *InspectionResult) Scan(value interface{}) error {
	if value == nil {
		return nil
	}
	bytes, ok := value.([]byte)
	if !ok {
		return errors.New("type assertion to []byte failed")
	}
	return json.Unmarshal(bytes, r)
}
