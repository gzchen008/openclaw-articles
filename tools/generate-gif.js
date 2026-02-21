const GIFEncoder = require('gifencoder');
const { createCanvas } = require('canvas');
const fs = require('fs');

/**
 * 生成 ASCII 旋转动画 GIF
 */

const WIDTH = 600;
const HEIGHT = 400;
const FRAMES = 30;

// 创建画布
const canvas = createCanvas(WIDTH, HEIGHT);
const ctx = canvas.getContext('2d');

// 初始化 GIF 编码器
const encoder = new GIFEncoder(WIDTH, HEIGHT);
encoder.createReadStream().pipe(fs.createWriteStream('ascii-rotate.gif'));
encoder.start();
encoder.setRepeat(0); // 循环
encoder.setDelay(100); // 100ms = 10fps
encoder.setQuality(10);

// 生成螺旋图案
function generateSpiral(frame) {
    const chars = '@#%*+=-:.';
    const angle = frame * 0.2;
    const size = 8;
    const charSize = 12;
    
    // 清屏
    ctx.fillStyle = '#0d1117';
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    
    // 设置字体
    ctx.font = `${charSize}px monospace`;
    ctx.textBaseline = 'middle';
    ctx.textAlign = 'center';
    
    const centerX = WIDTH / 2;
    const centerY = HEIGHT / 2;
    
    // 绘制螺旋
    for (let y = -15; y <= 15; y++) {
        for (let x = -30; x <= 30; x++) {
            const r = Math.sqrt(x * x + y * y);
            const theta = Math.atan2(y, x) + angle;
            
            // 创建螺旋图案
            const spiral = Math.sin(theta * 3 + r * 0.3) * Math.cos(r * 0.1);
            
            if (r < 15 && spiral > 0.3) {
                const index = Math.floor((spiral + 1) * (chars.length - 1) / 2);
                const char = chars[Math.max(0, Math.min(chars.length - 1, index))];
                
                // 根据深度设置颜色
                const brightness = Math.floor((spiral + 1) * 127 + 128);
                const color = `rgb(${brightness * 0.2}, ${brightness * 0.6}, ${brightness})`;
                
                ctx.fillStyle = color;
                ctx.fillText(char, centerX + x * charSize, centerY + y * charSize);
            }
        }
    }
    
    // 添加标题
    ctx.font = 'bold 24px monospace';
    ctx.fillStyle = '#58a6ff';
    ctx.fillText('WELCOME TO CODEX', centerX, 40);
    
    ctx.font = '16px monospace';
    ctx.fillStyle = '#8b949e';
    ctx.fillText('AI Coding Agent', centerX, 65);
    
    // 添加提示文字
    ctx.font = '14px monospace';
    ctx.fillStyle = '#238636';
    ctx.fillText('Loading...', centerX, HEIGHT - 40);
}

console.log('🎬 正在生成 GIF 动画...');

// 生成每一帧
for (let i = 0; i < FRAMES; i++) {
    generateSpiral(i);
    encoder.addFrame(ctx);
    
    if (i % 10 === 0) {
        console.log(`  进度: ${i}/${FRAMES}`);
    }
}

encoder.finish();

console.log('✅ GIF 生成完成: ascii-rotate.gif');
console.log(`📁 文件位置: ${process.cwd()}/ascii-rotate.gif`);