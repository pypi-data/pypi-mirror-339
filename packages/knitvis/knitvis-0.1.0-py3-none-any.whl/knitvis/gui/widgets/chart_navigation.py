from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
                             QPushButton, QSlider, QLabel, QSpinBox,
                             QFrame, QSizePolicy, QScrollBar)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont


class ChartNavigationWidget(QFrame):
    """Modern navigation widget for chart views with improved UI"""

    # Signals
    # row, col, row_zoom, col_zoom
    viewportChanged = pyqtSignal(int, int, int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.chart_rows = 0
        self.chart_cols = 0
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface with edge-aligned controls"""
        main_layout = QGridLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(4)

        # === Main Content Area (will be empty for chart content) ===
        content_frame = QFrame()
        content_frame.setFrameShape(QFrame.NoFrame)
        content_frame.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(content_frame, 0, 0)

        # === Right Edge Controls (Vertical) ===
        right_controls = QVBoxLayout()
        right_controls.setSpacing(8)

        # Row position scrollbar (vertical)
        self.row_pos = QScrollBar(Qt.Vertical)
        self.row_pos.setMinimum(0)
        self.row_pos.valueChanged.connect(self._emit_viewport_changed)
        right_controls.addWidget(self.row_pos, 1)  # 1 = stretch factor

        # Row zoom slider (vertical)
        self.row_zoom_slider = QSlider(Qt.Vertical)
        self.row_zoom_slider.setMinimum(5)  # Minimum 5 rows
        self.row_zoom_slider.setValue(20)
        self.row_zoom_slider.setTracking(True)
        self.row_zoom_slider.valueChanged.connect(self._emit_viewport_changed)
        self.row_zoom_slider.valueChanged.connect(self.on_row_zoom_changed)
        right_controls.addWidget(self.row_zoom_slider)

        # Add right controls to main layout
        main_layout.addLayout(right_controls, 0, 1)

        # === Bottom Edge Controls (Horizontal) ===
        bottom_controls = QHBoxLayout()
        bottom_controls.setSpacing(8)

        # Viewport range display (bottom left)
        self.viewport_display = QLabel("Rows 1-20 | Cols 1-20")
        self.viewport_display.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.viewport_display.setStyleSheet("font-size: 10px;")
        bottom_controls.addWidget(self.viewport_display)

        # Column position scrollbar
        self.col_pos = QScrollBar(Qt.Horizontal)
        self.col_pos.setMinimum(0)
        self.col_pos.valueChanged.connect(self._emit_viewport_changed)
        bottom_controls.addWidget(self.col_pos, 1)  # 1 = stretch factor

        # Column zoom slider (horizontal)
        self.col_zoom_slider = QSlider(Qt.Horizontal)
        self.col_zoom_slider.setMinimum(5)  # Minimum 5 columns
        self.col_zoom_slider.setValue(20)
        self.col_zoom_slider.setTracking(True)
        self.col_zoom_slider.valueChanged.connect(self._emit_viewport_changed)
        self.col_zoom_slider.valueChanged.connect(self.on_col_zoom_changed)
        bottom_controls.addWidget(self.col_zoom_slider)

        # Add bottom controls to main layout
        main_layout.addLayout(bottom_controls, 1, 0)

        # === Full Chart Button (Bottom Right) ===
        self.full_chart_button = QPushButton("🔍")
        self.full_chart_button.setToolTip("View Full Chart")
        self.full_chart_button.setFixedSize(24, 24)
        self.full_chart_button.clicked.connect(self.show_full_chart)
        main_layout.addWidget(self.full_chart_button, 1,
                              1, Qt.AlignBottom | Qt.AlignRight)

    def _emit_viewport_changed(self):
        """Emit signal when viewport parameters change"""
        # Update viewport display
        self._update_viewport_display()

        # Emit signal
        self.viewportChanged.emit(
            self.row_pos.value(),
            self.col_pos.value(),
            self.row_zoom_slider.value(),
            self.col_zoom_slider.value()
        )

    def _update_viewport_display(self):
        """Update the viewport range display"""
        row_start = self.row_pos.value() + 1  # 1-based display
        row_end = min(self.chart_rows, row_start +
                      self.row_zoom_slider.value() - 1)

        col_start = self.col_pos.value() + 1  # 1-based display
        col_end = min(self.chart_cols, col_start +
                      self.col_zoom_slider.value() - 1)

        self.viewport_display.setText(
            f"Rows {row_start}-{row_end} | Cols {col_start}-{col_end}")

    def update_navigation_limits(self, rows, cols):
        """Update navigation controls based on chart size and viewport"""
        self.chart_rows = rows
        self.chart_cols = cols

        # Update zoom slider maximums to match chart dimensions
        self.row_zoom_slider.setMaximum(rows)
        self.col_zoom_slider.setMaximum(cols)

        row_zoom = self.row_zoom_slider.value()
        col_zoom = self.col_zoom_slider.value()

        # Ensure zoom values don't exceed chart dimensions
        if row_zoom > rows:
            self.row_zoom_slider.setValue(rows)
            row_zoom = rows

        if col_zoom > cols:
            self.col_zoom_slider.setValue(cols)
            col_zoom = cols

        # Calculate maximum row and column positions
        max_row = max(0, rows - row_zoom)
        max_col = max(0, cols - col_zoom)

        # Configure row scrollbar
        if rows > row_zoom:
            self.row_pos.setRange(0, max_row)
            self.row_pos.setPageStep(row_zoom)
        else:
            self.row_pos.setRange(0, 0)
            self.row_pos.setPageStep(1)

        # Configure column scrollbar
        if cols > col_zoom:
            self.col_pos.setRange(0, max_col)
            self.col_pos.setPageStep(col_zoom)
        else:
            self.col_pos.setRange(0, 0)
            self.col_pos.setPageStep(1)

        # Ensure current position is valid
        if self.row_pos.value() > max_row:
            self.row_pos.setValue(max_row)

        if self.col_pos.value() > max_col:
            self.col_pos.setValue(max_col)

        # Update viewport display
        self._update_viewport_display()

    def show_full_chart(self):
        """Reset view to show the full chart"""
        # Block signals temporarily to avoid multiple updates
        self.row_pos.blockSignals(True)
        self.col_pos.blockSignals(True)
        self.row_zoom_slider.blockSignals(True)
        self.col_zoom_slider.blockSignals(True)

        try:
            # Reset position to start
            self.row_pos.setValue(0)
            self.col_pos.setValue(0)

            # Set zoom to show the entire chart (with limits for very large charts)
            max_rows = min(self.chart_rows, 100)
            max_cols = min(self.chart_cols, 100)

            # Set zoom levels
            self.row_zoom_slider.setValue(max_rows)
            self.col_zoom_slider.setValue(max_cols)

        finally:
            # Re-enable signals
            self.row_pos.blockSignals(False)
            self.col_pos.blockSignals(False)
            self.row_zoom_slider.blockSignals(False)
            self.col_zoom_slider.blockSignals(False)

            # Emit viewport changed signal once for the complete update
            self._emit_viewport_changed()

    def on_row_zoom_changed(self, value):
        """Handle row zoom change"""
        self._emit_viewport_changed()

    def on_col_zoom_changed(self, value):
        """Handle column zoom change"""
        self._emit_viewport_changed()
