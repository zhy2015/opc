#!/usr/bin/env python3
import json
import os
import subprocess
from pathlib import Path

ROOT = Path('/Users/hidream/.openclaw/workspace')
OPC = ROOT / 'projects' / 'opc'
OUT = OPC / 'artifacts' / 'comics' / 'renders'
SEEDREAM = ROOT / 'skills' / 'hidream-api-gen' / 'scripts' / 'seedream.py'

jobs = [
    {
        'name': 'cover',
        'out_dir': OUT / 'cover',
        'resolution': '2048*2048',
        'prompt': 'A Chinese knowledge comic cover about OPC architecture. One calm CEO stands in the central command room, facing a glowing orchestration control plane. Behind the CEO are eight illuminated independent work pods arranged in a precise arc. Outside the glass wall, a giant complex task storm approaches, with floating Chinese keywords like research, verification, analysis, writing, summary. Strong visual hierarchy, futuristic command center, clean sci-fi infographic style, blue-gray palette with red alert accents, highly polished and readable.',
    },
    {
        'name': 'page-01',
        'out_dir': OUT / 'page-01',
        'resolution': '2048*2048',
        'prompt': 'A full comic page in a futuristic command center. Page theme: why OPC starts only for complex decomposable tasks. Show a giant complex task storm outside the command room, the CEO facing an overloaded main screen, two decision options handle alone vs activate OPC, then pressing an activate OPC button, then a final panel showing the three-layer architecture: CEO session, control plane, child sessions x8. Chinese knowledge comic, cinematic infographic storytelling, clear narrative sequence, dramatic opening.',
    },
    {
        'name': 'page-05',
        'out_dir': OUT / 'page-05',
        'resolution': '2048*2048',
        'prompt': 'A Chinese knowledge comic page about concurrency slots. The control plane shows exactly eight active running slots. Eight work pods are occupied. A ninth task character holding a number 9 card waits in a clearly marked queue area. Then one finished pod releases a slot and the queued task enters. The page must clearly show that 8 is the maximum number of simultaneous child sessions, not the total number of tasks. Dynamic infographic comic style, clear flow arrows, fast rhythm.',
    },
    {
        'name': 'page-06',
        'out_dir': OUT / 'page-06',
        'resolution': '2048*2048',
        'prompt': 'A Chinese knowledge comic ending page about auto-reporting and final synthesis. Multiple completed child pods send result cards back through glowing pipelines into the control plane. The control plane categorizes and forwards them to the CEO. The CEO then assembles one unified final answer on the main screen. Final panel shows the complete stable system: CEO in the center, orchestration console in front, eight pods behind, calm and resolved atmosphere. Clean futuristic infographic storytelling, satisfying ending.',
    },
]

negative = 'no fantasy armor, no medieval aesthetics, no messy chaotic composition, no overly cartoonish chibi style, no extra hidden child agents, no humanoid control plane, no child agents discussing globally together in one room'

for job in jobs:
    job['out_dir'].mkdir(parents=True, exist_ok=True)
    cmd = [
        'python3', str(SEEDREAM),
        '--version', 'M1',
        '--prompt', job['prompt'],
        '--negative-prompt', negative,
        '--resolution', job['resolution'],
        '--img-count', '1',
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    result_path = job['out_dir'] / 'result.json'
    result_path.write_text(proc.stdout if proc.stdout else proc.stderr, encoding='utf-8')
    print(f"[{job['name']}] exit={proc.returncode} -> {result_path}")
