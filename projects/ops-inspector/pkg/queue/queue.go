package queue

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"github.com/google/uuid"
	"github.com/opsinspector/opsinspector/pkg/models"
)

// Queue 任务队列接口
type Queue interface {
	Push(ctx context.Context, task *models.InspectionTask) error
	Pop(ctx context.Context, timeout time.Duration) (*models.InspectionTask, error)
	Complete(ctx context.Context, taskID uuid.UUID) error
	Fail(ctx context.Context, taskID uuid.UUID, reason string) error
	Size(ctx context.Context) (int64, error)
}

// InspectionTask 巡检任务（队列专用）
type InspectionTask struct {
	ID           uuid.UUID             `json:"id"`
	InspectionID uuid.UUID             `json:"inspection_id"`
	Type         TaskType              `json:"type"`
	TriggeredBy  string                `json:"triggered_by"`
	ScheduledAt  time.Time             `json:"scheduled_at"`
	StartedAt    *time.Time            `json:"started_at,omitempty"`
	CompletedAt  *time.Time            `json:"completed_at,omitempty"`
	Attempts     int                   `json:"attempts"`
	MaxAttempts  int                   `json:"max_attempts"`
	Status       TaskStatus            `json:"status"`
	Result       *models.InspectionResult `json:"result,omitempty"`
	Error        string                `json:"error,omitempty"`
}

// TaskType 任务类型
type TaskType string

const (
	TaskTypeScheduled TaskType = "scheduled"
	TaskTypeManual    TaskType = "manual"
	TaskTypeEvent     TaskType = "event"
)

// TaskStatus 任务状态
type TaskStatus string

const (
	TaskStatusPending   TaskStatus = "pending"
	TaskStatusRunning   TaskStatus = "running"
	TaskStatusCompleted TaskStatus = "completed"
	TaskStatusFailed    TaskStatus = "failed"
)

// MemoryQueue 内存队列实现（开发/测试使用）
type MemoryQueue struct {
	tasks   chan *models.InspectionTask
	pending map[uuid.UUID]*models.InspectionTask
}

// NewMemoryQueue 创建内存队列
func NewMemoryQueue(size int) *MemoryQueue {
	return &MemoryQueue{
		tasks:   make(chan *models.InspectionTask, size),
		pending: make(map[uuid.UUID]*models.InspectionTask),
	}
}

// Push 推送任务
func (q *MemoryQueue) Push(ctx context.Context, task *models.InspectionTask) error {
	select {
	case q.tasks <- task:
		return nil
	case <-ctx.Done():
		return ctx.Err()
	}
}

// Pop 取出任务
func (q *MemoryQueue) Pop(ctx context.Context, timeout time.Duration) (*models.InspectionTask, error) {
	select {
	case task := <-q.tasks:
		task.Status = TaskStatusRunning
		now := time.Now()
		task.StartedAt = &now
		q.pending[task.ID] = task
		return task, nil
	case <-ctx.Done():
		return nil, ctx.Err()
	case <-time.After(timeout):
		return nil, nil
	}
}

// Complete 完成任务
func (q *MemoryQueue) Complete(ctx context.Context, taskID uuid.UUID) error {
	delete(q.pending, taskID)
	return nil
}

// Fail 标记任务失败
func (q *MemoryQueue) Fail(ctx context.Context, taskID uuid.UUID, reason string) error {
	if task, exists := q.pending[taskID]; exists {
		task.Status = TaskStatusFailed
		task.Error = reason
		now := time.Now()
		task.CompletedAt = &now
	}
	delete(q.pending, taskID)
	return nil
}

// Size 获取队列长度
func (q *MemoryQueue) Size(ctx context.Context) (int64, error) {
	return int64(len(q.tasks)), nil
}

// RedisQueue Redis队列实现（生产环境使用）
type RedisQueue struct {
	client      RedisClient
	queueKey    string
	workingKey  string
	maxRetries  int
	retryBackoff time.Duration
}

// RedisClient Redis客户端接口
type RedisClient interface {
	LPush(ctx context.Context, key string, values ...interface{}) error
	BRPopLPush(ctx context.Context, source, destination string, timeout time.Duration) (string, error)
	LRem(ctx context.Context, key string, count int64, value interface{}) error
	LLen(ctx context.Context, key string) (int64, error)
}

// NewRedisQueue 创建Redis队列
func NewRedisQueue(client RedisClient, queueKey string) *RedisQueue {
	return &RedisQueue{
		client:       client,
		queueKey:     queueKey,
		workingKey:   queueKey + ":working",
		maxRetries:   3,
		retryBackoff: time.Second * 5,
	}
}

// Push 推送任务到队列
func (q *RedisQueue) Push(ctx context.Context, task *models.InspectionTask) error {
	if task.ID == uuid.Nil {
		task.ID = uuid.New()
	}
	task.Status = TaskStatusPending
	if task.ScheduledAt.IsZero() {
		task.ScheduledAt = time.Now()
	}

	data, err := json.Marshal(task)
	if err != nil {
		return fmt.Errorf("failed to marshal task: %w", err)
	}

	return q.client.LPush(ctx, q.queueKey, data)
}

// Pop 从队列取出任务（阻塞式）
func (q *RedisQueue) Pop(ctx context.Context, timeout time.Duration) (*models.InspectionTask, error) {
	data, err := q.client.BRPopLPush(ctx, q.queueKey, q.workingKey, timeout)
	if err != nil {
		return nil, err
	}
	if data == "" {
		return nil, nil
	}

	var task models.InspectionTask
	if err := json.Unmarshal([]byte(data), &task); err != nil {
		return nil, fmt.Errorf("failed to unmarshal task: %w", err)
	}

	now := time.Now()
	task.StartedAt = &now
	task.Status = TaskStatusRunning

	return &task, nil
}

// Complete 完成任务
func (q *RedisQueue) Complete(ctx context.Context, taskID uuid.UUID) error {
	// 从 working 队列中移除
	data, _ := json.Marshal(map[string]string{"id": taskID.String()})
	return q.client.LRem(ctx, q.workingKey, 0, data)
}

// Fail 标记任务失败
func (q *RedisQueue) Fail(ctx context.Context, taskID uuid.UUID, reason string) error {
	// 实现重试逻辑
	return nil
}

// Size 获取队列长度
func (q *RedisQueue) Size(ctx context.Context) (int64, error) {
	return q.client.LLen(ctx, q.queueKey)
}
