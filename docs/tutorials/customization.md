# カスタマイズチュートリアル

このチュートリアルでは、Databricks UI Component Libraryのスタイルとカスタマイズについて説明します。

## 🎯 概要

ライブラリのコンポーネントは、色、フォント、レイアウト、アニメーションなど、様々な面でカスタマイズできます。

## 🎨 スタイルカスタマイズ

### 1. 基本的なスタイル設定

```python
from db_ui_components import ChartComponent, TableComponent

# グラフコンポーネントのスタイル設定
chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='売上推移'
)

# カスタムスタイルの適用
chart.set_style({
    'backgroundColor': '#f8f9fa',
    'borderRadius': '8px',
    'padding': '16px',
    'border': '1px solid #e9ecef',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
    'fontFamily': 'Arial, sans-serif',
    'fontSize': '14px',
    'color': '#333333'
})

displayHTML(chart.render())
```

### 2. テーマの適用

```python
# ダークテーマの設定
dark_theme = {
    'backgroundColor': '#1e1e1e',
    'color': '#ffffff',
    'borderColor': '#404040',
    'gridColor': '#404040',
    'titleColor': '#ffffff',
    'axisColor': '#cccccc'
}

# ライトテーマの設定
light_theme = {
    'backgroundColor': '#ffffff',
    'color': '#333333',
    'borderColor': '#e9ecef',
    'gridColor': '#f8f9fa',
    'titleColor': '#333333',
    'axisColor': '#666666'
}

# テーマの適用
chart.set_theme('dark')  # または 'light'
# または、カスタムテーマを直接設定
chart.set_style(dark_theme)
```

### 3. カラーパレットのカスタマイズ

```python
# カスタムカラーパレットの設定
custom_colors = {
    'primary': '#007bff',
    'secondary': '#6c757d',
    'success': '#28a745',
    'danger': '#dc3545',
    'warning': '#ffc107',
    'info': '#17a2b8',
    'light': '#f8f9fa',
    'dark': '#343a40'
}

# カラーパレットの適用
chart.set_color_palette(custom_colors)

# または、Plotlyのカラースケールを使用
chart.set_color_scale('Viridis')  # または 'Plasma', 'Inferno', 'Magma'
```

## 📊 グラフのカスタマイズ

### 1. 軸のカスタマイズ

```python
# 軸の設定
chart.set_axis_config({
    'xaxis': {
        'title': '日付',
        'titlefont': {'size': 14, 'color': '#333333'},
        'tickfont': {'size': 12, 'color': '#666666'},
        'gridcolor': '#e9ecef',
        'zeroline': False
    },
    'yaxis': {
        'title': '売上（万円）',
        'titlefont': {'size': 14, 'color': '#333333'},
        'tickfont': {'size': 12, 'color': '#666666'},
        'gridcolor': '#e9ecef',
        'zeroline': True,
        'zerolinecolor': '#cccccc'
    }
})
```

### 2. 凡例のカスタマイズ

```python
# 凡例の設定
chart.set_legend_config({
    'orientation': 'h',  # 水平配置
    'x': 0.5,  # 中央配置
    'y': -0.2,  # 下部配置
    'font': {'size': 12, 'color': '#333333'},
    'bgcolor': 'rgba(255,255,255,0.8)',
    'bordercolor': '#e9ecef',
    'borderwidth': 1
})
```

### 3. マーカーのカスタマイズ

```python
# マーカーの設定（散布図の場合）
scatter_chart = ChartComponent(
    data=df,
    chart_type='scatter',
    x_column='x',
    y_column='y',
    title='散布図'
)

scatter_chart.set_marker_config({
    'size': 10,
    'color': '#007bff',
    'opacity': 0.7,
    'line': {
        'color': '#ffffff',
        'width': 2
    }
})
```

## 📋 テーブルのカスタマイズ

### 1. テーブルスタイルの設定

```python
table = TableComponent(
    data=df,
    enable_csv_download=True,
    sortable=True,
    searchable=True
)

# テーブルスタイルの設定
table.set_style({
    'backgroundColor': '#ffffff',
    'borderRadius': '8px',
    'border': '1px solid #e9ecef',
    'fontFamily': 'Arial, sans-serif',
    'fontSize': '14px'
})

# ヘッダー行のスタイル
table.set_header_style({
    'backgroundColor': '#f8f9fa',
    'color': '#333333',
    'fontWeight': 'bold',
    'borderBottom': '2px solid #dee2e6'
})

# 行のスタイル（交互の色）
table.set_row_style({
    'even': {
        'backgroundColor': '#ffffff'
    },
    'odd': {
        'backgroundColor': '#f8f9fa'
    },
    'hover': {
        'backgroundColor': '#e3f2fd'
    }
})
```

### 2. 列のカスタマイズ

```python
# 特定の列のスタイル設定
table.set_column_style('sales', {
    'textAlign': 'right',
    'fontWeight': 'bold',
    'color': '#28a745'
})

table.set_column_style('date', {
    'textAlign': 'center',
    'fontStyle': 'italic'
})

# 列の幅設定
table.set_column_widths({
    'date': '120px',
    'category': '150px',
    'sales': '100px',
    'profit': '100px'
})
```

## 🔄 フィルターのカスタマイズ

### 1. フィルタースタイルの設定

```python
from db_ui_components import FilterComponent

filter_comp = FilterComponent(
    filter_type='dropdown',
    column='category',
    options=['A', 'B', 'C'],
    title='カテゴリ'
)

# フィルタースタイルの設定
filter_comp.set_style({
    'backgroundColor': '#ffffff',
    'borderRadius': '4px',
    'border': '1px solid #ced4da',
    'padding': '8px 12px',
    'fontSize': '14px',
    'color': '#495057'
})

# ラベルのスタイル
filter_comp.set_label_style({
    'fontWeight': 'bold',
    'color': '#333333',
    'marginBottom': '8px'
})
```

### 2. カスタムフィルターコンポーネント

```python
# カスタムフィルターコンポーネント
class CustomFilterComponent(FilterComponent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_style = {
            'backgroundColor': '#f8f9fa',
            'borderRadius': '8px',
            'padding': '16px',
            'margin': '8px 0'
        }
    
    def render(self):
        """カスタムレンダリング"""
        base_html = super().render()
        
        # カスタムスタイルを適用
        custom_css = f"""
        <style>
        .custom-filter {{
            {self._style_to_css(self.custom_style)}
        }}
        </style>
        """
        
        return custom_css + f'<div class="custom-filter">{base_html}</div>'
    
    def _style_to_css(self, style_dict):
        """スタイル辞書をCSSに変換"""
        css_properties = []
        for key, value in style_dict.items():
            css_key = key.replace('_', '-')
            css_properties.append(f'{css_key}: {value};')
        return '\n'.join(css_properties)

# 使用例
custom_filter = CustomFilterComponent(
    filter_type='multiselect',
    column='region',
    options=['North', 'South', 'East', 'West'],
    title='地域'
)

displayHTML(custom_filter.render())
```

## 🎭 アニメーションのカスタマイズ

### 1. アニメーション効果の設定

```python
# アニメーションの有効化
chart.enable_animation(True)

# アニメーション設定
chart.set_animation_config({
    'duration': 1000,  # ミリ秒
    'easing': 'cubic-bezier(0.4, 0, 0.2, 1)',
    'mode': 'immediate'  # または 'afterall'
})

# 特定のアニメーション効果
chart.set_transition_config({
    'frame': {
        'duration': 500,
        'redraw': True
    },
    'transition': {
        'duration': 300,
        'easing': 'cubic-in-out'
    }
})
```

### 2. インタラクティブアニメーション

```python
# ホバー効果の設定
chart.set_hover_config({
    'mode': 'closest',
    'hoverinfo': 'x+y+text',
    'hoverlabel': {
        'bgcolor': '#ffffff',
        'bordercolor': '#007bff',
        'font': {'size': 12}
    }
})

# クリック効果の設定
chart.set_click_config({
    'mode': 'event',
    'eventData': ['x', 'y', 'text']
})
```

## 📱 レスポンシブデザイン

### 1. レスポンシブ設定

```python
# レスポンシブ設定
chart.set_responsive_config({
    'responsive': True,
    'autosize': True,
    'breakpoints': {
        'mobile': 768,
        'tablet': 1024,
        'desktop': 1200
    }
})

# 画面サイズ別の設定
chart.set_responsive_styles({
    'mobile': {
        'height': 300,
        'fontSize': '12px'
    },
    'tablet': {
        'height': 400,
        'fontSize': '14px'
    },
    'desktop': {
        'height': 500,
        'fontSize': '16px'
    }
})
```

### 2. グリッドレイアウトのカスタマイズ

```python
from db_ui_components import Dashboard

# レスポンシブダッシュボード
dashboard = Dashboard(
    title='レスポンシブダッシュボード',
    layout='responsive'
)

# レスポンシブ設定
dashboard.set_responsive_config({
    'breakpoints': {
        'mobile': 768,
        'tablet': 1024,
        'desktop': 1200
    },
    'columns': {
        'mobile': 1,
        'tablet': 2,
        'desktop': 3
    }
})
```

## 🎨 カスタムCSS

### 1. カスタムCSSの追加

```python
# カスタムCSSの定義
custom_css = """
<style>
.custom-chart {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    margin: 16px 0;
}

.custom-chart:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
}

.custom-table {
    border-collapse: collapse;
    width: 100%;
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.custom-table th {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 12px;
    text-align: left;
}

.custom-table td {
    padding: 12px;
    border-bottom: 1px solid #e9ecef;
}

.custom-table tr:hover {
    background-color: #f8f9fa;
}
</style>
"""

# CSSの適用
chart.set_custom_css(custom_css)
table.set_custom_css(custom_css)
```

### 2. テーマシステム

```python
# テーマシステム
class ThemeManager:
    def __init__(self):
        self.themes = {
            'default': {
                'primary_color': '#007bff',
                'secondary_color': '#6c757d',
                'background_color': '#ffffff',
                'text_color': '#333333',
                'border_color': '#e9ecef'
            },
            'dark': {
                'primary_color': '#007bff',
                'secondary_color': '#6c757d',
                'background_color': '#1e1e1e',
                'text_color': '#ffffff',
                'border_color': '#404040'
            },
            'corporate': {
                'primary_color': '#2c3e50',
                'secondary_color': '#34495e',
                'background_color': '#ecf0f1',
                'text_color': '#2c3e50',
                'border_color': '#bdc3c7'
            }
        }
    
    def apply_theme(self, component, theme_name):
        """テーマを適用"""
        if theme_name not in self.themes:
            raise ValueError(f"Unknown theme: {theme_name}")
        
        theme = self.themes[theme_name]
        
        # テーマに基づいてスタイルを設定
        component.set_style({
            'backgroundColor': theme['background_color'],
            'color': theme['text_color'],
            'borderColor': theme['border_color']
        })
        
        # カラーパレットも更新
        component.set_color_palette({
            'primary': theme['primary_color'],
            'secondary': theme['secondary_color']
        })

# 使用例
theme_manager = ThemeManager()

chart = ChartComponent(data=df, chart_type='line', x_column='date', y_column='sales')
theme_manager.apply_theme(chart, 'dark')

table = TableComponent(data=df)
theme_manager.apply_theme(table, 'corporate')
```

## 🚀 高度なカスタマイズ

### 1. カスタムコンポーネントの作成

```python
# カスタムコンポーネント
class CustomChartComponent(ChartComponent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_features = {}
    
    def add_custom_feature(self, feature_name, feature_config):
        """カスタム機能を追加"""
        self.custom_features[feature_name] = feature_config
    
    def render(self):
        """カスタムレンダリング"""
        base_html = super().render()
        
        # カスタム機能を適用
        if 'watermark' in self.custom_features:
            watermark_config = self.custom_features['watermark']
            watermark_html = f"""
            <div style="
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                opacity: 0.1;
                font-size: 48px;
                color: {watermark_config.get('color', '#cccccc')};
                pointer-events: none;
                z-index: 1000;
            ">
                {watermark_config.get('text', 'DRAFT')}
            </div>
            """
            base_html = f'<div style="position: relative;">{base_html}{watermark_html}</div>'
        
        return base_html

# 使用例
custom_chart = CustomChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales'
)

# ウォーターマークを追加
custom_chart.add_custom_feature('watermark', {
    'text': 'CONFIDENTIAL',
    'color': '#ff0000'
})

displayHTML(custom_chart.render())
```

### 2. プラグインシステム

```python
# プラグインシステム
class PluginManager:
    def __init__(self):
        self.plugins = {}
    
    def register_plugin(self, name, plugin_func):
        """プラグインを登録"""
        self.plugins[name] = plugin_func
    
    def apply_plugin(self, component, plugin_name, **kwargs):
        """プラグインを適用"""
        if plugin_name not in self.plugins:
            raise ValueError(f"Unknown plugin: {plugin_name}")
        
        return self.plugins[plugin_name](component, **kwargs)

# プラグインの例
def add_tooltip_plugin(component, tooltip_text):
    """ツールチッププラグイン"""
    original_render = component.render
    
    def render_with_tooltip():
        html = original_render()
        tooltip_html = f"""
        <div style="position: relative;">
            {html}
            <div style="
                position: absolute;
                top: 10px;
                right: 10px;
                background: rgba(0,0,0,0.8);
                color: white;
                padding: 8px;
                border-radius: 4px;
                font-size: 12px;
                display: none;
            " class="tooltip">
                {tooltip_text}
            </div>
        </div>
        """
        return tooltip_html
    
    component.render = render_with_tooltip
    return component

# 使用例
plugin_manager = PluginManager()
plugin_manager.register_plugin('tooltip', add_tooltip_plugin)

chart = ChartComponent(data=df, chart_type='line', x_column='date', y_column='sales')
chart_with_tooltip = plugin_manager.apply_plugin(chart, 'tooltip', tooltip_text='売上データ')

displayHTML(chart_with_tooltip.render())
```

## 🚀 次のステップ

- [高度な可視化](./advanced_visualization.md) - 高度な可視化コンポーネント
- [パフォーマンス最適化](../guides/performance.md) - パフォーマンスの最適化
- [API リファレンス](../api/) - 全APIの詳細

## ❓ よくある質問

**Q: カスタムCSSが適用されない場合はどうすればよいですか？**
A: CSSの優先度を確認し、`!important`を使用するか、より具体的なセレクタを使用してください。

**Q: テーマを動的に変更できますか？**
A: はい、`set_theme()`メソッドを使用して動的にテーマを変更できます。

**Q: カスタムコンポーネントを作成する際のベストプラクティスは？**
A: 既存のコンポーネントを継承し、必要な機能のみをオーバーライドすることを推奨します。