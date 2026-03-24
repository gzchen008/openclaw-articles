/*
MumbleSDK 模板占位：MyBatis Mapper 接口（强制规范版）

说明：
- 为避免 IDE/语言服务将模板示例当作真实 Java 源解析导致报错，本 .java 文件仅保留占位与指引。
- 完整可复制的模板与示例代码已放置在同目录下的 Markdown 文档中，请按指引复制到真实工程并调整包名/类名后使用。

请打开并参考：
- mumble-sdk/templates/mybatis/mybatis-mapper-interface.md

强制规范要点摘要（复制到工程时务必遵守）：
1) 接口命名与 XML namespace 必须完全一致；
2) Mapper 接口的所有方法必须声明 throws SQLException；
3) XML 必须包含 BaseResultMap 与 Base_Column_List；
4) 禁止使用 select *；所有参数使用 #{param, jdbcType=...}；
5) 更新/删除必须具备明确 where 条件；
6) 时间统一使用 LocalDateTime；DTO/Condition 字段与 JDBC 类型一致。

复制步骤（建议）：
- 在 src/main/java 下创建真实接口文件（如 ActivityInfoMapper.java），将 .md 文档中的代码片段复制并按业务字段调整；
- 在 resources/mapper 下创建 ActivityInfoMapper.xml，并复制 .md 中的 XML 片段；
- 对齐企业 MyBatis/MySQL 配置与连接池最佳实践。
*/
