"""
Qianji Classical Text Parser

This module handles parsing and processing of classical Chinese texts
from the raw_books/bazi_classics directory, converting ancient terminology
into structured data for the AI engine.

Model Usage: Qwen Max for text analysis and logical processing, 
Doudou style only for final output formatting if needed
"""

class ClassicalParser:
    """Parser for classical Chinese命理 texts"""
    
    def __init__(self):
        self.heavenly_stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        self.earthly_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        self.five_elements = ['木', '火', '土', '金', '水']
        self.ten_gods = ['比肩', '劫财', '食神', '伤官', '偏财', '正财', '七杀', '正官', '偏印', '正印']
    
    def parse_bazi_text(self, text):
        """Parse classical bazi text and extract structured information"""
        # Extract heavenly stems and earthly branches
        stems_found = []
        branches_found = []
        
        for char in text:
            if char in self.heavenly_stems:
                stems_found.append(char)
            elif char in self.earthly_branches:
                branches_found.append(char)
        
        return {
            'heavenly_stems': stems_found,
            'earthly_branches': branches_found,
            'raw_text': text[:500] + '...' if len(text) > 500 else text
        }
    
    def extract_case_studies(self, text):
        """Extract命例 (case studies) from classical texts"""
        # Look for patterns like "命造" or "八字"
        case_patterns = ['命造', '八字', '命主', '造化', '格局']
        cases = []
        
        lines = text.split('\n')
        for line in lines:
            if any(pattern in line for pattern in case_patterns):
                cases.append(line.strip())
        
        return cases
    
    def process_classical_file(self, file_path):
        """Process a complete classical text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            parsed_data = self.parse_bazi_text(content)
            cases = self.extract_case_studies(content)
            
            return {
                'file_path': file_path,
                'parsed_data': parsed_data,
                'case_studies': cases,
                'total_characters': len(content)
            }
        except Exception as e:
            return {'error': str(e), 'file_path': file_path}