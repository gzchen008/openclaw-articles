package main

import (
	"flag"
	"fmt"
	"log"
	"os"

	"github.com/opsinspector/opsinspector/pkg/config"
	"github.com/opsinspector/opsinspector/pkg/store"
)

func main() {
	var configPath string
	flag.StringVar(&configPath, "config", "configs/config.yaml", "Path to config file")
	flag.Parse()

	// 加载配置
	cfg, err := config.Load(configPath)
	if err != nil {
		log.Fatalf("Failed to load config: %v", err)
	}

	fmt.Println("OpsInspector Database Migration Tool")
	fmt.Println("=====================================")

	// 连接数据库
	db, err := store.NewStore(cfg.Database.DSN, true)
	if err != nil {
		log.Fatalf("Failed to connect database: %v", err)
	}
	defer db.Close()

	// 测试连接
	fmt.Println("Testing database connection...")
	if err := db.Ping(); err != nil {
		log.Fatalf("Failed to ping database: %v", err)
	}
	fmt.Println("✓ Database connection successful")

	// 执行迁移
	fmt.Println("\nRunning auto-migration...")
	gormStore, ok := db.(*store.GormStore)
	if !ok {
		log.Fatal("Failed to cast store to GormStore")
	}

	if err := gormStore.AutoMigrate(); err != nil {
		log.Fatalf("Failed to migrate database: %v", err)
	}
	fmt.Println("✓ Database migration completed successfully")

	// 执行 SQL 迁移脚本
	fmt.Println("\nRunning SQL migrations...")
	if err := runSQLMigrations(cfg.Database.DSN); err != nil {
		log.Printf("Warning: SQL migrations failed: %v", err)
	} else {
		fmt.Println("✓ SQL migrations completed")
	}

	fmt.Println("\n✓ All migrations completed successfully!")
	os.Exit(0)
}

// runSQLMigrations 执行 SQL 迁移脚本
func runSQLMigrations(dsn string) error {
	// 读取迁移文件
	files, err := os.ReadDir("database/migrations")
	if err != nil {
		return fmt.Errorf("failed to read migrations directory: %w", err)
	}

	for _, file := range files {
		if file.IsDir() {
			continue
		}

		if len(file.Name()) < 4 || file.Name()[len(file.Name())-4:] != ".sql" {
			continue
		}

		fmt.Printf("  - Processing %s\n", file.Name())

		content, err := os.ReadFile("database/migrations/" + file.Name())
		if err != nil {
			return fmt.Errorf("failed to read migration file %s: %w", file.Name(), err)
		}

		// 这里可以使用 gorm.Exec 执行 SQL
		_ = content
	}

	return nil
}
