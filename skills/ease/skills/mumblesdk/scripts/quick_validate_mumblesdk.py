#!/usr/bin/env python3
"""
MumbleSDK 快速合规扫描脚本（模板）

用途：
- 针对目标工程目录（非本 skills 仓库），进行静态规则扫描，评估是否符合 MumbleSDK 集成最佳实践。
- 可与 CI 对接，用于在合并前做快速门禁检查（不替代正式的 Sonar/Checkstyle/PMD/SpotBugs）。

使用：
- python mumble-sdk/scripts/quick_validate_mumblesdk.py --path /path/to/your/project
- 可选：--json 将结果以 JSON 格式输出（便于 CI 解析）
- 结果分类：ERROR（将导致非零退出码），WARN（提示但不阻断）

检查范围（示例规则，按需扩展或调整）：
- Web 层（Controller）：
  * 继承 MumbleAbstractBaseController
  * 使用 execute(...) 模板方法
  * 在 finally 中调用 MumbleContextUtil.clear()
- Service 层：
  * 使用 @Transactional(rollbackFor = Exception.class)（至少有 @Transactional）
  * 分布式锁：存在 tryLock(...) 与 finally + unlock(...) 组合
  * 上下文与流水：存在 MumbleContextUtil.setBizSeqNo(...)、setTxnSeqNo(...) 且 finally 中调用 MumbleContextUtil.clear()
- RMB 服务：
  * 存在 @MumbleRmbService / @MumbleServiceMethod（或至少按示例结构使用 ResponseMessage）
  * finally 中调用 MumbleContextUtil.clear()
- DTO/校验：
  * Controller 使用 @Validated
  * 入参 DTO 使用金融级注解（WebankNotBlank/WebankMobilePhone/WebankIdNo 等）
- DAO/Mapper/XML：
  * 不允许 select *
  * 参数使用 #{param, jdbcType=...}
  * 建议存在 BaseResultMap / Base_Column_List
  * 语句具备 where 条件（简单检查）
  * Java DAO 接口方法声明 throws SQLException（建议）
  * DAO 类继承 AbstractSimpleDAO（建议）
  * 数据访问使用 try-with-resources 包裹 MumbleSqlSession（建议）
- 配置：
  * properties-only（禁止 YAML 配置文件）
  * 存在 application-*.properties
- 日志：
  * 如存在 logback-spring.xml，建议包含 %X{bizSeqNo} 与 %X{txnSeqNo}
- 序列：
  * Controller/Service 存在 MumbleSeqService.nextValue(...) 使用

注意：
- 本脚本以正则静态扫描为主，不能保证零误报/漏报；建议配合人工 Code Review 与更严格的静态分析工具。
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple

JAVA_EXT = (".java",)
XML_EXT = (".xml",)
PROPS_EXT = (".properties",)
YAML_EXT = (".yml", ".yaml")

def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        try:
            return path.read_text(encoding="latin-1", errors="ignore")
        except Exception:
            return ""

def find_files(root: Path, exts: Tuple[str, ...]) -> List[Path]:
    return [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in exts]

def has_pattern(content: str, pattern: str, flags: int = re.MULTILINE) -> bool:
    return re.search(pattern, content, flags) is not None

def collect_controller_files(java_files: List[Path]) -> List[Path]:
    res = []
    for p in java_files:
        name = p.name
        if "controller" in str(p.parent).lower() or name.endswith("Controller.java"):
            res.append(p)
    return res

def collect_service_files(java_files: List[Path]) -> List[Path]:
    res = []
    for p in java_files:
        name = p.name
        c = read_text(p)
        in_service_dir = "service" in str(p.parent).lower()
        is_impl = name.endswith("ServiceImpl.java")
        anno_service = has_pattern(c, r"@Service\b")
        if in_service_dir or is_impl or anno_service:
            res.append(p)
    return res

def collect_rmb_files(java_files: List[Path]) -> List[Path]:
    res = []
    for p in java_files:
        name = p.name.lower()
        if "rmb" in str(p.parent).lower() or "rmb" in name:
            res.append(p)
    return res

def collect_dto_files(java_files: List[Path]) -> List[Path]:
    res = []
    for p in java_files:
        if "dto" in str(p.parent).lower() or "request" in p.name.lower() or "req" in p.name.lower():
            res.append(p)
    return res

def collect_dao_files(java_files: List[Path]) -> List[Path]:
    res = []
    for p in java_files:
        name = p.name
        if "dao" in str(p.parent).lower() or name.endswith("Dao.java"):
            res.append(p)
    return res

def rule_controllers(files: List[Path]) -> Dict[str, Any]:
    findings = []
    for f in files:
        c = read_text(f)
        extends_base = has_pattern(c, r"extends\s+MumbleAbstractBaseController")
        use_execute = has_pattern(c, r"\bexecute\s*\(")
        clear_ctx = has_pattern(c, r"MumbleContextUtil\s*\.\s*clear\s*\(")
        validated = has_pattern(c, r"@Validated\b")
        transactional_on_controller = has_pattern(c, r"@Transactional\b")
        has_front_executor = has_pattern(c, r"\bgetFrontTaskExecutor\s*\(")
        has_biz_seq = has_pattern(c, r"\bgetBizSeqNo\s*\(")

        details = []
        sev = "OK"
        # 强制项缺失或违规 → ERROR
        if transactional_on_controller:
            sev = "ERROR"; details.append("控制器禁止使用 @Transactional")
        if not extends_base:
            sev = "ERROR"; details.append("未继承 MumbleAbstractBaseController")
        if not use_execute:
            sev = "ERROR"; details.append("未使用 execute(...) 模板方法")
        if not clear_ctx:
            sev = "ERROR"; details.append("未调用 MumbleContextUtil.clear()")
        # 建议项缺失 → WARN（在未触发 ERROR 时）
        if not validated:
            details.append("未发现 @Validated（建议）")
            if sev == "OK": sev = "WARN"
        if not has_front_executor:
            details.append("未实现 getFrontTaskExecutor()（建议）")
            if sev == "OK": sev = "WARN"
        if not has_biz_seq:
            details.append("未实现 getBizSeqNo()（建议）")
            if sev == "OK": sev = "WARN"

        findings.append({"file": str(f), "result": sev, "notes": details})
    return {"section": "controllers", "findings": findings}

def rule_services(files: List[Path]) -> Dict[str, Any]:
    findings = []
    for f in files:
        c = read_text(f)
        transactional = has_pattern(c, r"@Transactional\b")
        try_lock = has_pattern(c, r"\btryLock\s*\(")
        unlock = has_pattern(c, r"\bunlock\s*\(")
        has_finally = has_pattern(c, r"\bfinally\b")
        # 新增：服务层上下文与流水规范
        set_biz = has_pattern(c, r"MumbleContextUtil\s*\.\s*setBizSeqNo\s*\(")
        set_txn = has_pattern(c, r"MumbleContextUtil\s*\.\s*setTxnSeqNo\s*\(")
        clear_ctx = has_pattern(c, r"MumbleContextUtil\s*\.\s*clear\s*\(")

        notes = []
        sev = "OK"
        if not transactional:
            sev = "ERROR"; notes.append("未发现 @Transactional 注解")
        # 若存在加锁则检查 finally + unlock
        if try_lock and (not (has_finally and unlock)):
            sev = "ERROR"; notes.append("存在 tryLock(...) 但未发现 finally + unlock(...)")
        # 检查上下文设置与清理组合
        if not (set_biz and set_txn and has_finally and clear_ctx):
            sev = "ERROR"; notes.append("未发现 setBizSeqNo/setTxnSeqNo 与 finally + MumbleContextUtil.clear() 的组合")

        findings.append({"file": str(f), "result": sev, "notes": notes})
    return {"section": "services", "findings": findings}

def rule_rmb(files: List[Path]) -> Dict[str, Any]:
    findings = []
    for f in files:
        c = read_text(f)
        anno_service = has_pattern(c, r"@MumbleRmbService\b")
        anno_method = has_pattern(c, r"@MumbleServiceMethod\b")
        response_msg = has_pattern(c, r"\bResponseMessage\b")
        clear_ctx = has_pattern(c, r"MumbleContextUtil\s*\.\s*clear\s*\(")
        has_finally = has_pattern(c, r"\bfinally\b")
        notes = []
        sev = "OK"
        if not response_msg:
            sev = "ERROR"; notes.append("未发现统一响应 ResponseMessage 的使用")
        if not (has_finally and clear_ctx):
            sev = "ERROR"; notes.append("未发现 finally + MumbleContextUtil.clear()")
        if not anno_service:
            notes.append("未发现 @MumbleRmbService（建议）")
        if not anno_method:
            notes.append("未发现 @MumbleServiceMethod（建议）")
        findings.append({"file": str(f), "result": sev, "notes": notes})
    return {"section": "rmb", "findings": findings}

def rule_validation(java_files: List[Path], controller_files: List[Path], dto_files: List[Path]) -> Dict[str, Any]:
    findings = []
    # Controller @Validated
    for f in controller_files:
        c = read_text(f)
        validated = has_pattern(c, r"@Validated\b")
        sev = "OK" if validated else "WARN"
        notes = [] if validated else ["Controller 未使用 @Validated（建议）"]
        findings.append({"file": str(f), "result": sev, "notes": notes})
    # DTO 金融级注解
    webank_pat = r"@Webank(NotBlank|MobilePhone|IdNo|Email|CardNo|Length)\b"
    for f in dto_files:
        c = read_text(f)
        has_webank = has_pattern(c, webank_pat)
        sev = "OK" if has_webank else "WARN"
        notes = [] if has_webank else ["未发现 Webank* 金融级校验注解（视业务需要）"]
        findings.append({"file": str(f), "result": sev, "notes": notes})
    return {"section": "validation", "findings": findings}

def xml_has_select_star(content: str) -> bool:
    return has_pattern(content, r"(?i)\bselect\s+\*")

def xml_params_have_jdbc_type(content: str) -> bool:
    # 若存在 #{...} 参数，则至少应存在一个 jdbcType 使用
    has_param = has_pattern(content, r"#\{[^}]+}")
    has_jdbc = has_pattern(content, r"#\{[^}]+jdbcType\s*=")
    return (not has_param) or has_jdbc

def xml_has_base_maps(content: str) -> bool:
    has_base_result_map = has_pattern(content, r"BaseResultMap")
    has_base_column_list = has_pattern(content, r"Base_Column_List")
    return has_base_result_map and has_base_column_list

def xml_has_where(content: str) -> bool:
    # 使用 flags 参数统一大小写忽略，避免内联 (?i) 引发的 DeprecationWarning
    return has_pattern(content, r"<where>|\bwhere\b", flags=re.IGNORECASE | re.MULTILINE)

def strip_xml_comments(content: str) -> str:
    # 去除 XML 注释，避免将注释中的 "select *" 等内容误判
    return re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)

def is_mapper_xml(path: Path, content: str) -> bool:
    # 仅识别 MyBatis Mapper XML：包含 <mapper ...> 根标签或路径包含 mapper 关键字
    if has_pattern(content, r"<\s*mapper\b", flags=re.IGNORECASE | re.MULTILINE):
        return True
    p = str(path).lower()
    return ("mapper" in p) or ("mybatis" in p)

def rule_mapper_xml(xml_files: List[Path]) -> Dict[str, Any]:
    findings = []
    for f in xml_files:
        c_raw = read_text(f)
        c = strip_xml_comments(c_raw)
        # 仅针对 MyBatis Mapper XML 进行规则检查，其他 XML（如 pom.xml、logback）跳过
        if not is_mapper_xml(f, c_raw):
            findings.append({"file": str(f), "result": "OK", "notes": ["非 MyBatis Mapper XML，跳过"]})
            continue
        notes = []
        sev = "OK"
        if xml_has_select_star(c):
            sev = "ERROR"; notes.append("XML 中存在 select * 禁止使用")
        if not xml_params_have_jdbc_type(c):
            sev = "ERROR"; notes.append("存在 #{...} 参数但未声明 jdbcType（强制）")
        if not xml_has_base_maps(c):
            sev = "ERROR"; notes.append("未同时存在 BaseResultMap 与 Base_Column_List（强制）")
        if not xml_has_where(c):
            sev = "ERROR"; notes.append("未发现 WHERE 条件或 <where>（强制）")
        findings.append({"file": str(f), "result": sev, "notes": notes})
    return {"section": "mapper_xml", "findings": findings}

def rule_dao_java(files: List[Path]) -> Dict[str, Any]:
    findings = []
    for f in files:
        c = read_text(f)
        name = f.name.lower()
        is_class = has_pattern(c, r"\bclass\b")
        # 仅针对 DAO 实现类进行检查：文件名为 *DaoImpl.java / *DAOImpl.java，或显式继承 AbstractSimpleDAO
        is_impl = name.endswith("daoimpl.java") or name.endswith("impl.java") or has_pattern(c, r"extends\s+AbstractSimpleDAO\b")
        if not (is_class and is_impl):
            findings.append({"file": str(f), "result": "OK", "notes": ["非 DAO 实现类，跳过"]})
            continue

        # 类级别基本规则
        throws_sql_any = has_pattern(c, r"throws\s+SQLException\b")
        extends_simple = has_pattern(c, r"extends\s+AbstractSimpleDAO\b")
        try_with_session = has_pattern(c, r"try\s*\(\s*MumbleSqlSession\s+\w+\s*=")

        # 方法级解析：提取每个 public 方法的签名与方法体，进行逐方法检查
        def extract_methods(content: str) -> List[Tuple[str, str]]:
            methods: List[Tuple[str, str]] = []
            for m in re.finditer(r"public\s+[^{]+?\s+[A-Za-z_]\w*\s*\([^)]*\)\s*(?:throws\s+[^{]+?)?\s*\{", content):
                sig = m.group(0)
                start = m.end() - 1  # 位于 '{'
                depth = 0
                i = start
                end = i
                while i < len(content):
                    ch = content[i]
                    if ch == "{":
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                        if depth == 0:
                            end = i
                            break
                    i += 1
                body = content[start + 1:end] if end > start else ""
                methods.append((sig, body))
            return methods

        methods = extract_methods(c)

        # 逐方法 throws 检查（仅针对典型数据访问方法 insert/update/delete/select）
        missing_throws = False
        for sig, _body in methods:
            if re.search(r"public\s+[^\s]+\s+(insert|update|delete|select)\w*\s*\(", sig):
                if not re.search(r"throws\s+SQLException\b", sig):
                    missing_throws = True
                    break

        # 写操作显式 commit 检查：
        # 要求：任何包含 mapper.insert/update/delete* 的方法体，必须出现 commit(...)
        has_write_any = False
        missing_commit = False
        for _sig, body in methods:
            if has_pattern(body, r"mapper\s*\.\s*(insert|update|delete)\w*\s*\("):
                has_write_any = True
                # 放宽接收者名称，允许 session/sqlSession 等变量；只要存在 commit(...) 调用即可视为满足
                if not has_pattern(body, r"\b\w+\s*\.\s*commit\s*\(") and not has_pattern(body, r"\bcommit\s*\("):
                    missing_commit = True
                    break

        # 文件级兜底（若未成功解析方法体但文本存在写操作）
        if not methods:
            has_write_file = has_pattern(c, r"mapper\s*\.\s*(insert|update|delete)\w*\b")
            has_commit_file = has_pattern(c, r"\bcommit\s*\(")
            if has_write_file and (not has_commit_file):
                missing_commit = True

        notes = []
        sev = "OK"
        if missing_throws or (not throws_sql_any):
            notes.append("DAO 方法未声明 throws SQLException（强制）")
        if not extends_simple:
            notes.append("DAO 类未继承 AbstractSimpleDAO（强制）")
        if not try_with_session:
            notes.append("未使用 try-with-resources 包裹 MumbleSqlSession（强制）")
        if missing_commit:
            notes.append("写操作缺少显式 session.commit()（强制）")
        if notes:
            sev = "ERROR"
        findings.append({"file": str(f), "result": sev, "notes": notes})
    return {"section": "dao_java", "findings": findings}

def rule_config(root: Path) -> Dict[str, Any]:
    findings = []
    yaml_files = [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in YAML_EXT]
    props_files = [p for p in root.rglob("application-*.properties") if p.is_file()]
    if yaml_files:
        for f in yaml_files:
            fp = str(f).lower()
            # 例外：CI 配置 YAML 不受 properties-only 限制
            is_ci_yaml = (
                "quality-gates.yml" in fp or
                "/.github/" in fp or
                "/.gitlab/" in fp or
                "/ci/" in fp or
                "pipeline" in fp or
                "sonar" in fp
            )
            if is_ci_yaml:
                findings.append({"file": str(f), "result": "OK", "notes": ["CI 配置 YAML（不受 properties-only 限制）"]})
            else:
                findings.append({"file": str(f), "result": "ERROR", "notes": ["发现 YAML 配置文件，违反 properties-only 约定"]})
    else:
        findings.append({"file": "(glob: *.yml|*.yaml)", "result": "OK", "notes": []})
    if props_files:
        for f in props_files:
            findings.append({"file": str(f), "result": "OK", "notes": []})
    else:
        findings.append({"file": "(glob: application-*.properties)", "result": "WARN", "notes": ["未发现 application-*.properties 文件"]})
    return {"section": "config", "findings": findings}

def rule_logging(root: Path) -> Dict[str, Any]:
    findings = []
    logbacks = [p for p in root.rglob("logback-spring.xml")]
    if not logbacks:
        findings.append({"file": "(logback-spring.xml)", "result": "WARN", "notes": ["未发现 logback-spring.xml（建议检查 MDC 日志链路）"]})
        return {"section": "logging", "findings": findings}
    for f in logbacks:
        c = read_text(f)
        has_biz = has_pattern(c, r"%X\{bizSeqNo\}")
        has_txn = has_pattern(c, r"%X\{txnSeqNo\}")
        if has_biz and has_txn:
            findings.append({"file": str(f), "result": "OK", "notes": []})
        else:
            notes = []
            if not has_biz: notes.append("日志 Pattern 未包含 %X{bizSeqNo}")
            if not has_txn: notes.append("日志 Pattern 未包含 %X{txnSeqNo}")
            findings.append({"file": str(f), "result": "WARN", "notes": notes})
    return {"section": "logging", "findings": findings}

def rule_sequence(java_files: List[Path]) -> Dict[str, Any]:
    findings = []
    seq_usage_files = []
    for f in java_files:
        c = read_text(f)
        if has_pattern(c, r"MumbleSeqService\s*\.") and has_pattern(c, r"\bnextValue\s*\("):
            seq_usage_files.append(f)
    if seq_usage_files:
        for f in seq_usage_files:
            findings.append({"file": str(f), "result": "OK", "notes": []})
    else:
        findings.append({"file": "(search: MumbleSeqService.nextValue)", "result": "WARN", "notes": ["未发现序列服务使用（按需检查）"]})
    return {"section": "sequence", "findings": findings}

def aggregate(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = {"OK": 0, "WARN": 0, "ERROR": 0}
    for section in results:
        for f in section["findings"]:
            total[f["result"]] = total.get(f["result"], 0) + 1
    summary = {
        "ok": total["OK"],
        "warn": total["WARN"],
        "error": total["ERROR"],
    }
    return {"summary": summary, "results": results}

def print_human(agg: Dict[str, Any]) -> None:
    s = agg["summary"]
    print("MumbleSDK 快速合规扫描结果")
    print(f"- OK: {s['ok']} | WARN: {s['warn']} | ERROR: {s['error']}")
    print("")
    for section in agg["results"]:
        print(f"[{section['section']}]")
        for f in section["findings"]:
            notes = "; ".join(f.get("notes", []))
            print(f"  - {f['result']:6s} :: {f['file']}")
            if notes:
                print(f"    * {notes}")
        print("")

def main():
    parser = argparse.ArgumentParser(description="MumbleSDK 快速合规扫描脚本")
    parser.add_argument("--path", required=False, default=".", help="目标工程根目录（默认当前目录）")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出结果")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists() or not root.is_dir():
        print(f"ERROR: 目标目录不存在或不可访问: {root}", file=sys.stderr)
        sys.exit(2)

    java_files = find_files(root, JAVA_EXT)
    xml_files = find_files(root, XML_EXT)

    controller_files = collect_controller_files(java_files)
    service_files = collect_service_files(java_files)
    rmb_files = collect_rmb_files(java_files)
    dto_files = collect_dto_files(java_files)
    dao_files = collect_dao_files(java_files)

    results = [
        rule_controllers(controller_files),
        rule_services(service_files),
        rule_rmb(rmb_files),
        rule_validation(java_files, controller_files, dto_files),
        rule_mapper_xml(xml_files),
        rule_dao_java(dao_files),
        rule_config(root),
        rule_logging(root),
        rule_sequence(java_files),
    ]
    agg = aggregate(results)

    if args.json:
        print(json.dumps(agg, ensure_ascii=False, indent=2))
    else:
        print_human(agg)

    exit_code = 0 if agg["summary"]["error"] == 0 else 1
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
