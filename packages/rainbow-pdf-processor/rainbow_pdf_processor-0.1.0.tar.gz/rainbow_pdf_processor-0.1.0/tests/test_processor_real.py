"""
PDFProcessor 集成测试模块

使用实际PDF文件进行测试，包括：
1. 文本提取测试
2. 表格识别测试
3. 图片提取测试
4. 文档结构分析
"""

import pytest
import os
from pathlib import Path
import base64
from pdf_processor.processor import PDFProcessor
from .create_test_pdf import create_test_pdf

pytestmark = pytest.mark.asyncio  # 标记所有测试为异步测试

# 在测试开始前创建测试用PDF文件
@pytest.fixture(scope="session")
def test_pdf_path(tmp_path_factory):
    """创建测试用PDF文件并返回路径"""
    # 使用 tmp_path_factory 创建会话级别的临时目录
    test_dir = tmp_path_factory.mktemp("test_pdfs")
    pdf_path = test_dir / "test.pdf"
    create_test_pdf(pdf_path)
    return pdf_path

@pytest.fixture
def pdf_processor(test_pdf_path):
    """创建 PDFProcessor 实例"""
    return PDFProcessor(test_pdf_path)

class TestPDFProcessorWithRealFile:
    """使用真实PDF文件的PDFProcessor测试"""
    
    async def test_file_exists(self, test_pdf_path):
        """测试文件存在性"""
        pdf_path = Path(test_pdf_path)
        assert pdf_path.exists(), "测试文件不存在"
        assert pdf_path.is_file(), "测试路径不是文件"
        assert pdf_path.stat().st_size > 0, "文件大小为0"
        
    async def test_basic_info(self, pdf_processor):
        """测试基本信息获取"""
        async with pdf_processor:
            # 测试页数
            page_count = await pdf_processor.get_page_count()
            assert page_count == 3, "PDF应该有3页"
            print(f"PDF总页数: {page_count}")
            
            # 测试文档有效性
            is_valid = await pdf_processor.validate()
            assert is_valid, "PDF文件应该是有效的"
            
    async def test_text_extraction(self, pdf_processor):
        """测试文本提取"""
        # 提取第一页文本
        text = await pdf_processor.extract_text(start_page=0, end_page=0)
        assert text, "第一页应该包含文本"
        assert "这是第一页" in text, "第一页文本内容不正确"
        print(f"第一页文本预览: {text[:200]}...")
        
        # 提取所有页面文本
        full_text = await pdf_processor.extract_text()
        assert len(full_text) > len(text), "完整文本应该比第一页更长"
        assert "这是第二页" in full_text, "完整文本应该包含第二页内容"
        assert "这是第三页" in full_text, "完整文本应该包含第三页内容"
        
    async def test_text_extraction_by_pages(self, pdf_processor):
        """测试分页文本提取"""
        page_count = await pdf_processor.get_page_count()
        
        # 测试每一页的文本提取
        for page in range(page_count):
            text = await pdf_processor.extract_text(
                start_page=page,
                end_page=page
            )
            print(f"第 {page+1} 页文本长度: {len(text)}")
            assert isinstance(text, str), f"第 {page+1} 页文本提取失败"
            assert text, f"第 {page+1} 页不应该为空"
            
    async def test_image_extraction_path(self, pdf_processor, tmp_path):
        """测试图片提取（保存为文件）"""
        # 创建临时目录用于保存图片
        output_dir = tmp_path / "images"
        output_dir.mkdir(exist_ok=True)
        
        # 提取图片并保存为文件
        image_paths = await pdf_processor.extract_images(
            output_dir=output_dir,
            return_type="path",
            image_format="png"
        )
        
        # 验证提取结果
        if image_paths:
            print(f"成功提取 {len(image_paths)} 张图片")
            for path in image_paths:
                assert path.exists(), f"图片文件不存在: {path}"
                assert path.stat().st_size > 0, f"图片文件为空: {path}"
                print(f"图片已保存: {path}")
                
    async def test_image_extraction_base64(self, pdf_processor):
        """测试图片提取（Base64格式）"""
        images = await pdf_processor.extract_images(return_type="base64")
        assert isinstance(images, list), "应该返回列表"
        if images:  # 如果PDF中包含图片
            for img in images:
                assert isinstance(img, str), "每个图片应该是Base64字符串"
                assert img.startswith("data:image/"), "应该包含MIME类型"
                # 验证是否为有效的Base64字符串
                try:
                    decoded = base64.b64decode(img.split(',')[1])  # 去掉 data:image/xxx;base64, 前缀
                    assert len(decoded) > 0, "Base64解码后应该有数据"
                except Exception as e:
                    pytest.fail(f"无效的Base64字符串: {str(e)}")
                
    @pytest.mark.parametrize("page_range", [
        (0, 0),                  # 第一页
        (None, None),           # 所有页面
        (0, 2),                 # 前三页
    ])
    async def test_text_extraction_ranges(self, pdf_processor, page_range):
        """测试不同页面范围的文本提取"""
        start_page, end_page = page_range
        text = await pdf_processor.extract_text(
            start_page=start_page,
            end_page=end_page
        )
        assert isinstance(text, str), "文本提取应该返回字符串"
        assert text, "提取的文本不应该为空"
        print(f"页面范围 {page_range} 提取的文本长度: {len(text)}")
        
    async def test_invalid_page_ranges(self, pdf_processor):
        """测试无效页面范围"""
        page_count = await pdf_processor.get_page_count()
        
        # 测试页码越界
        with pytest.raises(ValueError):
            await pdf_processor.extract_text(
                start_page=page_count + 1,
                end_page=page_count + 2
            )
            
        # 测试起始页大于结束页
        with pytest.raises(ValueError):
            await pdf_processor.extract_text(
                start_page=2,
                end_page=1
            )
            
    async def test_metadata(self, pdf_processor):
        """测试元数据获取"""
        metadata = await pdf_processor.get_metadata()
        assert isinstance(metadata, dict), "元数据应该是字典类型"
        
    async def test_outline(self, pdf_processor):
        """测试大纲获取"""
        outline = await pdf_processor.get_outline()
        assert isinstance(outline, list), "大纲应该是列表类型"
            
    async def test_resource_cleanup(self, pdf_processor):
        """测试资源清理"""
        # 使用上下文管理器
        async with pdf_processor:
            assert pdf_processor._doc is not None, "文档应该被加载"
            
        # 验证资源已被清理
        assert pdf_processor._doc is None, "文档应该被关闭"

if __name__ == "__main__":
    pytest.main(["-v", __file__])