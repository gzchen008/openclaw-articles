/*
MumbleSDK 模板占位：MyBatis DAO 实现（强制规范版）

说明：
- 为避免 IDE/语言服务将模板示例当作真实 Java 源解析导致报错，本 .java 文件仅保留占位与指引，不包含任何示例代码。
- 完整可复制的模板与示例代码请参阅同目录下的 Markdown 文档：
  - mumble-sdk/templates/mybatis/mybatis-dao-impl-template.md

强制规范要点（DAO/Mapper/XML 三件套）：
1) Mapper 接口的所有方法必须声明 throws SQLException；
2) DAO 实现类必须继承 AbstractSimpleDAO，并通过 try-with-resources 管理 MumbleSqlSession；
3) DAO 实现调用 session.getMapper(YourMapper.class) 委托执行；
4) XML 必须包含 BaseResultMap 与 Base_Column_List；禁止 select *；参数必须 #{..., jdbcType=...}；
5) 更新/删除必须具备明确 where 条件；insertSelective/批量插入/选择性更新/软删除建议提供。

复制步骤（建议）：
- 在 src/main/java 下创建真实实现文件（如 ActivityInfoDAOImpl.java），将 .md 文档中的代码片段复制并按业务字段调整；
- 在 resources/mapper 下创建对应 XML，并复制 .md 或 XML 模板中的片段；
- 对齐企业 MyBatis/MySQL 配置与连接池最佳实践。
*/
