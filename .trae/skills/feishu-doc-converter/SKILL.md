---
name: "feishu-doc-converter"
description: "Converts local requirement documents to Feishu cloud documents. Invoke after writing requirement documents to upload them to Feishu Knowledge Base under the appropriate project directory."
---

# Feishu Document Converter

This skill helps you convert local Markdown requirement documents to Feishu cloud documents and upload them to the Feishu Knowledge Base.

## When to Invoke
- After completing a requirement document
- When you need to upload local documents to Feishu Knowledge Base
- When you need to organize documents under specific project directories in Feishu

## Prerequisites
- Feishu CLI installed and configured
- Local Markdown requirement document ready
- Access to Feishu Knowledge Base

## Conversion Process

### Step 1: Prepare Local Document
1. Ensure the document is in Markdown format
2. Use UTF-8 encoding to avoid character encoding issues
3. Include Mermaid diagrams using standard Markdown code blocks
4. **Verify all flowcharts and state diagrams use Mermaid syntax**

### Step 2: Check Feishu Knowledge Base Structure
1. Verify if the project directory exists in Feishu Knowledge Base
2. If not, create the project directory under the root of "KAKA 知识"

### Step 3: Find Target Document Link (IMPORTANT!)
**DO NOT hardcode document IDs. Always query the API to find the correct document link.**

1. **Get Knowledge Base Space ID**:
   ```powershell
   $spaces = lark-cli api GET /open-apis/wiki/v2/spaces | ConvertFrom-Json
   $kakaSpaceId = $spaces.data.items | Where-Object { $_.name -eq "KAKA 知识" } | Select-Object -ExpandProperty space_id
   ```

2. **Get Project Node Token**:
   ```powershell
   $rootNodes = lark-cli api GET "/open-apis/wiki/v2/spaces/$kakaSpaceId/nodes" | ConvertFrom-Json
   $projectNode = $rootNodes.data.items | Where-Object { $_.title -like "*项目名称*" } | Select-Object -First 1
   $projectNodeToken = $projectNode.node_token
   ```

3. **Get Target Document**:
   ```powershell
   $childNodes = lark-cli api GET "/open-apis/wiki/v2/spaces/$kakaSpaceId/nodes?parent_node_token=$projectNodeToken" | ConvertFrom-Json
   $targetDoc = $childNodes.data.items | Where-Object { $_.title -eq "文档标题" } | Select-Object -First 1
   $docObjToken = $targetDoc.obj_token
   ```

4. **Build Document URL**:
   ```powershell
   $domain = "https://ecnhoqsc3a6t.feishu.cn"
   $docUrl = "$domain/wiki/$docObjToken"
   ```

### Step 4: Read and Upload Document
1. **Read Local Document (Correct Encoding)**:
   ```powershell
   # Use .NET File class for reliable UTF-8 encoding
   $content = [System.IO.File]::ReadAllText("path/to/document.md", [System.Text.UTF8Encoding]::new($false))
   ```

2. **Upload to Feishu Document**:
   ```powershell
   lark-cli docs +update --doc "$docUrl" --mode overwrite --markdown "$content"
   ```

3. **Verify Upload Result**:
   ```powershell
   # Check the response JSON
   {
     "ok": true,
     "board_tokens": [...],  // Whiteboard tokens for Mermaid diagrams
     "doc_id": "xxx",
     "message": "文档更新成功（overwrite 模式）",
     "success": true
   }
   ```

### Step 5: Verify Mermaid Diagrams
1. **Fetch Document Content**:
   ```powershell
   lark-cli docs +fetch --doc "$docUrl" --format json | Select-String "whiteboard"
   ```

2. **Check Whiteboard Tokens**:
   - Verify that Mermaid code blocks were converted to whiteboards
   - Each Mermaid diagram should have a corresponding whiteboard token

3. **Open Feishu Document**:
   - Open the document URL in browser
   - Refresh page (Ctrl+F5) to ensure whiteboards are loaded
   - Verify all flowcharts display correctly as whiteboards

## Common Issues and Solutions

### Issue 1: Mermaid Diagrams Converted to Whiteboards
**Symptoms**: Mermaid code appears as `<whiteboard token="xxx"></whiteboard>` in fetched content

**This is NORMAL behavior!** Feishu automatically converts Mermaid code blocks to whiteboards.

**Solutions**:
- This is expected and correct - whiteboards will display as visual flowcharts in the Feishu UI
- Verify whiteboards render correctly by opening the document in browser
- Use `flowchart TD` layout for better visualization in whiteboards

### Issue 2: Character Encoding Issues
**Symptoms**: Chinese characters appear as garbled text

**Solutions**:
- Use `[System.IO.File]::ReadAllText()` with explicit UTF-8 encoding
- Do NOT use `Get-Content -Encoding UTF8` (unreliable)
- Verify the document is saved in UTF-8 format

### Issue 3: Wrong Document Link
**Symptoms**: Document update fails or updates wrong document

**Solutions**:
- **ALWAYS query API to find document links** - do not hardcode IDs
- Use the Step 3 process to dynamically find document URLs
- Build URL using format: `https://ecnhoqsc3a6t.feishu.cn/wiki/{obj_token}`

### Issue 4: Document Update Failures
**Symptoms**: Command fails with error messages

**Solutions**:
- Check Feishu CLI configuration
- Ensure proper permissions for the Knowledge Base
- Verify network connectivity
- Use correct document URLs (from API query, not hardcoded)

### Issue 5: JSON Format Errors
**Symptoms**: `--data invalid format, expected JSON object` error

**Solutions**:
- Use `lark-cli docs +create` command instead of direct API calls
- Ensure JSON format is correct when using API calls
- Avoid special characters that might break JSON parsing

### Issue 6: Document Created in Wrong Location
**Symptoms**: Document appears in incorrect directory or not in the Knowledge Base

**Solutions**:
- Use `--wiki-space` parameter to specify the target Knowledge Base
- Use `--wiki-node` parameter to specify the correct parent directory
- Verify the node token is correct for the parent directory

### Issue 7: Permission Issues
**Symptoms**: `Permission denied` or `missing scope` errors

**Solutions**:
- Run `lark-cli auth login --recommend` to get common permissions
- Add specific permissions if needed: `lark-cli auth login --scope "wiki:wiki:readonly wiki:node:read"`
- Check user permissions in Feishu Knowledge Base

### Issue 8: Token Expiration
**Symptoms**: `token expired` error

**Solutions**:
- Run `lark-cli auth login --recommend` to refresh the token
- Check the authorization status: `lark-cli auth status`

## Best Practices

### 1. Document Link Management
- **ALWAYS query API to find document links** - never hardcode or assume IDs
- Maintain a mapping of local files to Feishu document titles
- Build URLs dynamically using the domain and obj_token

### 2. File Naming
- Use clear, descriptive filenames
- Include project name and document type

### 3. Document Structure
- Follow standard requirement document structure
- Use consistent heading levels
- Include version control information

### 4. Mermaid Diagrams
- **Use `flowchart TD` layout** (top-down) for all flowcharts
- Use standard code block format: ```mermaid
- Keep diagrams simple and focused
- Test Mermaid syntax locally before uploading
- **Understand that Feishu converts Mermaid to whiteboards** - this is correct

### 5. Encoding
- **Always use `[System.IO.File]::ReadAllText()` with UTF-8 encoding**
- Do NOT use `Get-Content` for reading documents with Chinese characters

### 6. Knowledge Base Organization
- Create clear project directories
- Use consistent naming conventions
- Maintain document hierarchy

### 7. Verification
- Always verify upload by checking response JSON
- Check for `board_tokens` array in response (indicates Mermaid conversion)
- Open document in browser to visually confirm whiteboards display

## Example Workflow

### Complete Automated Upload Script
```powershell
# Configuration
$domain = "https://ecnhoqsc3a6t.feishu.cn"
$spaceId = "7418508651239784449"  # KAKA 知识 space ID
$projectNodeToken = "xxx"  # Project node token

# 1. Find target document
$childNodes = lark-cli api GET "/open-apis/wiki/v2/spaces/$spaceId/nodes?parent_node_token=$projectNodeToken" | ConvertFrom-Json
$targetDoc = $childNodes.data.items | Where-Object { $_.title -eq "需求分析文档" } | Select-Object -First 1
$docUrl = "$domain/wiki/$($targetDoc.obj_token)"

# 2. Read document with correct encoding
$content = [System.IO.File]::ReadAllText("d:\project\需求分析文档.md", [System.Text.UTF8Encoding]::new($false))

# 3. Upload
$result = lark-cli docs +update --doc "$docUrl" --mode overwrite --markdown "$content" | ConvertFrom-Json

# 4. Verify
if ($result.success) {
    Write-Host "✓ Upload successful. Whiteboard tokens: $($result.board_tokens.Count)"
} else {
    Write-Host "✗ Upload failed: $($result.message)"
}
```

## Troubleshooting

### Feishu CLI Commands
- **Check Feishu CLI version**: `lark-cli --version`
- **Test connection**: `lark-cli api GET /open-apis/tenant/v2/tenant/info`
- **List documents**: `lark-cli docs +list --query "project name"`

### Common Error Messages
- **Authentication failed**: Check Feishu CLI configuration
- **Document not found**: Query API to find correct document link
- **Permission denied**: Check user permissions in Feishu
- **Mermaid syntax error**: Fix Mermaid code in document

## Quick Reference

### Find Document Link
```powershell
# Get space ID
$spaces = lark-cli api GET /open-apis/wiki/v2/spaces | ConvertFrom-Json
$kakaSpaceId = ($spaces.data.items | Where-Object { $_.name -eq "KAKA 知识" }).space_id

# Get project node
$nodes = lark-cli api GET "/open-apis/wiki/v2/spaces/$kakaSpaceId/nodes" | ConvertFrom-Json
$project = ($nodes.data.items | Where-Object { $_.title -like "*贪吃蛇*" }) | Select-Object -First 1

# Get documents
$docs = lark-cli api GET "/open-apis/wiki/v2/spaces/$kakaSpaceId/nodes?parent_node_token=$($project.node_token)" | ConvertFrom-Json
$doc = ($docs.data.items | Where-Object { $_.title -eq "需求分析文档" }) | Select-Object -First 1

# Build URL
$docUrl = "https://ecnhoqsc3a6t.feishu.cn/wiki/$($doc.obj_token)"
```

### Upload Document
```powershell
$content = [System.IO.File]::ReadAllText("file.md", [System.Text.UTF8Encoding]::new($false))
lark-cli docs +update --doc "$docUrl" --mode overwrite --markdown "$content"
```

## Conclusion

This skill provides a structured approach to convert local requirement documents to Feishu cloud documents. Key points:

1. **Always query API to find document links** - never hardcode IDs
2. **Use correct UTF-8 encoding** - use .NET File class
3. **Mermaid diagrams become whiteboards** - this is normal and correct
4. **Verify upload** - check response and visually confirm in browser
5. **Use flowchart TD layout** - for best visualization

By following the outlined process and addressing common issues, you can efficiently manage requirement documents in the Feishu Knowledge Base.
