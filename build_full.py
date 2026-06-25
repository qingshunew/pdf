import openpyxl
import os
import hashlib
import json

# 1. 读取Excel，建立 身份证号 -> 姓名 映射
print("读取Excel...")
wb = openpyxl.load_workbook(r'E:\王丰协助\南宁师范\所有文件\考生名单.xlsx')
ws = wb.active
id_to_name = {}
for row in ws.iter_rows(min_row=2, values_only=True):
    if row[7] and row[3]:
        id_to_name[str(row[7]).strip()] = str(row[3]).strip()
print(f"  读取到 {len(id_to_name)} 条学生记录")

# 2. 扫描PDF目录
pdf_dir = r'E:\王丰协助\南宁师范\输出准考证\pdf'
pdfs = sorted([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
print(f"  找到 {len(pdfs)} 个PDF文件")

# 3. 生成STUDENTS对象
students = {}
match_count = 0
no_match = []
for pdf in pdfs:
    idcard = pdf.replace('.pdf', '')
    name = id_to_name.get(idcard)
    if name:
        combined = name + idcard
        key = hashlib.sha256(combined.encode('utf-8')).hexdigest()[:16]
        students[key] = {"n": name, "file": "pdf/" + pdf}
        match_count += 1
    else:
        no_match.append(pdf)

print(f"  成功匹配: {match_count}")
if no_match:
    print(f"  未匹配: {len(no_match)} 个: {no_match[:5]}...")

# 4. 生成JS对象字符串（紧凑格式，每个条目一行）
entries = []
for key, val in sorted(students.items()):
    entries.append(f'    "{key}": {json.dumps(val, ensure_ascii=False)}')
students_js = ",\n".join(entries)

# 5. 读取原始HTML模板，替换STUDENTS数据
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_start = 'var STUDENTS = {'
old_end = '};'

start_pos = html.index(old_start)
end_pos = html.index(old_end, start_pos) + len(old_end)

new_block = f'var STUDENTS = {{\n{students_js}\n  }};'

new_html = html[:start_pos] + new_block + html[end_pos:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

# 6. 输出统计
file_size_kb = len(new_html) / 1024
print(f"\n完成! index.html 已更新")
print(f"  文件大小: {file_size_kb:.1f} KB")
print(f"  学生条目: {len(students)} 条")
