package config

import (
	"fmt"
	"os"
	"time"

	"github.com/spf13/viper"
)

// Config 全局配置
type Config struct {
	Server         ServerConfig         `mapstructure:"server"`
	Database       DatabaseConfig       `mapstructure:"database"`
	Redis          RedisConfig          `mapstructure:"redis"`
	Queue          QueueConfig          `mapstructure:"queue"`
	Scheduler      SchedulerConfig      `mapstructure:"scheduler"`
	Worker         WorkerConfig         `mapstructure:"worker"`
	Notification   NotificationConfig   `mapstructure:"notification"`
	Observability  ObservabilityConfig  `mapstructure:"observability"`
	Plugins        PluginsConfig        `mapstructure:"plugins"`
}

// ServerConfig 服务器配置
type ServerConfig struct {
	Name         string        `mapstructure:"name"`
	Host         string        `mapstructure:"host"`
	Port         int           `mapstructure:"port"`
	GRPCPort     int           `mapstructure:"grpc_port"`
	MetricsPort  int           `mapstructure:"metrics_port"`
	ReadTimeout  time.Duration `mapstructure:"read_timeout"`
	WriteTimeout time.Duration `mapstructure:"write_timeout"`
	Mode         string        `mapstructure:"mode"`
}

// DatabaseConfig 数据库配置
type DatabaseConfig struct {
	Driver          string        `mapstructure:"driver"`
	DSN             string        `mapstructure:"dsn"`
	MaxOpenConns    int           `mapstructure:"max_open_conns"`
	MaxIdleConns    int           `mapstructure:"max_idle_conns"`
	ConnMaxLifetime time.Duration `mapstructure:"conn_max_lifetime"`
	ConnMaxIdleTime time.Duration `mapstructure:"conn_max_idle_time"`
}

// RedisConfig Redis配置
type RedisConfig struct {
	Addr     string `mapstructure:"addr"`
	Password string `mapstructure:"password"`
	DB       int    `mapstructure:"db"`
	PoolSize int    `mapstructure:"pool_size"`
}

// QueueConfig 队列配置
type QueueConfig struct {
	Driver            string        `mapstructure:"driver"`
	MaxRetries        int           `mapstructure:"max_retries"`
	RetryBackoff      time.Duration `mapstructure:"retry_backoff"`
	VisibilityTimeout time.Duration `mapstructure:"visibility_timeout"`
}

// SchedulerConfig 调度器配置
type SchedulerConfig struct {
	Enabled       bool          `mapstructure:"enabled"`
	MaxConcurrent int           `mapstructure:"max_concurrent"`
	CheckInterval time.Duration `mapstructure:"check_interval"`
}

// WorkerConfig Worker配置
type WorkerConfig struct {
	Enabled     bool     `mapstructure:"enabled"`
	Concurrency int      `mapstructure:"concurrency"`
	Queues      []string `mapstructure:"queues"`
}

// NotificationConfig 通知配置
type NotificationConfig struct {
	DefaultChannels []string      `mapstructure:"default_channels"`
	DedupWindow     time.Duration `mapstructure:"dedup_window"`
	BatchSize       int           `mapstructure:"batch_size"`
	BatchInterval   time.Duration `mapstructure:"batch_interval"`
}

// ObservabilityConfig 可观测性配置
type ObservabilityConfig struct {
	Metrics MetricsConfig `mapstructure:"metrics"`
	Tracing TracingConfig `mapstructure:"tracing"`
	Logging LoggingConfig `mapstructure:"logging"`
}

// MetricsConfig 指标配置
type MetricsConfig struct {
	Enabled bool   `mapstructure:"enabled"`
	Path    string `mapstructure:"path"`
}

// TracingConfig 链路追踪配置
type TracingConfig struct {
	Enabled  bool   `mapstructure:"enabled"`
	Endpoint string `mapstructure:"endpoint"`
}

// LoggingConfig 日志配置
type LoggingConfig struct {
	Level  string `mapstructure:"level"`
	Format string `mapstructure:"format"`
}

// PluginsConfig 插件配置
type PluginsConfig struct {
	Dir       string `mapstructure:"dir"`
	AutoLoad  bool   `mapstructure:"auto_load"`
}

// Load 加载配置
func Load(path string) (*Config, error) {
	viper.SetConfigFile(path)
	viper.SetConfigType("yaml")

	// 环境变量覆盖
	viper.SetEnvPrefix("OPSINSPECTOR")
	viper.AutomaticEnv()

	if err := viper.ReadInConfig(); err != nil {
		return nil, fmt.Errorf("failed to read config file: %w", err)
	}

	var cfg Config
	if err := viper.Unmarshal(&cfg); err != nil {
		return nil, fmt.Errorf("failed to unmarshal config: %w", err)
	}

	// 从环境变量读取敏感配置
	if dsn := os.Getenv("DATABASE_DSN"); dsn != "" {
		cfg.Database.DSN = dsn
	}

	return &cfg, nil
}

// GetDSN 获取数据库连接字符串
func (c *DatabaseConfig) GetDSN() string {
	return c.DSN
}
