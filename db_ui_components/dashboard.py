"""
ダッシュボードコンポーネント

Databricksダッシュボードを管理するコンポーネントです。
複数のコンポーネントを配置し、レイアウトを管理します。
"""

from typing import Dict, Any, List, Tuple, Optional
import json
from abc import ABC, abstractmethod


class LayoutManager:
    """レイアウト管理クラス"""
    
    def __init__(self, layout_type: str = "grid"):
        self.layout_type = layout_type
    
    def get_container_start_html(self) -> str:
        """コンテナの開始HTMLを取得"""
        if self.layout_type == "grid":
            return '''
            <div class="dashboard-container" style="display: grid; grid-template-columns: repeat(12, 1fr); gap: 20px; padding: 20px;">
            '''
        elif self.layout_type == "flex":
            return '''
            <div class="dashboard-container" style="display: flex; flex-wrap: wrap; gap: 20px; padding: 20px;">
            '''
        else:
            return '''
            <div class="dashboard-container" style="padding: 20px;">
            '''
    
    def get_container_end_html(self) -> str:
        """コンテナの終了HTMLを取得"""
        return '</div>'
    
    def get_component_style(self, position: Tuple[int, int], size: Tuple[int, int], 
                          custom_style: Dict[str, Any]) -> str:
        """コンポーネントのスタイルを取得"""
        if self.layout_type == "grid":
            grid_style = f'''
            grid-column: {position[1] + 1} / span {size[0]};
            grid-row: {position[0] + 1} / span {size[1]};
            '''
        elif self.layout_type == "flex":
            grid_style = f'''
            flex: {size[0]} {size[1]} 0;
            min-width: {size[0] * 200}px;
            '''
        else:
            grid_style = ""
        
        # カスタムスタイルの適用
        custom_style_str = ""
        for key, value in custom_style.items():
            custom_style_str += f"{key}: {value}; "
        
        return f'''
        {grid_style}
        {custom_style_str}
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        '''


class ComponentManager:
    """コンポーネント管理クラス"""
    
    def __init__(self):
        self.components: List[Dict[str, Any]] = []
        self.positions: Dict[str, Tuple[int, int]] = {}
        self.styles: Dict[str, Dict[str, Any]] = {}
    
    def add_component(self, component: Any, position: Tuple[int, int], 
                     size: Tuple[int, int] = (1, 1), **kwargs) -> str:
        """コンポーネントを追加"""
        component_id = f"component-{len(self.components)}"
        
        self.components.append({
            "id": component_id,
            "component": component,
            "position": position,
            "size": size,
            "kwargs": kwargs
        })
        
        self.positions[component_id] = position
        self.styles[component_id] = kwargs.get("style", {})
        
        return component_id
    
    def remove_component(self, component_id: str) -> None:
        """コンポーネントを削除"""
        self.components = [c for c in self.components if c["id"] != component_id]
        if component_id in self.positions:
            del self.positions[component_id]
        if component_id in self.styles:
            del self.styles[component_id]
    
    def update_component(self, component_id: str, new_component: Any) -> None:
        """コンポーネントを更新"""
        for comp_info in self.components:
            if comp_info["id"] == component_id:
                comp_info["component"] = new_component
                break
    
    def get_component(self, component_id: str) -> Optional[Any]:
        """コンポーネントを取得"""
        for comp_info in self.components:
            if comp_info["id"] == component_id:
                return comp_info["component"]
        return None
    
    def set_component_style(self, component_id: str, style: Dict[str, Any]) -> None:
        """コンポーネントのスタイルを設定"""
        self.styles[component_id] = style
    
    def get_all_components(self) -> List[Dict[str, Any]]:
        """すべてのコンポーネントを取得"""
        return self.components.copy()


class DashboardRenderer:
    """ダッシュボードレンダリングクラス"""
    
    def __init__(self, layout_manager: LayoutManager):
        self.layout_manager = layout_manager
    
    def render_header(self, title: Optional[str]) -> str:
        """ヘッダーをレンダリング"""
        if not title:
            return ""
        
        return f'''
        <div class="dashboard-header" style="margin-bottom: 20px; padding: 20px; background-color: #f8f9fa; border-radius: 8px;">
            <h1 style="margin: 0; color: #333; font-size: 24px;">{title}</h1>
        </div>
        '''
    
    def render_component(self, comp_info: Dict[str, Any], layout_manager: LayoutManager) -> str:
        """コンポーネントをレンダリング"""
        component = comp_info["component"]
        position = comp_info["position"]
        size = comp_info["size"]
        style = layout_manager.get_component_style(position, size, {})
        
        # コンポーネントのHTMLを取得
        component_html = component.render()
        
        return f'''
        <div class="dashboard-component" 
             id="{comp_info['id']}"
             style="{style}">
            {component_html}
        </div>
        '''


class Dashboard:
    """
    Databricksダッシュボード管理コンポーネント
    
    機能:
    - 複数コンポーネントの管理
    - グリッドレイアウト
    - レスポンシブデザイン
    - コンポーネント間の連携
    """
    
    def __init__(self, title: Optional[str] = None, layout: str = "grid"):
        """
        初期化
        
        Args:
            title: ダッシュボードのタイトル
            layout: レイアウトタイプ ('grid', 'flex', 'custom')
        """
        self.title = title
        self.layout_manager = LayoutManager(layout)
        self.component_manager = ComponentManager()
        self.renderer = DashboardRenderer(self.layout_manager)
        
    def add_component(self, component: Any, position: Tuple[int, int], 
                     size: Tuple[int, int] = (1, 1), **kwargs) -> str:
        """
        コンポーネントを追加
        
        Args:
            component: 追加するコンポーネント
            position: 位置 (row, column)
            size: サイズ (width, height)
            **kwargs: その他のパラメータ
            
        Returns:
            コンポーネントID
        """
        return self.component_manager.add_component(component, position, size, **kwargs)
    
    def remove_component(self, component_id: str) -> None:
        """
        コンポーネントを削除
        
        Args:
            component_id: 削除するコンポーネントのID
        """
        self.component_manager.remove_component(component_id)
    
    def render(self) -> str:
        """
        ダッシュボードをHTMLとしてレンダリング
        
        Returns:
            HTML文字列
        """
        html_parts = []
        
        # ダッシュボードの開始
        html_parts.append(self.renderer.render_header(self.title))
        html_parts.append(self.layout_manager.get_container_start_html())
        
        # コンポーネントのレンダリング
        for comp_info in self.component_manager.get_all_components():
            html_parts.append(self.renderer.render_component(comp_info, self.layout_manager))
        
        # ダッシュボードの終了
        html_parts.append(self.layout_manager.get_container_end_html())
        
        return '\n'.join(html_parts)
    
    def update_component(self, component_id: str, new_component: Any) -> None:
        """
        コンポーネントを更新
        
        Args:
            component_id: 更新するコンポーネントのID
            new_component: 新しいコンポーネント
        """
        self.component_manager.update_component(component_id, new_component)
    
    def set_component_style(self, component_id: str, style: Dict[str, Any]) -> None:
        """
        コンポーネントのスタイルを設定
        
        Args:
            component_id: コンポーネントのID
            style: スタイル設定の辞書
        """
        self.component_manager.set_component_style(component_id, style)
    
    def get_component(self, component_id: str) -> Optional[Any]:
        """
        コンポーネントを取得
        
        Args:
            component_id: コンポーネントのID
            
        Returns:
            コンポーネント（見つからない場合はNone）
        """
        return self.component_manager.get_component(component_id)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        ダッシュボードの設定を辞書として取得
        
        Returns:
            設定辞書
        """
        return {
            "title": self.title,
            "layout": self.layout_manager.layout_type,
            "components": [
                {
                    "id": comp["id"],
                    "position": comp["position"],
                    "size": comp["size"],
                    "kwargs": comp["kwargs"]
                }
                for comp in self.component_manager.get_all_components()
            ],
            "styles": self.component_manager.styles
        }
    
    def save_layout(self, filename: str) -> None:
        """
        レイアウトをファイルに保存
        
        Args:
            filename: 保存するファイル名
        """
        layout_data = self.to_dict()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(layout_data, f, ensure_ascii=False, indent=2)
    
    def load_layout(self, filename: str) -> None:
        """
        レイアウトをファイルから読み込み
        
        Args:
            filename: 読み込むファイル名
        """
        with open(filename, 'r', encoding='utf-8') as f:
            layout_data = json.load(f)
        
        self.title = layout_data.get("title")
        self.layout_manager = LayoutManager(layout_data.get("layout", "grid"))
        self.component_manager.styles = layout_data.get("styles", {})
        
        # コンポーネントの位置情報を復元
        for comp_data in layout_data.get("components", []):
            self.component_manager.positions[comp_data["id"]] = comp_data["position"] 