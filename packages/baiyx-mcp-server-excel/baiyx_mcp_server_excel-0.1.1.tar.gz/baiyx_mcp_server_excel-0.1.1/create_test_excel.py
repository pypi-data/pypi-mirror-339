import pandas as pd
import numpy as np

# 创建示例数据
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'Salary': [50000, 60000, 70000]
}
df = pd.DataFrame(data)

# 创建 Excel 文件
with pd.ExcelWriter('test.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    
    # 创建第二个工作表，包含公式
    df2 = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    df2.to_excel(writer, sheet_name='Sheet2', index=False)
    
    # 获取工作簿对象
    workbook = writer.book
    worksheet = workbook['Sheet2']
    
    # 添加公式
    worksheet['C1'] = 'Sum'
    worksheet['C2'] = '=A2+B2'
    worksheet['C3'] = '=A3+B3'
    worksheet['C4'] = '=A4+B4' 