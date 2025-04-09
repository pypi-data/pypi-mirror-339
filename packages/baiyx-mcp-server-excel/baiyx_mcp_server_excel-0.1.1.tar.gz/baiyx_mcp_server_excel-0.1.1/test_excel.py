from mcp_server_excel.server import ExcelServer

def test_excel_operations():
    # 创建服务器实例
    server = ExcelServer()
    tools = server._tools
    
    # 1. 先创建一个测试用的 Excel 文件
    print("\n1. 写入测试数据...")
    data = [
        ["Name", "Age", "Salary"],
        ["Alice", 25, 50000],
        ["Bob", 30, 60000],
        ["Charlie", 35, 70000]
    ]
    success = tools['write_sheet_data']("test.xlsx", "Sheet1", "A1", data)
    print(f"写入数据{'成功' if success else '失败'}")
    
    # 2. 写入带公式的工作表
    print("\n2. 写入公式数据...")
    data2 = [
        ["A", "B", "Sum"],
        [1, 4, "=A2+B2"],
        [2, 5, "=A3+B3"],
        [3, 6, "=A4+B4"]
    ]
    success = tools['write_sheet_data']("test.xlsx", "Sheet2", "A1", data2)
    print(f"写入数据{'成功' if success else '失败'}")
    
    # 3. 获取工作簿信息
    print("\n3. 读取工作簿信息...")
    workbook_info = tools['get_workbook_info']("test.xlsx")
    print(f"找到 {len(workbook_info.sheets)} 个工作表:")
    for sheet in workbook_info.sheets:
        print(f"  - {sheet.name}:")
        print(f"    表头: {sheet.headers}")
        print(f"    数据范围: {sheet.data_range}")
        print(f"    行数: {sheet.row_count}")
        print(f"    列数: {sheet.column_count}")
    
    # 4. 读取数据
    print("\n4. 读取数据...")
    data = tools['read_sheet_data']("test.xlsx", "Sheet1", "A1:C3")
    print("Sheet1 数据:")
    for row in data.data:
        print(f"  {row}")
    
    # 5. 读取公式
    print("\n5. 读取公式...")
    formulas = tools['read_sheet_formula']("test.xlsx", "Sheet2")
    print("Sheet2 公式:")
    for formula in formulas.formulas:
        print(f"  {formula}")

if __name__ == "__main__":
    test_excel_operations() 