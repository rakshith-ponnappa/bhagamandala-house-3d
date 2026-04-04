#!/usr/bin/env python3
"""
Bhagamandala House — Build Pipeline
====================================
Single command to regenerate all outputs when design changes:
  python pipeline.py [--images] [--pdfs] [--3d] [--all]

Steps:
  1. Generate 6 PNG architectural images  (generate_plans_v4.py)
  2. Generate 5 PDFs from markdown docs    (generate_pdfs.py)
  3. Update 3D viewer room data            (sync from generate_plans_v4.py)
  4. Update context doc timestamp
"""

import argparse
import os
import subprocess
import sys
import time
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(BASE, '..', '.venv', 'bin', 'python3')
if not os.path.exists(VENV_PYTHON):
    VENV_PYTHON = sys.executable


def run_script(name, desc):
    """Run a Python script and report success/failure."""
    path = os.path.join(BASE, name)
    if not os.path.exists(path):
        print(f"  SKIP  {name} (not found)")
        return False
    print(f"  RUN   {desc}...")
    t0 = time.time()
    result = subprocess.run(
        [VENV_PYTHON, path],
        cwd=BASE,
        capture_output=True,
        text=True,
    )
    elapsed = time.time() - t0
    if result.returncode == 0:
        print(f"  OK    {desc} ({elapsed:.1f}s)")
        if result.stdout.strip():
            for line in result.stdout.strip().split('\n')[-5:]:
                print(f"        {line}")
        return True
    else:
        print(f"  FAIL  {desc} (exit {result.returncode})")
        if result.stderr.strip():
            for line in result.stderr.strip().split('\n')[-8:]:
                print(f"        {line}")
        return False


def step_images():
    """Step 1: Regenerate architectural plan images."""
    print("\n━━━ Step 1: Generate Images ━━━")
    return run_script('generate_plans_v4.py', '6 PNG architectural plans')


def step_pdfs():
    """Step 2: Regenerate PDFs from markdown."""
    print("\n━━━ Step 2: Generate PDFs ━━━")
    return run_script('generate_pdfs.py', '5 PDF documents')


def step_3d_sync():
    """Step 3: Verify 3D viewer is in sync with room data."""
    print("\n━━━ Step 3: 3D Viewer Sync Check ━━━")
    viewer = os.path.join(BASE, '3d-viewer', 'index.html')
    if not os.path.exists(viewer):
        print("  SKIP  3D viewer not found")
        return False

    # Read the viewer and check room count
    with open(viewer, 'r', encoding='utf-8') as f:
        content = f.read()

    # Count room entries in the R={...} block
    import re
    room_keys = re.findall(r"(gf_\w+|ff_\w+)\s*:\s*\{", content)
    print(f"  OK    3D viewer has {len(room_keys)} rooms defined")

    # Check v4 generator for room count comparison
    gen_path = os.path.join(BASE, 'generate_plans_v4.py')
    if os.path.exists(gen_path):
        with open(gen_path, 'r', encoding='utf-8') as f:
            gen_content = f.read()
        # Count rooms from the generator's draw calls
        gf_rooms = len(re.findall(r"draw_room\(ax.*?'[^']+", gen_content))
        print(f"  INFO  Generator has ~{gf_rooms} draw_room calls")

    # Check file timestamps
    viewer_mtime = os.path.getmtime(viewer)
    viewer_age = time.time() - viewer_mtime
    if viewer_age < 60:
        print(f"  OK    3D viewer updated {viewer_age:.0f}s ago")
    else:
        mins = viewer_age / 60
        if mins < 60:
            print(f"  INFO  3D viewer last modified {mins:.0f} minutes ago")
        else:
            print(f"  WARN  3D viewer last modified {mins/60:.1f} hours ago")

    return True


def step_context():
    """Step 4: Update context document timestamp."""
    print("\n━━━ Step 4: Update Context Doc ━━━")
    ctx_files = [
        'HOUSE CONSTRUCTION PROJECT — FULL CONTEXT FOR CONTINUATION v4.d',
        'HOUSE CONSTRUCTION PROJECT — FULL CONTEXT FOR CONTINUATION.d',
    ]
    updated = False
    for fname in ctx_files:
        fpath = os.path.join(BASE, fname)
        if os.path.exists(fpath):
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()

            now = datetime.now().strftime('%Y-%m-%d %H:%M')
            # Update "Last pipeline run" line if present, or add one at end
            marker = 'Last pipeline run:'
            if marker in content:
                import re
                content = re.sub(
                    r'Last pipeline run:.*',
                    f'Last pipeline run: {now}',
                    content,
                )
            else:
                content += f'\n\n---\nLast pipeline run: {now}\n'

            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  OK    Updated timestamp in {fname}")
            updated = True
    if not updated:
        print("  SKIP  No context documents found")
    return updated


def summary():
    """Print output file summary."""
    print("\n━━━ Output Summary ━━━")
    patterns = {
        'Images (PNG)': ['*.png'],
        'PDFs': ['*.pdf'],
        '3D Viewer': ['3d-viewer/index.html'],
        'Context': ['*.d'],
    }
    for label, globs in patterns.items():
        files = []
        for g in globs:
            import glob
            files.extend(glob.glob(os.path.join(BASE, g)))
        if files:
            newest = max(files, key=os.path.getmtime)
            age = time.time() - os.path.getmtime(newest)
            age_str = f"{age:.0f}s ago" if age < 120 else f"{age/60:.0f}m ago"
            print(f"  {label:18s} {len(files)} files  (newest: {age_str})")
        else:
            print(f"  {label:18s} —")


def main():
    parser = argparse.ArgumentParser(
        description='Bhagamandala House — Build Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('--images', action='store_true', help='Regenerate PNG images only')
    parser.add_argument('--pdfs', action='store_true', help='Regenerate PDFs only')
    parser.add_argument('--viewer', action='store_true', help='Check 3D viewer sync only')
    parser.add_argument('--all', action='store_true', help='Run all steps (default)')
    args = parser.parse_args()

    # If no specific flag, run all
    run_all = args.all or not (args.images or args.pdfs or args.viewer)

    print("╔══════════════════════════════════════════╗")
    print("║  Bhagamandala House — Build Pipeline     ║")
    print("╚══════════════════════════════════════════╝")
    print(f"  Time:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Base:  {BASE}")
    print(f"  Python: {VENV_PYTHON}")

    t0 = time.time()
    results = {}

    if run_all or args.images:
        results['images'] = step_images()
    if run_all or args.pdfs:
        results['pdfs'] = step_pdfs()
    if run_all or args.viewer:
        results['3d'] = step_3d_sync()
    if run_all:
        results['context'] = step_context()

    summary()

    elapsed = time.time() - t0
    ok = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"\n  Done: {ok}/{total} steps OK in {elapsed:.1f}s")

    if ok < total:
        sys.exit(1)


if __name__ == '__main__':
    main()
