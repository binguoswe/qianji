"""
Qianji Knowledge Graph Builder

This module constructs a knowledge graph for Chinese metaphysics concepts
including heavenly stems, earthly branches, five elements, ten gods, 
and other bazi/destiny related entities and relationships.
"""

class MetaphysicsKnowledgeGraph:
    def __init__(self):
        self.graph = {}
        self.initialize_core_concepts()
    
    def initialize_core_concepts(self):
        """Initialize core metaphysical concepts and relationships"""
        # Heavenly Stems (天干)
        heavenly_stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        
        # Earthly Branches (地支)  
        earthly_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        # Five Elements (五行)
        five_elements = ['木', '火', '土', '金', '水']
        
        # Ten Gods (十神)
        ten_gods = ['正官', '七杀', '正印', '偏印', '正财', '偏财', '食神', '伤官', '比肩', '劫财']
        
        # Build relationships
        self.build_heavenly_earthly_relationships(heavenly_stems, earthly_branches)
        self.build_five_elements_system(five_elements)
        self.build_ten_gods_framework(ten_gods)
    
    def build_heavenly_earthly_relationships(self, stems, branches):
        """Build relationships between heavenly stems and earthly branches"""
        # Each stem-branch combination forms a unique energy signature
        for i, stem in enumerate(stems):
            for j, branch in enumerate(branches):
                combination = f"{stem}{branch}"
                self.graph[combination] = {
                    'type': 'stem_branch_combination',
                    'stem': stem,
                    'branch': branch,
                    'element': self.get_element_from_combination(stem, branch),
                    'relationships': []
                }
    
    def build_five_elements_system(self, elements):
        """Build the five elements generation and control cycles"""
        # Generation cycle (相生): Wood → Fire → Earth → Metal → Water → Wood
        generation_cycle = {
            '木': '火',
            '火': '土', 
            '土': '金',
            '金': '水',
            '水': '木'
        }
        
        # Control cycle (相克): Wood → Earth → Water → Fire → Metal → Wood  
        control_cycle = {
            '木': '土',
            '土': '水',
            '水': '火', 
            '火': '金',
            '金': '木'
        }
        
        for element in elements:
            self.graph[element] = {
                'type': 'five_element',
                'generates': generation_cycle[element],
                'controls': control_cycle[element],
                'is_generated_by': [k for k, v in generation_cycle.items() if v == element],
                'is_controlled_by': [k for k, v in control_cycle.items() if v == element]
            }
    
    def build_ten_gods_framework(self, ten_gods):
        """Build the ten gods relationship framework"""
        # Ten gods are derived from the relationship between day master and other stems/branches
        for god in ten_gods:
            self.graph[god] = {
                'type': 'ten_god',
                'characteristics': self.get_god_characteristics(god),
                'favorable_conditions': [],
                'unfavorable_conditions': []
            }
    
    def get_element_from_combination(self, stem, branch):
        """Determine the five element from stem-branch combination"""
        # This is a simplified mapping - actual logic is more complex
        stem_elements = {'甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土', '己': '土', 
                        '庚': '金', '辛': '金', '壬': '水', '癸': '水'}
        branch_elements = {'寅': '木', '卯': '木', '巳': '火', '午': '火', '辰': '土', '戌': '土',
                          '丑': '土', '未': '土', '申': '金', '酉': '金', '亥': '水', '子': '水'}
        
        return stem_elements.get(stem, branch_elements.get(branch, '土'))
    
    def get_god_characteristics(self, god):
        """Get characteristics of each ten god"""
        characteristics = {
            '正官': '正直、有责任感、守规矩',
            '七杀': '果断、有魄力、竞争性强', 
            '正印': '仁慈、有学识、保护性强',
            '偏印': '独特、有创意、内向',
            '正财': '稳定、务实、节俭',
            '偏财': '灵活、投机、慷慨',
            '食神': '温和、有才华、享受生活',
            '伤官': '聪明、叛逆、创新',
            '比肩': '独立、竞争、自我',
            '劫财': '冲动、豪爽、冒险'
        }
        return characteristics.get(god, '')
    
    def add_classical_text_relationships(self, text_name, concepts):
        """Add relationships extracted from classical texts"""
        if text_name not in self.graph:
            self.graph[text_name] = {'type': 'classical_text', 'concepts': []}
        
        self.graph[text_name]['concepts'].extend(concepts)
    
    def query_relationships(self, entity):
        """Query relationships for a given entity"""
        return self.graph.get(entity, {})
    
    def export_graph(self, format='json'):
        """Export the knowledge graph in specified format"""
        if format == 'json':
            import json
            return json.dumps(self.graph, ensure_ascii=False, indent=2)
        return str(self.graph)

# Usage example
if __name__ == "__main__":
    kg = MetaphysicsKnowledgeGraph()
    print("Knowledge graph initialized with core metaphysical concepts")
    print(f"Total entities: {len(kg.graph)}")