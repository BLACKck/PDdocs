#!/usr/bin/env pwsh

# 自动上传文档至GitHub的脚本
# 监控PDdocs目录下的文件变化，当文件变化时自动提交并推送至GitHub

# 设置变量
$repoPath = "d:\PDM\PDdocs"
$gitExe = "git"
$commitMessage = "Auto commit: Update documentation"

# 进入仓库目录
Set-Location -Path $repoPath

# 检查是否为git仓库
if (-not (Test-Path -Path ".git" -PathType Container)) {
    Write-Host "Error: Not a git repository. Please initialize git repository first." -ForegroundColor Red
    exit 1
}

# 检查git是否可用
if (-not (Get-Command $gitExe -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Git is not installed or not in PATH." -ForegroundColor Red
    exit 1
}

Write-Host "Starting auto-upload script..." -ForegroundColor Green
Write-Host "Monitoring directory: $repoPath" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop." -ForegroundColor Yellow

# 初始化上次检查的文件状态
$lastCheck = Get-ChildItem -Path $repoPath -Recurse -File | Select-Object FullName, LastWriteTime

# 主循环
while ($true) {
    # 获取当前文件状态
    $currentCheck = Get-ChildItem -Path $repoPath -Recurse -File | Select-Object FullName, LastWriteTime
    
    # 比较文件状态，检查是否有变化
    $changes = Compare-Object -ReferenceObject $lastCheck -DifferenceObject $currentCheck -Property FullName, LastWriteTime
    
    if ($changes) {
        Write-Host "Detected changes. Committing and pushing..." -ForegroundColor Cyan
        
        try {
            # 执行git操作
            & $gitExe add .
            & $gitExe commit -m $commitMessage
            & $gitExe push
            
            Write-Host "Successfully pushed changes to GitHub." -ForegroundColor Green
            
            # 更新上次检查的文件状态
            $lastCheck = $currentCheck
        } catch {
            Write-Host "Error during git operations: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    
    # 等待一段时间后再次检查
    Start-Sleep -Seconds 60
}