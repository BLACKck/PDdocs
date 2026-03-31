$token = "t-g1043qecETJ2DMQWAIZTSF6Q52SG52F6PKM56X6X"
$url = "https://open.feishu.cn/open-apis/mcp/v1/tools"
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}
$body = @{
    toolcalls = @(
        @{
            thought = "测试MCP连接"
            name = "get-user"
            params = @{}
        }
    )
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri $url -Method POST -Headers $headers -Body $body
    Write-Host "响应状态码: $($response.StatusCode)"
    Write-Host "响应内容: $($response.Content)"
} catch {
    Write-Host "请求失败: $($_.Exception.Message)"
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $errorResponse = $reader.ReadToEnd()
        $reader.Close()
        Write-Host "错误响应: $errorResponse"
    }
}
