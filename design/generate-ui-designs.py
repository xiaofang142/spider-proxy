#!/usr/bin/env python3
"""
Spider Proxy UI Design Generator
Generates SVG design mockups for 6 core pages
"""

import svgwrite
from svgwrite import mm, px
import os
from datetime import datetime

# Design System Colors
COLORS = {
    'primary': '#FF6B35',
    'primary_dark': '#E55A2B',
    'primary_light': '#FF8C61',
    'success': '#4CAF50',
    'warning': '#FFC107',
    'error': '#F44336',
    'info': '#2196F3',
    'black': '#1A1A1A',
    'dark_gray': '#333333',
    'medium_gray': '#666666',
    'light_gray': '#999999',
    'extra_light_gray': '#E0E0E0',
    'white': '#FFFFFF',
    'background': '#F5F7FA',
    'surface': '#FFFFFF',
}

# Dimensions
CANVAS_WIDTH = 1440
CANVAS_HEIGHT = 900
SIDEBAR_WIDTH = 240
TOPBAR_HEIGHT = 64

def create_base_drawing(filename):
    """Create base SVG drawing with background"""
    dwg = svgwrite.Drawing(filename, size=(f'{CANVAS_WIDTH}px', f'{CANVAS_HEIGHT}px'), profile='full')
    
    # Background
    dwg.add(dwg.rect(insert=(0, 0), size=(CANVAS_WIDTH, CANVAS_HEIGHT), fill=COLORS['background']))
    
    return dwg

def draw_topbar(dwg, y=0):
    """Draw top navigation bar"""
    # Background
    dwg.add(dwg.rect(insert=(0, y), size=(CANVAS_WIDTH, TOPBAR_HEIGHT), fill=COLORS['surface']))
    dwg.add(dwg.line(start=(0, y + TOPBAR_HEIGHT), end=(CANVAS_WIDTH, y + TOPBAR_HEIGHT), 
                     stroke=COLORS['extra_light_gray'], stroke_width=1))
    
    # Logo
    dwg.add(dwg.circle(center=(32 + 16, y + 32), r=14, fill=COLORS['primary']))
    dwg.add(dwg.text('Spider Proxy', insert=(64, y + 42), 
                     fill=COLORS['black'], font_size=18, font_weight='bold', font_family='Arial'))
    
    # Search bar
    search_x = 400
    dwg.add(dwg.rect(insert=(search_x, y + 12), size=(300, 40), 
                     fill=COLORS['background'], stroke=COLORS['extra_light_gray'], 
                     stroke_width=1, rx=6))
    dwg.add(dwg.text('🔍 搜索请求 (支持自然语言)...', insert=(search_x + 36, y + 38),
                     fill=COLORS['light_gray'], font_size=14, font_family='Arial'))
    
    # Right icons
    icons = ['🔔', '⚙️', '👤']
    icon_x = CANVAS_WIDTH - 180
    for i, icon in enumerate(icons):
        dwg.add(dwg.text(icon, insert=(icon_x + i * 60, y + 42),
                        font_size=20, font_family='Arial'))
    
    return y + TOPBAR_HEIGHT

def draw_sidebar(dwg, y=64, active_index=0):
    """Draw side navigation"""
    items = [
        ('📊', '仪表盘'),
        ('📦', '抓包列表'),
        ('🔍', '过滤器'),
        ('📜', '脚本编辑'),
        ('⚙️', '设置'),
    ]
    
    for i, (icon, text) in enumerate(items):
        item_y = y + i * 56
        
        # Active state background
        if i == active_index:
            dwg.add(dwg.rect(insert=(0, item_y), size=(SIDEBAR_WIDTH, 56), fill='#FFF3ED'))
            dwg.add(dwg.rect(insert=(0, item_y), size=(4, 56), fill=COLORS['primary']))
            fill = COLORS['primary']
        else:
            fill = COLORS['dark_gray']
        
        dwg.add(dwg.text(f'{icon}  {text}', insert=(24, item_y + 36),
                        fill=fill, font_size=14, font_family='Arial'))
    
    return SIDEBAR_WIDTH

def draw_status_card(dwg, x, y, title, status, status_color, details):
    """Draw a status card"""
    card_width = 280
    card_height = 160
    
    # Card background
    dwg.add(dwg.rect(insert=(x, y), size=(card_width, card_height), 
                     fill=COLORS['surface'], rx=8))
    dwg.add(dwg.rect(insert=(x, y), size=(card_width, card_height), 
                     stroke=COLORS['extra_light_gray'], stroke_width=1, rx=8, fill='none'))
    
    # Title
    dwg.add(dwg.text(title, insert=(x + 20, y + 30),
                    fill=COLORS['medium_gray'], font_size=14, font_family='Arial'))
    
    # Status indicator
    dwg.add(dwg.circle(center=(x + 28, y + 60), r=8, fill=status_color))
    dwg.add(dwg.text(status, insert=(x + 48, y + 66),
                    fill=COLORS['black'], font_size=20, font_weight='bold', font_family='Arial'))
    
    # Details
    for i, detail in enumerate(details):
        dwg.add(dwg.text(detail, insert=(x + 20, y + 100 + i * 24),
                        fill=COLORS['dark_gray'], font_size=14, font_family='Arial'))
    
    return card_width

def draw_stats_card(dwg, x, y, title, value, trend, trend_up):
    """Draw a statistics card"""
    card_width = 220
    card_height = 140
    
    # Card background
    dwg.add(dwg.rect(insert=(x, y), size=(card_width, card_height), 
                     fill=COLORS['surface'], rx=8))
    dwg.add(dwg.rect(insert=(x, y), size=(card_width, card_height), 
                     stroke=COLORS['extra_light_gray'], stroke_width=1, rx=8, fill='none'))
    
    # Title with icon
    dwg.add(dwg.text(f'📊 {title}', insert=(x + 20, y + 30),
                    fill=COLORS['medium_gray'], font_size=14, font_family='Arial'))
    
    # Value
    dwg.add(dwg.text(value, insert=(x + 20, y + 75),
                    fill=COLORS['black'], font_size=32, font_weight='bold', font_family='Arial'))
    
    # Trend
    trend_color = COLORS['success'] if trend_up else COLORS['error']
    trend_icon = '↑' if trend_up else '↓'
    dwg.add(dwg.text(f'{trend_icon} {trend}', insert=(x + 20, y + 105),
                    fill=trend_color, font_size=14, font_family='Arial'))
    
    return card_width

def draw_packet_list(dwg, x, y, width, height):
    """Draw packet list table"""
    # Header
    headers = ['方法', 'URL', '状态', '时间', '大小']
    header_colors = ['#61AFD6', COLORS['dark_gray'], '#98C379', COLORS['medium_gray'], COLORS['medium_gray']]
    
    dwg.add(dwg.rect(insert=(x, y), size=(width, 48), fill=COLORS['background']))
    
    col_widths = [80, 400, 80, 100, 100]
    current_x = x + 20
    for i, (header, color) in enumerate(zip(headers, header_colors)):
        dwg.add(dwg.text(header, insert=(current_x, y + 30),
                        fill=color, font_size=13, font_weight='bold', font_family='Arial'))
        current_x += col_widths[i] + 20
    
    # Sample rows
    packets = [
        ('GET', 'https://api.example.com/users', '200', '45ms', '1.2KB'),
        ('POST', 'https://api.example.com/login', '401', '32ms', '256B'),
        ('GET', 'https://cdn.example.com/app.js', '200', '12ms', '45KB'),
        ('WS', 'wss://realtime.example.com/ws', '101', '-', '-'),
        ('GET', 'https://api.example.com/products', '200', '67ms', '8.4KB'),
    ]
    
    method_colors = {
        'GET': '#61AFD6',
        'POST': '#98C379',
        'PUT': '#E5C07B',
        'DELETE': '#E06C75',
        'WS': '#C678DD',
    }
    
    for i, packet in enumerate(packets):
        row_y = y + 56 + i * 56
        
        # Row background (hover effect for first row)
        if i == 0:
            dwg.add(dwg.rect(insert=(x, row_y), size=(width, 56), fill='#FAFAFA'))
        
        current_x = x + 20
        for j, (value, col_width) in enumerate(zip(packet, col_widths)):
            if j == 0:  # Method
                color = method_colors.get(value, COLORS['dark_gray'])
                dwg.add(dwg.rect(insert=(current_x, row_y + 14), size=(60, 28), 
                               fill=color, rx=4))
                dwg.add(dwg.text(value, insert=(current_x + 30, row_y + 34),
                               fill=COLORS['white'], font_size=12, font_weight='bold',
                               text_anchor='middle', font_family='Arial'))
            elif j == 2:  # Status
                color = COLORS['success'] if value == '200' else COLORS['warning'] if value == '401' else COLORS['error']
                dwg.add(dwg.text(value, insert=(current_x, row_y + 34),
                               fill=color, font_size=14, font_weight='bold', font_family='Arial'))
            else:
                dwg.add(dwg.text(value, insert=(current_x, row_y + 34),
                               fill=COLORS['dark_gray'], font_size=14, font_family='Arial'))
            current_x += col_widths[j] + 20
    
    # Bottom border
    dwg.add(dwg.line(start=(x, y + 56 + len(packets) * 56), 
                     end=(x + width, y + 56 + len(packets) * 56),
                     stroke=COLORS['extra_light_gray'], stroke_width=1))

def draw_request_detail(dwg, x, y, width, height):
    """Draw request detail view"""
    # Top info bar
    dwg.add(dwg.rect(insert=(x, y), size=(width, 80), fill=COLORS['surface']))
    dwg.add(dwg.rect(insert=(x, y), size=(width, 80), 
                     stroke=COLORS['extra_light_gray'], stroke_width=1))
    
    # URL
    dwg.add(dwg.text('URL:', insert=(x + 20, y + 25),
                    fill=COLORS['medium_gray'], font_size=13, font_family='Arial'))
    dwg.add(dwg.text('https://api.example.com/users/123', insert=(x + 20, y + 50),
                    fill=COLORS['dark_gray'], font_size=14, font_family='Arial'))
    
    # Method badge
    dwg.add(dwg.rect(insert=(x + width - 150, y + 20), size=(70, 32), 
                     fill='#61AFD6', rx=4))
    dwg.add(dwg.text('GET', insert=(x + width - 115, y + 42),
                    fill=COLORS['white'], font_size=14, font_weight='bold',
                    text_anchor='middle', font_family='Arial'))
    
    # Status badge
    dwg.add(dwg.rect(insert=(x + width - 70, y + 20), size=(50, 32), 
                     fill=COLORS['success'], rx=4))
    dwg.add(dwg.text('200', insert=(x + width - 45, y + 42),
                    fill=COLORS['white'], font_size=14, font_weight='bold',
                    text_anchor='middle', font_family='Arial'))
    
    # Tabs
    tab_y = y + 80
    tabs = ['概览', '请求', '响应', 'Cookie', '时间线']
    tab_width = width / len(tabs)
    
    for i, tab in enumerate(tabs):
        tab_x = x + i * tab_width
        if i == 1:  # Active tab
            dwg.add(dwg.rect(insert=(tab_x, tab_y), size=(tab_width, 48), fill=COLORS['surface']))
            dwg.add(dwg.rect(insert=(tab_x, tab_y + 46), size=(tab_width, 2), fill=COLORS['primary']))
            fill = COLORS['primary']
        else:
            fill = COLORS['medium_gray']
        
        dwg.add(dwg.text(tab, insert=(tab_x + tab_width/2, tab_y + 30),
                        fill=fill, font_size=14, font_family='Arial',
                        text_anchor='middle'))
    
    # Content area (Headers)
    content_y = tab_y + 48
    dwg.add(dwg.rect(insert=(x, content_y), size=(width, height - content_y + y), 
                     fill=COLORS['surface']))
    dwg.add(dwg.rect(insert=(x, content_y), size=(width, height - content_y + y), 
                     stroke=COLORS['extra_light_gray'], stroke_width=1))
    
    # Request headers
    dwg.add(dwg.text('Request Headers', insert=(x + 20, content_y + 35),
                    fill=COLORS['black'], font_size=14, font_weight='bold', font_family='Arial'))
    
    headers = [
        ('Host:', 'api.example.com'),
        ('User-Agent:', 'SpiderProxy/1.0'),
        ('Accept:', 'application/json'),
        ('Authorization:', 'Bearer eyJhbGc...'),
    ]
    
    for i, (key, value) in enumerate(headers):
        header_y = content_y + 60 + i * 28
        dwg.add(dwg.text(key, insert=(x + 20, header_y + 18),
                        fill=COLORS['medium_gray'], font_size=13, font_family='Arial'))
        dwg.add(dwg.text(value, insert=(x + 150, header_y + 18),
                        fill=COLORS['dark_gray'], font_size=13, font_family='Arial'))

def draw_filter_card(dwg, x, y, title, conditions):
    """Draw filter configuration card"""
    card_width = 400
    card_height = 200
    
    # Card
    dwg.add(dwg.rect(insert=(x, y), size=(card_width, card_height), 
                     fill=COLORS['surface'], rx=8))
    dwg.add(dwg.rect(insert=(x, y), size=(card_width, card_height), 
                     stroke=COLORS['extra_light_gray'], stroke_width=1, rx=8, fill='none'))
    
    # Title
    dwg.add(dwg.text(title, insert=(x + 20, y + 35),
                    fill=COLORS['black'], font_size=16, font_weight='bold', font_family='Arial'))
    
    # Conditions
    for i, condition in enumerate(conditions):
        cond_y = y + 70 + i * 40
        dwg.add(dwg.text(condition['label'], insert=(x + 20, cond_y + 18),
                        fill=COLORS['medium_gray'], font_size=13, font_family='Arial'))
        
        # Input field
        dwg.add(dwg.rect(insert=(x + 120, cond_y + 4), size=(260, 32), 
                         fill=COLORS['background'], stroke=COLORS['extra_light_gray'], 
                         stroke_width=1, rx=4))
        dwg.add(dwg.text(condition['value'], insert=(x + 130, cond_y + 26),
                        fill=COLORS['dark_gray'], font_size=14, font_family='Arial'))

def draw_script_editor(dwg, x, y, width, height):
    """Draw script editor view"""
    # Sidebar (script list)
    sidebar_width = 200
    dwg.add(dwg.rect(insert=(x, y), size=(sidebar_width, height), 
                     fill=COLORS['background']))
    dwg.add(dwg.rect(insert=(x + sidebar_width, y), size=(2, height), 
                     fill=COLORS['extra_light_gray']))
    
    # Script items
    scripts = ['request-filter.js', 'response-modify.js', 'auth-inject.js']
    for i, script in enumerate(scripts):
        item_y = y + 20 + i * 48
        if i == 0:
            dwg.add(dwg.rect(insert=(x + 10, item_y), size=(sidebar_width - 20, 40), 
                           fill=COLORS['surface'], rx=4))
            fill = COLORS['primary']
        else:
            fill = COLORS['dark_gray']
        
        dwg.add(dwg.text(f'📜 {script}', insert=(x + 24, item_y + 26),
                        fill=fill, font_size=13, font_family='Arial'))
    
    # Code editor area
    editor_x = x + sidebar_width
    dwg.add(dwg.rect(insert=(editor_x, y), size=(width - sidebar_width, height), 
                     fill='#1E1E1E'))
    
    # Line numbers
    for i in range(1, 11):
        line_y = y + 30 + i * 24
        dwg.add(dwg.text(str(i), insert=(editor_x + 15, line_y + 8),
                        fill='#666666', font_size=13, font_family='Courier'))
    
    # Code content (syntax highlighted)
    code_lines = [
        ('// Spider Proxy Script', '#666666'),
        ('function onRequest(request) {', '#C678DD'),
        ('  if (request.url.includes("api")) {', '#E06C75'),
        ('    request.headers["X-Custom"] = "value";', '#98C379'),
        ('  }', '#E06C75'),
        ('  return request;', '#61AFD6'),
        ('}', '#C678DD'),
        ('', ''),
        ('function onResponse(response) {', '#C678DD'),
        ('  return response;', '#61AFD6'),
    ]
    
    for i, (code, color) in enumerate(code_lines):
        line_y = y + 30 + i * 24
        dwg.add(dwg.text(code, insert=(editor_x + 50, line_y + 8),
                        fill=color if color else '#D4D4D4', 
                        font_size=13, font_family='Courier'))
    
    # Run button
    dwg.add(dwg.rect(insert=(editor_x + width - sidebar_width - 120, y + height - 50), 
                     size=(100, 36), fill=COLORS['success'], rx=6))
    dwg.add(dwg.text('▶ 运行', insert=(editor_x + width - sidebar_width - 70, y + height - 26),
                    fill=COLORS['white'], font_size=14, font_weight='bold', 
                    text_anchor='middle', font_family='Arial'))

def draw_settings_group(dwg, x, y, title, items):
    """Draw settings group"""
    group_width = 500
    
    # Title
    dwg.add(dwg.text(title, insert=(x, y + 20),
                    fill=COLORS['medium_gray'], font_size=14, font_family='Arial'))
    
    # Items
    for i, item in enumerate(items):
        item_y = y + 40 + i * 56
        
        dwg.add(dwg.rect(insert=(x, item_y), size=(group_width, 56), 
                         fill=COLORS['surface']))
        dwg.add(dwg.line(start=(x, item_y + 56), end=(x + group_width, item_y + 56),
                        stroke=COLORS['extra_light_gray'], stroke_width=1))
        
        # Label
        dwg.add(dwg.text(item['label'], insert=(x + 20, item_y + 34),
                        fill=COLORS['dark_gray'], font_size=14, font_family='Arial'))
        
        # Control
        if item['type'] == 'switch':
            # Switch
            switch_x = x + group_width - 60
            bg_color = COLORS['success'] if item.get('value', False) else COLORS['extra_light_gray']
            dwg.add(dwg.rect(insert=(switch_x, item_y + 16), size=(44, 24), 
                           fill=bg_color, rx=12))
            circle_x = switch_x + 20 if item.get('value', False) else switch_x + 4
            dwg.add(dwg.circle(center=(circle_x, item_y + 28), r=10, fill=COLORS['white']))
        elif item['type'] == 'select':
            # Select
            select_x = x + group_width - 150
            dwg.add(dwg.rect(insert=(select_x, item_y + 12), size=(130, 32), 
                           fill=COLORS['background'], stroke=COLORS['extra_light_gray'], 
                           stroke_width=1, rx=4))
            dwg.add(dwg.text(item['value'], insert=(select_x + 12, item_y + 34),
                           fill=COLORS['dark_gray'], font_size=14, font_family='Arial'))
            dwg.add(dwg.text('▼', insert=(select_x + 105, item_y + 34),
                           fill=COLORS['medium_gray'], font_size=12, font_family='Arial'))

def generate_dashboard(filename):
    """Generate Dashboard page"""
    dwg = create_base_drawing(filename)
    
    # Top bar
    draw_topbar(dwg)
    
    # Sidebar
    draw_sidebar(dwg, active_index=0)
    
    # Main content
    content_x = SIDEBAR_WIDTH + 40
    content_y = TOPBAR_HEIGHT + 32
    
    # Page title
    dwg.add(dwg.text('仪表盘', insert=(content_x, content_y + 30),
                    fill=COLORS['black'], font_size=28, font_weight='bold', font_family='Arial'))
    
    # Status card
    draw_status_card(dwg, content_x, content_y + 60, '抓包状态', '运行中', 
                    COLORS['success'], ['已运行：2 小时 15 分', '抓包数量：1,234'])
    
    # Stats cards
    draw_stats_card(dwg, content_x + 320, content_y + 60, '今日流量', '1.2 GB', '15%', True)
    draw_stats_card(dwg, content_x + 580, content_y + 60, '请求总数', '12,345', '8%', True)
    draw_stats_card(dwg, content_x + 840, content_y + 60, '平均响应', '45ms', '3%', False)
    
    # Control buttons
    btn_y = content_y + 260
    dwg.add(dwg.rect(insert=(content_x, btn_y), size=(140, 48), 
                     fill=COLORS['primary'], rx=6))
    dwg.add(dwg.text('▶ 开始抓包', insert=(content_x + 70, btn_y + 30),
                    fill=COLORS['white'], font_size=16, font_weight='bold',
                    text_anchor='middle', font_family='Arial'))
    
    dwg.add(dwg.rect(insert=(content_x + 160, btn_y), size=(140, 48), 
                     fill='none', stroke=COLORS['primary'], stroke_width=2, rx=6))
    dwg.add(dwg.text('⏸ 暂停', insert=(content_x + 230, btn_y + 30),
                    fill=COLORS['primary'], font_size=16, font_weight='bold',
                    text_anchor='middle', font_family='Arial'))
    
    dwg.add(dwg.rect(insert=(content_x + 320, btn_y), size=(140, 48), 
                     fill=COLORS['error'], rx=6))
    dwg.add(dwg.text('⏹ 停止', insert=(content_x + 390, btn_y + 30),
                    fill=COLORS['white'], font_size=16, font_weight='bold',
                    text_anchor='middle', font_family='Arial'))
    
    # Recent packets section
    dwg.add(dwg.text('最近抓包记录', insert=(content_x, btn_y + 100),
                    fill=COLORS['black'], font_size=20, font_weight='bold', font_family='Arial'))
    
    draw_packet_list(dwg, content_x, btn_y + 140, CANVAS_WIDTH - content_x - 80, 350)
    
    dwg.save()
    print(f'Generated: {filename}')

def generate_packet_list(filename):
    """Generate Packet List page"""
    dwg = create_base_drawing(filename)
    
    # Top bar
    draw_topbar(dwg)
    
    # Sidebar
    draw_sidebar(dwg, active_index=1)
    
    # Main content
    content_x = SIDEBAR_WIDTH + 40
    content_y = TOPBAR_HEIGHT + 32
    
    # Page title
    dwg.add(dwg.text('抓包列表', insert=(content_x, content_y + 30),
                    fill=COLORS['black'], font_size=28, font_weight='bold', font_family='Arial'))
    
    # Filter chips
    chip_y = content_y + 60
    chips = ['全部', 'HTTP', 'HTTPS', 'WS']
    for i, chip in enumerate(chips):
        chip_x = content_x + i * 100
        bg = COLORS['primary'] if i == 0 else COLORS['extra_light_gray']
        text = COLORS['white'] if i == 0 else COLORS['dark_gray']
        
        dwg.add(dwg.rect(insert=(chip_x, chip_y), size=(80, 32), fill=bg, rx=16))
        dwg.add(dwg.text(f'{"× " if i == 0 else ""}{chip}', insert=(chip_x + 40, chip_y + 22),
                        fill=text, font_size=14, text_anchor='middle', font_family='Arial'))
    
    # Packet list
    draw_packet_list(dwg, content_x, chip_y + 60, CANVAS_WIDTH - content_x - 80, 500)
    
    # Pagination
    page_y = chip_y + 60 + 500 + 30
    dwg.add(dwg.text('共 1,234 条记录', insert=(content_x, page_y + 18),
                    fill=COLORS['medium_gray'], font_size=14, font_family='Arial'))
    
    # Page numbers
    pages = ['<', '1', '2', '3', '...', '50', '>']
    page_x = CANVAS_WIDTH - 300
    for i, page in enumerate(pages):
        px = page_x + i * 40
        if page == '2':
            dwg.add(dwg.circle(center=(px + 16, page_y + 18), r=16, fill=COLORS['primary']))
            dwg.add(dwg.text(page, insert=(px + 16, page_y + 23),
                           fill=COLORS['white'], font_size=14, text_anchor='middle', font_family='Arial'))
        else:
            dwg.add(dwg.text(page, insert=(px + 16, page_y + 23),
                           fill=COLORS['dark_gray'], font_size=14, text_anchor='middle', font_family='Arial'))
    
    dwg.save()
    print(f'Generated: {filename}')

def generate_request_detail(filename):
    """Generate Request Detail page"""
    dwg = create_base_drawing(filename)
    
    # Top bar
    draw_topbar(dwg)
    
    # Sidebar
    draw_sidebar(dwg, active_index=1)
    
    # Main content
    content_x = SIDEBAR_WIDTH + 40
    content_y = TOPBAR_HEIGHT + 32
    
    # Draw request detail view
    draw_request_detail(dwg, content_x, content_y + 20, CANVAS_WIDTH - content_x - 80, 600)
    
    # Action buttons
    btn_y = content_y + 650
    buttons = [
        ('📋 复制', COLORS['primary']),
        ('🔄 重放', COLORS['success']),
        ('📤 导出', COLORS['info']),
    ]
    
    for i, (text, color) in enumerate(buttons):
        btn_x = content_x + i * 140
        dwg.add(dwg.rect(insert=(btn_x, btn_y), size=(120, 40), fill=color, rx=6))
        dwg.add(dwg.text(text, insert=(btn_x + 60, btn_y + 26),
                        fill=COLORS['white'], font_size=14, font_weight='bold',
                        text_anchor='middle', font_family='Arial'))
    
    dwg.save()
    print(f'Generated: {filename}')

def generate_filter_manager(filename):
    """Generate Filter Manager page"""
    dwg = create_base_drawing(filename)
    
    # Top bar
    draw_topbar(dwg)
    
    # Sidebar
    draw_sidebar(dwg, active_index=2)
    
    # Main content
    content_x = SIDEBAR_WIDTH + 40
    content_y = TOPBAR_HEIGHT + 32
    
    # Page title
    dwg.add(dwg.text('过滤器管理', insert=(content_x, content_y + 30),
                    fill=COLORS['black'], font_size=28, font_weight='bold', font_family='Arial'))
    
    # New filter button
    dwg.add(dwg.rect(insert=(CANVAS_WIDTH - 200, content_y + 10), size=(160, 44), 
                     fill=COLORS['primary'], rx=6))
    dwg.add(dwg.text('+ 新建过滤器', insert=(CANVAS_WIDTH - 120, content_y + 38),
                    fill=COLORS['white'], font_size=16, font_weight='bold',
                    text_anchor='middle', font_family='Arial'))
    
    # Preset filters
    preset_y = content_y + 80
    presets = [
        ('🔍 API 请求', '域名：api.* | 方法：GET,POST'),
        ('📸 图片资源', '内容类型：image/*'),
        ('🔐 认证请求', '路径：/login,/auth'),
        ('⚡ 慢请求', '响应时间：>1000ms'),
    ]
    
    for i, (title, desc) in enumerate(presets):
        card_y = preset_y + i * 100
        dwg.add(dwg.rect(insert=(content_x, card_y), size=(400, 80), 
                         fill=COLORS['surface'], rx=8))
        dwg.add(dwg.rect(insert=(content_x, card_y), size=(400, 80), 
                         stroke=COLORS['extra_light_gray'], stroke_width=1, rx=8, fill='none'))
        
        dwg.add(dwg.text(title, insert=(content_x + 20, card_y + 30),
                        fill=COLORS['black'], font_size=16, font_weight='bold', font_family='Arial'))
        dwg.add(dwg.text(desc, insert=(content_x + 20, card_y + 55),
                        fill=COLORS['medium_gray'], font_size=13, font_family='Arial'))
        
        # Edit/Delete buttons
        dwg.add(dwg.text('✏️', insert=(content_x + 340, card_y + 30),
                        font_size=18, font_family='Arial'))
        dwg.add(dwg.text('🗑️', insert=(content_x + 370, card_y + 30),
                        font_size=18, font_family='Arial'))
    
    # Filter configuration cards
    filter_y = content_y + 80
    filter_x = content_x + 440
    
    draw_filter_card(dwg, filter_x, filter_y, '过滤条件配置', [
        {'label': '域名匹配:', 'value': 'api.example.com'},
        {'label': 'HTTP 方法:', 'value': 'GET, POST'},
        {'label': '状态码:', 'value': '200, 201'},
    ])
    
    # Regex test tool
    regex_y = filter_y + 240
    dwg.add(dwg.rect(insert=(filter_x, regex_y), size=(400, 150), 
                     fill=COLORS['surface'], rx=8))
    dwg.add(dwg.rect(insert=(filter_x, regex_y), size=(400, 150), 
                     stroke=COLORS['extra_light_gray'], stroke_width=1, rx=8, fill='none'))
    
    dwg.add(dwg.text('正则表达式测试', insert=(filter_x + 20, regex_y + 35),
                    fill=COLORS['black'], font_size=16, font_weight='bold', font_family='Arial'))
    
    # Test input
    dwg.add(dwg.rect(insert=(filter_x + 20, regex_y + 55), size=(360, 36), 
                     fill=COLORS['background'], stroke=COLORS['extra_light_gray'], 
                     stroke_width=1, rx=4))
    dwg.add(dwg.text('Pattern: ^/api/v[0-9]+/.*', insert=(filter_x + 30, regex_y + 78),
                    fill=COLORS['dark_gray'], font_size=13, font_family='Courier'))
    
    # Test button
    dwg.add(dwg.rect(insert=(filter_x + 280, regex_y + 105), size=(100, 32), 
                     fill=COLORS['primary'], rx=4))
    dwg.add(dwg.text('测试', insert=(filter_x + 330, regex_y + 126),
                    fill=COLORS['white'], font_size=14, text_anchor='middle', font_family='Arial'))
    
    # Save/Delete buttons
    save_y = filter_y + 420
    dwg.add(dwg.rect(insert=(filter_x, save_y), size=(120, 44), 
                     fill=COLORS['primary'], rx=6))
    dwg.add(dwg.text('保存预设', insert=(filter_x + 60, save_y + 28),
                    fill=COLORS['white'], font_size=14, font_weight='bold',
                    text_anchor='middle', font_family='Arial'))
    
    dwg.add(dwg.rect(insert=(filter_x + 140, save_y), size=(120, 44), 
                     fill=COLORS['error'], rx=6))
    dwg.add(dwg.text('删除预设', insert=(filter_x + 200, save_y + 28),
                    fill=COLORS['white'], font_size=14, font_weight='bold',
                    text_anchor='middle', font_family='Arial'))
    
    dwg.save()
    print(f'Generated: {filename}')

def generate_script_editor(filename):
    """Generate Script Editor page"""
    dwg = create_base_drawing(filename)
    
    # Top bar
    draw_topbar(dwg)
    
    # Sidebar
    draw_sidebar(dwg, active_index=3)
    
    # Main content
    content_x = SIDEBAR_WIDTH + 40
    content_y = TOPBAR_HEIGHT + 32
    
    # Draw script editor
    draw_script_editor(dwg, content_x, content_y + 20, CANVAS_WIDTH - content_x - 80, 600)
    
    # Template selector
    template_y = content_y + 650
    dwg.add(dwg.text('模板选择:', insert=(content_x, template_y + 20),
                    fill=COLORS['medium_gray'], font_size=14, font_family='Arial'))
    
    templates = ['请求修改', '响应修改', '认证注入', '日志记录']
    for i, template in enumerate(templates):
        tpl_x = content_x + 100 + i * 140
        dwg.add(dwg.rect(insert=(tpl_x, template_y), size=(120, 40), 
                         fill=COLORS['surface'], stroke=COLORS['extra_light_gray'], 
                         stroke_width=1, rx=4))
        dwg.add(dwg.text(template, insert=(tpl_x + 60, template_y + 26),
                        fill=COLORS['dark_gray'], font_size=13, text_anchor='middle', 
                        font_family='Arial'))
    
    # Console output
    console_y = template_y + 70
    dwg.add(dwg.rect(insert=(content_x, console_y), size=(CANVAS_WIDTH - content_x - 80, 150), 
                     fill='#1E1E1E', rx=4))
    
    dwg.add(dwg.text('Console Output', insert=(content_x + 20, console_y + 30),
                    fill='#666666', font_size=13, font_family='Arial'))
    
    console_lines = [
        ('[INFO] Script loaded successfully', '#98C379'),
        ('[DEBUG] Processing request...', '#61AFD6'),
        ('[INFO] Request modified', '#98C379'),
    ]
    
    for i, (line, color) in enumerate(console_lines):
        line_y = console_y + 55 + i * 28
        dwg.add(dwg.text(line, insert=(content_x + 20, line_y + 8),
                        fill=color, font_size=13, font_family='Courier'))
    
    dwg.save()
    print(f'Generated: {filename}')

def generate_settings(filename):
    """Generate Settings page"""
    dwg = create_base_drawing(filename)
    
    # Top bar
    draw_topbar(dwg)
    
    # Sidebar
    draw_sidebar(dwg, active_index=4)
    
    # Main content
    content_x = SIDEBAR_WIDTH + 40
    content_y = TOPBAR_HEIGHT + 32
    
    # Page title
    dwg.add(dwg.text('设置', insert=(content_x, content_y + 30),
                    fill=COLORS['black'], font_size=28, font_weight='bold', font_family='Arial'))
    
    # Settings groups
    group_y = content_y + 80
    
    draw_settings_group(dwg, content_x, group_y, '抓包设置', [
        {'label': '启用 HTTPS 解密', 'type': 'switch', 'value': True},
        {'label': '自动开始抓包', 'type': 'switch', 'value': False},
        {'label': '最大抓包数量', 'type': 'select', 'value': '10,000'},
    ])
    
    draw_settings_group(dwg, content_x, group_y + 220, '证书管理', [
        {'label': '证书状态', 'type': 'select', 'value': '已安装'},
        {'label': '证书有效期', 'type': 'select', 'value': '365 天'},
    ])
    
    # Certificate status card
    cert_x = content_x + 540
    cert_y = group_y + 220
    dwg.add(dwg.rect(insert=(cert_x, cert_y), size=(350, 120), 
                     fill=COLORS['surface'], rx=8))
    dwg.add(dwg.rect(insert=(cert_x, cert_y), size=(350, 120), 
                     stroke=COLORS['extra_light_gray'], stroke_width=1, rx=8, fill='none'))
    
    dwg.add(dwg.text('📜 SSL 证书', insert=(cert_x + 20, cert_y + 35),
                    fill=COLORS['black'], font_size=16, font_weight='bold', font_family='Arial'))
    dwg.add(dwg.text('状态：已安装并信任', insert=(cert_x + 20, cert_y + 65),
                    fill=COLORS['success'], font_size=14, font_family='Arial'))
    dwg.add(dwg.text('有效期至：2027-03-24', insert=(cert_x + 20, cert_y + 90),
                    fill=COLORS['medium_gray'], font_size=13, font_family='Arial'))
    
    # Certificate buttons
    dwg.add(dwg.text('👁️ 查看', insert=(cert_x + 200, cert_y + 90),
                    fill=COLORS['primary'], font_size=13, font_family='Arial'))
    dwg.add(dwg.text('🗑️ 删除', insert=(cert_x + 280, cert_y + 90),
                    fill=COLORS['error'], font_size=13, font_family='Arial'))
    
    draw_settings_group(dwg, content_x, group_y + 380, '显示设置', [
        {'label': '主题', 'type': 'select', 'value': '跟随系统'},
        {'label': '字体大小', 'type': 'select', 'value': '标准'},
        {'label': '紧凑模式', 'type': 'switch', 'value': False},
    ])
    
    draw_settings_group(dwg, content_x, group_y + 600, '存储设置', [
        {'label': '存储位置', 'type': 'select', 'value': '~/Documents/SpiderProxy'},
        {'label': '自动清理', 'type': 'switch', 'value': True},
        {'label': '保留天数', 'type': 'select', 'value': '30 天'},
    ])
    
    # About section
    about_y = group_y + 820
    dwg.add(dwg.text('关于', insert=(content_x, about_y + 20),
                    fill=COLORS['medium_gray'], font_size=14, font_family='Arial'))
    
    dwg.add(dwg.rect(insert=(content_x, about_y + 40), size=(500, 80), 
                     fill=COLORS['surface'], rx=8))
    dwg.add(dwg.rect(insert=(content_x, about_y + 40), size=(500, 80), 
                     stroke=COLORS['extra_light_gray'], stroke_width=1, rx=8, fill='none'))
    
    dwg.add(dwg.text('Spider Proxy v1.0.0', insert=(content_x + 20, about_y + 70),
                    fill=COLORS['black'], font_size=16, font_weight='bold', font_family='Arial'))
    dwg.add(dwg.text('© 2026 Spider Proxy Team. Built with ❤️', insert=(content_x + 20, about_y + 95),
                    fill=COLORS['medium_gray'], font_size=13, font_family='Arial'))
    
    dwg.save()
    print(f'Generated: {filename}')

def generate_png(svg_path, png_path, scale=2):
    """Convert SVG to PNG using PIL (if available)"""
    try:
        import cairosvg
        
        # Convert SVG to PNG
        cairosvg.svg2png(url=svg_path, write_to=png_path, scale=scale)
        print(f'Generated PNG ({scale}x): {png_path}')
        return True
    except Exception as e:
        print(f'Skip PNG generation (cairo library not available): {png_path}')
        print(f'  Error: {str(e)[:100]}...')
        return False

def main():
    """Generate all design mockups"""
    output_dir = os.path.dirname(os.path.abspath(__file__))
    ui_dir = os.path.join(output_dir, 'UI 设计稿')
    
    os.makedirs(ui_dir, exist_ok=True)
    
    pages = [
        ('dashboard', '仪表盘', generate_dashboard),
        ('packet-list', '抓包列表', generate_packet_list),
        ('request-detail', '请求详情', generate_request_detail),
        ('filter-manager', '过滤器管理', generate_filter_manager),
        ('script-editor', '脚本编辑', generate_script_editor),
        ('settings', '设置', generate_settings),
    ]
    
    print('=' * 60)
    print('Spider Proxy UI Design Generator')
    print('=' * 60)
    print(f'Output directory: {ui_dir}')
    print()
    
    for filename, name, generator in pages:
        print(f'Generating {name}...')
        svg_path = os.path.join(ui_dir, f'{filename}.svg')
        generator(svg_path)
        
        # Generate PNG versions (@2x and @3x)
        generate_png(svg_path, os.path.join(ui_dir, f'{filename}@2x.png'), scale=2)
        generate_png(svg_path, os.path.join(ui_dir, f'{filename}@3x.png'), scale=3)
    
    print()
    print('=' * 60)
    print('Design generation complete!')
    print('=' * 60)
    print(f'\nOutput files in: {ui_dir}')
    print('\nGenerated files:')
    for filename, name, _ in pages:
        print(f'  - {filename}.svg (矢量设计稿)')
        print(f'  - {filename}@2x.png (Retina 显示)')
        print(f'  - {filename}@3x.png (高清显示)')

if __name__ == '__main__':
    main()