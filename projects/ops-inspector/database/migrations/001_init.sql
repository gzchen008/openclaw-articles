-- 创建巡检任务表
CREATE TABLE IF NOT EXISTS inspections (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    type VARCHAR(50) NOT NULL,
    schedule VARCHAR(100),
    config JSON,
    notify_channels JSON,
    sop_id CHAR(36),
    enabled BOOLEAN DEFAULT TRUE,
    suppress_window INT DEFAULT 0,
    timeout INT DEFAULT 300,
    retries INT DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    INDEX idx_inspections_type (type),
    INDEX idx_inspections_enabled (enabled),
    INDEX idx_inspections_deleted_at (deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建巡检执行记录表
CREATE TABLE IF NOT EXISTS inspection_runs (
    id CHAR(36) PRIMARY KEY,
    inspection_id CHAR(36) NOT NULL,
    status VARCHAR(50) NOT NULL,
    triggered_by VARCHAR(100),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    duration INT DEFAULT 0,
    result JSON,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_runs_inspection_id (inspection_id),
    INDEX idx_runs_status (status),
    INDEX idx_runs_started_at (started_at),
    FOREIGN KEY (inspection_id) REFERENCES inspections(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建SOP表
CREATE TABLE IF NOT EXISTS sops (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    version VARCHAR(20) DEFAULT '1.0.0',
    definition JSON,
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_sops_enabled (enabled)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建SOP执行实例表
CREATE TABLE IF NOT EXISTS sop_instances (
    id CHAR(36) PRIMARY KEY,
    sop_id CHAR(36) NOT NULL,
    run_id CHAR(36) NOT NULL,
    status VARCHAR(50) NOT NULL,
    variables JSON,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_sop_instances_sop_id (sop_id),
    INDEX idx_sop_instances_run_id (run_id),
    INDEX idx_sop_instances_status (status),
    FOREIGN KEY (sop_id) REFERENCES sops(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建通知渠道表
CREATE TABLE IF NOT EXISTS notification_channels (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    type VARCHAR(50) NOT NULL,
    config JSON,
    enabled BOOLEAN DEFAULT TRUE,
    priority INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_channels_type (type),
    INDEX idx_channels_enabled (enabled)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建通知记录表
CREATE TABLE IF NOT EXISTS notification_records (
    id CHAR(36) PRIMARY KEY,
    run_id CHAR(36) NOT NULL,
    channel_id CHAR(36) NOT NULL,
    status VARCHAR(50) NOT NULL,
    content TEXT,
    error TEXT,
    sent_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_notifications_run_id (run_id),
    INDEX idx_notifications_status (status),
    INDEX idx_notifications_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入默认通知渠道
INSERT INTO notification_channels (id, name, type, config, enabled) VALUES
('00000000-0000-0000-0000-000000000001', 'default-webhook', 'webhook', '{"url": "http://localhost:8080/webhook"}', TRUE);
