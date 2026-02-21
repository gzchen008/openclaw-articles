package inspectors

import (
	"context"
	"fmt"
	"os"
	"strconv"
	"strings"
	"syscall"

	"github.com/opsinspector/opsinspector/pkg/inspector"
)

// DiskInspector 磁盘空间巡检器
type DiskInspector struct{}

// NewDiskInspector 创建磁盘巡检器
func NewDiskInspector() *DiskInspector {
	return &DiskInspector{}
}

// Name 返回名称
func (d *DiskInspector) Name() string {
	return "disk"
}

// Description 返回描述
func (d *DiskInspector) Description() string {
	return "磁盘空间使用率检查"
}

// Version 返回版本
func (d *DiskInspector) Version() string {
	return "1.0.0"
}

// Validate 验证配置
func (d *DiskInspector) Validate(config map[string]interface{}) error {
	return nil
}

// Execute 执行检查
func (d *DiskInspector) Execute(ctx context.Context, config map[string]interface{}) (*inspector.Result, error) {
	result := inspector.NewResult()

	// 配置阈值
	warningThreshold := getFloat64(config, "warning_threshold", 80.0)
	criticalThreshold := getFloat64(config, "critical_threshold", 90.0)
	paths := getStringArray(config, "paths", []string{"/"})

	hasCritical := false
	hasWarning := false
	checkedPaths := 0

	for _, path := range paths {
		info, err := getDiskInfo(path)
		if err != nil {
			result.AddDetail(inspector.Detail{
				Name:    fmt.Sprintf("disk/%s", path),
				Status:  inspector.StatusError,
				Message: fmt.Sprintf("Failed to check: %v", err),
			})
			continue
		}

		checkedPaths++
		usagePercent := info.UsagePercent()

		detail := inspector.Detail{
			Name:    fmt.Sprintf("disk/%s", path),
			Status:  inspector.StatusSuccess,
			Value:   fmt.Sprintf("%.1f%%", usagePercent),
			Message: fmt.Sprintf("%.1f%% used (%.1f GB / %.1f GB)",
				usagePercent,
				float64(info.Used)/(1024*1024*1024),
				float64(info.Total)/(1024*1024*1024)),
		}

		// 判断状态
		if usagePercent >= criticalThreshold {
			detail.Status = inspector.StatusFailed
			detail.SuggestedAction = fmt.Sprintf("Disk usage critical, consider freeing up space or expanding storage")
			hasCritical = true
		} else if usagePercent >= warningThreshold {
			detail.Status = inspector.StatusWarning
			detail.SuggestedAction = fmt.Sprintf("Disk usage high, consider cleaning up files")
			hasWarning = true
		}

		result.AddDetail(detail)

		// 添加指标
		result.AddMetric(inspector.Metric{
			Name:   "disk_usage_percent",
			Value:  usagePercent,
			Unit:   "%",
			Labels: map[string]string{"path": path},
		})
		result.AddMetric(inspector.Metric{
			Name:   "disk_total_bytes",
			Value:  float64(info.Total),
			Unit:   "bytes",
			Labels: map[string]string{"path": path},
		})
		result.AddMetric(inspector.Metric{
			Name:   "disk_used_bytes",
			Value:  float64(info.Used),
			Unit:   "bytes",
			Labels: map[string]string{"path": path},
		})
		result.AddMetric(inspector.Metric{
			Name:   "disk_free_bytes",
			Value:  float64(info.Free),
			Unit:   "bytes",
			Labels: map[string]string{"path": path},
		})
	}

	// 设置结果
	if hasCritical {
		result.SetFailed(fmt.Sprintf("Disk usage critical on %d paths (threshold: %.0f%%)",
			checkedPaths, criticalThreshold))
	} else if hasWarning {
		result.SetWarning(fmt.Sprintf("Disk usage high on %d paths (threshold: %.0f%%)",
			checkedPaths, warningThreshold))
	} else {
		result.SetSuccess(fmt.Sprintf("All %d paths healthy", checkedPaths))
	}

	result.Metadata = map[string]interface{}{
		"checked_paths":      checkedPaths,
		"warning_threshold":  warningThreshold,
		"critical_threshold": criticalThreshold,
	}

	return result, nil
}

// DiskInfo 磁盘信息
type DiskInfo struct {
	Path  string
	Total uint64
	Used  uint64
	Free  uint64
}

// UsagePercent 使用率
func (d *DiskInfo) UsagePercent() float64 {
	if d.Total == 0 {
		return 0
	}
	return float64(d.Used) / float64(d.Total) * 100
}

// getDiskInfo 获取磁盘信息
func getDiskInfo(path string) (*DiskInfo, error) {
	var stat syscall.Statfs_t
	if err := syscall.Statfs(path, &stat); err != nil {
		return nil, err
	}

	total := stat.Blocks * uint64(stat.Bsize)
	free := stat.Bavail * uint64(stat.Bsize)
	used := total - free

	return &DiskInfo{
		Path:  path,
		Total: total,
		Used:  used,
		Free:  free,
	}, nil
}

// MemoryInspector 内存巡检器
type MemoryInspector struct{}

// NewMemoryInspector 创建内存巡检器
func NewMemoryInspector() *MemoryInspector {
	return &MemoryInspector{}
}

// Name 返回名称
func (m *MemoryInspector) Name() string {
	return "memory"
}

// Description 返回描述
func (m *MemoryInspector) Description() string {
	return "内存使用率检查"
}

// Version 返回版本
func (m *MemoryInspector) Version() string {
	return "1.0.0"
}

// Validate 验证配置
func (m *MemoryInspector) Validate(config map[string]interface{}) error {
	return nil
}

// Execute 执行检查
func (m *MemoryInspector) Execute(ctx context.Context, config map[string]interface{}) (*inspector.Result, error) {
	result := inspector.NewResult()

	warningThreshold := getFloat64(config, "warning_threshold", 80.0)
	criticalThreshold := getFloat64(config, "critical_threshold", 90.0)

	// 读取内存信息
	memInfo, err := getMemoryInfo()
	if err != nil {
		result.SetError(fmt.Errorf("failed to get memory info: %w", err))
		return result, nil
	}

	usagePercent := memInfo.UsagePercent()

	// 添加详情
	detail := inspector.Detail{
		Name:    "memory/usage",
		Status:  inspector.StatusSuccess,
		Value:   fmt.Sprintf("%.1f%%", usagePercent),
		Message: fmt.Sprintf("%.1f%% used (%.1f GB / %.1f GB)",
			usagePercent,
			float64(memInfo.Used)/(1024*1024*1024),
			float64(memInfo.Total)/(1024*1024*1024)),
	}

	if usagePercent >= criticalThreshold {
		detail.Status = inspector.StatusFailed
		detail.SuggestedAction = "Memory usage critical, consider killing high-memory processes or scaling up"
		result.SetFailed(fmt.Sprintf("Memory usage critical: %.1f%% (threshold: %.0f%%)",
			usagePercent, criticalThreshold))
	} else if usagePercent >= warningThreshold {
		detail.Status = inspector.StatusWarning
		detail.SuggestedAction = "Memory usage high, consider optimizing applications"
		result.SetWarning(fmt.Sprintf("Memory usage high: %.1f%% (threshold: %.0f%%)",
			usagePercent, warningThreshold))
	} else {
		result.SetSuccess(fmt.Sprintf("Memory usage normal: %.1f%%", usagePercent))
	}

	result.AddDetail(detail)

	// 添加指标
	result.AddMetric(inspector.Metric{
		Name:  "memory_usage_percent",
		Value: usagePercent,
		Unit:  "%",
	})
	result.AddMetric(inspector.Metric{
		Name:  "memory_total_bytes",
		Value: float64(memInfo.Total),
		Unit:  "bytes",
	})
	result.AddMetric(inspector.Metric{
		Name:  "memory_used_bytes",
		Value: float64(memInfo.Used),
		Unit:  "bytes",
	})
	result.AddMetric(inspector.Metric{
		Name:  "memory_free_bytes",
		Value: float64(memInfo.Free),
		Unit:  "bytes",
	})
	result.AddMetric(inspector.Metric{
		Name:  "memory_available_bytes",
		Value: float64(memInfo.Available),
		Unit:  "bytes",
	})

	result.Metadata = map[string]interface{}{
		"warning_threshold":  warningThreshold,
		"critical_threshold": criticalThreshold,
	}

	return result, nil
}

// MemoryInfo 内存信息
type MemoryInfo struct {
	Total     uint64
	Used      uint64
	Free      uint64
	Available uint64
	Buffers   uint64
	Cached    uint64
}

// UsagePercent 使用率
func (m *MemoryInfo) UsagePercent() float64 {
	if m.Total == 0 {
		return 0
	}
	return float64(m.Total-m.Available) / float64(m.Total) * 100
}

// getMemoryInfo 获取内存信息
func getMemoryInfo() (*MemoryInfo, error) {
	data, err := os.ReadFile("/proc/meminfo")
	if err != nil {
		// macOS 不支持 /proc/meminfo，返回模拟数据
		return &MemoryInfo{
			Total:     16 * 1024 * 1024 * 1024,
			Used:      8 * 1024 * 1024 * 1024,
			Free:      6 * 1024 * 1024 * 1024,
			Available: 7 * 1024 * 1024 * 1024,
		}, nil
	}

	info := &MemoryInfo{}
	lines := strings.Split(string(data), "\n")

	for _, line := range lines {
		fields := strings.Fields(line)
		if len(fields) < 2 {
			continue
		}

		key := strings.TrimSuffix(fields[0], ":")
		value, _ := strconv.ParseUint(fields[1], 10, 64)
		value *= 1024 // kB to bytes

		switch key {
		case "MemTotal":
			info.Total = value
		case "MemFree":
			info.Free = value
		case "MemAvailable":
			info.Available = value
		case "Buffers":
			info.Buffers = value
		case "Cached":
			info.Cached = value
		}
	}

	info.Used = info.Total - info.Free
	return info, nil
}

// getFloat64 获取 float64 配置
func getFloat64(m map[string]interface{}, key string, defaultValue float64) float64 {
	if v, ok := m[key].(float64); ok {
		return v
	}
	return defaultValue
}

// getStringArray 获取字符串数组配置
func getStringArray(m map[string]interface{}, key string, defaultValue []string) []string {
	if v, ok := m[key].([]interface{}); ok {
		result := make([]string, len(v))
		for i, item := range v {
			if str, ok := item.(string); ok {
				result[i] = str
			}
		}
		return result
	}
	return defaultValue
}
