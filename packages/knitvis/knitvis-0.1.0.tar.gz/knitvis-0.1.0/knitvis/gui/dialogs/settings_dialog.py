from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                             QWidget, QCheckBox, QLabel, QSlider, QPushButton,
                             QGroupBox, QFormLayout, QSpinBox, QComboBox,
                             QDoubleSpinBox)
from PyQt5.QtCore import Qt, pyqtSignal


class SettingsDialog(QDialog):
    """Global settings dialog for the application"""

    # Signal emitted when settings have been applied
    settingsApplied = pyqtSignal()

    def __init__(self, parent=None, settings_manager=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.setWindowTitle("Settings")
        self.setMinimumWidth(450)
        self.init_ui()

    def init_ui(self):
        """Initialize the settings dialog UI"""
        layout = QVBoxLayout(self)

        # Create tabs for different settings categories
        self.tabs = QTabWidget()
        self.general_tab = QWidget()
        self.chart_tab = QWidget()
        self.fabric_tab = QWidget()

        self.tabs.addTab(self.general_tab, "General")
        self.tabs.addTab(self.chart_tab, "Chart View")
        self.tabs.addTab(self.fabric_tab, "Fabric View")

        # Set up the general settings tab
        self.setup_general_tab()

        # Set up the chart view tab
        self.setup_chart_tab()

        # Set up the fabric view tab
        self.setup_fabric_tab()

        layout.addWidget(self.tabs)

        # Buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        self.apply_button = QPushButton("Apply")
        self.reset_button = QPushButton("Reset to Defaults")

        self.ok_button.clicked.connect(self.accept_settings)
        self.cancel_button.clicked.connect(self.reject)
        self.apply_button.clicked.connect(self.apply_settings)
        self.reset_button.clicked.connect(self.reset_settings)

        button_layout.addWidget(self.reset_button)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.apply_button)

        layout.addLayout(button_layout)

    def setup_general_tab(self):
        """Set up the general settings tab with options common to all views"""
        layout = QVBoxLayout(self.general_tab)

        # Display options
        display_group = QGroupBox("Display Options")
        display_layout = QFormLayout()

        self.show_row_numbers = QCheckBox()
        self.show_row_numbers.setChecked(
            self.settings_manager.get('show_row_numbers', True))
        display_layout.addRow("Show Row Numbers:", self.show_row_numbers)

        self.show_col_numbers = QCheckBox()
        self.show_col_numbers.setChecked(
            self.settings_manager.get('show_col_numbers', True))
        display_layout.addRow("Show Column Numbers:", self.show_col_numbers)

        # Add general opacity control
        self.opacity = QDoubleSpinBox()
        self.opacity.setRange(0.1, 1.0)
        self.opacity.setSingleStep(0.05)
        self.opacity.setDecimals(2)
        self.opacity.setValue(self.settings_manager.get('opacity', 1.0))
        display_layout.addRow("Default Opacity:", self.opacity)

        # Add tick frequency controls
        self.x_axis_ticks_every_n = QSpinBox()
        self.x_axis_ticks_every_n.setRange(1, 10)
        self.x_axis_ticks_every_n.setValue(
            self.settings_manager.get('x_axis_ticks_every_n', 1))
        display_layout.addRow("Column Tick Every:", self.x_axis_ticks_every_n)

        self.y_axis_ticks_every_n = QSpinBox()
        self.y_axis_ticks_every_n.setRange(1, 10)
        self.y_axis_ticks_every_n.setValue(
            self.settings_manager.get('y_axis_ticks_every_n', 1))
        display_layout.addRow("Row Tick Every:", self.y_axis_ticks_every_n)

        self.x_axis_ticks_numbers_every_n_tics = QSpinBox()
        self.x_axis_ticks_numbers_every_n_tics.setRange(1, 10)
        self.x_axis_ticks_numbers_every_n_tics.setValue(
            self.settings_manager.get('x_axis_ticks_numbers_every_n_tics', 1))
        display_layout.addRow("Column Number Every:",
                              self.x_axis_ticks_numbers_every_n_tics)

        self.y_axis_ticks_numbers_every_n_ticks = QSpinBox()
        self.y_axis_ticks_numbers_every_n_ticks.setRange(1, 10)
        self.y_axis_ticks_numbers_every_n_ticks.setValue(
            self.settings_manager.get('y_axis_ticks_numbers_every_n_ticks', 1))
        display_layout.addRow("Row Number Every:",
                              self.y_axis_ticks_numbers_every_n_ticks)

        display_group.setLayout(display_layout)
        layout.addWidget(display_group)

        # Navigation options
        nav_group = QGroupBox("Navigation Defaults")
        nav_layout = QFormLayout()

        self.default_row_zoom = QSpinBox()
        self.default_row_zoom.setRange(5, 100)
        self.default_row_zoom.setValue(
            self.settings_manager.get('default_row_zoom', 20))
        nav_layout.addRow("Default Row Zoom:", self.default_row_zoom)

        self.default_col_zoom = QSpinBox()
        self.default_col_zoom.setRange(5, 100)
        self.default_col_zoom.setValue(
            self.settings_manager.get('default_col_zoom', 20))
        nav_layout.addRow("Default Column Zoom:", self.default_col_zoom)

        nav_group.setLayout(nav_layout)
        layout.addWidget(nav_group)

        # Add background image section
        bg_group = QGroupBox("Background Image")
        bg_layout = QFormLayout()

        self.background_image_enabled = QCheckBox()
        self.background_image_enabled.setChecked(
            self.settings_manager.get('background_image_enabled', False))
        bg_layout.addRow("Enable Default Background:",
                         self.background_image_enabled)

        self.background_image_button = QPushButton(
            "Configure Background Image...")
        self.background_image_button.clicked.connect(
            self.configure_background_image)
        bg_layout.addRow("", self.background_image_button)

        bg_group.setLayout(bg_layout)
        layout.addWidget(bg_group)

        layout.addStretch(1)

    def setup_chart_tab(self):
        """Set up chart view settings tab"""
        layout = QVBoxLayout(self.chart_tab)

        # Appearance options
        appearance_group = QGroupBox("Chart Appearance")
        appearance_layout = QFormLayout()

        self.chart_cell_border = QCheckBox()
        self.chart_cell_border.setChecked(
            self.settings_manager.get('chart_cell_border', True))
        appearance_layout.addRow("Show Cell Borders:", self.chart_cell_border)

        self.chart_symbol_size = QSpinBox()
        self.chart_symbol_size.setRange(0, 24)  # Allow 0 to hide symbols
        self.chart_symbol_size.setValue(
            self.settings_manager.get('chart_symbol_size', 12))
        appearance_layout.addRow(
            "Symbol Size (0 to hide):", self.chart_symbol_size)

        # Remove the checkbox connection code

        # Add chart-specific opacity control
        self.chart_opacity = QDoubleSpinBox()
        self.chart_opacity.setRange(0.1, 1.0)
        self.chart_opacity.setSingleStep(0.05)
        self.chart_opacity.setDecimals(2)
        self.chart_opacity.setValue(
            self.settings_manager.get('chart_opacity', 1.0))
        appearance_layout.addRow("Chart Opacity:", self.chart_opacity)

        appearance_group.setLayout(appearance_layout)
        layout.addWidget(appearance_group)

        # Add chart-specific background image settings
        bg_group = QGroupBox("Chart Background Image")
        bg_layout = QFormLayout()

        self.chart_background_image_enabled = QCheckBox()
        self.chart_background_image_enabled.setChecked(
            self.settings_manager.get('chart_background_image_enabled', False))
        bg_layout.addRow("Enable Chart Background:",
                         self.chart_background_image_enabled)

        self.chart_background_image_button = QPushButton(
            "Configure Chart Background...")
        self.chart_background_image_button.clicked.connect(
            lambda: self.configure_background_image('chart'))
        bg_layout.addRow("", self.chart_background_image_button)

        bg_group.setLayout(bg_layout)
        layout.addWidget(bg_group)

        layout.addStretch(1)

    def setup_fabric_tab(self):
        """Set up fabric view settings tab"""
        layout = QVBoxLayout(self.fabric_tab)

        # Stitch options
        stitch_group = QGroupBox("Stitch Appearance")
        stitch_layout = QFormLayout()

        self.fabric_show_outlines = QCheckBox()
        self.fabric_show_outlines.setChecked(
            self.settings_manager.get('fabric_show_outlines', False))
        stitch_layout.addRow("Show Stitch Outlines:",
                             self.fabric_show_outlines)

        # Use direct value for row spacing
        self.fabric_row_spacing = QDoubleSpinBox()
        self.fabric_row_spacing.setRange(0.1, 1.0)
        self.fabric_row_spacing.setSingleStep(0.05)
        self.fabric_row_spacing.setDecimals(2)
        # Get direct value
        self.fabric_row_spacing.setValue(
            self.settings_manager.get('fabric_row_spacing', 0.7))
        stitch_layout.addRow("Row Spacing:", self.fabric_row_spacing)

        # Add padding control
        self.fabric_padding = QDoubleSpinBox()
        self.fabric_padding.setRange(0.001, 0.1)
        self.fabric_padding.setSingleStep(0.005)
        self.fabric_padding.setDecimals(3)
        self.fabric_padding.setValue(
            self.settings_manager.get('fabric_padding', 0.01))
        stitch_layout.addRow("Stitch Padding:", self.fabric_padding)

        # Add fabric-specific opacity control
        self.fabric_opacity = QDoubleSpinBox()
        self.fabric_opacity.setRange(0.1, 1.0)
        self.fabric_opacity.setSingleStep(0.05)
        self.fabric_opacity.setDecimals(2)
        self.fabric_opacity.setValue(
            self.settings_manager.get('fabric_opacity', 1.0))
        stitch_layout.addRow("Fabric Opacity:", self.fabric_opacity)

        stitch_group.setLayout(stitch_layout)
        layout.addWidget(stitch_group)

        # Add fabric-specific background image settings
        bg_group = QGroupBox("Fabric Background Image")
        bg_layout = QFormLayout()

        self.fabric_background_image_enabled = QCheckBox()
        self.fabric_background_image_enabled.setChecked(
            self.settings_manager.get('fabric_background_image_enabled', False))
        bg_layout.addRow("Enable Fabric Background:",
                         self.fabric_background_image_enabled)

        self.fabric_background_image_button = QPushButton(
            "Configure Fabric Background...")
        self.fabric_background_image_button.clicked.connect(
            lambda: self.configure_background_image('fabric'))
        bg_layout.addRow("", self.fabric_background_image_button)

        bg_group.setLayout(bg_layout)
        layout.addWidget(bg_group)

        layout.addStretch(1)

    def configure_background_image(self, view_type=None):
        """Open the background image configuration dialog"""
        from knitvis.gui.dialogs.background_image_dialog import BackgroundImageDialog

        # Determine which settings to use based on view_type
        if view_type == 'chart':
            prefix = 'chart_'
        elif view_type == 'fabric':
            prefix = 'fabric_'
        else:
            prefix = ''

        current_settings = {
            'background_image_enabled': self.settings_manager.get(f'{prefix}background_image_enabled', False),
            'background_image_path': self.settings_manager.get(f'{prefix}background_image_path', ''),
            'background_image_opacity': self.settings_manager.get(f'{prefix}background_image_opacity', 0.3),
        }

        dialog = BackgroundImageDialog(self, current_settings)
        dialog.settingsApplied.connect(
            lambda settings: self.apply_bg_settings(settings, prefix))

        if dialog.exec_():
            # Settings were accepted
            pass

    def apply_bg_settings(self, settings, prefix=''):
        """Apply background image settings from the dialog"""
        # Store settings based on the prefix (general, chart, or fabric)
        for key, value in settings.items():
            self.settings_manager.set(f'{prefix}{key}', value)

        # Update the corresponding checkbox
        if prefix == 'chart_':
            self.chart_background_image_enabled.setChecked(
                settings['background_image_enabled'])
        elif prefix == 'fabric_':
            self.fabric_background_image_enabled.setChecked(
                settings['background_image_enabled'])
        else:
            self.background_image_enabled.setChecked(
                settings['background_image_enabled'])

        # Signal that settings have changed
        self.settingsApplied.emit()

    def gather_settings(self):
        """Gather all settings from the dialog into a dictionary"""
        return {
            # General settings
            'show_row_numbers': self.show_row_numbers.isChecked(),
            'show_col_numbers': self.show_col_numbers.isChecked(),
            'default_row_zoom': self.default_row_zoom.value(),
            'default_col_zoom': self.default_col_zoom.value(),
            'opacity': self.opacity.value(),  # General opacity
            'x_axis_ticks_every_n': self.x_axis_ticks_every_n.value(),
            'y_axis_ticks_every_n': self.y_axis_ticks_every_n.value(),
            'x_axis_ticks_numbers_every_n_tics': self.x_axis_ticks_numbers_every_n_tics.value(),
            'y_axis_ticks_numbers_every_n_ticks': self.y_axis_ticks_numbers_every_n_ticks.value(),
            'background_image_enabled': self.background_image_enabled.isChecked(),
            # We don't change path and opacity here because they're managed by the background image dialog

            # Chart view settings
            'chart_cell_border': self.chart_cell_border.isChecked(),
            # Remove chart_show_symbols setting
            'chart_symbol_size': self.chart_symbol_size.value(),
            'chart_opacity': self.chart_opacity.value(),  # Chart-specific opacity
            'chart_background_image_enabled': self.chart_background_image_enabled.isChecked(),
            # We don't change path and opacity here because they're managed by the background image dialog

            # Fabric view settings
            'fabric_show_outlines': self.fabric_show_outlines.isChecked(),
            'fabric_row_spacing': self.fabric_row_spacing.value(),
            'fabric_padding': self.fabric_padding.value(),
            'fabric_opacity': self.fabric_opacity.value(),  # Fabric-specific opacity
            'fabric_background_image_enabled': self.fabric_background_image_enabled.isChecked(),
            # We don't change path and opacity here because they're managed by the background image dialog
        }

    def accept_settings(self):
        """Apply settings and close dialog"""
        self.apply_settings()
        self.accept()

    def apply_settings(self):
        """Apply the current settings"""
        settings = self.gather_settings()
        self.settings_manager.update(settings)
        self.settingsApplied.emit()

    def reset_settings(self):
        """Reset to default settings"""
        if self.settings_manager:
            self.settings_manager.reset()

            # Update dialog controls with new values
            self.show_row_numbers.setChecked(
                self.settings_manager.get('show_row_numbers'))
            self.show_col_numbers.setChecked(
                self.settings_manager.get('show_col_numbers'))
            self.opacity.setValue(self.settings_manager.get(
                'opacity'))  # General opacity
            self.default_row_zoom.setValue(
                self.settings_manager.get('default_row_zoom'))
            self.default_col_zoom.setValue(
                self.settings_manager.get('default_col_zoom'))

            # Update tick controls
            self.x_axis_ticks_every_n.setValue(
                self.settings_manager.get('x_axis_ticks_every_n'))
            self.y_axis_ticks_every_n.setValue(
                self.settings_manager.get('y_axis_ticks_every_n'))
            self.x_axis_ticks_numbers_every_n_tics.setValue(
                self.settings_manager.get('x_axis_ticks_numbers_every_n_tics'))
            self.y_axis_ticks_numbers_every_n_ticks.setValue(
                self.settings_manager.get('y_axis_ticks_numbers_every_n_ticks'))

            # Chart settings
            self.chart_cell_border.setChecked(
                self.settings_manager.get('chart_cell_border'))
            # Remove chart_show_symbols reset
            self.chart_symbol_size.setValue(
                self.settings_manager.get('chart_symbol_size'))
            self.chart_opacity.setValue(
                self.settings_manager.get('chart_opacity'))  # Chart opacity

            # Fabric settings
            self.fabric_show_outlines.setChecked(
                self.settings_manager.get('fabric_show_outlines'))
            self.fabric_row_spacing.setValue(
                self.settings_manager.get('fabric_row_spacing'))
            self.fabric_padding.setValue(
                self.settings_manager.get('fabric_padding'))
            self.fabric_opacity.setValue(
                self.settings_manager.get('fabric_opacity'))  # Fabric opacity

            # Update background image checkboxes
            self.background_image_enabled.setChecked(
                self.settings_manager.get('background_image_enabled'))
            self.chart_background_image_enabled.setChecked(
                self.settings_manager.get('chart_background_image_enabled'))
            self.fabric_background_image_enabled.setChecked(
                self.settings_manager.get('fabric_background_image_enabled'))

            self.settingsApplied.emit()
