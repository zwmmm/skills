#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UniApp Custom Component Analyzer
Scans project components and generates components.csv

Usage:
    python analyze_components.py /path/to/uniapp-project
    python analyze_components.py /path/to/uniapp-project -o data/components.csv
"""

import os
import re
import csv
import argparse
from pathlib import Path
from typing import List, Dict, Set


def scan_components(project_path: str) -> List[Dict]:
    """Scan project for .vue files in components/ directory"""
    components = []
    components_dir = Path(project_path) / "components"

    if not components_dir.exists():
        print(f"Warning: components directory not found at {components_dir}")
        return []

    vue_files = list(components_dir.rglob("*.vue"))
    print(f"Found {len(vue_files)} .vue files in components/")

    for vue_file in vue_files:
        try:
            component_info = analyze_vue_file(vue_file, project_path)
            if component_info:
                components.append(component_info)
                print(f"  ✓ Analyzed: {vue_file.name}")
        except Exception as e:
            print(f"  ✗ Error analyzing {vue_file.name}: {e}")

    return components


def analyze_vue_file(file_path: Path, project_root: str) -> Dict:
    """Extract component metadata from .vue file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    component_name = file_path.stem

    # Extract sections
    template = extract_section(content, 'template')
    script = extract_section(content, 'script')

    # Extract metadata
    css_classes = extract_css_classes(template)
    props = extract_props(script)
    emits = extract_emits(script)
    slots = extract_slots(template)
    html_pattern = extract_root_element(template)
    use_case = infer_use_case(component_name, template, props)
    category = infer_category(component_name, template)
    code_example = generate_code_example(component_name, props, emits)

    return {
        "Component Name": component_name,
        "File Path": str(file_path.relative_to(project_root)),
        "HTML Pattern": html_pattern,
        "CSS Classes": " ".join(css_classes),
        "Props": props,
        "Slots": ",".join(slots) if slots else "",
        "Events": ",".join(emits) if emits else "",
        "Use Case": use_case,
        "Category": category,
        "Code Example": code_example,
        "Priority": "1"  # Custom components always have highest priority
    }


def extract_section(content: str, section_name: str) -> str:
    """Extract <template>, <script>, or <style> section"""
    pattern = rf'<{section_name}[^>]*>(.*?)</{section_name}>'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1) if match else ""


def extract_css_classes(template: str) -> List[str]:
    """Extract class names from template"""
    class_pattern = r'class=["\']([^"\']+)["\']'
    classes = re.findall(class_pattern, template)
    unique_classes: Set[str] = set()
    for class_str in classes:
        unique_classes.update(class_str.split())
    return sorted(list(unique_classes))


def extract_props(script: str) -> str:
    """Extract props from defineProps"""
    # Pattern 1: defineProps<{ ... }>()
    ts_pattern = r'defineProps<\{([^}]+)\}>\(\)'
    ts_match = re.search(ts_pattern, script, re.DOTALL)

    if ts_match:
        props_str = ts_match.group(1)
        return parse_ts_props(props_str)

    # Pattern 2: defineProps({ ... })
    js_pattern = r'defineProps\(\{([^}]+)\}\)'
    js_match = re.search(js_pattern, script, re.DOTALL)

    if js_match:
        props_str = js_match.group(1)
        return parse_js_props(props_str)

    return "{}"


def parse_ts_props(props_str: str) -> str:
    """Parse TypeScript props interface to JSON-like format"""
    # Simple parsing: extract prop names and types
    props = {}
    lines = props_str.strip().split('\n')
    for line in lines:
        line = line.strip()
        if ':' in line:
            # Match pattern like "title: string" or "price?: number"
            match = re.match(r'(\w+)\??\s*:\s*(\w+)', line)
            if match:
                prop_name, prop_type = match.groups()
                props[prop_name] = prop_type

    if props:
        # Format as JSON-like string
        return str(props).replace("'", '"')
    return "{}"


def parse_js_props(props_str: str) -> str:
    """Parse JavaScript props object to JSON format"""
    # This is a simplified parser - real implementation might need more robust parsing
    props = {}
    lines = props_str.strip().split('\n')
    for line in lines:
        line = line.strip().rstrip(',')
        if ':' in line:
            parts = line.split(':')
            if len(parts) >= 2:
                prop_name = parts[0].strip()
                # Extract type from { type: String, ... }
                if 'type' in parts[1]:
                    type_match = re.search(r'type:\s*(\w+)', parts[1])
                    if type_match:
                        props[prop_name] = type_match.group(1).lower()

    if props:
        return str(props).replace("'", '"')
    return "{}"


def extract_emits(script: str) -> List[str]:
    """Extract emits from defineEmits"""
    # Pattern 1: defineEmits<{ ... }>
    ts_pattern = r'defineEmits<\{([^}]+)\}>'
    ts_match = re.search(ts_pattern, script, re.DOTALL)

    if ts_match:
        emits_str = ts_match.group(1)
        # Extract event names like "click: ()" or "change: (value: string)"
        events = re.findall(r'(\w+):', emits_str)
        return events

    # Pattern 2: defineEmits(['click', 'change'])
    array_pattern = r"defineEmits\(\[(.*?)\]\)"
    array_match = re.search(array_pattern, script)

    if array_match:
        events_str = array_match.group(1)
        events = re.findall(r'["\'](\w+)["\']', events_str)
        return events

    return []


def extract_slots(template: str) -> List[str]:
    """Extract slot names from template"""
    # Find named slots: <slot name="header">
    slot_pattern = r'<slot\s+name=["\'](\w+)["\']'
    named_slots = re.findall(slot_pattern, template)

    # Check for default slot
    if '<slot' in template:
        if not named_slots or '<slot>' in template or '<slot />' in template:
            return ['default'] + named_slots if named_slots else ['default']

    return named_slots if named_slots else []


def extract_root_element(template: str) -> str:
    """Extract root element tag"""
    template = template.strip()

    # Match first tag
    tag_match = re.search(r'<(\w+)', template)

    if tag_match:
        return f"<{tag_match.group(1)}>"

    return "<view>"


def infer_use_case(name: str, template: str, props: str) -> str:
    """Infer component use case from name and structure"""
    name_lower = name.lower()

    use_case_map = {
        'button': '自定义按钮组件',
        'card': '卡片容器组件',
        'list': '列表项组件',
        'item': '通用项组件',
        'avatar': '用户头像显示',
        'badge': '徽章指示器',
        'tag': '标签标记',
        'icon': '图标包装',
        'image': '图片展示',
        'input': '自定义输入框',
        'form': '表单组件',
        'modal': '模态对话框',
        'popup': '弹出层组件',
        'drawer': '抽屉面板',
        'tab': 'Tab 组件',
        'navbar': '导航栏',
        'header': '页面头部',
        'footer': '页面底部',
        'loading': '加载指示器',
        'empty': '空状态',
        'error': '错误状态',
        'product': '商品组件',
        'user': '用户组件',
        'order': '订单组件',
    }

    for keyword, use_case in use_case_map.items():
        if keyword in name_lower:
            return use_case

    return f"自定义 {name} 组件"


def infer_category(name: str, template: str) -> str:
    """Infer component category"""
    name_lower = name.lower()

    category_map = {
        'button': 'button',
        'input': 'form',
        'form': 'form',
        'select': 'form',
        'checkbox': 'form',
        'radio': 'form',
        'card': 'layout',
        'list': 'data',
        'table': 'data',
        'grid': 'layout',
        'avatar': 'display',
        'image': 'display',
        'icon': 'display',
        'badge': 'feedback',
        'tag': 'display',
        'modal': 'feedback',
        'popup': 'feedback',
        'dialog': 'feedback',
        'toast': 'feedback',
        'loading': 'feedback',
        'drawer': 'navigation',
        'navbar': 'navigation',
        'tab': 'navigation',
        'menu': 'navigation',
        'header': 'layout',
        'footer': 'layout',
        'product': 'business',
        'user': 'business',
        'order': 'business',
    }

    for keyword, category in category_map.items():
        if keyword in name_lower:
            return category

    return 'custom'


def generate_code_example(name: str, props: str, emits: List[str]) -> str:
    """Generate usage example"""
    # Parse props to generate sample attributes
    try:
        props_dict = eval(props) if props != "{}" else {}
    except:
        props_dict = {}

    # Generate prop bindings
    prop_parts = []
    for prop_name, prop_type in props_dict.items():
        if prop_type.lower() in ['string', 'str']:
            prop_parts.append(f':{prop_name}="标题"')
        elif prop_type.lower() in ['number', 'int', 'float']:
            prop_parts.append(f':{prop_name}="99"')
        elif prop_type.lower() in ['boolean', 'bool']:
            prop_parts.append(f':{prop_name}="true"')
        else:
            prop_parts.append(f':{prop_name}="value"')

    # Generate event bindings
    event_parts = []
    for event in emits[:2]:  # Limit to first 2 events
        event_parts.append(f'@{event}="handle{event.capitalize()}"')

    all_parts = prop_parts + event_parts

    if all_parts:
        return f"<{name} {' '.join(all_parts)} />"
    else:
        return f"<{name} />"


def write_csv(components: List[Dict], output_file: str):
    """Write components to CSV file"""
    if not components:
        print("No components to write")
        return

    fieldnames = [
        "No", "Component Name", "File Path", "HTML Pattern",
        "CSS Classes", "Props", "Slots", "Events",
        "Use Case", "Category", "Code Example", "Priority"
    ]

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i, component in enumerate(components, 1):
            component["No"] = i
            writer.writerow(component)

    print(f"\n✓ Generated {output_file} with {len(components)} components")


def main():
    parser = argparse.ArgumentParser(description="Analyze UniApp custom components")
    parser.add_argument("project_path", help="Path to UniApp project")
    parser.add_argument("-o", "--output", default="components.csv", help="Output CSV file (default: components.csv)")

    args = parser.parse_args()

    print(f"Scanning components in {args.project_path}...")
    components = scan_components(args.project_path)

    if components:
        write_csv(components, args.output)
    else:
        print("\nNo components found. Make sure the project has a 'components/' directory with .vue files.")


if __name__ == "__main__":
    main()
