#!/usr/bin/env python3
"""
Pixabay Sound Effects GUI (Qt Version)
Search, preview, and download sound effects from Pixabay
"""

import os
import re
import sys
import time
import threading
import tempfile
from pathlib import Path
import requests

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QProgressBar, QFileDialog, QSpinBox, QMessageBox, QHeaderView,
    QFrame, QSplitter
)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl
from PyQt6.QtGui import QFont, QPalette, QColor

try:
    from pygame import mixer
    PYGAME_AVAILABLE = True
    mixer.init()
except ImportError:
    PYGAME_AVAILABLE = False
    print("Warning: pygame not available. Install with: pip install pygame")

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("Warning: Selenium not available. Install with: pip install selenium")


class SearchWorker(QThread):
    """Background worker for searching"""
    result_found = pyqtSignal(dict)
    search_complete = pyqtSignal(bool, str)
    status_update = pyqtSignal(str)
    
    def __init__(self, search_term, max_results):
        super().__init__()
        self.search_term = search_term
        self.max_results = max_results
        self.driver = None
    
    def run(self):
        try:
            self.setup_driver()
            if not self.driver:
                self.search_complete.emit(False, "Failed to initialize browser")
                return
            
            url = f"https://pixabay.com/sound-effects/search/{self.search_term}/"
            self.status_update.emit(f"Loading {url}...")
            self.driver.get(url)
            time.sleep(3)
            
            sound_rows = self.driver.find_elements(By.CSS_SELECTOR, 'div.audioRow--nAm4Z')
            
            for i, row in enumerate(sound_rows[:self.max_results]):
                try:
                    title_elem = row.find_element(By.CSS_SELECTOR, 'a.title--7N7Nr')
                    title = title_elem.text.strip()
                    detail_url = title_elem.get_attribute('href')
                    
                    try:
                        author_elem = row.find_element(By.CSS_SELECTOR, 'a.name--yfZpi')
                        author = author_elem.text.strip()
                    except:
                        author = "Unknown"
                    
                    self.result_found.emit({
                        'title': title,
                        'author': author,
                        'url': detail_url,
                        'download_url': None
                    })
                    self.status_update.emit(f"Found: {title}")
                except Exception as e:
                    continue
            
            self.search_complete.emit(True, f"Found {min(len(sound_rows), self.max_results)} sounds")
            
        except Exception as e:
            self.search_complete.emit(False, f"Error: {str(e)}")
        finally:
            self.cleanup_driver()
    
    def setup_driver(self):
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            self.driver = webdriver.Chrome(options=options)
        except Exception as e:
            print(f"Driver error: {e}")
            self.driver = None
    
    def cleanup_driver(self):
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None


class DownloadWorker(QThread):
    """Background worker for downloading"""
    progress_update = pyqtSignal(int, str)
    download_complete = pyqtSignal(bool, str)
    status_update = pyqtSignal(str)
    url_found = pyqtSignal(int, str)
    
    def __init__(self, sounds, indices, output_dir):
        super().__init__()
        self.sounds = sounds
        self.indices = indices
        self.output_dir = Path(output_dir)
        self.driver = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
    
    def run(self):
        try:
            self.setup_driver()
            
            for i, idx in enumerate(self.indices):
                sound = self.sounds[idx]
                self.status_update.emit(f"[{i+1}/{len(self.indices)}] {sound['title']}")
                self.progress_update.emit(idx, "Downloading...")
                
                # Get URL if needed
                if not sound.get('download_url'):
                    url = self.get_download_url(sound['url'])
                    if url:
                        self.sounds[idx]['download_url'] = url
                        self.url_found.emit(idx, url)
                
                download_url = self.sounds[idx].get('download_url')
                if not download_url:
                    self.progress_update.emit(idx, "❌ Failed")
                    continue
                
                # Download
                filename = self.sanitize_filename(f"{sound['title']}_{sound['author']}.mp3")
                filepath = self.output_dir / filename
                
                if filepath.exists():
                    self.progress_update.emit(idx, "📁 Exists")
                    continue
                
                response = self.session.get(download_url)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    self.progress_update.emit(idx, "✅ Done")
                else:
                    self.progress_update.emit(idx, "❌ Failed")
                
                time.sleep(1)
            
            self.download_complete.emit(True, f"Downloaded to: {self.output_dir}")
            
        except Exception as e:
            self.download_complete.emit(False, str(e))
        finally:
            self.cleanup_driver()
    
    def get_download_url(self, detail_url):
        try:
            if not self.driver:
                return None
            self.driver.get(detail_url)
            time.sleep(2)
            
            page_source = self.driver.page_source
            mp3_matches = re.findall(r'https://[^\s"\'<>]+\.mp3', page_source)
            
            for url in mp3_matches:
                if 'cdn.pixabay.com' in url:
                    return url
            return mp3_matches[0] if mp3_matches else None
        except:
            return None
    
    def setup_driver(self):
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            self.driver = webdriver.Chrome(options=options)
        except:
            self.driver = None
    
    def cleanup_driver(self):
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
    
    def sanitize_filename(self, filename):
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = filename.replace(' ', '_')
        return filename[:200] if len(filename) > 200 else filename


class PixabaySoundGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎵 Pixabay Sound Effects")
        self.setMinimumSize(1000, 700)
        self.resize(1100, 750)
        
        # State
        self.results = []
        self.search_worker = None
        self.download_worker = None
        self.download_dir = Path("sound_effects")
        self.download_dir.mkdir(exist_ok=True)
        
        # Audio player
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.8)
        
        # Session for downloads
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        
        # Setup UI
        self.setup_theme()
        self.setup_ui()
    
    def setup_theme(self):
        """Apply dark theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a2e;
            }
            QWidget {
                background-color: #1a1a2e;
                color: #eaeaea;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }
            QLabel {
                color: #eaeaea;
            }
            QLineEdit {
                background-color: #16213e;
                border: 2px solid #0f3460;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #eaeaea;
            }
            QLineEdit:focus {
                border-color: #e94560;
            }
            QPushButton {
                background-color: #e94560;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff6b6b;
            }
            QPushButton:pressed {
                background-color: #c73e54;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
            }
            QPushButton#secondaryBtn {
                background-color: #0f3460;
            }
            QPushButton#secondaryBtn:hover {
                background-color: #1a4a7a;
            }
            QPushButton#successBtn {
                background-color: #4ecca3;
                color: #1a1a2e;
            }
            QPushButton#successBtn:hover {
                background-color: #5fd9b0;
            }
            QTableWidget {
                background-color: #16213e;
                border: 2px solid #0f3460;
                border-radius: 8px;
                gridline-color: #0f3460;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #0f3460;
            }
            QTableWidget::item:selected {
                background-color: #e94560;
            }
            QHeaderView::section {
                background-color: #0f3460;
                color: #eaeaea;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
            QScrollBar:vertical {
                background-color: #16213e;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #0f3460;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #e94560;
            }
            QProgressBar {
                background-color: #16213e;
                border: none;
                border-radius: 4px;
                height: 6px;
            }
            QProgressBar::chunk {
                background-color: #e94560;
                border-radius: 4px;
            }
            QSpinBox {
                background-color: #16213e;
                border: 2px solid #0f3460;
                border-radius: 6px;
                padding: 8px;
                color: #eaeaea;
            }
        """)
    
    def setup_ui(self):
        """Create UI layout"""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("🎵 Pixabay Sound Effects")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: #e94560;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_layout.setSpacing(15)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term (e.g., swoosh, click, pop)...")
        self.search_input.setText("swoosh")
        self.search_input.returnPressed.connect(self.start_search)
        search_layout.addWidget(self.search_input, stretch=3)
        
        # Max results spinner
        max_label = QLabel("Max:")
        max_label.setStyleSheet("color: #a0a0a0;")
        search_layout.addWidget(max_label)
        
        self.max_spin = QSpinBox()
        self.max_spin.setRange(5, 50)
        self.max_spin.setValue(20)
        self.max_spin.setSingleStep(5)
        search_layout.addWidget(self.max_spin)
        
        self.search_btn = QPushButton("🔍 Search")
        self.search_btn.clicked.connect(self.start_search)
        self.search_btn.setFixedWidth(140)
        search_layout.addWidget(self.search_btn)
        
        layout.addLayout(search_layout)
        
        # Results table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Title", "Author", "Status", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.doubleClicked.connect(self.play_selected)
        layout.addWidget(self.table, stretch=1)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        self.play_btn = QPushButton("▶️ Play")
        self.play_btn.setObjectName("successBtn")
        self.play_btn.clicked.connect(self.play_selected)
        self.play_btn.setFixedWidth(120)
        btn_layout.addWidget(self.play_btn)
        
        self.stop_btn = QPushButton("⏹️ Stop")
        self.stop_btn.setObjectName("secondaryBtn")
        self.stop_btn.clicked.connect(self.stop_playback)
        self.stop_btn.setFixedWidth(120)
        btn_layout.addWidget(self.stop_btn)
        
        btn_layout.addStretch()
        
        self.download_btn = QPushButton("⬇️ Download Selected")
        self.download_btn.clicked.connect(self.download_selected)
        self.download_btn.setFixedWidth(180)
        btn_layout.addWidget(self.download_btn)
        
        self.download_all_btn = QPushButton("⬇️ Download All")
        self.download_all_btn.setObjectName("secondaryBtn")
        self.download_all_btn.clicked.connect(self.download_all)
        self.download_all_btn.setFixedWidth(160)
        btn_layout.addWidget(self.download_all_btn)
        
        layout.addLayout(btn_layout)
        
        # Output directory
        dir_layout = QHBoxLayout()
        dir_layout.setSpacing(10)
        
        dir_label = QLabel("📁 Output:")
        dir_label.setStyleSheet("color: #a0a0a0;")
        dir_layout.addWidget(dir_label)
        
        self.dir_input = QLineEdit()
        self.dir_input.setText(str(self.download_dir.absolute()))
        dir_layout.addWidget(self.dir_input, stretch=1)
        
        browse_btn = QPushButton("Browse")
        browse_btn.setObjectName("secondaryBtn")
        browse_btn.clicked.connect(self.browse_directory)
        browse_btn.setFixedWidth(100)
        dir_layout.addWidget(browse_btn)
        
        layout.addLayout(dir_layout)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setMaximum(0)
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # Status bar
        self.status = QLabel("Ready. Enter a search term and click Search.")
        self.status.setStyleSheet("""
            background-color: #16213e;
            padding: 12px;
            border-radius: 6px;
            color: #a0a0a0;
        """)
        layout.addWidget(self.status)
    
    def browse_directory(self):
        """Open directory picker"""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory", str(self.download_dir))
        if dir_path:
            self.download_dir = Path(dir_path)
            self.dir_input.setText(str(self.download_dir.absolute()))
    
    def start_search(self):
        """Start background search"""
        if self.search_worker and self.search_worker.isRunning():
            return
        
        search_term = self.search_input.text().strip()
        if not search_term:
            QMessageBox.warning(self, "Warning", "Please enter a search term")
            return
        
        if not SELENIUM_AVAILABLE:
            QMessageBox.critical(self, "Error", "Selenium is not installed.\nInstall with: pip install selenium")
            return
        
        # Clear previous results
        self.table.setRowCount(0)
        self.results = []
        
        # Start search
        self.search_btn.setEnabled(False)
        self.progress.setVisible(True)
        self.status.setText(f"Searching for '{search_term}'...")
        
        self.search_worker = SearchWorker(search_term, self.max_spin.value())
        self.search_worker.result_found.connect(self.add_result)
        self.search_worker.search_complete.connect(self.search_complete)
        self.search_worker.status_update.connect(lambda s: self.status.setText(s))
        self.search_worker.start()
    
    def add_result(self, sound):
        """Add a result to the table"""
        self.results.append(sound)
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        self.table.setItem(row, 0, QTableWidgetItem(sound['title']))
        self.table.setItem(row, 1, QTableWidgetItem(sound['author']))
        self.table.setItem(row, 2, QTableWidgetItem("Ready"))
        
        # Play button in actions column
        play_btn = QPushButton("▶️")
        play_btn.setFixedSize(40, 30)
        play_btn.setStyleSheet("""
            QPushButton {
                background-color: #4ecca3;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #5fd9b0;
            }
        """)
        play_btn.clicked.connect(lambda checked, r=row: self.play_row(r))
        self.table.setCellWidget(row, 3, play_btn)
    
    def search_complete(self, success, message):
        """Handle search completion"""
        self.search_btn.setEnabled(True)
        self.progress.setVisible(False)
        self.status.setText(message)
        
        if not success:
            QMessageBox.critical(self, "Search Error", message)
    
    def play_row(self, row):
        """Play sound at specific row"""
        if row >= len(self.results):
            return
        self.table.selectRow(row)
        self.play_selected()
    
    def play_selected(self):
        """Play the selected sound"""
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            QMessageBox.warning(self, "Warning", "Please select a sound to play")
            return
        
        row = rows[0].row()
        if row >= len(self.results):
            return
        
        sound = self.results[row]
        self.status.setText(f"Getting preview for: {sound['title']}...")
        
        # Get and play in background thread
        thread = threading.Thread(target=self._do_play, args=(row,))
        thread.daemon = True
        thread.start()
    
    def _do_play(self, row):
        """Get and play sound (background)"""
        try:
            sound = self.results[row]
            
            # Get download URL if not cached
            if not sound.get('download_url'):
                driver = None
                try:
                    options = Options()
                    options.add_argument('--headless')
                    options.add_argument('--no-sandbox')
                    options.add_argument('--disable-dev-shm-usage')
                    options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64)')
                    options.add_experimental_option("excludeSwitches", ["enable-automation"])
                    driver = webdriver.Chrome(options=options)
                    
                    driver.get(sound['url'])
                    time.sleep(2)
                    
                    page_source = driver.page_source
                    mp3_matches = re.findall(r'https://[^\s"\'<>]+\.mp3', page_source)
                    
                    for url in mp3_matches:
                        if 'cdn.pixabay.com' in url:
                            self.results[row]['download_url'] = url
                            break
                    
                    if not self.results[row].get('download_url') and mp3_matches:
                        self.results[row]['download_url'] = mp3_matches[0]
                        
                finally:
                    if driver:
                        driver.quit()
            
            download_url = self.results[row].get('download_url')
            if not download_url:
                self.status.setText("Could not get audio URL")
                return
            
            # Download to temp file
            response = self.session.get(download_url)
            if response.status_code == 200:
                temp_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
                temp_file.write(response.content)
                temp_file.close()
                
                # Play using Qt
                self.player.setSource(QUrl.fromLocalFile(temp_file.name))
                self.player.play()
                self.status.setText(f"▶️ Playing: {sound['title']}")
                
        except Exception as e:
            print(f"Play error: {e}")
            self.status.setText(f"Play error: {str(e)}")
    
    def stop_playback(self):
        """Stop audio playback"""
        self.player.stop()
        self.status.setText("Playback stopped")
    
    def download_selected(self):
        """Download selected sounds"""
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            QMessageBox.warning(self, "Warning", "Please select sounds to download")
            return
        
        indices = [r.row() for r in rows]
        self._start_download(indices)
    
    def download_all(self):
        """Download all sounds"""
        if not self.results:
            QMessageBox.warning(self, "Warning", "No sounds to download. Search first.")
            return
        
        indices = list(range(len(self.results)))
        self._start_download(indices)
    
    def _start_download(self, indices):
        """Start download worker"""
        if self.download_worker and self.download_worker.isRunning():
            QMessageBox.warning(self, "Warning", "Download already in progress")
            return
        
        self.download_dir = Path(self.dir_input.text())
        self.download_dir.mkdir(exist_ok=True)
        
        self.download_btn.setEnabled(False)
        self.download_all_btn.setEnabled(False)
        self.progress.setVisible(True)
        
        self.download_worker = DownloadWorker(self.results, indices, self.download_dir)
        self.download_worker.progress_update.connect(self.update_row_status)
        self.download_worker.download_complete.connect(self.download_complete)
        self.download_worker.status_update.connect(lambda s: self.status.setText(s))
        self.download_worker.url_found.connect(lambda i, u: self.results.__setitem__(i, {**self.results[i], 'download_url': u}))
        self.download_worker.start()
    
    def update_row_status(self, row, status):
        """Update status column for a row"""
        if row < self.table.rowCount():
            self.table.setItem(row, 2, QTableWidgetItem(status))
    
    def download_complete(self, success, message):
        """Handle download completion"""
        self.download_btn.setEnabled(True)
        self.download_all_btn.setEnabled(True)
        self.progress.setVisible(False)
        self.status.setText(message)
        
        if success:
            QMessageBox.information(self, "Complete", message)
    
    def closeEvent(self, event):
        """Cleanup on close"""
        self.player.stop()
        if self.search_worker and self.search_worker.isRunning():
            self.search_worker.terminate()
        if self.download_worker and self.download_worker.isRunning():
            self.download_worker.terminate()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = PixabaySoundGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
