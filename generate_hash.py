import openpyxl
import os
import hashlib

# 读取Excel，建立 身份证号 -> 姓名 映射
wb = openpyxl.load_workbook(r'E:\王丰协助\南宁师范\所有文件\考生名单.xlsx')
ws = wb.active
id_to_name = {}
for row in ws.iter_rows(min_row=2, values_only=True):
    if row[7] and row[3]:  # 身份证号, 姓名
        id_to_name[str(row[7]).strip()] = str(row[3]).strip()

# 读取PDF目录
pdf_dir = r'E:\王丰协助\南宁师范\输出准考证\pdf'
pdfs = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]

print(f'找到 {len(pdfs)} 个PDF文件：')
print('-' * 50)

students_js = {}
for pdf in pdfs:
    idcard = pdf.replace('.pdf', '')
    name = id_to_name.get(idcard, '未找到')
    if name != '未找到':
        # 生成SHA256哈希（前16位作为key）
        combined = name + idcard
        full_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        key = full_hash[:16]
        students_js[key] = {'n': name, 'file': 'pdf/' + pdf}
        print(f'{pdf} -> {name} (key: {key})')
    else:
        print(f'{pdf} -> 未找到对应姓名')

# 输出JS对象
print('\n' + '=' * 50)
print('STUDENTS JS对象：')
print('=' * 50)
print('var STUDENTS = {')
for key, val in students_js.items():
    print(f'  "{key}": {{ n: "{val["n"]}", file: "{val["file"]}" }},')
print('};')
