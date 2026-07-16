from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint

class ToastNotification(QWidget):
    """A non-intrusive, auto-hiding toast notification widget."""
    def __init__(self, parent, text, duration_ms=3000, theme="info"):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.ToolTip | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        
        # Simple styling based on theme
        colors = {
            "info": ("#268bd2", "#fdf6e3"),
            "success": ("#859900", "#fdf6e3"),
            "warning": ("#b58900", "#fdf6e3"),
            "error": ("#dc322f", "#fdf6e3")
        }
        bg, fg = colors.get(theme, colors["info"])
        
        self.label.setStyleSheet(f"""
            QLabel {{
                background-color: {bg};
                color: {fg};
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
                border: 1px solid #111;
            }}
        """)
        layout.addWidget(self.label)
        
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)
        
        self.duration_ms = duration_ms
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Connect animation finished signal to hide or destroy
        self.animation.finished.connect(self._on_animation_finished)
        self.is_fading_out = False
        
        # Position at the bottom center of parent
        self.adjustSize()
        self._position_toast()
        
    def _position_toast(self):
        if self.parent():
            parent_rect = self.parent().rect()
            x = parent_rect.center().x() - self.width() // 2
            y = parent_rect.bottom() - self.height() - 50  # 50px above bottom
            self.move(QPoint(x, y))

    def show_toast(self):
        self.show()
        self.raise_()
        self.is_fading_out = False
        self.animation.stop()
        self.animation.setDuration(300)
        self.animation.setStartValue(self.opacity_effect.opacity())
        self.animation.setEndValue(0.95)
        self.animation.start()
        
        QTimer.singleShot(self.duration_ms, self.fade_out)

    def fade_out(self):
        self.is_fading_out = True
        self.animation.stop()
        self.animation.setDuration(500)
        self.animation.setStartValue(self.opacity_effect.opacity())
        self.animation.setEndValue(0.0)
        self.animation.start()

    def _on_animation_finished(self):
        if self.is_fading_out:
            self.hide()
            self.deleteLater()
