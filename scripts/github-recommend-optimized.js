#!/usr/bin/env node
/**
 * GitHub开源项目智能推荐系统 - 优化版
 * 
 * 功能：
 * 1. 主题轮换（6个主题）
 * 2. 智能筛选（Star数、活跃度、质量）
 * 3. 避免重复推荐
 * 4. 超时保护
 * 5. 完整的项目信息
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
  // 最小Star数（优先10k+）
  minStars: 1000,
  preferredStars: 10000,
  
  // 项目更新时间（30天内）
  maxDaysSinceUpdate: 30,
  
  // 主题轮换（周一到周六）
  themes: [
    { name: 'AI Agent框架', keywords: ['agent', 'ai', 'llm', 'autonomous', 'langchain', 'autogpt'] },
    { name: '代码助手/IDE插件', keywords: ['copilot', 'assistant', 'ide', 'vscode', 'jetbrains', 'code-completion'] },
    { name: 'Skill/工具库', keywords: ['skill', 'tools', 'automation', 'workflow', 'n8n', 'zapier'] },
    { name: '开源大模型', keywords: ['llm', 'model', 'gpt', 'transformer', 'pytorch', 'tensorflow'] },
    { name: '开发效率工具', keywords: ['cli', 'productivity', 'devtools', 'developer-tools', 'terminal'] },
    { name: '自动化工作流', keywords: ['workflow', 'automation', 'ci-cd', 'pipeline', 'devops'] }
  ],
  
  // 状态文件路径
  stateFile: process.env.STATE_FILE || path.join(__dirname, '../memory/github-recommend-state.json'),
  
  // 飞书配置
  targetChannel: process.env.TARGET_CHANNEL || 'feishu',
  targetUser: process.env.TARGET_USER || 'ou_c8b2454b01e8ab6e8957044ebae17f69',
  
  // 超时设置（5分钟）
  timeout: 300000
};

// 读取状态
function loadState() {
  try {
    if (fs.existsSync(CONFIG.stateFile)) {
      return JSON.parse(fs.readFileSync(CONFIG.stateFile, 'utf8'));
    }
  } catch (error) {
    console.error('读取状态文件失败:', error.message);
  }
  
  return {
    lastRun: null,
    currentThemeIndex: 0,
    recommendedProjects: [],
    lastRecommendDate: null
  };
}

// 保存状态
function saveState(state) {
  try {
    const dir = path.dirname(CONFIG.stateFile);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(CONFIG.stateFile, JSON.stringify(state, null, 2));
  } catch (error) {
    console.error('保存状态文件失败:', error.message);
  }
}

// 获取当前主题
function getCurrentTheme() {
  const state = loadState();
  const today = new Date().toISOString().split('T')[0];
  
  // 如果是新的一天，切换到下一个主题
  if (state.lastRecommendDate !== today) {
    state.currentThemeIndex = (state.currentThemeIndex + 1) % CONFIG.themes.length;
    state.lastRecommendDate = today;
    saveState(state);
  }
  
  return CONFIG.themes[state.currentThemeIndex];
}

// 搜索GitHub项目
async function searchGitHubProjects(theme) {
  const query = encodeURIComponent(
    `${theme.keywords.join(' ')} stars:>=${CONFIG.minStars} pushed:>${CONFIG.maxDaysSinceUpdate}days`
  );
  
  const url = `https://api.github.com/search/repositories?q=${query}&sort=stars&order=desc&per_page=30`;
  
  return new Promise((resolve, reject) => {
    const req = https.get(url, {
      headers: {
        'User-Agent': 'OpenClaw-GitHub-Recommend',
        'Accept': 'application/vnd.github.v3+json'
      }
    }, (res) => {
      let data = '';
      
      res.on('data', chunk => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          resolve(result.items || []);
        } catch (error) {
          reject(error);
        }
      });
    });
    
    req.on('error', reject);
    req.setTimeout(30000, () => {
      req.destroy();
      reject(new Error('GitHub API 请求超时'));
    });
  });
}

// 筛选项目
function filterProjects(projects, state) {
  return projects
    // 过滤已推荐的项目
    .filter(p => !state.recommendedProjects.includes(p.full_name))
    // 优先10k+ stars
    .sort((a, b) => {
      const aScore = a.stargazers_count >= CONFIG.preferredStars ? 1 : 0;
      const bScore = b.stargazers_count >= CONFIG.preferredStars ? 1 : 0;
      return bScore - aScore || b.stargazers_count - a.stargazers_count;
    })
    // 质量检查：有描述、有readme、最近更新
    .filter(p => {
      const updatedAt = new Date(p.updated_at);
      const daysSinceUpdate = (Date.now() - updatedAt.getTime()) / (1000 * 60 * 60 * 24);
      return p.description && daysSinceUpdate <= CONFIG.maxDaysSinceUpdate;
    })
    .slice(0, 1)[0]; // 取第一个
}

// 生成推荐内容
function generateRecommendation(project, theme) {
  const stars = (project.stargazers_count / 1000).toFixed(1) + 'k';
  const updatedAt = new Date(project.updated_at).toLocaleDateString('zh-CN');
  
  return `🌟 **今日GitHub推荐** (${new Date().toLocaleDateString('zh-CN', { weekday: 'long' })})

📌 **主题**: ${theme.name}

---

## ${project.full_name}

${project.description || '暂无描述'}

### 📊 项目数据
- ⭐ Stars: **${stars}**
- 🍴 Forks: **${project.forks_count}**
- 📅 最近更新: ${updatedAt}
- 🔗 链接: ${project.html_url}

### 💡 推荐理由
${generateReason(project, theme)}

### 🎯 适用场景
${generateUseCases(project, theme)}

---
*每日8:00准时推送 · 由OpenClaw智能推荐*
`;
}

// 生成推荐理由
function generateReason(project, theme) {
  const reasons = [];
  
  if (project.stargazers_count >= 10000) {
    reasons.push('✅ 社区活跃度高（10k+ stars）');
  }
  
  const updatedAt = new Date(project.updated_at);
  const daysSinceUpdate = (Date.now() - updatedAt.getTime()) / (1000 * 60 * 60 * 24);
  if (daysSinceUpdate <= 7) {
    reasons.push('✅ 最近7天内有更新');
  } else if (daysSinceUpdate <= 30) {
    reasons.push('✅ 30天内持续维护');
  }
  
  if (project.language) {
    reasons.push(`✅ 主要语言: ${project.language}`);
  }
  
  if (project.topics && project.topics.length > 0) {
    reasons.push(`✅ 标签: ${project.topics.slice(0, 3).join(', ')}`);
  }
  
  return reasons.join('\n');
}

// 生成适用场景
function generateUseCases(project, theme) {
  const useCases = {
    'AI Agent框架': '• 构建智能对话系统\n• 开发AI助手应用\n• 自动化任务处理',
    '代码助手/IDE插件': '• 提升编码效率\n• 代码智能补全\n• 自动化代码审查',
    'Skill/工具库': '• 工作流自动化\n• 工具集成开发\n• 任务调度管理',
    '开源大模型': '• 本地部署AI模型\n• 定制化模型训练\n• 研究和学习',
    '开发效率工具': '• 提升开发效率\n• 命令行增强\n• 项目管理优化',
    '自动化工作流': '• CI/CD流程优化\n• 自动化测试\n• 部署自动化'
  };
  
  return useCases[theme.name] || '• 适合开发者使用\n• 提升工作效率\n• 学习优秀实践';
}

// 主函数
async function main() {
  const startTime = Date.now();
  const timeout = setTimeout(() => {
    console.error('任务执行超时');
    process.exit(1);
  }, CONFIG.timeout);
  
  try {
    // 加载状态
    const state = loadState();
    
    // 检查是否今天已经运行
    const today = new Date().toISOString().split('T')[0];
    if (state.lastRun === today) {
      console.log('今日已执行过推荐任务，跳过');
      process.exit(0);
    }
    
    // 获取当前主题
    const theme = getCurrentTheme();
    console.log(`当前主题: ${theme.name}`);
    
    // 搜索项目
    console.log('正在搜索GitHub项目...');
    const projects = await searchGitHubProjects(theme);
    console.log(`找到 ${projects.length} 个项目`);
    
    // 筛选项目
    const selectedProject = filterProjects(projects, state);
    
    if (!selectedProject) {
      console.log('未找到符合条件的项目');
      process.exit(0);
    }
    
    // 生成推荐内容
    const content = generateRecommendation(selectedProject, theme);
    
    // 更新状态
    state.lastRun = today;
    state.recommendedProjects.push(selectedProject.full_name);
    // 只保留最近30个推荐
    if (state.recommendedProjects.length > 30) {
      state.recommendedProjects = state.recommendedProjects.slice(-30);
    }
    saveState(state);
    
    // 输出结果（由OpenClaw发送）
    console.log('===RECOMMENDATION_START===');
    console.log(content);
    console.log('===RECOMMENDATION_END===');
    console.log(`Target: ${CONFIG.targetChannel}:${CONFIG.targetUser}`);
    
    clearTimeout(timeout);
    process.exit(0);
    
  } catch (error) {
    console.error('任务执行失败:', error);
    clearTimeout(timeout);
    process.exit(1);
  }
}

// 执行
main();
