from mcp_server_excel.server import ExcelServer

def test_excel_formulas():
    # 创建服务器实例
    server = ExcelServer()
    tools = server._tools
    
    # 1. 创建测试数据和各种公式
    print("\n1. 写入测试数据和公式...")
    data = [
        ["数字", "平方", "立方", "求和", "平均值", "最大值", "最小值", "计数"],
        [2, "=A2^2", "=A2^3", "=SUM(A2:A6)", "=AVERAGE(A2:A6)", "=MAX(A2:A6)", "=MIN(A2:A6)", "=COUNT(A2:A6)"],
        [4, "=A3^2", "=A3^3", "", "", "", "", ""],
        [6, "=A4^2", "=A4^3", "", "", "", "", ""],
        [8, "=A5^2", "=A5^3", "", "", "", "", ""],
        [10, "=A6^2", "=A6^3", "", "", "", "", ""]
    ]
    success = tools['write_sheet_data']("test_formula.xlsx", "公式测试", "A1", data)
    print(f"写入数据和公式{'成功' if success else '失败'}")
    
    # 2. 读取工作簿信息
    print("\n2. 读取工作簿信息...")
    workbook_info = tools['get_workbook_info']("test_formula.xlsx")
    print(f"工作表信息:")
    for sheet in workbook_info.sheets:
        print(f"  - {sheet.name}:")
        print(f"    表头: {sheet.headers}")
        print(f"    数据范围: {sheet.data_range}")
        print(f"    行数: {sheet.row_count}")
        print(f"    列数: {sheet.column_count}")
    
    # 3. 读取所有公式
    print("\n3. 读取所有公式...")
    formulas = tools['read_sheet_formula']("test_formula.xlsx", "公式测试")
    print("公式列表:")
    for formula in formulas.formulas:
        print(f"  {formula}")
    
    # 4. 读取特定范围的公式
    print("\n4. 读取平方列的公式...")
    square_formulas = tools['read_sheet_formula']("test_formula.xlsx", "公式测试", "B2:B6")
    print("平方公式:")
    for formula in square_formulas.formulas:
        print(f"  {formula}")
    
    # 5. 读取统计公式
    print("\n5. 读取统计公式...")
    stat_formulas = tools['read_sheet_formula']("test_formula.xlsx", "公式测试", "D2:H2")
    print("统计公式:")
    for formula in stat_formulas.formulas:
        print(f"  {formula}")

if __name__ == "__main__":
    test_excel_formulas() 