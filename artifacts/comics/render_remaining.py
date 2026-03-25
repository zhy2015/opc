#!/usr/bin/env python3
import subprocess
from pathlib import Path

ROOT = Path('/Users/hidream/.openclaw/workspace')
OPC = ROOT / 'projects' / 'opc'
OUT = OPC / 'artifacts' / 'comics' / 'renders'
SEEDREAM = ROOT / 'skills' / 'hidream-api-gen' / 'scripts' / 'seedream.py'
negative = 'no fantasy armor, no medieval aesthetics, no messy chaotic composition, no overly cartoonish chibi style, no extra hidden child agents, no humanoid control plane, no child agents discussing globally together in one room'

jobs = [
    {
        'name': 'page-02',
        'prompt': 'A Chinese knowledge comic page explaining the three-layer structure of OPC. The CEO breaks one large mission into multiple modular task cards. A control plane console routes these cards into different execution pods. Several child agents work in parallel in separate pods. Final panel clearly shows three layers: CEO for thinking and final synthesis, control plane for orchestration and collection, child sessions for isolated execution. Futuristic command room, infographic clarity, clean and structured layouts.'
    },
    {
        'name': 'page-03',
        'prompt': 'A Chinese knowledge comic page about independent sessions and isolated context. Three adjacent but isolated work pods, each with different task materials on screens, clearly separated by walls. One child agent notices a warning that says it only handles assigned work. The CEO dispatches different briefing packets from the control plane. Strong emphasis on isolated context, no shared mind, no cross-pod leakage. Clean sci-fi knowledge comic style.'
    },
    {
        'name': 'page-04',
        'prompt': 'A Chinese knowledge comic page focused on governance rules. A giant glowing rules board appears in the command room: only CEO can dispatch tasks. Arrows only flow from CEO to control plane to child pods. One child agent tries to press a nested spawn button and receives a bright red forbidden warning. The scene should strongly communicate no nested spawning, centralized control, and system stability. Futuristic system-governance comic style, strong red warning accents.'
    },
]

for job in jobs:
    out_dir = OUT / job['name']
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        'python3', str(SEEDREAM),
        '--version', 'M1',
        '--prompt', job['prompt'],
        '--negative-prompt', negative,
        '--resolution', '2048*2048',
        '--img-count', '1',
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    (out_dir / 'result.json').write_text(proc.stdout if proc.stdout else proc.stderr, encoding='utf-8')
    print(f"[{job['name']}] exit={proc.returncode}")
