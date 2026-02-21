#!/usr/bin/env node

/**
 * ASCII 旋转动画生成器
 * 类似 OpenAI Codex CLI 的启动动画效果
 */

const readline = require('readline');

// 清屏
const clearScreen = () => {
    process.stdout.write('\x1Bc');
};

// 移动光标到指定位置
const moveCursor = (x, y) => {
    process.stdout.write(`\x1B[${y};${x}H`);
};

// 隐藏光标
const hideCursor = () => {
    process.stdout.write('\x1B[?25l');
};

// 显示光标
const showCursor = () => {
    process.stdout.write('\x1B[?25h');
};

// 生成旋转的圆环 ASCII 艺术
const generateRotatingCircle = (frame, size = 15) => {
    const chars = '.,-~:;=!*#$@';
    const frames = [];
    
    // 使用不同字符创建立体效果
    const getChar = (angle1, angle2) => {
        const luminance = Math.sin(angle1) * Math.cos(angle2);
        const index = Math.floor((luminance + 1) * (chars.length - 1) / 2);
        return chars[Math.max(0, Math.min(chars.length - 1, index))];
    };
    
    // 生成甜甜圈形状
    const donut = [];
    const A = frame * 0.1; // 旋转角度 A
    const B = frame * 0.05; // 旋转角度 B
    
    for (let y = -size; y <= size; y++) {
        let line = '';
        for (let x = -size * 2; x <= size * 2; x++) {
            // 3D 甜甜圈数学公式
            const x1 = x / size;
            const y1 = y / size;
            const z = Math.sqrt(Math.max(0, 1 - x1 * x1 - y1 * y1));
            
            if (z > 0) {
                // 计算光照
                const light = Math.sin(A) * x1 + Math.cos(A) * z;
                const lum = Math.floor((light + 1) * 5);
                const charIndex = Math.max(0, Math.min(chars.length - 1, lum));
                line += chars[charIndex];
            } else {
                line += ' ';
            }
        }
        donut.push(line);
    }
    
    return donut;
};

// 生成螺旋旋转效果
const generateSpiral = (frame, size = 12) => {
    const result = [];
    const chars = '@#%*+=-:.';
    const angle = frame * 0.2;
    
    for (let y = -size; y <= size; y++) {
        let line = '';
        for (let x = -size * 2; x <= size * 2; x++) {
            const r = Math.sqrt(x * x + y * y);
            const theta = Math.atan2(y, x) + angle;
            
            // 创建螺旋图案
            const spiral = Math.sin(theta * 3 + r * 0.3) * Math.cos(r * 0.1);
            
            if (r < size * 2 && spiral > 0.3) {
                const index = Math.floor((spiral + 1) * (chars.length - 1) / 2);
                line += chars[index];
            } else {
                line += ' ';
            }
        }
        result.push(line);
    }
    
    return result;
};

// 生成带文字标题的旋转动画
const generateLogoWithText = (frame) => {
    const art = generateSpiral(frame, 10);
    const title = 'WELCOME TO CODEX';
    const subtitle = 'AI Coding Agent';
    
    // 在底部添加文字
    const emptyLines = 2;
    for (let i = 0; i < emptyLines; i++) {
        art.push('');
    }
    
    // 居中文本
    const width = art[0]?.length || 40;
    const titlePadding = Math.max(0, Math.floor((width - title.length) / 2));
    const subtitlePadding = Math.max(0, Math.floor((width - subtitle.length) / 2));
    
    art.push(' '.repeat(titlePadding) + '\x1B[1;36m' + title + '\x1B[0m');
    art.push(' '.repeat(subtitlePadding) + '\x1B[90m' + subtitle + '\x1B[0m');
    
    return art;
};

// 主动画函数
class ASCIIAnimator {
    constructor(options = {}) {
        this.frame = 0;
        this.isRunning = false;
        this.speed = options.speed || 100; // 毫秒
        this.duration = options.duration || 5000; // 总时长
        this.type = options.type || 'spiral'; // spiral, circle, wave
    }
    
    start() {
        this.isRunning = true;
        hideCursor();
        clearScreen();
        
        const startTime = Date.now();
        
        const animate = () => {
            if (!this.isRunning) return;
            
            // 检查是否超时
            if (Date.now() - startTime > this.duration) {
                this.stop();
                return;
            }
            
            // 清屏并移动光标到顶部
            moveCursor(1, 1);
            
            // 生成当前帧
            let art;
            switch (this.type) {
                case 'circle':
                    art = generateRotatingCircle(this.frame);
                    break;
                case 'wave':
                    art = generateWave(this.frame);
                    break;
                case 'logo':
                    art = generateLogoWithText(this.frame);
                    break;
                default:
                    art = generateSpiral(this.frame);
            }
            
            // 打印
            console.log(art.join('\n'));
            
            this.frame++;
            setTimeout(animate, this.speed);
        };
        
        animate();
    }
    
    stop() {
        this.isRunning = false;
        showCursor();
        console.log('\n\n✨ Animation complete!\n');
    }
}

// 波浪效果
const generateWave = (frame) => {
    const result = [];
    const chars = '@#%*+=-:.';
    const width = 60;
    const height = 20;
    
    for (let y = 0; y < height; y++) {
        let line = '';
        for (let x = 0; x < width; x++) {
            const wave1 = Math.sin((x + frame) * 0.2) * 5;
            const wave2 = Math.cos((y + frame * 0.5) * 0.3) * 3;
            const value = wave1 + wave2;
            
            if (Math.abs(value - (y - height / 2)) < 1) {
                const index = Math.floor(Math.abs(value) * 2) % chars.length;
                line += chars[index];
            } else {
                line += ' ';
            }
        }
        result.push(line);
    }
    
    return result;
};

// 简单的旋转 spinner
class Spinner {
    constructor(message = 'Loading') {
        this.frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
        this.message = message;
        this.frame = 0;
        this.interval = null;
    }
    
    start() {
        hideCursor();
        this.interval = setInterval(() => {
            process.stdout.write(`\r\x1B[36m${this.frames[this.frame]}\x1B[0m ${this.message}...`);
            this.frame = (this.frame + 1) % this.frames.length;
        }, 80);
    }
    
    stop(success = true) {
        if (this.interval) {
            clearInterval(this.interval);
            const icon = success ? '✓' : '✗';
            const color = success ? '32' : '31';
            console.log(`\r\x1B[${color}m${icon}\x1B[0m ${this.message} ${success ? 'done' : 'failed'}    `);
            showCursor();
        }
    }
}

// 命令行参数处理
const args = process.argv.slice(2);
const type = args[0] || 'spiral';
const duration = parseInt(args[1]) || 5000;

// 显示帮助
if (args.includes('--help') || args.includes('-h')) {
    console.log(`
ASCII 旋转动画生成器

用法: node ascii-rotate.js [类型] [时长]

类型:
  spiral  - 螺旋旋转效果 (默认)
  circle  - 3D 圆环效果
  wave    - 波浪动画
  logo    - 带标题的 Logo 动画
  spinner - 简单的加载 spinner

时长:
  动画持续时间，单位毫秒 (默认 5000)

示例:
  node ascii-rotate.js spiral 10000
  node ascii-rotate.js logo
  node ascii-rotate.js spinner
`);
    process.exit(0);
}

// 运行
console.log('\x1B[?25l'); // 隐藏光标

if (type === 'spinner') {
    // 简单的 spinner 模式
    const spinner = new Spinner('Processing');
    spinner.start();
    
    // 5秒后停止
    setTimeout(() => {
        spinner.stop(true);
        process.exit(0);
    }, 5000);
} else {
    // 动画模式
    const animator = new ASCIIAnimator({
        type: type,
        duration: duration,
        speed: 100
    });
    
    // 按任意键停止
    process.stdin.setRawMode(true);
    process.stdin.resume();
    process.stdin.on('data', () => {
        animator.stop();
        process.exit(0);
    });
    
    animator.start();
}