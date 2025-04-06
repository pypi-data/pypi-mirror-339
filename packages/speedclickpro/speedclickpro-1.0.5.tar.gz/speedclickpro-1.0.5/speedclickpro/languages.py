"""
Language module for SpeedClick Pro
Provides translations for the application UI
"""

# Available languages
LANGUAGES = {
    "th": "ไทย",
    "en": "English",
    "zh": "中文",
    "ja": "日本語",
    "ko": "한국어"
}

# Default language
DEFAULT_LANGUAGE = "th"

# Translations dictionary
TRANSLATIONS = {
    # Thai translations (default)
    "th": {
        # Program info
        "program_name": "SpeedClick Pro",
        "program_subtitle": "โปรแกรมคลิกอัตโนมัติ",
        "version": "เวอร์ชัน",
        "copyright": "© 2025 Professional Edition",
        
        # Header
        "mode_super_fast": "โหมด Super Fast",
        
        # Position panel
        "positions_frame": " ตำแหน่งที่จะคลิกและเวลา ",
        "positions_count": "{} ตำแหน่ง",
        "add_position": "เพิ่มตำแหน่ง",
        "clear_positions": "ล้างตำแหน่งทั้งหมด",
        "column_number": "ลำดับ",
        "column_x": "พิกัด X",
        "column_y": "พิกัด Y",
        "column_duration": "เวลา(วินาที)",
        "delete_position": "ลบตำแหน่งนี้",
        "edit_position": "แก้ไขตำแหน่ง",
        "edit_duration": "แก้ไขเวลา",
        "confirm_edit": "ต้องการเปลี่ยนตำแหน่งใหม่?",
        "enter_duration": "กำหนดเวลาคลิก (วินาที):",
        "sequence_mode": "โหมดลำดับอนิเมชั่น",
        "repeat_mode": "ทำซ้ำแบบอนิเมชั่น",
        
        # Stats panel
        "stats_frame": " สถิติ ",
        "click_count": "จำนวนคลิก:",
        "runtime": "เวลาทำงาน:",
        "last_started": "เริ่มล่าสุด:",
        "last_stopped": "หยุดล่าสุด:",
        
        # Control panel
        "control_frame": " ควบคุมการทำงาน ",
        "start_clicking": "เริ่มคลิก",
        "stop_clicking": "หยุดคลิก",
        "shortcut_info": "ปุ่มลัด: Ctrl+G (เริ่ม/หยุด)",
        
        # Settings panel
        "settings_frame": " ตั้งค่า ",
        "always_on_top": "แสดงหน้าต่างบนสุดเสมอ",
        "mini_mode": "โหมดย่อ (แสดงเฉพาะปุ่มควบคุม)",
        "language": "ภาษา:",
        
        # Profiles panel
        "profiles_frame": " โปรไฟล์ ",
        "profile": "โปรไฟล์:",
        "save_profile": "บันทึกโปรไฟล์",
        "load_profile": "โหลดโปรไฟล์",
        "profile_name_prompt": "ชื่อโปรไฟล์:",
        
        # Messages
        "ready": "พร้อมใช้งาน | กด Ctrl+G เพื่อเริ่ม/หยุดการคลิก",
        "position_added": "เพิ่มตำแหน่ง ({}, {}) แล้ว",
        "all_positions_cleared": "ล้างตำแหน่งทั้งหมดแล้ว",
        "position_deleted": "ลบตำแหน่งที่ {} แล้ว",
        "position_edited": "แก้ไขตำแหน่งที่ {} เป็น ({}, {}) แล้ว",
        "profile_saved": "บันทึกโปรไฟล์ '{}' แล้ว",
        "profile_loaded": "โหลดโปรไฟล์ '{}' แล้ว",
        "working": "กำลังทำงาน... กด Ctrl+G เพื่อหยุด",
        "stopped": "หยุดคลิกแล้ว | กด Ctrl+G เพื่อเริ่มคลิกใหม่อีกครั้ง",
        "warning": "คำเตือน",
        "error": "ข้อผิดพลาด",
        "add_position_first": "กรุณาเพิ่มตำแหน่งก่อนเริ่มคลิก",
        "profile_save_error": "ไม่สามารถบันทึกโปรไฟล์: {}",
        "profile_not_found": "ไม่พบโปรไฟล์ '{}'",
    },
    
    # English translations
    "en": {
        # Program info
        "program_name": "SpeedClick Pro",
        "program_subtitle": "Automatic Clicking Program",
        "version": "Version",
        "copyright": "© 2025 Professional Edition",
        
        # Header
        "mode_super_fast": "Super Fast Mode",
        
        # Position panel
        "positions_frame": " Click Positions & Timing ",
        "positions_count": "{} positions",
        "add_position": "Add Position",
        "clear_positions": "Clear All",
        "column_number": "No.",
        "column_x": "X",
        "column_y": "Y",
        "column_duration": "Duration(s)",
        "delete_position": "Delete Position",
        "edit_position": "Edit Position",
        "edit_duration": "Edit Duration",
        "confirm_edit": "Change to new position?",
        "enter_duration": "Enter click duration (seconds):",
        "sequence_mode": "Animation Sequence Mode",
        "repeat_mode": "Animation Repeat",
        
        # Stats panel
        "stats_frame": " Statistics ",
        "click_count": "Click count:",
        "runtime": "Runtime:",
        "last_started": "Started:",
        "last_stopped": "Stopped:",
        
        # Control panel
        "control_frame": " Controls ",
        "start_clicking": "Start",
        "stop_clicking": "Stop",
        "shortcut_info": "Shortcut: Ctrl+G (Start/Stop)",
        
        # Settings panel
        "settings_frame": " Settings ",
        "always_on_top": "Always on top",
        "mini_mode": "Mini mode (controls only)",
        "language": "Language:",
        
        # Profiles panel
        "profiles_frame": " Profiles ",
        "profile": "Profile:",
        "save_profile": "Save Profile",
        "load_profile": "Load Profile",
        "profile_name_prompt": "Profile name:",
        
        # Messages
        "ready": "Ready | Press Ctrl+G to start/stop clicking",
        "position_added": "Added position ({}, {})",
        "all_positions_cleared": "All positions cleared",
        "position_deleted": "Deleted position {}",
        "position_edited": "Edited position {} to ({}, {})",
        "profile_saved": "Profile '{}' saved",
        "profile_loaded": "Profile '{}' loaded",
        "working": "Working... Press Ctrl+G to stop",
        "stopped": "Stopped | Press Ctrl+G to start again",
        "warning": "Warning",
        "error": "Error",
        "add_position_first": "Please add positions before starting",
        "profile_save_error": "Could not save profile: {}",
        "profile_not_found": "Profile '{}' not found",
    },
    
    # Chinese translations
    "zh": {
        # Program info
        "program_name": "SpeedClick Pro",
        "program_subtitle": "自动点击程序",
        "version": "版本",
        "copyright": "© 2025 专业版",
        
        # Header
        "mode_super_fast": "超快速模式",
        
        # Position panel
        "positions_frame": " 点击位置和时间 ",
        "positions_count": "{} 位置",
        "add_position": "添加位置",
        "clear_positions": "清除全部",
        "column_number": "序号",
        "column_x": "X坐标",
        "column_y": "Y坐标",
        "column_duration": "时长(秒)",
        "delete_position": "删除位置",
        "edit_position": "编辑位置",
        "edit_duration": "编辑时长",
        "confirm_edit": "更改到新位置?",
        "enter_duration": "输入点击时长(秒):",
        "sequence_mode": "动画序列模式",
        "repeat_mode": "动画重复",
        
        # Stats panel
        "stats_frame": " 统计 ",
        "click_count": "点击次数:",
        "runtime": "运行时间:",
        "last_started": "开始时间:",
        "last_stopped": "停止时间:",
        
        # Control panel
        "control_frame": " 控制 ",
        "start_clicking": "开始",
        "stop_clicking": "停止",
        "shortcut_info": "快捷键: Ctrl+G (开始/停止)",
        
        # Settings panel
        "settings_frame": " 设置 ",
        "always_on_top": "窗口总在最前",
        "mini_mode": "迷你模式 (仅控制按钮)",
        "language": "语言:",
        
        # Profiles panel
        "profiles_frame": " 配置文件 ",
        "profile": "配置:",
        "save_profile": "保存配置",
        "load_profile": "加载配置",
        "profile_name_prompt": "配置名称:",
        
        # Messages
        "ready": "就绪 | 按Ctrl+G开始/停止点击",
        "position_added": "已添加位置 ({}, {})",
        "all_positions_cleared": "已清除所有位置",
        "position_deleted": "已删除位置 {}",
        "position_edited": "已编辑位置 {} 为 ({}, {})",
        "profile_saved": "配置 '{}' 已保存",
        "profile_loaded": "配置 '{}' 已加载",
        "working": "运行中... 按Ctrl+G停止",
        "stopped": "已停止 | 按Ctrl+G重新开始",
        "warning": "警告",
        "error": "错误",
        "add_position_first": "请先添加点击位置",
        "profile_save_error": "无法保存配置: {}",
        "profile_not_found": "找不到配置 '{}'",
    },
    
    # Japanese translations
    "ja": {
        # Program info
        "program_name": "SpeedClick Pro",
        "program_subtitle": "自動クリックプログラム",
        "version": "バージョン",
        "copyright": "© 2025 プロフェッショナル版",
        
        # Header
        "mode_super_fast": "超高速モード",
        
        # Position panel
        "positions_frame": " クリック位置と時間 ",
        "positions_count": "{}箇所",
        "add_position": "位置追加",
        "clear_positions": "全て消去",
        "column_number": "番号",
        "column_x": "X座標",
        "column_y": "Y座標",
        "column_duration": "期間(秒)",
        "delete_position": "位置削除",
        "edit_position": "位置編集",
        "edit_duration": "時間編集",
        "confirm_edit": "新しい位置に変更しますか?",
        "enter_duration": "クリック時間を入力(秒):",
        "sequence_mode": "アニメーション順序モード",
        "repeat_mode": "アニメーション繰り返し",
        
        # Stats panel
        "stats_frame": " 統計 ",
        "click_count": "クリック数:",
        "runtime": "実行時間:",
        "last_started": "開始時間:",
        "last_stopped": "終了時間:",
        
        # Control panel
        "control_frame": " コントロール ",
        "start_clicking": "開始",
        "stop_clicking": "停止",
        "shortcut_info": "ショートカット: Ctrl+G (開始/停止)",
        
        # Settings panel
        "settings_frame": " 設定 ",
        "always_on_top": "常に前面に表示",
        "mini_mode": "ミニモード (コントロールのみ)",
        "language": "言語:",
        
        # Profiles panel
        "profiles_frame": " プロファイル ",
        "profile": "プロファイル:",
        "save_profile": "保存",
        "load_profile": "読込",
        "profile_name_prompt": "プロファイル名:",
        
        # Messages
        "ready": "準備完了 | Ctrl+Gで開始/停止",
        "position_added": "位置を追加しました ({}, {})",
        "all_positions_cleared": "全位置を消去しました",
        "position_deleted": "位置{}を削除しました",
        "position_edited": "位置{}を ({}, {}) に編集しました",
        "profile_saved": "プロファイル '{}' を保存しました",
        "profile_loaded": "プロファイル '{}' を読み込みました",
        "working": "実行中... Ctrl+Gで停止",
        "stopped": "停止しました | Ctrl+Gで再開",
        "warning": "警告",
        "error": "エラー",
        "add_position_first": "開始前に位置を追加してください",
        "profile_save_error": "プロファイルの保存に失敗: {}",
        "profile_not_found": "プロファイル '{}' が見つかりません",
    },
    
    # Korean translations
    "ko": {
        # Program info
        "program_name": "SpeedClick Pro",
        "program_subtitle": "자동 클릭 프로그램",
        "version": "버전",
        "copyright": "© 2025 프로페셔널 에디션",
        
        # Header
        "mode_super_fast": "초고속 모드",
        
        # Position panel
        "positions_frame": " 클릭 위치 및 시간 ",
        "positions_count": "{}개 위치",
        "add_position": "위치 추가",
        "clear_positions": "모두 지우기",
        "column_number": "번호",
        "column_x": "X좌표",
        "column_y": "Y좌표",
        "column_duration": "지속시간(초)",
        "delete_position": "위치 삭제",
        "edit_position": "위치 편집",
        "edit_duration": "시간 편집",
        "confirm_edit": "새 위치로 변경하시겠습니까?",
        "enter_duration": "클릭 지속시간 입력(초):",
        "sequence_mode": "애니메이션 시퀀스 모드",
        "repeat_mode": "애니메이션 반복",
        
        # Stats panel
        "stats_frame": " 통계 ",
        "click_count": "클릭 수:",
        "runtime": "실행 시간:",
        "last_started": "시작 시간:",
        "last_stopped": "정지 시간:",
        
        # Control panel
        "control_frame": " 컨트롤 ",
        "start_clicking": "시작",
        "stop_clicking": "정지",
        "shortcut_info": "단축키: Ctrl+G (시작/정지)",
        
        # Settings panel
        "settings_frame": " 설정 ",
        "always_on_top": "항상 위에 표시",
        "mini_mode": "미니 모드 (컨트롤만)",
        "language": "언어:",
        
        # Profiles panel
        "profiles_frame": " 프로필 ",
        "profile": "프로필:",
        "save_profile": "프로필 저장",
        "load_profile": "프로필 불러오기",
        "profile_name_prompt": "프로필 이름:",
        
        # Messages
        "ready": "준비 완료 | Ctrl+G로 시작/정지",
        "position_added": "위치 추가됨 ({}, {})",
        "all_positions_cleared": "모든 위치가 지워짐",
        "position_deleted": "위치 {}이(가) 삭제됨",
        "position_edited": "위치 {}이(가) ({}, {})로 변경됨",
        "profile_saved": "프로필 '{}'이(가) 저장됨",
        "profile_loaded": "프로필 '{}'이(가) 로드됨",
        "working": "작동 중... Ctrl+G로 정지",
        "stopped": "정지됨 | Ctrl+G로 다시 시작",
        "warning": "경고",
        "error": "오류",
        "add_position_first": "시작하기 전에 위치를 추가하세요",
        "profile_save_error": "프로필을 저장할 수 없음: {}",
        "profile_not_found": "프로필 '{}'을(를) 찾을 수 없음",
    }
}

class Translator:
    """Translator class for handling language translations"""
    
    def __init__(self, lang=DEFAULT_LANGUAGE):
        """Initialize the translator with the specified language"""
        self.set_language(lang)
    
    def set_language(self, lang):
        """Set the current language"""
        if lang in TRANSLATIONS:
            self.current_lang = lang
        else:
            self.current_lang = DEFAULT_LANGUAGE
    
    def get_text(self, key, *args, **kwargs):
        """Get translated text for the given key"""
        # Get the translation dictionary for the current language
        translations = TRANSLATIONS.get(self.current_lang, TRANSLATIONS[DEFAULT_LANGUAGE])
        
        # Get the text from the dictionary, fallback to the key itself
        text = translations.get(key, key)
        
        # Format the text with any provided arguments
        if args or kwargs:
            text = text.format(*args, **kwargs)
            
        return text
    
    def get_languages(self):
        """Get available languages"""
        return LANGUAGES
