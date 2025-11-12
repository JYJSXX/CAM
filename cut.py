from PyPDF2 import PdfReader, PdfWriter
import copy

def split_page_to_three(input_path, output_path, crop_boxes):
    """
    将每页PDF拆分成三个独立页面
    crop_boxes: 包含三个裁剪区域的坐标 [(x1,y1,x2,y2), (x1,y1,x2,y2), (x1,y1,x2,y2)]
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    # 处理每一页
    for page in reader.pages:
        # 为每个裁剪区域创建新页面
        for crop_box in crop_boxes:
            # 复制原页面
            new_page = copy.deepcopy(page)
            # 设置新的裁剪区域
            new_page.mediabox.lower_left = (crop_box[0], crop_box[1])
            new_page.mediabox.upper_right = (crop_box[2], crop_box[3])
            writer.add_page(new_page)
    
    # 保存新的PDF
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

# 使用示例
input_file = "1.4贝叶斯分类器.pdf"
output_file = "split/" + input_file

# 定义三个裁剪区域的坐标
crop_boxes = [
    (55,573, 285, 745),    # 第一个区域
    (55,335, 285, 507),  # 第二个区域
    (55,100, 285, 270)   # 第三个区域
]

split_page_to_three(input_file, output_file, crop_boxes)