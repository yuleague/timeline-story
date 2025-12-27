import json
import os
from datetime import datetime
from pathlib import Path

def generate_sample_timeline_json():
    """生成包含10组模拟数据的 TimelineJS JSON 文件"""
    
    # TimelineJS 数据格式
    timeline_data = {
        "events": [
            {
                "unique_id": "event-1",
                "start_date": {
                    "year": 2024,
                    "month": 1,
                    "day": 15
                },
                "text": {
                    "headline": "时间线故事项目启动",
                    "text": "基于Flask和Supabase的时间线故事网站正式启动开发。该项目使用TimelineJS库展示历史事件。"
                },
                "media": {
                    "url": "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=800&h=600&fit=crop",
                    "caption": "项目启动会议",
                    "credit": "Unsplash"
                },
                "group": "项目里程碑",
                "display_date": "2024年1月15日",
                "background": {
                    "color": "#2c3e50"
                },
                "autolink": True
            },
            {
                "unique_id": "event-2",
                "start_date": {
                    "year": 2024,
                    "month": 2,
                    "day": 10
                },
                "end_date": {
                    "year": 2024,
                    "month": 2,
                    "day": 15
                },
                "text": {
                    "headline": "前端界面设计完成",
                    "text": "完成了响应式网页设计，支持桌面和移动设备。采用了现代化的UI/UX设计原则。"
                },
                "media": {
                    "url": "https://images.unsplash.com/photo-1558655146-9f40138edfeb?w-800&h=600&fit=crop",
                    "caption": "界面设计稿",
                    "credit": "Design Team"
                },
                "group": "开发阶段",
                "display_date": "2024年2月10-15日",
                "autolink": True
            },
            {
                "unique_id": "event-3",
                "start_date": {
                    "year": 2024,
                    "month": 3,
                    "day": 5
                },
                "text": {
                    "headline": "Flask后端API开发",
                    "text": "实现了完整的RESTful API，包括用户认证、事件管理和数据导出功能。"
                },
                "media": {
                    "url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=600&fit=crop",
                    "caption": "代码开发",
                    "credit": "Development Team"
                },
                "group": "开发阶段",
                "display_date": "2024年3月5日",
                "background": {
                    "url": "https://images.unsplash.com/photo-1556075798-4825dfaaf498?w=800&h=400&fit=crop"
                },
                "autolink": True
            },
            {
                "unique_id": "event-4",
                "start_date": {
                    "year": 2024,
                    "month": 3,
                    "day": 20
                },
                "text": {
                    "headline": "Supabase集成完成",
                    "text": "成功集成Supabase作为后端数据库，实现了实时数据同步和用户认证系统。"
                },
                "media": {
                    "url": "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=800&h=600&fit=crop",
                    "caption": "数据库架构",
                    "credit": "Database Team"
                },
                "group": "技术集成",
                "display_date": "2024年3月20日",
                "autolink": True
            },
            {
                "unique_id": "event-5",
                "start_date": {
                    "year": 2024,
                    "month": 4,
                    "day": 1
                },
                "text": {
                    "headline": "TimelineJS数据导出功能",
                    "text": "实现了将数据库事件数据自动导出为TimelineJS兼容的JSON格式文件。"
                },
                "media": {
                    "url": "https://images.unsplash.com/photo-1545235617-9465d2a55698?w=800&h=600&fit=crop",
                    "caption": "数据转换流程",
                    "credit": "Data Team"
                },
                "group": "核心功能",
                "display_date": "2024年4月1日",
                "autolink": False
            },
            {
                "unique_id": "event-6",
                "start_date": {
                    "year": 2024,
                    "month": 4,
                    "day": 15
                },
                "end_date": {
                    "year": 2024,
                    "month": 4,
                    "day": 20
                },
                "text": {
                    "headline": "Alpha测试阶段",
                    "text": "内部Alpha测试，邀请50名用户进行功能测试和反馈收集。修复了23个主要bug。"
                },
                "media": {
                    "url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop",
                    "caption": "测试报告",
                    "credit": "QA Team"
                },
                "group": "测试阶段",
                "display_date": "2024年4月15-20日",
                "autolink": True
            },
            {
                "unique_id": "event-7",
                "start_date": {
                    "year": 2024,
                    "month": 5,
                    "day": 10
                },
                "text": {
                    "headline": "用户白名单系统上线",
                    "text": "实现了基于白名单的用户注册系统，确保只有授权用户可以注册为会员。"
                },
                "media": {
                    "url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&h=600&fit=crop",
                    "caption": "用户管理界面",
                    "credit": "Security Team"
                },
                "group": "安全功能",
                "display_date": "2024年5月10日",
                "background": {
                    "color": "#3498db"
                },
                "autolink": True
            },
            {
                "unique_id": "event-8",
                "start_date": {
                    "year": 2024,
                    "month": 5,
                    "day": 25
                },
                "text": {
                    "headline": "管理员后台发布",
                    "text": "发布了完整的管理员后台，支持事件管理、用户管理和系统配置功能。"
                },
                "media": {
                    "url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop",
                    "caption": "管理员控制面板",
                    "credit": "Admin Team"
                },
                "group": "管理功能",
                "display_date": "2024年5月25日",
                "autolink": True
            },
            {
                "unique_id": "event-9",
                "start_date": {
                    "year": 2024,
                    "month": 6,
                    "day": 5
                },
                "text": {
                    "headline": "Beta公测开始",
                    "text": "开放Beta公测，前1000名注册用户获得免费会员资格。收集了大量用户反馈。"
                },
                "media": {
                    "url": "https://images.unsplash.com/photo-1551836026-d5c2c5af78e4?w=800&h=600&fit=crop",
                    "caption": "公测发布会",
                    "credit": "Marketing Team"
                },
                "group": "发布阶段",
                "display_date": "2024年6月5日",
                "autolink": True
            },
            {
                "unique_id": "event-10",
                "start_date": {
                    "year": 2024,
                    "month": 6,
                    "day": 20
                },
                "text": {
                    "headline": "正式版本发布",
                    "text": "时间线故事1.0正式版发布！包含所有计划功能，支持多语言和自定义主题。"
                },
                "media": {
                    "url": "https://images.unsplash.com/photo-1545235617-9465d2a55698?w=800&h=600&fit=crop",
                    "caption": "发布庆祝活动",
                    "credit": "All Teams"
                },
                "group": "发布阶段",
                "display_date": "2024年6月20日",
                "background": {
                    "color": "#27ae60"
                },
                "autolink": True
            }
        ],
        "title": {
            "text": {
                "headline": "时间线故事发展历程",
                "text": "从项目启动到正式发布的完整历程"
            },
            "media": {
                "url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200&h=600&fit=crop",
                "caption": "时间线故事项目",
                "credit": "Project Timeline"
            }
        },
        "eras": [
            {
                "start_date": {
                    "year": 2024,
                    "month": 1,
                    "day": 1
                },
                "end_date": {
                    "year": 2024,
                    "month": 3,
                    "day": 31
                },
                "text": {
                    "headline": "开发阶段",
                    "text": "项目初始开发和功能实现"
                }
            },
            {
                "start_date": {
                    "year": 2024,
                    "month": 4,
                    "day": 1
                },
                "end_date": {
                    "year": 2024,
                    "month": 5,
                    "day": 31
                },
                "text": {
                    "headline": "测试阶段",
                    "text": "内部测试和功能完善"
                }
            },
            {
                "start_date": {
                    "year": 2024,
                    "month": 6,
                    "day": 1
                },
                "end_date": {
                    "year": 2024,
                    "month": 12,
                    "day": 31
                },
                "text": {
                    "headline": "发布阶段",
                    "text": "公测和正式发布"
                }
            }
        ],
        "scale": "human"
    }
    
    # 确保输出目录存在
    output_dir = Path("app/static/data")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 输出路径
    output_path = output_dir / "timeline-story.json"
    
    # 写入JSON文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(timeline_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 成功生成包含10组模拟数据的TimelineJS JSON文件")
    print(f"📁 文件位置: {output_path}")
    print(f"📊 包含数据:")
    print(f"   - {len(timeline_data['events'])} 个事件")
    print(f"   - 1 个标题幻灯片")
    print(f"   - {len(timeline_data['eras'])} 个时代划分")
    print(f"   - 时间范围: 2024年1月 - 2024年12月")
    
    return output_path

def display_json_preview():
    """显示JSON文件预览"""
    output_path = Path("app/static/data/timeline-story.json")
    
    if output_path.exists():
        with open(output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("\n📋 JSON文件预览:")
        print("=" * 50)
        print(f"标题: {data['title']['text']['headline']}")
        print(f"事件数量: {len(data['events'])}")
        print(f"时间尺度: {data['scale']}")
        print("\n前3个事件:")
        for i, event in enumerate(data['events'][:3], 1):
            print(f"  {i}. {event['text']['headline']} - {event['display_date']}")
        
        print("\n时代划分:")
        for era in data['eras']:
            print(f"  - {era['text']['headline']}: {era['start_date']['year']}.{era['start_date']['month']} - {era['end_date']['year']}.{era['end_date']['month']}")

def create_html_preview():
    """创建HTML预览文件"""
    html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>时间线故事 - 预览</title>
    <link rel="stylesheet" href="https://cdn.knightlab.com/libs/timeline3/latest/css/timeline.css">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f7fa;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            padding: 20px;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        #timeline-embed {
            width: 100%;
            height: 700px;
            border-radius: 8px;
            overflow: hidden;
        }
        .info {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>时间线故事 - 发展历程</h1>
        <div id="timeline-embed"></div>
        <div class="info">
            <p><strong>数据信息：</strong>此时间线展示了10个模拟事件，涵盖项目开发的全过程。所有数据存储在<code>timeline-story.json</code>文件中。</p>
            <p><strong>技术：</strong>使用TimelineJS 3.0 + Flask + Supabase</p>
        </div>
    </div>

    <script src="https://cdn.knightlab.com/libs/timeline3/latest/js/timeline.js"></script>
    <script>
        var options = {
            language: "zh-cn",
            start_at_end: false,
            timenav_height_percentage: 50,
            default_bg_color: "#f5f7fa",
            scale_factor: 2
        };
        
        var timeline = new TL.Timeline('timeline-embed', 'app/static/data/timeline-story.json', options);
        
        // 添加键盘控制
        document.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowLeft') {
                timeline.goToPrev();
            } else if (e.key === 'ArrowRight') {
                timeline.goToNext();
            }
        });
    </script>
</body>
</html>'''
    
    output_path = Path("timeline_preview.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n🌐 已创建HTML预览文件: {output_path}")
    print("💡 提示: 在浏览器中打开此文件查看时间线效果")

if __name__ == "__main__":
    # 生成JSON数据
    json_path = generate_sample_timeline_json()
    
    # 显示预览
    display_json_preview()
    
    # 创建HTML预览
    create_html_preview()
    
    print("\n🎉 数据生成完成！")
    print("接下来可以:")
    print("1. 在浏览器中打开 timeline_preview.html 查看效果")
    print("2. 将 timeline-story.json 部署到Flask项目的静态文件夹")
    print("3. 使用Flask应用中的 postgres_to_json.py 替换为真实数据库数据")