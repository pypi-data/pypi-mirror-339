# MCP Excel Server

一个基于 Model Context Protocol (MCP) 的 Excel 处理服务器，提供以下功能：

1. 获取 Excel 工作簿信息
   - 读取所有工作表名称
   - 获取每个工作表的表头
   - 获取数据范围信息

2. 读取 Excel 数据
   - 支持按范围读取数据
   - 支持读取公式

3. 写入 Excel 数据
   - 支持按范围写入数据
   - 支持写入公式

## 安装

```bash
pip install baiyx-mcp-server-excel
```

## 使用方法

启动服务器：

```bash
baiyx-mcp-server-excel
```

## 功能说明

### 1. 获取工作簿信息

```python
get_workbook_info(file_path: str) -> WorkbookInfo
```

返回工作簿中所有工作表的信息，包括表名、表头和数据范围。

### 2. 读取数据

```python
read_sheet_data(file_path: str, sheet_name: str, range: Optional[str] = None) -> ExcelData
```

从指定工作表读取数据，可以指定读取范围（例如："A1:C10"）。

### 3. 读取公式

```python
read_sheet_formula(file_path: str, sheet_name: str, range: Optional[str] = None) -> ExcelFormula
```

从指定工作表读取公式，可以指定读取范围。

### 4. 写入数据

```python
write_sheet_data(file_path: str, sheet_name: str, range: str, data: List[List[Any]]) -> bool
```

向指定工作表写入数据，需要指定写入范围。

### 5. 写入公式

```python
write_sheet_formula(file_path: str, sheet_name: str, range: str, formulas: List[str]) -> bool
```

向指定工作表写入公式，需要指定写入范围。

## 示例

```python
# 获取工作簿信息
workbook_info = get_workbook_info("example.xlsx")
print(f"Found {len(workbook_info.sheets)} sheets")

# 读取数据
data = read_sheet_data("example.xlsx", "Sheet1", "A1:C10")
print(f"Read {len(data.data)} rows")

# 写入数据
success = write_sheet_data("example.xlsx", "Sheet1", "A1", [[1, 2, 3], [4, 5, 6]])
print(f"Write {'successful' if success else 'failed'}")
```

## 依赖

- Python >= 3.10
- mcp >= 1.6.0
- pandas >= 2.0.0
- openpyxl >= 3.1.2

## 许可证

MIT
