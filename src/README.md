# Qianji Project - Source Code

## Architecture Overview
- **Core Engine**: Qwen Max model for all logic, reasoning, and bazi calculations
- **Data Processing**: Classical Chinese text parsing and modern interpretation
- **Communication Style**: Doudou model for conversational interface only
- **Knowledge Base**: Traditional classics from `../raw_books/bazi_classics/`

## Model Usage Policy
- **Qwen Max**: Used for all analytical tasks, bazi computations, pattern recognition, 
  logical reasoning, and knowledge synthesis from classical texts
- **Doudou**: Used exclusively for conversation style, tone, and user interaction formatting
- **Separation**: Keep model responsibilities clearly separated - Qwen for thinking, 
  Doudou for talking

## Directory Structure
- `core/` - Main AI engine and bazi calculation logic (Qwen Max)
- `data/` - Processed datasets and embeddings (Qwen Max)
- `interface/` - User interaction and communication layer (Doudou style)
- `utils/` - Helper functions and utilities (Qwen Max for logic, Doudou for output)

## Next Steps
1. Implement classical text parser for raw books
2. Build bazi calculation engine with Qwen Max
3. Develop Doudou-style conversation interface
4. Integrate models with clear separation of responsibilities