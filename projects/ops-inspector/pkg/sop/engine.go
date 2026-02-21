package sop

import (
	"context"
	"fmt"
	"time"

	"github.com/google/uuid"
	"github.com/opsinspector/opsinspector/pkg/models"
	"github.com/opsinspector/opsinspector/pkg/observability"
	"github.com/opsinspector/opsinspector/pkg/store"
	"go.uber.org/zap"
	"gopkg.in/yaml.v3"
)

// Engine SOP 引擎
type Engine struct {
	store  store.Store
	logger *zap.Logger
	
	// 动作注册表
	actions map[string]Action
	
	// 正在执行的实例
	instances map[string]*Instance
}

// Action SOP 动作接口
type Action interface {
	Name() string
	Execute(ctx context.Context, input map[string]interface{}, vars map[string]interface{}) (*ActionResult, error)
}

// ActionResult 动作执行结果
type ActionResult struct {
	Success bool                   `json:"success"`
	Output  map[string]interface{} `json:"output"`
	Error   string                 `json:"error,omitempty"`
}

// Instance SOP 执行实例
type Instance struct {
	ID       string
	SOPID    uuid.UUID
	RunID    uuid.UUID
	Status   models.SOPStatus
	Vars     map[string]interface{}
	Steps    []StepState
	Current  int
	Logger   *zap.Logger
}

// StepState 步骤状态
type StepState struct {
	ID       string
	Name     string
	Status   models.SOPStatus
	Started  *time.Time
	Finished *time.Time
	Output   map[string]interface{}
	Error    string
}

// NewEngine 创建 SOP 引擎
func NewEngine(store store.Store, logger *zap.Logger) *Engine {
	return &Engine{
		store:     store,
		logger:    logger,
		actions:   make(map[string]Action),
		instances: make(map[string]*Instance),
	}
}

// RegisterAction 注册动作
func (e *Engine) RegisterAction(action Action) {
	e.actions[action.Name()] = action
}

// StartSOP 启动 SOP 执行
func (e *Engine) StartSOP(ctx context.Context, sopID uuid.UUID, runID uuid.UUID, vars map[string]interface{}) (*Instance, error) {
	// 获取 SOP 定义
	sop, err := e.store.GetSOP(ctx, sopID.String())
	if err != nil {
		return nil, fmt.Errorf("failed to get SOP: %w", err)
	}
	if sop == nil {
		return nil, fmt.Errorf("SOP not found: %s", sopID)
	}

	// 解析 SOP 定义
	var definition SOPDefinition
	if err := mapToStruct(sop.Definition, &definition); err != nil {
		return nil, fmt.Errorf("failed to parse SOP definition: %w", err)
	}

	// 创建实例
	instance := &Instance{
		ID:     uuid.New().String(),
		SOPID:  sopID,
		RunID:  runID,
		Status: models.SOPStatusRunning,
		Vars:   mergeVars(definition.Variables, vars),
		Steps:  make([]StepState, len(definition.Steps)),
		Logger: e.logger.With(
			zap.String("sop_id", sopID.String()),
			zap.String("instance_id", uuid.New().String()),
		),
	}

	// 初始化步骤状态
	for i, step := range definition.Steps {
		instance.Steps[i] = StepState{
			ID:     step.ID,
			Name:   step.Name,
			Status: models.SOPStatusPending,
		}
	}

	// 保存实例
	e.instances[instance.ID] = instance

	// 异步执行
	go e.executeSOP(instance, definition)

	return instance, nil
}

// executeSOP 执行 SOP
func (e *Engine) executeSOP(instance *Instance, definition SOPDefinition) {
	ctx := context.Background()
	startTime := time.Now()

	instance.Logger.Info("Starting SOP execution",
		zap.Int("total_steps", len(definition.Steps)),
	)

	for i, step := range definition.Steps {
		instance.Current = i
		stepState := &instance.Steps[i]

		// 检查条件
		if step.Condition != "" {
			if !e.evaluateCondition(step.Condition, instance.Vars) {
				stepState.Status = models.SOPStatusSkipped
				instance.Logger.Info("Step skipped due to condition",
					zap.String("step_id", step.ID),
				)
				continue
			}
		}

		// 执行步骤
		stepState.Status = models.SOPStatusRunning
		now := time.Now()
		stepState.Started = &now

		instance.Logger.Info("Executing step",
			zap.String("step_id", step.ID),
			zap.String("action", step.Action),
		)

		result := e.executeStep(ctx, step, instance.Vars)

		finished := time.Now()
		stepState.Finished = &finished
		stepState.Output = result.Output

		if result.Success {
			stepState.Status = models.SOPStatusCompleted
			// 更新变量
			for k, v := range result.Output {
				instance.Vars[k] = v
			}
		} else {
			stepState.Status = models.SOPStatusFailed
			stepState.Error = result.Error

			// 检查失败处理策略
			if definition.OnFailure == "abort" {
				instance.Status = models.SOPStatusFailed
				instance.Logger.Error("SOP failed, aborting",
					zap.String("step_id", step.ID),
					zap.String("error", result.Error),
				)
				break
			}
		}
	}

	// 更新最终状态
	if instance.Status == models.SOPStatusRunning {
		instance.Status = models.SOPStatusCompleted
	}

	duration := time.Since(startTime).Seconds()
	observability.RecordSOPExecution(definition.Name, string(instance.Status), duration)

	instance.Logger.Info("SOP execution completed",
		zap.String("status", string(instance.Status)),
		zap.Float64("duration", duration),
	)
}

// executeStep 执行单个步骤
func (e *Engine) executeStep(ctx context.Context, step Step, vars map[string]interface{}) *ActionResult {
	action, ok := e.actions[step.Action]
	if !ok {
		return &ActionResult{
			Success: false,
			Error:   fmt.Sprintf("action not found: %s", step.Action),
		}
	}

	// 渲染输入（变量替换）
	input := renderVars(step.Input, vars)

	// 执行动作
	result, err := action.Execute(ctx, input, vars)
	if err != nil {
		return &ActionResult{
			Success: false,
			Error:   err.Error(),
		}
	}

	return result
}

// evaluateCondition 评估条件
func (e *Engine) evaluateCondition(condition string, vars map[string]interface{}) bool {
	// 简化实现，实际可以使用表达式引擎
	// 例如: "steps['get-pod-info'].output.restartCount > 3"
	return true
}

// GetInstance 获取实例
func (e *Engine) GetInstance(id string) (*Instance, bool) {
	instance, ok := e.instances[id]
	return instance, ok
}

// SOPDefinition SOP 定义结构
type SOPDefinition struct {
	Name        string                 `yaml:"name" json:"name"`
	Description string                 `yaml:"description" json:"description"`
	Version     string                 `yaml:"version" json:"version"`
	Timeout     string                 `yaml:"timeout" json:"timeout"`
	Retries     int                    `yaml:"retries" json:"retries"`
	OnFailure   string                 `yaml:"onFailure" json:"on_failure"`
	Variables   map[string]interface{} `yaml:"variables" json:"variables"`
	Steps       []Step                 `yaml:"steps" json:"steps"`
}

// Step SOP 步骤
type Step struct {
	ID          string                 `yaml:"id" json:"id"`
	Name        string                 `yaml:"name" json:"name"`
	Action      string                 `yaml:"action" json:"action"`
	Input       map[string]interface{} `yaml:"input" json:"input"`
	Condition   string                 `yaml:"condition,omitempty" json:"condition,omitempty"`
	Timeout     string                 `yaml:"timeout,omitempty" json:"timeout,omitempty"`
	Retries     int                    `yaml:"retries,omitempty" json:"retries,omitempty"`
	RetryDelay  string                 `yaml:"retryDelay,omitempty" json:"retry_delay,omitempty"`
	Parallel    bool                   `yaml:"parallel,omitempty" json:"parallel,omitempty"`
}

// 内置动作

// HTTPAction HTTP 请求动作
type HTTPAction struct{}

func (a *HTTPAction) Name() string { return "http:request" }
func (a *HTTPAction) Execute(ctx context.Context, input map[string]interface{}, vars map[string]interface{}) (*ActionResult, error) {
	// 实现 HTTP 请求
	return &ActionResult{Success: true, Output: map[string]interface{}{}}, nil
}

// K8sGetAction K8s 获取资源动作
type K8sGetAction struct{}

func (a *K8sGetAction) Name() string { return "k8s:get" }
func (a *K8sGetAction) Execute(ctx context.Context, input map[string]interface{}, vars map[string]interface{}) (*ActionResult, error) {
	// 实现 K8s 资源获取
	return &ActionResult{Success: true, Output: map[string]interface{}{}}, nil
}

// NotifyAction 通知动作
type NotifyAction struct{}

func (a *NotifyAction) Name() string { return "notify:send" }
func (a *NotifyAction) Execute(ctx context.Context, input map[string]interface{}, vars map[string]interface{}) (*ActionResult, error) {
	// 实现通知发送
	return &ActionResult{Success: true, Output: map[string]interface{}{}}, nil
}

// ExecAction 执行命令动作
type ExecAction struct{}

func (a *ExecAction) Name() string { return "exec:command" }
func (a *ExecAction) Execute(ctx context.Context, input map[string]interface{}, vars map[string]interface{}) (*ActionResult, error) {
	// 实现命令执行
	return &ActionResult{Success: true, Output: map[string]interface{}{}}, nil
}

// 辅助函数

func mergeVars(defaults, overrides map[string]interface{}) map[string]interface{} {
	result := make(map[string]interface{})
	for k, v := range defaults {
		result[k] = v
	}
	for k, v := range overrides {
		result[k] = v
	}
	return result
}

func renderVars(input map[string]interface{}, vars map[string]interface{}) map[string]interface{} {
	result := make(map[string]interface{})
	for k, v := range input {
		result[k] = renderVar(v, vars)
	}
	return result
}

func renderVar(v interface{}, vars map[string]interface{}) interface{} {
	str, ok := v.(string)
	if !ok {
		return v
	}

	// 简单的变量替换 ${varname}
	// 实际可以使用模板引擎
	return str
}

func mapToStruct(m map[string]interface{}, s interface{}) error {
	data, err := yaml.Marshal(m)
	if err != nil {
		return err
	}
	return yaml.Unmarshal(data, s)
}

// InitDefaultActions 初始化默认动作
func (e *Engine) InitDefaultActions() {
	e.RegisterAction(&HTTPAction{})
	e.RegisterAction(&K8sGetAction{})
	e.RegisterAction(&NotifyAction{})
	e.RegisterAction(&ExecAction{})
}
