#!/usr/bin/env pwsh

# 进入仓库目录
Set-Location -Path "d:\PDM\PDdocs"

# 执行git操作
git add .
git commit -m "Split requirements into module-specific folders"
git push
