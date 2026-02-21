package inspectors

import (
	"context"
	"crypto/tls"
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"

	"github.com/opsinspector/opsinspector/pkg/inspector"
)

// HTTPInspector HTTP健康检查巡检器
type HTTPInspector struct{}

// NewHTTPInspector 创建HTTP巡检器
func NewHTTPInspector() *HTTPInspector {
	return &HTTPInspector{}
}

// Name 返回巡检器名称
func (h *HTTPInspector) Name() string {
	return "http"
}

// Description 返回描述
func (h *HTTPInspector) Description() string {
	return "HTTP/HTTPS 接口健康检查"
}

// Version 返回版本
func (h *HTTPInspector) Version() string {
	return "1.0.0"
}

// Validate 验证配置
func (h *HTTPInspector) Validate(config map[string]interface{}) error {
	url, ok := config["url"].(string)
	if !ok || url == "" {
		return fmt.Errorf("url is required")
	}
	if !strings.HasPrefix(url, "http://") && !strings.HasPrefix(url, "https://") {
		return fmt.Errorf("url must start with http:// or https://")
	}
	return nil
}

// Execute 执行检查
func (h *HTTPInspector) Execute(ctx context.Context, config map[string]interface{}) (*inspector.Result, error) {
	result := inspector.NewResult()

	// 解析配置
	url := getString(config, "url", "")
	method := getString(config, "method", "GET")
	timeout := getInt(config, "timeout", 10)
	expectedStatus := getInt(config, "expected_status", 200)
	expectedBody := getString(config, "expected_body", "")
	followRedirects := getBool(config, "follow_redirects", true)
	insecureSSL := getBool(config, "insecure_ssl", false)
	headers := getMap(config, "headers")

	// 创建 HTTP 客户端
	transport := &http.Transport{
		TLSClientConfig: &tls.Config{
			InsecureSkipVerify: insecureSSL,
		},
	}

	client := &http.Client{
		Transport: transport,
		Timeout:   time.Duration(timeout) * time.Second,
	}

	if !followRedirects {
		client.CheckRedirect = func(req *http.Request, via []*http.Request) error {
			return http.ErrUseLastResponse
		}
	}

	// 创建请求
	req, err := http.NewRequestWithContext(ctx, method, url, nil)
	if err != nil {
		result.SetError(fmt.Errorf("failed to create request: %w", err))
		return result, nil
	}

	// 添加请求头
	for key, value := range headers {
		if strValue, ok := value.(string); ok {
			req.Header.Set(key, strValue)
		}
	}

	// 设置默认 User-Agent
	if req.Header.Get("User-Agent") == "" {
		req.Header.Set("User-Agent", "OpsInspector/1.0")
	}

	// 发送请求
	startTime := time.Now()
	resp, err := client.Do(req)
	responseTime := time.Since(startTime)

	if err != nil {
		result.SetFailed(fmt.Sprintf("Request failed: %v", err))
		result.AddDetail(inspector.Detail{
			Name:    "connection",
			Status:  inspector.StatusFailed,
			Message: err.Error(),
		})
		return result, nil
	}
	defer resp.Body.Close()

	// 读取响应体
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		result.SetFailed(fmt.Sprintf("Failed to read response body: %v", err))
		return result, nil
	}

	bodyStr := string(body)

	// 检查状态码
	statusOK := resp.StatusCode == expectedStatus
	bodyOK := true
	if expectedBody != "" {
		bodyOK = strings.Contains(bodyStr, expectedBody)
	}

	// 添加指标
	result.AddMetric(inspector.Metric{
		Name:  "response_time_ms",
		Value: float64(responseTime.Milliseconds()),
		Unit:  "ms",
	})
	result.AddMetric(inspector.Metric{
		Name:  "status_code",
		Value: float64(resp.StatusCode),
		Unit:  "",
	})
	result.AddMetric(inspector.Metric{
		Name:  "response_size",
		Value: float64(len(body)),
		Unit:  "bytes",
	})

	// 添加详情
	result.AddDetail(inspector.Detail{
		Name:    "status_code",
		Status:  boolToStatus(statusOK),
		Message: fmt.Sprintf("HTTP %d (expected %d)", resp.StatusCode, expectedStatus),
		Value:   resp.StatusCode,
		Threshold: expectedStatus,
	})

	result.AddDetail(inspector.Detail{
		Name:    "response_time",
		Status:  inspector.StatusSuccess,
		Message: fmt.Sprintf("Response time: %v", responseTime),
		Value:   responseTime.Milliseconds(),
		Unit:    "ms",
	})

	if expectedBody != "" {
		result.AddDetail(inspector.Detail{
			Name:    "body_check",
			Status:  boolToStatus(bodyOK),
			Message: fmt.Sprintf("Body contains expected content: %v", bodyOK),
		})
	}

	// 设置最终结果
	if !statusOK {
		result.SetFailed(fmt.Sprintf("Unexpected status code: %d (expected %d)", resp.StatusCode, expectedStatus))
	} else if !bodyOK {
		result.SetFailed("Response body does not contain expected content")
	} else {
		result.SetSuccess(fmt.Sprintf("HTTP check passed: %d in %v", resp.StatusCode, responseTime))
	}

	result.Metadata = map[string]interface{}{
		"url":            url,
		"method":         method,
		"status_code":    resp.StatusCode,
		"response_time":  responseTime.Milliseconds(),
		"content_length": len(body),
	}

	return result, nil
}

// 辅助函数
func getString(m map[string]interface{}, key, defaultValue string) string {
	if v, ok := m[key].(string); ok && v != "" {
		return v
	}
	return defaultValue
}

func getInt(m map[string]interface{}, key string, defaultValue int) int {
	if v, ok := m[key].(float64); ok {
		return int(v)
	}
	if v, ok := m[key].(int); ok {
		return v
	}
	return defaultValue
}

func getBool(m map[string]interface{}, key string, defaultValue bool) bool {
	if v, ok := m[key].(bool); ok {
		return v
	}
	return defaultValue
}

func getMap(m map[string]interface{}, key string) map[string]interface{} {
	if v, ok := m[key].(map[string]interface{}); ok {
		return v
	}
	return make(map[string]interface{})
}

func boolToStatus(ok bool) inspector.Status {
	if ok {
		return inspector.StatusSuccess
	}
	return inspector.StatusFailed
}
