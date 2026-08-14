#!/usr/bin/env python3
"""
跨平台PDF处理命令行工具
支持功能：
1. 合并PDF文件
2. 拆分PDF文件
3. 提取PDF页面
4. 旋转PDF页面
5. 添加水印
6. 压缩PDF文件
"""

import os
import sys
import argparse
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import tempfile

def merge_pdfs(pdf_list, output_path):
    """合并多个PDF文件"""
    try:
        merger = PyPDF2.PdfMerger()
        for pdf in pdf_list:
            if not os.path.exists(pdf):
                print(f"错误：文件 '{pdf}' 不存在")
                return False
            merger.append(pdf)
        merger.write(output_path)
        merger.close()
        print(f"成功：PDF文件已合并到 '{output_path}'")
        return True
    except Exception as e:
        print(f"错误：合并PDF时发生异常 - {str(e)}")
        return False

def split_pdf(input_path, output_dir):
    """拆分PDF文件为单页"""
    try:
        if not os.path.exists(input_path):
            print(f"错误：文件 '{input_path}' 不存在")
            return False
            
        os.makedirs(output_dir, exist_ok=True)
        
        with open(input_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            
            for page_num in range(total_pages):
                writer = PyPDF2.PdfWriter()
                writer.add_page(reader.pages[page_num])
                
                output_path = os.path.join(output_dir, f"page_{page_num + 1}.pdf")
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                
            print(f"成功：PDF已拆分为 {total_pages} 个页面，保存在 '{output_dir}' 目录")
            return True
    except Exception as e:
        print(f"错误：拆分PDF时发生异常 - {str(e)}")
        return False

def extract_pages(input_path, page_ranges, output_path):
    """提取指定页面"""
    try:
        if not os.path.exists(input_path):
            print(f"错误：文件 '{input_path}' 不存在")
            return False
            
        with open(input_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            
            # 解析页码范围
            pages_to_extract = set()
            for item in page_ranges:
                if '-' in item:
                    start, end = map(int, item.split('-'))
                    pages_to_extract.update(range(start - 1, end))
                else:
                    pages_to_extract.add(int(item) - 1)
            
            # 验证页码
            for page in pages_to_extract:
                if page < 0 or page >= total_pages:
                    print(f"错误：页码 {page + 1} 超出范围 (1-{total_pages})")
                    return False
            
            writer = PyPDF2.PdfWriter()
            for page_num in sorted(pages_to_extract):
                writer.add_page(reader.pages[page_num])
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            print(f"成功：提取了 {len(pages_to_extract)} 页到 '{output_path}'")
            return True
    except Exception as e:
        print(f"错误：提取页面时发生异常 - {str(e)}")
        return False

def rotate_pages(input_path, rotation, output_path, pages=None):
    """旋转PDF页面"""
    try:
        if not os.path.exists(input_path):
            print(f"错误：文件 '{input_path}' 不存在")
            return False
            
        with open(input_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()
            
            # 如果未指定页面，则旋转所有页面
            if pages is None:
                pages = list(range(len(reader.pages)))
            else:
                # 转换为0基索引
                pages = [int(p) - 1 for p in pages]
            
            for i, page in enumerate(reader.pages):
                if i in pages:
                    page.rotate(rotation)
                writer.add_page(page)
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            print(f"成功：旋转页面后保存到 '{output_path}'")
            return True
    except Exception as e:
        print(f"错误：旋转页面时发生异常 - {str(e)}")
        return False

def add_watermark(input_path, watermark_text, output_path, position="center"):
    """添加文字水印"""
    try:
        if not os.path.exists(input_path):
            print(f"错误：文件 '{input_path}' 不存在")
            return False
        
        # 创建临时水印PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            watermark_pdf = temp_file.name
        
        # 创建水印PDF
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        width, height = letter
        
        # 设置水印样式 - 使用支持中文的字体
        font_paths = [
            "C:/Windows/Fonts/simhei.ttf",  # Windows 黑体
            "C:/Windows/Fonts/simsun.ttc",  # Windows 宋体
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",  # Linux 文泉驿
            "/System/Library/Fonts/PingFang.ttc",  # macOS
        ]
        
        chinese_font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                from reportlab.pdfbase import pdfmetrics
                from reportlab.pdfbase.ttfonts import TTFont
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                chinese_font = 'ChineseFont'
                break
        
        if chinese_font is None:
            can.setFont("Helvetica", 30)
        else:
            can.setFont(chinese_font, 30)
        
        can.setFillGray(0.5, 0.3)  # 半透明灰色
        
        # 根据位置设置水印
        if position == "center":
            can.saveState()
            can.translate(width / 2, height / 2)
            can.rotate(45)
            can.drawCentredString(0, 0, watermark_text)
            can.restoreState()
        elif position == "top-right":
            can.drawString(width - 150, height - 50, watermark_text)
        elif position == "bottom-left":
            can.drawString(50, 50, watermark_text)
        else:  # default center
            can.saveState()
            can.translate(width / 2, height / 2)
            can.rotate(45)
            can.drawCentredString(0, 0, watermark_text)
            can.restoreState()
        
        can.save()
        packet.seek(0)
        
        # 将水印应用到原PDF
        with open(watermark_pdf, 'wb') as f:
            f.write(packet.getvalue())
        
        with open(input_path, 'rb') as input_file:
            reader = PyPDF2.PdfReader(input_file)
            writer = PyPDF2.PdfWriter()
            
            with open(watermark_pdf, 'rb') as watermark_file:
                watermark_reader = PyPDF2.PdfReader(watermark_file)
                watermark_page = watermark_reader.pages[0]
                
                for page in reader.pages:
                    page.merge_page(watermark_page)
                    writer.add_page(page)
                
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
        
        # 清理临时文件
        os.unlink(watermark_pdf)
        
        print(f"成功：水印添加到 '{output_path}'")
        return True
    except Exception as e:
        print(f"错误：添加水印时发生异常 - {str(e)}")
        return False

def compress_pdf(input_path, output_path):
    """压缩PDF文件（通过重新写入和优化）"""
    try:
        if not os.path.exists(input_path):
            print(f"错误：文件 '{input_path}' 不存在")
            return False
            
        with open(input_path, 'rb') as input_file:
            reader = PyPDF2.PdfReader(input_file)
            writer = PyPDF2.PdfWriter()
            
            for page in reader.pages:
                # 尝试压缩内容流
                if "/Filter" in page:
                    # 如果已有压缩过滤器，保持原样
                    pass
                writer.add_page(page)
            
            # 写入压缩版本
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
        
        # 比较文件大小
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        reduction = ((original_size - compressed_size) / original_size) * 100
        
        print(f"成功：PDF压缩完成")
        print(f"原始大小: {original_size / 1024:.2f} KB")
        print(f"压缩后大小: {compressed_size / 1024:.2f} KB")
        print(f"减少: {reduction:.1f}%")
        return True
    except Exception as e:
        print(f"错误：压缩PDF时发生异常 - {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='PDF处理命令行工具 - 支持合并、拆分、提取、旋转、添加水印和压缩PDF文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例：
  # 合并PDF
  pdf_tool.py merge -o merged.pdf file1.pdf file2.pdf file3.pdf
  
  # 拆分PDF
  pdf_tool.py split -d output_dir input.pdf
  
  # 提取指定页面
  pdf_tool.py extract -p 1-3,5,7-9 -o extracted.pdf input.pdf
  
  # 旋转页面
  pdf_tool.py rotate -r 90 -p 1,3 -o rotated.pdf input.pdf
  
  # 添加水印
  pdf_tool.py watermark -t "机密文件" -o watermarked.pdf input.pdf
  
  # 压缩PDF
  pdf_tool.py compress -o compressed.pdf input.pdf
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 合并命令
    merge_parser = subparsers.add_parser('merge', help='合并多个PDF文件')
    merge_parser.add_argument('pdfs', nargs='+', help='要合并的PDF文件')
    merge_parser.add_argument('-o', '--output', default='merged.pdf', help='输出文件名')
    
    # 拆分命令
    split_parser = subparsers.add_parser('split', help='拆分PDF为单页')
    split_parser.add_argument('input', help='输入PDF文件')
    split_parser.add_argument('-d', '--directory', default='split_pages', help='输出目录')
    
    # 提取命令
    extract_parser = subparsers.add_parser('extract', help='提取指定页面')
    extract_parser.add_argument('input', help='输入PDF文件')
    extract_parser.add_argument('-p', '--pages', nargs='+', required=True, 
                               help='页码范围 (例如: 1-3,5,7-9)')
    extract_parser.add_argument('-o', '--output', default='extracted.pdf', help='输出文件名')
    
    # 旋转命令
    rotate_parser = subparsers.add_parser('rotate', help='旋转页面')
    rotate_parser.add_argument('input', help='输入PDF文件')
    rotate_parser.add_argument('-r', '--rotation', type=int, choices=[90, 180, 270], 
                              required=True, help='旋转角度 (90, 180, 270)')
    rotate_parser.add_argument('-p', '--pages', nargs='+', help='要旋转的页码 (默认: 所有页)')
    rotate_parser.add_argument('-o', '--output', default='rotated.pdf', help='输出文件名')
    
    # 水印命令
    watermark_parser = subparsers.add_parser('watermark', help='添加文字水印')
    watermark_parser.add_argument('input', help='输入PDF文件')
    watermark_parser.add_argument('-t', '--text', required=True, help='水印文字')
    watermark_parser.add_argument('-pos', '--position', 
                                 choices=['center', 'top-right', 'bottom-left'], 
                                 default='center', help='水印位置')
    watermark_parser.add_argument('-o', '--output', default='watermarked.pdf', help='输出文件名')
    
    # 压缩命令
    compress_parser = subparsers.add_parser('compress', help='压缩PDF文件')
    compress_parser.add_argument('input', help='输入PDF文件')
    compress_parser.add_argument('-o', '--output', default='compressed.pdf', help='输出文件名')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'merge':
        success = merge_pdfs(args.pdfs, args.output)
    elif args.command == 'split':
        success = split_pdf(args.input, args.directory)
    elif args.command == 'extract':
        success = extract_pages(args.input, args.pages, args.output)
    elif args.command == 'rotate':
        success = rotate_pages(args.input, args.rotation, args.output, 
                              args.pages.split(',') if args.pages else None)
    elif args.command == 'watermark':
        success = add_watermark(args.input, args.text, args.output, args.position)
    elif args.command == 'compress':
        success = compress_pdf(args.input, args.output)
    else:
        parser.print_help()
        success = False
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()