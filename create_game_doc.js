const https = require('https');
const http = require('http');

// 贪吃蛇游戏需求文档内容
const gameRequirementContent = `# 贪吃蛇游戏需求文档

## 1. 项目背景
贪吃蛇是一款经典的休闲游戏，玩家通过控制蛇的移动方向来收集食物，使蛇的身体不断变长，同时避免撞到墙壁或自身。本项目旨在开发一个基于Web的贪吃蛇游戏，提供良好的用户体验和游戏玩法。

## 2. 目标用户
- 休闲游戏爱好者
- 各年龄段的玩家
- 喜欢简单易上手游戏的用户

## 3. 功能需求

### 3.1 核心功能
- **游戏控制**：通过方向键或触摸屏幕控制蛇的移动方向
- **食物系统**：随机生成食物，蛇吃到食物后身体变长
- **碰撞检测**：检测蛇是否撞到墙壁或自身
- **得分系统**：根据吃到的食物数量计算得分
- **游戏结束**：当蛇撞到墙壁或自身时游戏结束

### 3.2 界面功能
- **游戏主界面**：显示游戏区域、得分、游戏状态
- **开始菜单**：提供开始游戏、设置、关于等选项
- **游戏结束界面**：显示最终得分、重新开始按钮
- **设置界面**：调整游戏速度、难度等参数

### 3.3 游戏模式
- **经典模式**：传统贪吃蛇玩法
- **计时模式**：在限定时间内获取最高分
- **无尽模式**：没有时间限制，挑战最长长度

## 4. 非功能需求

### 4.1 性能需求
- 游戏运行流畅，无卡顿
- 响应速度快，操作延迟低

### 4.2 兼容性需求
- 支持主流浏览器（Chrome、Firefox、Safari、Edge）
- 支持移动端和桌面端

### 4.3 用户体验
- 界面简洁美观
- 操作简单直观
- 游戏反馈及时

## 5. 技术实现

### 5.1 前端技术
- HTML5 Canvas：用于绘制游戏界面
- JavaScript：游戏逻辑实现
- CSS3：样式设计
- 响应式设计：适配不同设备

### 5.2 游戏逻辑
- 蛇的移动：使用数组存储蛇的身体 segments
- 碰撞检测：检测蛇头与墙壁、自身的碰撞
- 食物生成：随机生成食物位置，避免与蛇身重叠
- 得分计算：每吃到一个食物增加一定分数

## 6. 项目范围
- 开发Web版贪吃蛇游戏
- 实现核心游戏功能
- 提供基本的游戏设置
- 适配移动端和桌面端

## 7. 风险分析
- **技术风险**：Canvas性能优化，确保游戏流畅运行
- **兼容性风险**：不同浏览器的兼容性问题
- **用户体验风险**：操作响应速度和游戏平衡性

## 8. 验收标准
- 游戏能够正常运行，无bug
- 操作流畅，响应及时
- 界面美观，用户体验良好
- 适配不同设备和浏览器

## 9. 交付物
- 完整的游戏代码
- 游戏说明文档
- 测试报告

## 10. 项目时间计划
- 需求分析：1天
- 前端开发：3天
- 游戏逻辑实现：2天
- 测试和优化：2天
- 总计：8天
`;

// 创建MCP请求
const createDocRequest = {
  jsonrpc: "2.0",
  id: "1",
  method: "tool.call",
  params: {
    name: "create-doc",
    params: {
      title: "贪吃蛇游戏需求文档",
      content: gameRequirementContent
    }
  }
};

// 发送HTTP请求到Feishu-MCP服务
function sendMcpRequest() {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify(createDocRequest);
    
    console.log('发送请求到Feishu-MCP服务...');
    console.log('请求数据:', JSON.stringify(createDocRequest, null, 2));
    
    const options = {
      hostname: 'localhost',
      port: 3333,
      path: '/mcp',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = http.request(options, (res) => {
      console.log('响应状态码:', res.statusCode);
      console.log('响应头:', res.headers);
      
      let data = '';
      res.on('data', (chunk) => {
        data += chunk;
      });
      res.on('end', () => {
        console.log('响应数据:', data);
        try {
          const result = JSON.parse(data);
          resolve(result);
        } catch (error) {
          reject(new Error('解析响应失败: ' + error.message + '，响应数据: ' + data));
        }
      });
    });

    req.on('error', (error) => {
      console.error('请求错误:', error);
      reject(error);
    });

    req.write(postData);
    req.end();
  });
}

// 执行请求
sendMcpRequest()
  .then(result => {
    console.log('创建文档请求结果:', JSON.stringify(result, null, 2));
    if (result.result && result.result.document) {
      console.log('✅ 文档创建成功！');
      console.log('文档标题:', result.result.document.title);
      console.log('文档链接:', result.result.document.url);
    } else if (result.error) {
      console.error('❌ 创建文档失败:', result.error.message);
    }
  })
  .catch(error => {
    console.error('❌ 请求失败:', error.message);
  });
