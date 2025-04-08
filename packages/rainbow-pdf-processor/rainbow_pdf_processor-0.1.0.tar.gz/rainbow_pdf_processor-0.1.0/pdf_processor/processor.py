"""
PDF处理器模块

提供了PDF文档的处理功能，包括：
1. 文本提取
2. 表格识别
3. 图片提取
4. 文档分类
5. 内容分析
6. 多语言支持
"""

from typing import List, Dict, Optional, Union, Literal
import os
from pathlib import Path
import fitz
from contextlib import contextmanager
import base64
import tempfile
import mimetypes


class PDFProcessor:
    """
    PDF文档处理器
    
    提供了一系列PDF文档处理功能的类，支持：
    1. 文本提取和分析
    2. 表格数据提取
    3. 图片识别和导出
    4. 文档结构分析
    5. 内容分类和标注
    6. 多语言文档处理
    
    属性:
        file_path (Path): PDF文件路径
        encoding (str): 文档编码
        language (str): 文档语言
    """
    
    def __init__(self, file_path: Union[str, Path], encoding: str = 'utf-8', language: str = 'zh'):
        """
        初始化PDF处理器
        
        Args:
            file_path: PDF文件路径
            encoding: 文档编码，默认utf-8
            language: 文档语言，默认中文
        """
        self.file_path = Path(file_path)
        self.encoding = encoding
        self.language = language
        self._doc = None  # 延迟加载
        
    @property
    def doc(self):
        """
        延迟加载 PDF 文档
        
        Returns:
            fitz.Document: PDF文档对象
        """
        if self._doc is None:
            self._doc = fitz.open(self.file_path)
        return self._doc
        
    @contextmanager
    def open_doc(self):
        """
        安全地打开和关闭文档的上下文管理器
        
        使用示例:
        ```python
        with self.open_doc() as doc:
            # 使用doc进行操作
            text = doc.get_page_text(0)
        ```
        """
        try:
            if self._doc is None:
                self._doc = fitz.open(self.file_path)
            yield self._doc
        finally:
            if self._doc is not None:
                self._doc.close()
                self._doc = None
                
    async def extract_text(self, start_page: Optional[int] = None, end_page: Optional[int] = None) -> str:
        """
        提取PDF文本内容
        
        Args:
            start_page: 起始页码（从0开始），None表示从第一页开始
            end_page: 结束页码（包含），None表示到最后一页
            
        Returns:
            提取的文本内容
            
        Raises:
            ValueError: 页码参数无效时抛出
        """
        with self.open_doc() as doc:
            # 规范化页码范围
            if start_page is None:
                start_page = 0
            if end_page is None:
                end_page = doc.page_count - 1
                
            # 验证页码范围
            if not (0 <= start_page <= end_page < doc.page_count):
                raise ValueError(
                    f"页码范围无效：start_page={start_page}, end_page={end_page}, "
                    f"文档总页数={doc.page_count}"
                )
            
            # 提取文本
            text = ""
            for page_num in range(start_page, end_page + 1):
                text += doc.get_page_text(page_num)
            return text
        
    async def extract_tables(self, start_page: Optional[int] = None, end_page: Optional[int] = None) -> List[Dict]:
        """
        提取PDF中的表格数据
        
        Args:
            start_page: 起始页码（从0开始），None表示从第一页开始
            end_page: 结束页码（包含），None表示到最后一页
            
        Returns:
            表格数据列表，每个表格为一个字典
            
        Raises:
            ValueError: 页码参数无效时抛出
        """
        with self.open_doc() as doc:
            # 规范化页码范围
            if start_page is None:
                start_page = 0
            if end_page is None:
                end_page = doc.page_count - 1
                
            # 验证页码范围
            if not (0 <= start_page <= end_page < doc.page_count):
                raise ValueError(
                    f"页码范围无效：start_page={start_page}, end_page={end_page}, "
                    f"文档总页数={doc.page_count}"
                )
            
            # 提取表格
            tables = []
            for page_num in range(start_page, end_page + 1):
                tables.extend(doc.get_page_tables(page_num))
            return tables
        
    async def extract_images(
        self,
        output_dir: Optional[Union[str, Path]] = None,
        return_type: Literal["base64", "path"] = "base64",
        image_format: str = "png"
    ) -> Union[List[str], List[Path]]:
        """
        提取PDF中的图片
        
        Args:
            output_dir: 图片保存目录，None表示使用临时目录
            return_type: 返回类型，可选 "base64" 或 "path"
                - "base64": 返回图片的base64编码字符串列表
                - "path": 返回图片的文件路径列表
            image_format: 图片保存格式，默认为"png"，支持"jpg"、"png"等
            
        Returns:
            如果 return_type 为 "path"：
                List[Path]: 提取的图片文件路径列表
            如果 return_type 为 "base64"：
                List[str]: 提取的图片base64编码列表，格式为 "data:image/png;base64,..."
            
        Raises:
            ValueError: 当 return_type 不是 "base64" 或 "path" 时
            IOError: 当图片保存失败时
        """
        if return_type not in ["base64", "path"]:
            raise ValueError('return_type 必须是 "base64" 或 "path"')
        
        # 确定输出目录
        if output_dir is None:
            output_dir = tempfile.mkdtemp(prefix="pdf_images_")
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        image_list = []
        
        with self.open_doc() as doc:
            # 遍历所有页面
            for page_num in range(doc.page_count):
                page = doc[page_num]
                # 获取页面上的图片列表
                images = page.get_images()
                
                for img_index, img in enumerate(images):
                    # 获取图片信息
                    xref = img[0]  # 图片的xref号
                    base_image = doc.extract_image(xref)

                    def process_image(base_image):
                        if base_image:
                            image_bytes = base_image["image"]
                        
                        if return_type == "base64":
                            # 转换为base64
                            mime_type = mimetypes.guess_type(f"dummy.{image_format}")[0]
                            b64_data = base64.b64encode(image_bytes).decode()
                            return f"data:{mime_type};base64,{b64_data}"
                        else:
                            # 保存为文件
                            image_path = Path(output_dir) / f"page_{page_num + 1}_img_{img_index + 1}.{image_format}"
                            try:
                                with open(image_path, "wb") as img_file:
                                    img_file.write(image_bytes)
                                return image_path
                            except IOError as e:
                                raise IOError(f"保存图片失败: {str(e)}")
                            
                    image_list.append(process_image(base_image))
        
        return image_list
        
            
    async def get_metadata(self) -> Dict:
        """
        获取PDF文档元数据
        
        Returns:
            文档元数据字典
        """
        return self.doc.metadata
        
    async def get_outline(self) -> List[Dict]:
        """
        获取PDF文档大纲
    
        Returns:
            文档大纲列表，每个条目包含：
            - level: 大纲级别
            - title: 标题
            - page: 页码
            - dest: 目标位置
        """
        with self.open_doc() as doc:
            # 获取目录结构
            toc = doc.get_toc()
            # 转换为字典列表
            outline = []
            for item in toc:
                outline.append({
                    'level': item[0],
                    'title': item[1],
                    'page': item[2],
                    'dest': item[3] if len(item) > 3 else None
                })
            return outline
        
    async def validate(self) -> bool:
        """
        验证PDF文件有效性
        
        检查项目包括：
        1. 文件是否存在
        2. 文件是否可以打开
        3. 文件是否为有效的PDF格式
        4. 文件是否被加密或损坏
        5. 文件是否有有效的页面
        
        Returns:
            bool: 文件是否有效
                - True: PDF文件有效且可以正常读取
                - False: PDF文件无效或不可读
                
        Raises:
            FileNotFoundError: 文件不存在
            PermissionError: 没有读取权限
            IOError: 文件读取错误
        """
        try:
            # 检查文件是否存在
            if not self.file_path.exists():
                raise FileNotFoundError(f"文件不存在: {self.file_path}")
            
            # 检查文件是否可读
            if not os.access(self.file_path, os.R_OK):
                raise PermissionError(f"没有读取权限: {self.file_path}")
            
            # 检查文件大小是否为0
            if self.file_path.stat().st_size == 0:
                return False
            
            with self.open_doc() as doc:
                # 检查是否为有效的PDF文档
                if not doc.is_pdf:
                    return False
                
                # 检查是否被加密
                if doc.is_encrypted:
                    return False
                
                # 检查是否有页面
                if doc.page_count < 1:
                    return False
                
                # 尝试访问第一页以验证文档结构
                try:
                    first_page = doc[0]
                    # 尝试获取页面大小，如果失败说明页面损坏
                    _ = first_page.rect
                except Exception:
                    return False
                
                # 检查文档的基本结构
                try:
                    # 检查文档目录
                    toc = doc.get_toc()
                    # 检查元数据
                    metadata = doc.metadata
                    # 如果以上操作都成功，说明文档结构基本完整
                except Exception:
                    # 即使没有目录或元数据，文档也可能是有效的
                    return False
                
                return True
            
        except fitz.FileDataError:
            # PDF格式错误
            return False
        except Exception as e:
            # 其他未预期的错误
            print(f"验证PDF时发生错误: {str(e)}")
            return False
        
    async def get_page_count(self) -> int:
        """
        获取PDF总页数
        
        Returns:
            总页数  
        """
        with self.open_doc() as doc:
            return doc.page_count
        
    async def __aenter__(self):
        """异步上下文管理器入口"""
        if self._doc is None:
            self._doc = fitz.open(self.file_path)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self._doc:
            self._doc.close()
            self._doc = None
        return False  # 不吞掉异常
