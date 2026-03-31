class CatMatchGame {
    constructor() {
        this.boardSize = 8;
        // 使用不同颜色和品种的漫画风格猫咪SVG - 更可爱的设计
        this.cats = [
            { // 1. 橙色小橘猫 - 圆脸大眼
                color: '#FF6B35',
                bg: '#FFE5D9',
                svg: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <!-- 脸 -->
                    <ellipse cx="50" cy="58" rx="38" ry="32" fill="#FF6B35"/>
                    <!-- 耳朵 -->
                    <path d="M22 35 L18 12 L38 28 Z" fill="#FF6B35"/>
                    <path d="M78 35 L82 12 L62 28 Z" fill="#FF6B35"/>
                    <path d="M24 32 L22 18 L34 28 Z" fill="#FFB8A8"/>
                    <path d="M76 32 L78 18 L66 28 Z" fill="#FFB8A8"/>
                    <!-- 眼睛 -->
                    <ellipse cx="35" cy="52" rx="10" ry="12" fill="white"/>
                    <ellipse cx="65" cy="52" rx="10" ry="12" fill="white"/>
                    <circle cx="35" cy="54" r="6" fill="#2ECC71"/>
                    <circle cx="65" cy="54" r="6" fill="#2ECC71"/>
                    <circle cx="35" cy="54" r="3" fill="black"/>
                    <circle cx="65" cy="54" r="3" fill="black"/>
                    <circle cx="37" cy="51" r="2" fill="white"/>
                    <circle cx="67" cy="51" r="2" fill="white"/>
                    <!-- 鼻子 -->
                    <ellipse cx="50" cy="65" rx="5" ry="3" fill="#FF8FAB"/>
                    <!-- 嘴巴 -->
                    <path d="M45 70 Q50 75 55 70" stroke="#333" stroke-width="2.5" fill="none" stroke-linecap="round"/>
                    <!-- 胡须 -->
                    <path d="M20 58 L5 55 M20 63 L3 63 M20 68 L5 71" stroke="#333" stroke-width="1.5" opacity="0.6"/>
                    <path d="M80 58 L95 55 M80 63 L97 63 M80 68 L95 71" stroke="#333" stroke-width="1.5" opacity="0.6"/>
                    <!-- 腮红 -->
                    <ellipse cx="22" cy="62" rx="6" ry="4" fill="#FFB8A8" opacity="0.6"/>
                    <ellipse cx="78" cy="62" rx="6" ry="4" fill="#FFB8A8" opacity="0.6"/>
                </svg>`
            },
            { // 2. 蓝色猫咪 - 冷酷风格
                color: '#4ECDC4',
                bg: '#E0F7FA',
                svg: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <!-- 脸 -->
                    <ellipse cx="50" cy="58" rx="36" ry="30" fill="#4ECDC4"/>
                    <!-- 耳朵 - 尖耳朵 -->
                    <path d="M20 38 L15 8 L40 30 Z" fill="#4ECDC4"/>
                    <path d="M80 38 L85 8 L60 30 Z" fill="#4ECDC4"/>
                    <path d="M22 35 L20 15 L35 30 Z" fill="#81D4FA"/>
                    <path d="M78 35 L80 15 L65 30 Z" fill="#81D4FA"/>
                    <!-- 眼睛 - 细长眼 -->
                    <ellipse cx="35" cy="54" rx="11" ry="8" fill="#FFD700"/>
                    <ellipse cx="65" cy="54" rx="11" ry="8" fill="#FFD700"/>
                    <ellipse cx="35" cy="54" rx="4" ry="6" fill="black"/>
                    <ellipse cx="65" cy="54" rx="4" ry="6" fill="black"/>
                    <circle cx="33" cy="52" r="2" fill="white"/>
                    <circle cx="63" cy="52" r="2" fill="white"/>
                    <!-- 鼻子 -->
                    <polygon points="50,62 46,68 54,68" fill="#FF6B9D"/>
                    <!-- 嘴巴 -->
                    <path d="M46 72 L50 76 L54 72" stroke="#333" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
                    <!-- 胡须 -->
                    <path d="M18 55 L2 50 M18 62 L0 62 M18 69 L2 74" stroke="#006064" stroke-width="1.5"/>
                    <path d="M82 55 L98 50 M82 62 L100 62 M82 69 L98 74" stroke="#006064" stroke-width="1.5"/>
                    <!-- 花纹 -->
                    <path d="M35 35 L40 40 L45 35" stroke="#00838F" stroke-width="2" fill="none"/>
                    <path d="M65 35 L60 40 L55 35" stroke="#00838F" stroke-width="2" fill="none"/>
                </svg>`
            },
            { // 3. 紫色猫咪 - 神秘风格
                color: '#9B59B6',
                bg: '#F3E5F5',
                svg: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <!-- 脸 -->
                    <ellipse cx="50" cy="58" rx="37" ry="31" fill="#9B59B6"/>
                    <!-- 耳朵 -->
                    <path d="M22 36 L18 10 L38 30 Z" fill="#9B59B6"/>
                    <path d="M78 36 L82 10 L62 30 Z" fill="#9B59B6"/>
                    <path d="M24 33 L22 15 L34 28 Z" fill="#CE93D8"/>
                    <path d="M76 33 L78 15 L66 28 Z" fill="#CE93D8"/>
                    <!-- 眼睛 - 大眼睛 -->
                    <circle cx="35" cy="54" r="11" fill="#E1BEE7"/>
                    <circle cx="65" cy="54" r="11" fill="#E1BEE7"/>
                    <circle cx="35" cy="54" r="7" fill="#8E24AA"/>
                    <circle cx="65" cy="54" r="7" fill="#8E24AA"/>
                    <circle cx="35" cy="54" r="3" fill="black"/>
                    <circle cx="65" cy="54" r="3" fill="black"/>
                    <circle cx="38" cy="51" r="2.5" fill="white"/>
                    <circle cx="68" cy="51" r="2.5" fill="white"/>
                    <!-- 星星眼特效 -->
                    <path d="M28 48 L30 45 L32 48 L35 49 L32 51 L30 54 L28 51 L25 49 Z" fill="white" opacity="0.8"/>
                    <path d="M72 48 L70 45 L68 48 L65 49 L68 51 L70 54 L72 51 L75 49 Z" fill="white" opacity="0.8"/>
                    <!-- 鼻子 -->
                    <ellipse cx="50" cy="66" rx="4" ry="3" fill="#FF80AB"/>
                    <!-- 嘴巴 -->
                    <path d="M46 72 Q50 77 54 72" stroke="#4A148C" stroke-width="2.5" fill="none" stroke-linecap="round"/>
                    <!-- 胡须 -->
                    <path d="M18 58 L3 53 M18 64 L1 64 M18 70 L3 75" stroke="#4A148C" stroke-width="1.5" opacity="0.7"/>
                    <path d="M82 58 L97 53 M82 64 L99 64 M82 70 L97 75" stroke="#4A148C" stroke-width="1.5" opacity="0.7"/>
                </svg>`
            },
            { // 4. 粉色猫咪 - 可爱风格
                color: '#FF69B4',
                bg: '#FCE4EC',
                svg: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <!-- 脸 -->
                    <ellipse cx="50" cy="58" rx="38" ry="33" fill="#FF69B4"/>
                    <!-- 耳朵 - 圆耳朵 -->
                    <ellipse cx="28" cy="28" rx="14" ry="16" fill="#FF69B4"/>
                    <ellipse cx="72" cy="28" rx="14" ry="16" fill="#FF69B4"/>
                    <ellipse cx="28" cy="30" rx="9" ry="10" fill="#FFB6C1"/>
                    <ellipse cx="72" cy="30" rx="9" ry="10" fill="#FFB6C1"/>
                    <!-- 眼睛 - 爱心眼 -->
                    <ellipse cx="35" cy="55" rx="10" ry="12" fill="white"/>
                    <ellipse cx="65" cy="55" rx="10" ry="12" fill="white"/>
                    <!-- 爱心瞳孔 -->
                    <path d="M35 58 C30 53, 30 48, 35 48 C40 48, 40 53, 35 58" fill="#C2185B"/>
                    <path d="M35 58 C40 53, 40 48, 35 48 C30 48, 30 53, 35 58" fill="#C2185B"/>
                    <path d="M65 58 C60 53, 60 48, 65 48 C70 48, 70 53, 65 58" fill="#C2185B"/>
                    <path d="M65 58 C70 53, 70 48, 65 48 C60 48, 60 53, 65 58" fill="#C2185B"/>
                    <!-- 鼻子 -->
                    <ellipse cx="50" cy="67" rx="5" ry="3" fill="#FF1744"/>
                    <!-- 嘴巴 - W形 -->
                    <path d="M43 73 Q47 77 50 73 Q53 77 57 73" stroke="#880E4F" stroke-width="2.5" fill="none" stroke-linecap="round"/>
                    <!-- 腮红 - 大圆形 -->
                    <circle cx="20" cy="62" r="8" fill="#FF8FAB" opacity="0.5"/>
                    <circle cx="80" cy="62" r="8" fill="#FF8FAB" opacity="0.5"/>
                    <!-- 胡须 -->
                    <path d="M15 58 L0 52 M15 65 L-2 65 M15 72 L0 78" stroke="#AD1457" stroke-width="1.5" opacity="0.5"/>
                    <path d="M85 58 L100 52 M85 65 L102 65 M85 72 L100 78" stroke="#AD1457" stroke-width="1.5" opacity="0.5"/>
                </svg>`
            },
            { // 5. 绿色猫咪 - 自然风格
                color: '#2ECC71',
                bg: '#E8F5E9',
                svg: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <!-- 脸 -->
                    <ellipse cx="50" cy="58" rx="36" ry="31" fill="#2ECC71"/>
                    <!-- 耳朵 -->
                    <path d="M24 38 L20 15 L40 32 Z" fill="#2ECC71"/>
                    <path d="M76 38 L80 15 L60 32 Z" fill="#2ECC71"/>
                    <path d="M26 35 L24 22 L36 32 Z" fill="#A5D6A7"/>
                    <path d="M74 35 L76 22 L64 32 Z" fill="#A5D6A7"/>
                    <!-- 眼睛 - 眯眯眼 -->
                    <path d="M25 52 Q35 48 45 52" stroke="#1B5E20" stroke-width="3" fill="none" stroke-linecap="round"/>
                    <path d="M55 52 Q65 48 75 52" stroke="#1B5E20" stroke-width="3" fill="none" stroke-linecap="round"/>
                    <!-- 鼻子 -->
                    <ellipse cx="50" cy="62" rx="4" ry="3" fill="#FF8A80"/>
                    <!-- 嘴巴 -->
                    <path d="M46 68 Q50 74 54 68" stroke="#1B5E20" stroke-width="2.5" fill="none" stroke-linecap="round"/>
                    <!-- 叶子装饰 -->
                    <path d="M15 45 Q10 40 15 35 Q20 40 15 45" fill="#4CAF50"/>
                    <path d="M85 45 Q90 40 85 35 Q80 40 85 45" fill="#4CAF50"/>
                    <!-- 胡须 -->
                    <path d="M20 58 L5 54 M20 64 L2 64 M20 70 L5 74" stroke="#2E7D32" stroke-width="1.5"/>
                    <path d="M80 58 L95 54 M80 64 L98 64 M80 70 L95 74" stroke="#2E7D32" stroke-width="1.5"/>
                    <!-- 条纹 -->
                    <path d="M50 28 L50 35 M40 30 L43 36 M60 30 L57 36" stroke="#1B5E20" stroke-width="2" stroke-linecap="round"/>
                </svg>`
            },
            { // 6. 黄色猫咪 - 阳光风格
                color: '#F1C40F',
                bg: '#FFF9E6',
                svg: `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <!-- 脸 -->
                    <ellipse cx="50" cy="58" rx="38" ry="32" fill="#F1C40F"/>
                    <!-- 耳朵 -->
                    <path d="M22 36 L16 8 L40 30 Z" fill="#F1C40F"/>
                    <path d="M78 36 L84 8 L60 30 Z" fill="#F1C40F"/>
                    <path d="M24 33 L22 12 L36 28 Z" fill="#FFE082"/>
                    <path d="M76 33 L78 12 L64 28 Z" fill="#FFE082"/>
                    <!-- 眼睛 - 圆形大眼 -->
                    <circle cx="35" cy="54" r="12" fill="white"/>
                    <circle cx="65" cy="54" r="12" fill="white"/>
                    <circle cx="35" cy="54" r="8" fill="#FF6F00"/>
                    <circle cx="65" cy="54" r="8" fill="#FF6F00"/>
                    <circle cx="35" cy="54" r="4" fill="black"/>
                    <circle cx="65" cy="54" r="4" fill="black"/>
                    <circle cx="38" cy="51" r="3" fill="white"/>
                    <circle cx="68" cy="51" r="3" fill="white"/>
                    <!-- 鼻子 -->
                    <ellipse cx="50" cy="66" rx="5" ry="3" fill="#FF8A65"/>
                    <!-- 嘴巴 - 大笑 -->
                    <path d="M42 72 Q50 82 58 72" stroke="#E65100" stroke-width="3" fill="none" stroke-linecap="round"/>
                    <!-- 舌头 -->
                    <ellipse cx="50" cy="78" rx="4" ry="6" fill="#FF8A80"/>
                    <!-- 腮红 -->
                    <ellipse cx="22" cy="64" rx="7" ry="5" fill="#FFCC80" opacity="0.7"/>
                    <ellipse cx="78" cy="64" rx="7" ry="5" fill="#FFCC80" opacity="0.7"/>
                    <!-- 胡须 -->
                    <path d="M18 58 L2 52 M18 65 L0 65 M18 72 L2 78" stroke="#E65100" stroke-width="1.5" opacity="0.6"/>
                    <path d="M82 58 L98 52 M82 65 L100 65 M82 72 L98 78" stroke="#E65100" stroke-width="1.5" opacity="0.6"/>
                    <!-- 太阳光芒 -->
                    <line x1="50" y1="5" x2="50" y2="12" stroke="#FFB300" stroke-width="3" stroke-linecap="round"/>
                    <line x1="30" y1="10" x2="35" y2="16" stroke="#FFB300" stroke-width="3" stroke-linecap="round"/>
                    <line x1="70" y1="10" x2="65" y2="16" stroke="#FFB300" stroke-width="3" stroke-linecap="round"/>
                </svg>`
            }
        ];
        this.board = [];
        this.score = 0;
        this.level = 1;
        this.moves = 30;
        this.target = 1000;
        this.selectedCell = null;
        this.isProcessing = false;
        this.combo = 0;
        this.powerUps = {
            hammer: 3,
            bomb: 2,
            shuffle: 2,
            rainbow: 1
        };
        this.activePowerUp = null;
        this.particles = [];
        this.animationId = null;
    }

    init() {
        console.log('Initializing game...');
        this.boardElement = document.getElementById('gameBoard');
        this.canvas = document.getElementById('effectsCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.comboDisplay = document.getElementById('comboDisplay');
        
        if (!this.boardElement || !this.canvas || !this.comboDisplay) {
            console.error('Required elements not found!');
            return;
        }
        
        this.setupCanvas();
        this.createBoard();
        this.setupEventListeners();
        this.updateUI();
        
        // 初始检查并移除匹配
        setTimeout(() => this.removeInitialMatches(), 100);
        console.log('Game initialized successfully!');
    }

    setupCanvas() {
        const rect = this.boardElement.getBoundingClientRect();
        this.canvas.width = rect.width;
        this.canvas.height = rect.height;
        
        window.addEventListener('resize', () => {
            const rect = this.boardElement.getBoundingClientRect();
            this.canvas.width = rect.width;
            this.canvas.height = rect.height;
        });
    }

    createBoard() {
        this.board = [];
        this.boardElement.innerHTML = '';
        
        for (let row = 0; row < this.boardSize; row++) {
            this.board[row] = [];
            for (let col = 0; col < this.boardSize; col++) {
                let catType;
                let attempts = 0;
                do {
                    catType = Math.floor(Math.random() * this.cats.length);
                    attempts++;
                } while (this.wouldCreateMatch(row, col, catType) && attempts < 10);
                
                this.board[row][col] = catType;
                this.createCell(row, col, catType);
            }
        }
    }

    wouldCreateMatch(row, col, type) {
        // 检查水平
        let horizontalCount = 1;
        for (let c = col - 1; c >= 0 && this.board[row] && this.board[row][c] === type; c--) horizontalCount++;
        for (let c = col + 1; c < this.boardSize && this.board[row] && this.board[row][c] === type; c++) horizontalCount++;
        if (horizontalCount >= 3) return true;
        
        // 检查垂直
        let verticalCount = 1;
        for (let r = row - 1; r >= 0 && this.board[r] && this.board[r][col] === type; r--) verticalCount++;
        for (let r = row + 1; r < this.boardSize && this.board[r] && this.board[r][col] === type; r++) verticalCount++;
        if (verticalCount >= 3) return true;
        
        return false;
    }

    createCell(row, col, type) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.dataset.row = row;
        cell.dataset.col = col;
        cell.dataset.type = type;
        
        const cat = this.cats[type];
        if (cat) {
            cell.innerHTML = cat.svg;
            cell.style.background = `linear-gradient(135deg, ${cat.bg}, rgba(255,255,255,0.1))`;
        }
        
        cell.addEventListener('click', (e) => {
            e.preventDefault();
            this.handleCellClick(row, col);
        });
        
        this.boardElement.appendChild(cell);
    }

    handleCellClick(row, col) {
        if (this.isProcessing) return;
        
        // 如果使用道具
        if (this.activePowerUp) {
            this.usePowerUp(row, col);
            return;
        }
        
        const clickedCell = this.getCellElement(row, col);
        if (!clickedCell) return;
        
        if (!this.selectedCell) {
            this.selectedCell = { row, col };
            clickedCell.classList.add('selected');
        } else {
            const prevRow = this.selectedCell.row;
            const prevCol = this.selectedCell.col;
            const prevCell = this.getCellElement(prevRow, prevCol);
            
            if (prevCell) {
                prevCell.classList.remove('selected');
            }
            
            if (prevRow === row && prevCol === col) {
                this.selectedCell = null;
            } else if (this.isAdjacent(this.selectedCell, { row, col })) {
                this.swapCells(this.selectedCell, { row, col });
                this.selectedCell = null;
            } else {
                this.selectedCell = { row, col };
                clickedCell.classList.add('selected');
            }
        }
    }

    isAdjacent(cell1, cell2) {
        const rowDiff = Math.abs(cell1.row - cell2.row);
        const colDiff = Math.abs(cell1.col - cell2.col);
        return (rowDiff === 1 && colDiff === 0) || (rowDiff === 0 && colDiff === 1);
    }

    async swapCells(cell1, cell2) {
        this.isProcessing = true;
        
        // 交换数据
        const temp = this.board[cell1.row][cell1.col];
        this.board[cell1.row][cell1.col] = this.board[cell2.row][cell2.col];
        this.board[cell2.row][cell2.col] = temp;
        
        // 更新显示
        this.updateCell(cell1.row, cell1.col);
        this.updateCell(cell2.row, cell2.col);
        
        // 检查匹配
        const matches = this.findMatches();
        
        if (matches.length > 0) {
            this.moves--;
            this.updateUI();
            await this.processMatches(matches);
        } else {
            // 没有匹配，交换回来
            await this.sleep(300);
            const temp2 = this.board[cell1.row][cell1.col];
            this.board[cell1.row][cell1.col] = this.board[cell2.row][cell2.col];
            this.board[cell2.row][cell2.col] = temp2;
            this.updateCell(cell1.row, cell1.col);
            this.updateCell(cell2.row, cell2.col);
            
            // 震动效果
            const cell1El = this.getCellElement(cell1.row, cell1.col);
            const cell2El = this.getCellElement(cell2.row, cell2.col);
            if (cell1El) cell1El.classList.add('shake');
            if (cell2El) cell2El.classList.add('shake');
            setTimeout(() => {
                if (cell1El) cell1El.classList.remove('shake');
                if (cell2El) cell2El.classList.remove('shake');
            }, 500);
        }
        
        this.isProcessing = false;
        this.checkGameStatus();
    }

    findMatches() {
        const matches = [];
        const visited = new Set();
        
        // 检查水平匹配
        for (let row = 0; row < this.boardSize; row++) {
            for (let col = 0; col < this.boardSize - 2; col++) {
                const type = this.board[row][col];
                if (type === -1 || type === undefined) continue;
                
                let matchLength = 1;
                while (col + matchLength < this.boardSize && this.board[row][col + matchLength] === type) {
                    matchLength++;
                }
                
                if (matchLength >= 3) {
                    for (let i = 0; i < matchLength; i++) {
                        const key = `${row},${col + i}`;
                        if (!visited.has(key)) {
                            visited.add(key);
                            matches.push({ row, col: col + i, type });
                        }
                    }
                }
            }
        }
        
        // 检查垂直匹配
        for (let col = 0; col < this.boardSize; col++) {
            for (let row = 0; row < this.boardSize - 2; row++) {
                const type = this.board[row][col];
                if (type === -1 || type === undefined) continue;
                
                let matchLength = 1;
                while (row + matchLength < this.boardSize && this.board[row + matchLength][col] === type) {
                    matchLength++;
                }
                
                if (matchLength >= 3) {
                    for (let i = 0; i < matchLength; i++) {
                        const key = `${row + i},${col}`;
                        if (!visited.has(key)) {
                            visited.add(key);
                            matches.push({ row: row + i, col, type });
                        }
                    }
                }
            }
        }
        
        return matches;
    }

    async processMatches(matches) {
        this.combo++;
        
        // 计算分数
        const basePoints = matches.length * 10;
        const comboBonus = this.combo > 1 ? (this.combo - 1) * 20 : 0;
        const totalPoints = basePoints + comboBonus;
        this.score += totalPoints;
        
        // 显示连击
        if (this.combo > 1) {
            this.showCombo(this.combo);
        }
        
        // 特效 - 只添加动画类，不改变内容
        matches.forEach(match => {
            const cell = this.getCellElement(match.row, match.col);
            if (cell) {
                const rect = cell.getBoundingClientRect();
                const boardRect = this.boardElement.getBoundingClientRect();
                const x = rect.left - boardRect.left + rect.width / 2;
                const y = rect.top - boardRect.top + rect.height / 2;
                
                this.createExplosion(x, y, this.getCatColor(match.type));
                cell.classList.add('matched');
            }
        });
        
        this.updateUI();
        
        await this.sleep(400);
        
        // 移除匹配的猫咪 - 先清空内容再更新数据
        matches.forEach(match => {
            const cell = this.getCellElement(match.row, match.col);
            if (cell) {
                cell.innerHTML = '';
                cell.style.background = '';
                cell.classList.remove('matched');
            }
            this.board[match.row][match.col] = -1;
        });
        
        // 下落
        await this.dropCells();
        
        // 填充新猫咪
        await this.fillBoard();
        
        // 检查新的匹配
        const newMatches = this.findMatches();
        if (newMatches.length > 0) {
            await this.sleep(300);
            await this.processMatches(newMatches);
        } else {
            this.combo = 0;
        }
    }

    async dropCells() {
        for (let col = 0; col < this.boardSize; col++) {
            let writePos = this.boardSize - 1;
            
            for (let row = this.boardSize - 1; row >= 0; row--) {
                if (this.board[row][col] !== -1) {
                    if (writePos !== row) {
                        this.board[writePos][col] = this.board[row][col];
                        this.board[row][col] = -1;
                    }
                    writePos--;
                }
            }
        }
        
        this.updateBoard();
        await this.sleep(300);
    }

    async fillBoard() {
        for (let col = 0; col < this.boardSize; col++) {
            for (let row = 0; row < this.boardSize; row++) {
                if (this.board[row][col] === -1) {
                    this.board[row][col] = Math.floor(Math.random() * this.cats.length);
                }
            }
        }
        
        this.updateBoard();
        
        // 添加下落动画
        const cells = this.boardElement.querySelectorAll('.cell');
        cells.forEach(cell => {
            cell.classList.add('falling');
            setTimeout(() => cell.classList.remove('falling'), 500);
        });
        
        await this.sleep(500);
    }

    updateCell(row, col) {
        const cell = this.getCellElement(row, col);
        if (!cell) return;
        const type = this.board[row][col];
        cell.dataset.type = type;
        
        if (type >= 0 && this.cats[type]) {
            const cat = this.cats[type];
            cell.innerHTML = cat.svg;
            cell.style.background = `linear-gradient(135deg, ${cat.bg}, rgba(255,255,255,0.1))`;
        } else {
            cell.innerHTML = '';
            cell.style.background = '';
        }
    }

    updateBoard() {
        for (let row = 0; row < this.boardSize; row++) {
            for (let col = 0; col < this.boardSize; col++) {
                this.updateCell(row, col);
            }
        }
    }

    getCellElement(row, col) {
        return this.boardElement.querySelector(`[data-row="${row}"][data-col="${col}"]`);
    }

    getCatColor(type) {
        if (this.cats[type] && this.cats[type].color) {
            return this.cats[type].color;
        }
        return '#ffffff';
    }

    // 粒子特效系统
    createExplosion(x, y, color) {
        const particleCount = 20;
        
        for (let i = 0; i < particleCount; i++) {
            const angle = (Math.PI * 2 * i) / particleCount;
            const velocity = 2 + Math.random() * 3;
            
            this.particles.push({
                x,
                y,
                vx: Math.cos(angle) * velocity,
                vy: Math.sin(angle) * velocity,
                life: 1,
                color,
                size: 3 + Math.random() * 4
            });
        }
    }

    updateParticles() {
        if (!this.ctx) return;
        
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const p = this.particles[i];
            
            p.x += p.vx;
            p.y += p.vy;
            p.vy += 0.1; // 重力
            p.life -= 0.02;
            
            if (p.life <= 0) {
                this.particles.splice(i, 1);
                continue;
            }
            
            this.ctx.save();
            this.ctx.globalAlpha = p.life;
            this.ctx.fillStyle = p.color;
            this.ctx.shadowBlur = 15;
            this.ctx.shadowColor = p.color;
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.size * p.life, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.restore();
        }
        
        this.animationId = requestAnimationFrame(() => this.updateParticles());
    }

    showCombo(combo) {
        const comboText = document.createElement('div');
        comboText.className = 'combo-text';
        comboText.textContent = `${combo} COMBO!`;
        this.comboDisplay.appendChild(comboText);
        
        setTimeout(() => {
            if (comboText.parentNode) {
                comboText.remove();
            }
        }, 1000);
    }

    // 道具系统
    setupEventListeners() {
        const startBtn = document.getElementById('startBtn');
        const restartBtn = document.getElementById('restartBtn');
        
        if (startBtn) {
            startBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                console.log('Start button clicked!');
                const modal = document.getElementById('startModal');
                if (modal) {
                    modal.classList.add('hidden');
                }
                this.startParticleSystem();
            });
        }
        
        if (restartBtn) {
            restartBtn.addEventListener('click', (e) => {
                e.preventDefault();
                location.reload();
            });
        }
        
        // 道具按钮
        const hammer = document.getElementById('hammer');
        const bomb = document.getElementById('bomb');
        const shuffle = document.getElementById('shuffle');
        const rainbow = document.getElementById('rainbow');
        
        if (hammer) hammer.addEventListener('click', () => this.selectPowerUp('hammer'));
        if (bomb) bomb.addEventListener('click', () => this.selectPowerUp('bomb'));
        if (shuffle) shuffle.addEventListener('click', () => this.useShuffle());
        if (rainbow) rainbow.addEventListener('click', () => this.selectPowerUp('rainbow'));
    }

    selectPowerUp(type) {
        if (this.powerUps[type] > 0) {
            this.activePowerUp = type;
            this.boardElement.style.cursor = 'crosshair';
            
            // 高亮道具按钮
            document.querySelectorAll('.power-up').forEach(btn => btn.classList.remove('selected'));
            const btn = document.getElementById(type);
            if (btn) btn.classList.add('selected');
        }
    }

    async usePowerUp(row, col) {
        if (this.powerUps[this.activePowerUp] <= 0) return;
        
        this.powerUps[this.activePowerUp]--;
        this.updatePowerUpUI();
        
        const cell = this.getCellElement(row, col);
        if (!cell) return;
        
        const rect = cell.getBoundingClientRect();
        const boardRect = this.boardElement.getBoundingClientRect();
        const x = rect.left - boardRect.left + rect.width / 2;
        const y = rect.top - boardRect.top + rect.height / 2;
        
        switch (this.activePowerUp) {
            case 'hammer':
                this.createExplosion(x, y, '#ffffff');
                this.board[row][col] = -1;
                this.score += 50;
                break;
                
            case 'bomb':
                for (let r = row - 1; r <= row + 1; r++) {
                    for (let c = col - 1; c <= col + 1; c++) {
                        if (r >= 0 && r < this.boardSize && c >= 0 && c < this.boardSize) {
                            const bombCell = this.getCellElement(r, c);
                            if (bombCell) {
                                const bombRect = bombCell.getBoundingClientRect();
                                const bx = bombRect.left - boardRect.left + bombRect.width / 2;
                                const by = bombRect.top - boardRect.top + bombRect.height / 2;
                                this.createExplosion(bx, by, '#ff6600');
                            }
                            this.board[r][c] = -1;
                        }
                    }
                }
                this.score += 150;
                break;
                
            case 'rainbow':
                const targetType = this.board[row][col];
                for (let r = 0; r < this.boardSize; r++) {
                    for (let c = 0; c < this.boardSize; c++) {
                        if (this.board[r][c] === targetType) {
                            const rainbowCell = this.getCellElement(r, c);
                            if (rainbowCell) {
                                const rainbowRect = rainbowCell.getBoundingClientRect();
                                const rx = rainbowRect.left - boardRect.left + rainbowRect.width / 2;
                                const ry = rainbowRect.top - boardRect.top + rainbowRect.height / 2;
                                this.createExplosion(rx, ry, this.getCatColor(targetType));
                            }
                            this.board[r][c] = -1;
                        }
                    }
                }
                this.score += 200;
                break;
        }
        
        this.updateBoard();
        await this.dropCells();
        await this.fillBoard();
        
        this.activePowerUp = null;
        this.boardElement.style.cursor = 'pointer';
        document.querySelectorAll('.power-up').forEach(btn => btn.classList.remove('selected'));
        
        this.updateUI();
    }

    async useShuffle() {
        if (this.powerUps.shuffle <= 0) return;
        
        this.powerUps.shuffle--;
        this.updatePowerUpUI();
        
        // 随机打乱
        for (let i = 0; i < 100; i++) {
            const row1 = Math.floor(Math.random() * this.boardSize);
            const col1 = Math.floor(Math.random() * this.boardSize);
            const row2 = Math.floor(Math.random() * this.boardSize);
            const col2 = Math.floor(Math.random() * this.boardSize);
            
            const temp = this.board[row1][col1];
            this.board[row1][col1] = this.board[row2][col2];
            this.board[row2][col2] = temp;
        }
        
        this.updateBoard();
        
        // 检查并处理匹配
        const matches = this.findMatches();
        if (matches.length > 0) {
            await this.processMatches(matches);
        }
    }

    updatePowerUpUI() {
        const hammerCount = document.querySelector('#hammer .power-up-count');
        const bombCount = document.querySelector('#bomb .power-up-count');
        const shuffleCount = document.querySelector('#shuffle .power-up-count');
        const rainbowCount = document.querySelector('#rainbow .power-up-count');
        
        if (hammerCount) hammerCount.textContent = this.powerUps.hammer;
        if (bombCount) bombCount.textContent = this.powerUps.bomb;
        if (shuffleCount) shuffleCount.textContent = this.powerUps.shuffle;
        if (rainbowCount) rainbowCount.textContent = this.powerUps.rainbow;
        
        Object.keys(this.powerUps).forEach(type => {
            const btn = document.getElementById(type);
            if (btn) btn.disabled = this.powerUps[type] <= 0;
        });
    }

    // 初始移除匹配
    async removeInitialMatches() {
        let matches = this.findMatches();
        let attempts = 0;
        while (matches.length > 0 && attempts < 100) {
            matches.forEach(match => {
                this.board[match.row][match.col] = Math.floor(Math.random() * this.cats.length);
            });
            this.updateBoard();
            matches = this.findMatches();
            attempts++;
        }
    }

    updateUI() {
        const scoreEl = document.getElementById('score');
        const levelEl = document.getElementById('level');
        const movesEl = document.getElementById('moves');
        const targetEl = document.getElementById('target');
        
        if (scoreEl) scoreEl.textContent = this.score;
        if (levelEl) levelEl.textContent = this.level;
        if (movesEl) movesEl.textContent = this.moves;
        if (targetEl) targetEl.textContent = this.target;
        
        this.updatePowerUpUI();
    }

    checkGameStatus() {
        if (this.score >= this.target) {
            this.levelComplete();
        } else if (this.moves <= 0) {
            this.gameOver();
        }
    }

    levelComplete() {
        const modal = document.getElementById('gameOverModal');
        const title = document.getElementById('gameOverTitle');
        const message = document.getElementById('gameOverMessage');
        const finalScore = document.getElementById('finalScore');
        
        if (title) title.textContent = '关卡完成！';
        if (message) message.textContent = `恭喜你完成第 ${this.level} 关！`;
        if (finalScore) finalScore.textContent = this.score;
        if (modal) modal.classList.remove('hidden');
    }

    gameOver() {
        const modal = document.getElementById('gameOverModal');
        const title = document.getElementById('gameOverTitle');
        const message = document.getElementById('gameOverMessage');
        const finalScore = document.getElementById('finalScore');
        
        if (title) title.textContent = '游戏结束';
        if (message) message.textContent = '步数用完了，再试一次吧！';
        if (finalScore) finalScore.textContent = this.score;
        if (modal) modal.classList.remove('hidden');
    }

    startParticleSystem() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        this.updateParticles();
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// 启动游戏
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, starting game...');
    const game = new CatMatchGame();
    game.init();
});
