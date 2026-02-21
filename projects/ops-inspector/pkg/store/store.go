
// UpdateNotificationRecord 更新通知记录
func (s *GormStore) UpdateNotificationRecord(ctx context.Context, record *models.NotificationRecord) error {
	return s.db.WithContext(ctx).Save(record).Error
}

// DB 返回 GORM DB 实例
func (s *GormStore) DB() *gorm.DB {
	return s.db
}
