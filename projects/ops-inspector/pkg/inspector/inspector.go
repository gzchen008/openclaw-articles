package inspector

import (
	"context"
	"fmt"
	"time"
)

// Inspector 巡检器接口
type Inspector interface {
	Name() string
	Description() string
	Version() string
	Validate(config map[string]interface{}) error
	Execute(ctx context.Context, config map[string]interface{}) (*Result, error)
}

// Result 巡检结果
type Result struct {
	Status    Status                 `json:"status"`
	Level     Level                  `json:"level"`
	Summary   string                 `json:"summary"`
	Details   []Detail               `json:"details"`
	Metrics   map[string]Metric      `json:"metrics"`
	StartTime time.Time              `json:"start_time"`
	EndTime   time.Time              `json:"end_time"`
	Duration  time.Duration          `json:"duration"`
	Metadata  map[string]interface{} `json:"metadata"`
}

// Status 巡检状态
type Status string

const (
	StatusSuccess Status = "success"
	StatusWarning Status = "warning"
	StatusFailed  Status = "failed"
	StatusError   Status = "error"
)

// Level 严重程度
type Level string

const (
	LevelNormal   Level = "normal"
	LevelWarning  Level = "warning"
	LevelCritical Level = "critical"
)

// Detail 检查项详情
type Detail struct {
	Name            string                 `json:"name"`
	Status          Status                 `json:"status"`
	Message         string                 `json:"message"`
	Value           interface{}            `json:"value"`
	Threshold       interface{}            `json:"threshold,omitempty"`
	SuggestedAction string                 `json:"suggested_action,omitempty"`
	Metadata        map[string]interface{} `json:"metadata,omitempty"`
}

// Metric 指标数据
type Metric struct {
	Name   string            `json:"name"`
	Value  float64           `json:"value"`
	Labels map[string]string `json:"labels,omitempty"`
	Unit   string            `json:"unit,omitempty"`
}

// Registry 巡检器注册表
type Registry struct {
	inspectors map[string]Inspector
}

// NewRegistry 创建注册表
func NewRegistry() *Registry {
	return &Registry{
		inspectors: make(map[string]Inspector),
	}
}

// Register 注册巡检器
func (r *Registry) Register(inspector Inspector) error {
	name := inspector.Name()
	if _, exists := r.inspectors[name]; exists {
		return fmt.Errorf("inspector %s already registered", name)
	}
	r.inspectors[name] = inspector
	return nil
}

// Get 获取巡检器
func (r *Registry) Get(name string) (Inspector, bool) {
	insp, exists := r.inspectors[name]
	return insp, exists
}

// List 列出所有巡检器
func (r *Registry) List() []Inspector {
	list := make([]Inspector, 0, len(r.inspectors))
	for _, insp := range r.inspectors {
		list = append(list, insp)
	}
	return list
}

// NewResult 创建结果
func NewResult() *Result {
	return &Result{
		Status:   StatusSuccess,
		Level:    LevelNormal,
		Details:  make([]Detail, 0),
		Metrics:  make(map[string]Metric),
		Metadata: make(map[string]interface{}),
		StartTime: time.Now(),
	}
}

// SetError 设置错误结果
func (r *Result) SetError(err error) {
	r.Status = StatusError
	r.Level = LevelCritical
	r.Summary = err.Error()
	r.EndTime = time.Now()
	r.Duration = r.EndTime.Sub(r.StartTime)
}

// SetFailed 设置失败结果
func (r *Result) SetFailed(message string) {
	r.Status = StatusFailed
	r.Level = LevelCritical
	r.Summary = message
	r.EndTime = time.Now()
	r.Duration = r.EndTime.Sub(r.StartTime)
}

// SetWarning 设置警告结果
func (r *Result) SetWarning(message string) {
	r.Status = StatusWarning
	r.Level = LevelWarning
	r.Summary = message
	r.EndTime = time.Now()
	r.Duration = r.EndTime.Sub(r.StartTime)
}

// SetSuccess 设置成功结果
func (r *Result) SetSuccess(message string) {
	r.Status = StatusSuccess
	r.Level = LevelNormal
	r.Summary = message
	r.EndTime = time.Now()
	r.Duration = r.EndTime.Sub(r.StartTime)
}

// AddDetail 添加检查项详情
func (r *Result) AddDetail(detail Detail) {
	r.Details = append(r.Details, detail)
	// 根据详情更新整体状态
	if detail.Status == StatusError && r.Status != StatusError {
		r.Status = StatusError
		r.Level = LevelCritical
	} else if detail.Status == StatusFailed && r.Status == StatusSuccess {
		r.Status = StatusFailed
		r.Level = LevelCritical
	} else if detail.Status == StatusWarning && r.Status == StatusSuccess {
		r.Status = StatusWarning
		r.Level = LevelWarning
	}
}

// AddMetric 添加指标
func (r *Result) AddMetric(metric Metric) {
	r.Metrics[metric.Name] = metric
}
