# Simple HTTP Server Script

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:8000/")
$listener.Start()

Write-Host "Server started at: http://localhost:8000"
Write-Host "Press Ctrl+C to stop the server"

try {
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response

        # Handle request path
        $path = $request.Url.LocalPath
        if ($path -eq "/") {
            $path = "/贪吃蛇游戏.html"
        }

        # Build file path
        $filePath = Join-Path (Get-Location) $path.Substring(1)

        # Check if file exists
        if (Test-Path $filePath -PathType Leaf) {
            # Read file content
            $content = Get-Content -Path $filePath -Raw

            # Set content type
            if ($filePath -like "*.html") {
                $response.ContentType = "text/html"
            } elseif ($filePath -like "*.css") {
                $response.ContentType = "text/css"
            } elseif ($filePath -like "*.js") {
                $response.ContentType = "application/javascript"
            }

            # Send response
            $buffer = [System.Text.Encoding]::UTF8.GetBytes($content)
            $response.ContentLength64 = $buffer.Length
            $response.OutputStream.Write($buffer, 0, $buffer.Length)
        } else {
            # File not found
            $response.StatusCode = 404
            $content = "404 Not Found"
            $buffer = [System.Text.Encoding]::UTF8.GetBytes($content)
            $response.ContentLength64 = $buffer.Length
            $response.OutputStream.Write($buffer, 0, $buffer.Length)
        }

        $response.Close()
    }
} finally {
    $listener.Stop()
    $listener.Dispose()
    Write-Host "Server stopped"
}