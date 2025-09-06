# -*- coding: utf-8 -*-
"""
Gelir/Gider Kayıt Modülü - PyQt5
Muhasebe odaklı, erişilebilir ve okunur arayüz
"""

import sys
import sqlite3
import csv
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QGroupBox, QLabel, QLineEdit, QComboBox, QDateEdit,
    QDoubleSpinBox, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView, QFileDialog, QAbstractItemView
)
from PyQt5.QtCore import Qt, QDate, QTimer
from PyQt5.QtGui import QFont, QPalette, QPixmap, QIcon


class IncomeExpenseWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1000, 700)
        
        # Logo'yu pencere ikonuna ayarla
        self.set_window_icon()
        
        # Anlık saat güncellemesi için timer başlat
        self.setup_title_timer()
        
        # Veritabanı bağlantısı
        self.init_database()
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(16, 16, 16, 16)
        
        # Form grubu
        self.create_form_group()
        main_layout.addWidget(self.form_group)
        
        # Tablo grubu
        self.create_table_group()
        main_layout.addWidget(self.table_group)
        
        # Özet bar
        self.create_summary_bar()
        main_layout.addWidget(self.summary_widget)
        
        # Stil uygula
        self.apply_styles()
        
        # Verileri yükle
        self.load_records()
        self.update_summary()
        
        # Sinyal bağlantıları
        self.connect_signals()
        
        # İlk belge numarası önizlemesi
        self.update_doc_number_preview()

    def set_window_icon(self):
        """Pencere ve taskbar ikonunu logo ile ayarla"""
        try:
            # Logo dosyasının yolunu belirle
            logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
            if os.path.exists(logo_path):
                # Logo'yu pencere ikonuna ayarla
                icon = QIcon(logo_path)
                self.setWindowIcon(icon)
                
                # Taskbar için de uygulama ikonunu ayarla
                QApplication.instance().setWindowIcon(icon)
                
                # Ana başlık bölümü için logo widget'ı oluştur
                self.logo_pixmap = QPixmap(logo_path)
                # Logo'yu uygun boyuta ölçekle (32x32 piksel)
                self.logo_pixmap = self.logo_pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            else:
                print("Logo dosyası bulunamadı:", logo_path)
        except Exception as e:
            print("Logo yüklenirken hata oluştu:", str(e))

    def setup_title_timer(self):
        """Pencere başlığında anlık saat için timer ayarla"""
        # Anlık saat güncellemesi için timer
        self.title_timer = QTimer()
        self.title_timer.timeout.connect(self.update_window_title)
        self.title_timer.start(1000)  # Her saniye güncelle
        
        # İlk güncelleme
        self.update_window_title()

    def update_window_title(self):
        """Pencere başlığını tarih ve saat ile güncelle"""
        now = datetime.now()
        title = f"AzGelir - {now.strftime('%d.%m.%Y %H:%M:%S')}"
        self.setWindowTitle(title)

    def init_database(self):
        """Veritabanını başlat"""
        self.conn = sqlite3.connect('records.db')
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                vat_rate REAL NOT NULL,
                vat_amount REAL NOT NULL,
                total_amount REAL NOT NULL,
                account TEXT NOT NULL,
                category TEXT NOT NULL,
                doc_no TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def create_form_group(self):
        """Form grubu oluştur"""
        self.form_group = QGroupBox("🧾 Yeni Kayıt")
        form_layout = QGridLayout(self.form_group)
        form_layout.setSpacing(8)
        form_layout.setContentsMargins(12, 12, 12, 12)
        
        # Tarih
        form_layout.addWidget(QLabel("Tarih:"), 0, 0)
        
        # Tarih seçimi için horizontal layout
        date_layout = QHBoxLayout()
        
        self.dateEdit = QDateEdit()
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setDate(QDate.currentDate())
        self.dateEdit.setDisplayFormat("dd.MM.yyyy")  # Türkçe tarih formatı
        self.dateEdit.setCalendarPopup(True)
        
        # Tarih aralığı ayarla (geçmişte 5 yıl, gelecekte 1 yıl)
        min_date = QDate.currentDate().addYears(-5)
        max_date = QDate.currentDate().addYears(1)
        self.dateEdit.setDateRange(min_date, max_date)
        
        date_layout.addWidget(self.dateEdit)
        
        # Hızlı tarih seçenekleri
        today_btn = QPushButton("Bugün")
        today_btn.setObjectName("todayBtn")
        today_btn.setMaximumWidth(60)
        today_btn.clicked.connect(lambda: self.dateEdit.setDate(QDate.currentDate()))
        date_layout.addWidget(today_btn)
        
        yesterday_btn = QPushButton("Dün")
        yesterday_btn.setObjectName("yesterdayBtn")
        yesterday_btn.setMaximumWidth(60)
        yesterday_btn.clicked.connect(lambda: self.dateEdit.setDate(QDate.currentDate().addDays(-1)))
        date_layout.addWidget(yesterday_btn)
        
        form_layout.addLayout(date_layout, 0, 1)
        
        # Tür
        form_layout.addWidget(QLabel("Tür:"), 0, 2)
        self.typeCombo = QComboBox()
        self.typeCombo.setObjectName("typeCombo")
        self.typeCombo.addItems(["Gelir", "Gider"])
        form_layout.addWidget(self.typeCombo, 0, 3)
        
        # Tutar
        form_layout.addWidget(QLabel("Tutar:"), 1, 0)
        self.amountEdit = QLineEdit()
        self.amountEdit.setObjectName("amountEdit")
        self.amountEdit.setPlaceholderText("0,00")
        self.amountEdit.setAlignment(Qt.AlignRight)
        form_layout.addWidget(self.amountEdit, 1, 1)
        
        # KDV (İsteğe bağlı)
        form_layout.addWidget(QLabel("KDV (İsteğe bağlı):"), 1, 2)
        self.vatCombo = QComboBox()
        self.vatCombo.setObjectName("vatCombo")
        self.vatCombo.addItems(["KDV Yok", "%1", "%10", "%18"])
        self.vatCombo.setCurrentText("KDV Yok")
        form_layout.addWidget(self.vatCombo, 1, 3)
        
        # Hesap
        form_layout.addWidget(QLabel("Hesap:"), 2, 0)
        self.accountCombo = QComboBox()
        self.accountCombo.setObjectName("accountCombo")
        self.accountCombo.addItems([
            "100 - Kasa",
            "101 - Alınan Çekler", 
            "102 - Banka",
            "120 - Alıcılar",
            "320 - Satıcılar"
        ])
        form_layout.addWidget(self.accountCombo, 2, 1)
        
        # Kategori
        form_layout.addWidget(QLabel("Kategori:"), 2, 2)
        self.categoryCombo = QComboBox()
        self.categoryCombo.setObjectName("categoryCombo")
        self.categoryCombo.addItems([
            "Satış", "Hizmet", "Kira", "Fatura", 
            "Ofis", "Maaş", "Diğer"
        ])
        form_layout.addWidget(self.categoryCombo, 2, 3)
        
        # Belge No (Otomatik)
        form_layout.addWidget(QLabel("Belge No (Otomatik):"), 3, 0)
        self.docNoEdit = QLineEdit()
        self.docNoEdit.setObjectName("docNoEdit")
        self.docNoEdit.setPlaceholderText("Otomatik oluşturulacak...")
        self.docNoEdit.setReadOnly(True)
        self.docNoEdit.setStyleSheet("background-color: #F3F4F6; color: #6B7280;")
        form_layout.addWidget(self.docNoEdit, 3, 1)
        
        # Açıklama
        form_layout.addWidget(QLabel("Açıklama:"), 3, 2)
        self.descEdit = QLineEdit()
        self.descEdit.setObjectName("descEdit")
        self.descEdit.setPlaceholderText("İşlem açıklaması…")
        form_layout.addWidget(self.descEdit, 3, 3)
        
        # Butonlar
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        self.saveBtn = QPushButton("Kaydet")
        self.saveBtn.setObjectName("saveBtn")
        self.saveBtn.setDefault(True)
        button_layout.addWidget(self.saveBtn)
        
        self.clearBtn = QPushButton("Temizle")
        self.clearBtn.setObjectName("clearBtn")
        button_layout.addWidget(self.clearBtn)
        
        self.deleteBtn = QPushButton("Sil")
        self.deleteBtn.setObjectName("deleteBtn")
        button_layout.addWidget(self.deleteBtn)
        
        self.exportBtn = QPushButton("Dışa Aktar (CSV)")
        self.exportBtn.setObjectName("exportBtn")
        button_layout.addWidget(self.exportBtn)
        
        button_layout.addStretch()
        form_layout.addLayout(button_layout, 4, 0, 1, 4)

    def create_table_group(self):
        """Tablo grubu oluştur"""
        self.table_group = QGroupBox("📊 Kayıtlar")
        table_layout = QVBoxLayout(self.table_group)
        table_layout.setContentsMargins(12, 12, 12, 12)
        
        # Filtre alanı
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Tarih Filtresi:"))
        
        self.filterStartDate = QDateEdit()
        self.filterStartDate.setDate(QDate.currentDate().addDays(-30))  # Son 30 gün
        self.filterStartDate.setDisplayFormat("dd.MM.yyyy")
        self.filterStartDate.setCalendarPopup(True)
        filter_layout.addWidget(self.filterStartDate)
        
        filter_layout.addWidget(QLabel("-"))
        
        self.filterEndDate = QDateEdit()
        self.filterEndDate.setDate(QDate.currentDate())
        self.filterEndDate.setDisplayFormat("dd.MM.yyyy")
        self.filterEndDate.setCalendarPopup(True)
        filter_layout.addWidget(self.filterEndDate)
        
        self.filterBtn = QPushButton("Filtrele")
        self.filterBtn.setObjectName("filterBtn")
        self.filterBtn.clicked.connect(self.load_records)
        filter_layout.addWidget(self.filterBtn)
        
        self.clearFilterBtn = QPushButton("Tümü")
        self.clearFilterBtn.setObjectName("clearFilterBtn")
        self.clearFilterBtn.clicked.connect(self.clear_filter)
        filter_layout.addWidget(self.clearFilterBtn)
        
        filter_layout.addStretch()
        table_layout.addLayout(filter_layout)
        
        self.recordsTable = QTableWidget()
        self.recordsTable.setObjectName("recordsTable")
        
        # Sütun başlıkları
        headers = ["Tarih", "Tür", "Tutar", "KDV", "Toplam", "Hesap", "Kategori", "Belge No", "Açıklama"]
        self.recordsTable.setColumnCount(len(headers))
        self.recordsTable.setHorizontalHeaderLabels(headers)
        
        # Tablo özellikleri
        self.recordsTable.setAlternatingRowColors(True)
        self.recordsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.recordsTable.setGridStyle(Qt.SolidLine)
        
        # Sütun genişlikleri
        header = self.recordsTable.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(len(headers)):
            if i in [2, 3, 4]:  # Tutar sütunları
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
            else:
                header.setSectionResizeMode(i, QHeaderView.Interactive)
        
        table_layout.addWidget(self.recordsTable)

    def create_summary_bar(self):
        """Özet bar oluştur"""
        self.summary_widget = QWidget()
        summary_layout = QHBoxLayout(self.summary_widget)
        summary_layout.setContentsMargins(12, 8, 12, 8)
        
        # Toplam Gelir
        summary_layout.addWidget(QLabel("Toplam Gelir:"))
        self.totalIncomeLbl = QLabel("0,00 ₺")
        self.totalIncomeLbl.setObjectName("totalIncomeLbl")
        summary_layout.addWidget(self.totalIncomeLbl)
        
        summary_layout.addSpacing(20)
        
        # Toplam Gider
        summary_layout.addWidget(QLabel("Toplam Gider:"))
        self.totalExpenseLbl = QLabel("0,00 ₺")
        self.totalExpenseLbl.setObjectName("totalExpenseLbl")
        summary_layout.addWidget(self.totalExpenseLbl)
        
        summary_layout.addSpacing(20)
        
        # Bakiye
        summary_layout.addWidget(QLabel("Bakiye:"))
        self.balanceLbl = QLabel("0,00 ₺")
        self.balanceLbl.setObjectName("balanceLbl")
        summary_layout.addWidget(self.balanceLbl)
        
        summary_layout.addStretch()

    def connect_signals(self):
        """Sinyal bağlantıları"""
        self.saveBtn.clicked.connect(self.save_record)
        self.clearBtn.clicked.connect(self.clear_form)
        self.deleteBtn.clicked.connect(self.delete_record)
        self.exportBtn.clicked.connect(self.export_csv)
        self.vatCombo.currentTextChanged.connect(self.calculate_totals)
        self.amountEdit.textChanged.connect(self.calculate_totals)
        self.typeCombo.currentTextChanged.connect(self.update_doc_number_preview)
        self.dateEdit.dateChanged.connect(self.update_doc_number_preview)

    def update_doc_number_preview(self):
        """Belge numarası önizlemesini güncelle"""
        record_type = self.typeCombo.currentText()
        date = self.dateEdit.date().toString("yyyy-MM-dd")
        preview_doc_no = self.generate_doc_number(record_type, date)
        self.docNoEdit.setText(preview_doc_no)

    def calculate_totals(self):
        """KDV ve toplam hesapla"""
        try:
            # Tutarı text'ten al ve Türkçe virgül formatını destekle
            amount_text = self.amountEdit.text().replace(",", ".")
            amount = float(amount_text) if amount_text else 0.0
        except ValueError:
            amount = 0.0
            
        vat_text = self.vatCombo.currentText()
        
        # KDV hesaplama - "KDV Yok" seçiliyse 0, diğer durumda % değerini al
        if vat_text == "KDV Yok":
            vat_rate = 0
        else:
            vat_rate = float(vat_text.replace("%", "")) / 100
        
        vat_amount = amount * vat_rate
        total_amount = amount + vat_amount
        
        # Hesaplanan değerleri göster (görsel geri bildirim için)
        if vat_rate > 0:
            self.amountEdit.setToolTip(f"KDV (%{vat_rate*100:.0f}): {vat_amount:.2f} ₺\nToplam: {total_amount:.2f} ₺")
        else:
            self.amountEdit.setToolTip(f"KDV Yok\nToplam: {total_amount:.2f} ₺")

    def generate_doc_number(self, record_type, date_str):
        """Otomatik belge numarası oluştur"""
        # Tür prefix'i
        prefix = "G" if record_type == "Gelir" else "F"  # Gelir veya Fatura
        
        # Tarih formatı (YYYYMMDD)
        date_part = date_str.replace("-", "")
        
        # O gün için sıralı numara
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM entries 
            WHERE date = ? AND type = ?
        """, (date_str, record_type))
        count = cursor.fetchone()[0] + 1
        
        # Belge numarası: G20250906001 veya F20250906001 formatında
        doc_number = f"{prefix}{date_part}{count:03d}"
        return doc_number

    def save_record(self):
        """Kayıt kaydet"""
        # Tutar doğrulama
        try:
            amount_text = self.amountEdit.text().replace(",", ".")
            amount = float(amount_text) if amount_text else 0.0
        except ValueError:
            QMessageBox.warning(self, "Uyarı", "Geçerli bir tutar giriniz!")
            return
            
        if amount < 0:
            QMessageBox.warning(self, "Uyarı", "Tutar negatif olamaz!")
            return
        
        # Değerleri al
        date = self.dateEdit.date().toString("yyyy-MM-dd")
        record_type = self.typeCombo.currentText()
        vat_text = self.vatCombo.currentText()
        
        # KDV hesaplama - "KDV Yok" seçiliyse 0, diğer durumda % değerini al
        if vat_text == "KDV Yok":
            vat_rate = 0
        else:
            vat_rate = float(vat_text.replace("%", "")) / 100
            
        vat_amount = amount * vat_rate
        total_amount = amount + vat_amount
        account = self.accountCombo.currentText()
        category = self.categoryCombo.currentText()
        
        # Otomatik belge numarası oluştur
        doc_no = self.generate_doc_number(record_type, date)
        description = self.descEdit.text().strip()
        
        # Veritabanına kaydet
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO entries (date, type, amount, vat_rate, vat_amount, 
                               total_amount, account, category, doc_no, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (date, record_type, amount, vat_rate, vat_amount, total_amount,
              account, category, doc_no, description))
        self.conn.commit()
        
        # Tabloyu güncelle
        self.load_records()
        self.update_summary()
        self.clear_form()
        
        QMessageBox.information(self, "Başarılı", "Kayıt başarıyla eklendi!")

    def clear_form(self):
        """Formu temizle"""
        self.dateEdit.setDate(QDate.currentDate())
        self.typeCombo.setCurrentText("Gelir")
        self.amountEdit.clear()  # Boş yap
        self.vatCombo.setCurrentText("KDV Yok")
        self.accountCombo.setCurrentIndex(0)
        self.categoryCombo.setCurrentIndex(0)
        self.descEdit.clear()
        # Belge numarası önizlemesini güncelle
        self.update_doc_number_preview()

    def delete_record(self):
        """Seçili kaydı sil"""
        current_row = self.recordsTable.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Uyarı", "Silinecek kayıt seçiniz!")
            return
        
        reply = QMessageBox.question(self, "Onay", "Seçili kaydı silmek istediğinizden emin misiniz?",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Seçili kayıtın ID'sini almak için veritabanından sorgula
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT id FROM entries ORDER BY date DESC, id DESC LIMIT 1 OFFSET ?
            ''', (current_row,))
            result = cursor.fetchone()
            
            if result:
                record_id = result[0]
                cursor.execute("DELETE FROM entries WHERE id = ?", (record_id,))
                self.conn.commit()
                
                # Tabloyu güncelle
                self.load_records()
                self.update_summary()
                QMessageBox.information(self, "Başarılı", "Kayıt başarıyla silindi!")
            else:
                QMessageBox.warning(self, "Hata", "Kayıt bulunamadı!")

    def export_csv(self):
        """CSV'ye aktar"""
        if self.recordsTable.rowCount() == 0:
            QMessageBox.warning(self, "Uyarı", "Aktarılacak kayıt bulunmuyor!")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "CSV Dosyası Kaydet", 
            f"gelir_gider_{datetime.now().strftime('%Y%m%d')}.csv",
            "CSV Files (*.csv)"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    
                    # Başlık satırı
                    headers = []
                    for col in range(self.recordsTable.columnCount()):
                        headers.append(self.recordsTable.horizontalHeaderItem(col).text())
                    writer.writerow(headers)
                    
                    # Veri satırları
                    for row in range(self.recordsTable.rowCount()):
                        row_data = []
                        for col in range(self.recordsTable.columnCount()):
                            item = self.recordsTable.item(row, col)
                            row_data.append(item.text() if item else "")
                        writer.writerow(row_data)
                
                QMessageBox.information(self, "Başarılı", f"Veriler {filename} dosyasına aktarıldı!")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Dosya kaydedilemedi: {str(e)}")

    def clear_filter(self):
        """Tarih filtresini temizle ve tüm kayıtları göster"""
        self.filterStartDate.setDate(QDate.currentDate().addYears(-5))
        self.filterEndDate.setDate(QDate.currentDate().addYears(1))
        self.load_records()

    def load_records(self):
        """Kayıtları yükle (tarih filtresi ile)"""
        cursor = self.conn.cursor()
        
        # Tarih filtresi kontrolü
        start_date = self.filterStartDate.date().toString("yyyy-MM-dd")
        end_date = self.filterEndDate.date().toString("yyyy-MM-dd")
        
        cursor.execute('''
            SELECT date, type, amount, vat_amount, total_amount, 
                   account, category, doc_no, description 
            FROM entries 
            WHERE date BETWEEN ? AND ?
            ORDER BY date DESC, id DESC
        ''', (start_date, end_date))
        records = cursor.fetchall()
        
        self.recordsTable.setRowCount(len(records))
        
        for row, record in enumerate(records):
            for col, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                
                # Tarih formatı (ilk sütun)
                if col == 0:  # Tarih sütunu
                    try:
                        # Veritabanından gelen tarihi parse et ve Türkçe formatına çevir
                        date_obj = datetime.strptime(str(value), "%Y-%m-%d")
                        formatted_date = date_obj.strftime("%d.%m.%Y")
                        item.setText(formatted_date)
                    except:
                        item.setText(str(value))  # Hata durumunda orijinal değeri göster
                        
                # Para formatı
                elif col in [2, 3, 4]:  # Tutar sütunları
                    item.setText(f"{float(value):,.2f} ₺")
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                
                self.recordsTable.setItem(row, col, item)

    def update_summary(self):
        """Özet bilgileri güncelle"""
        cursor = self.conn.cursor()
        
        # Toplam gelir
        cursor.execute("SELECT SUM(total_amount) FROM entries WHERE type = 'Gelir'")
        total_income = cursor.fetchone()[0] or 0
        
        # Toplam gider
        cursor.execute("SELECT SUM(total_amount) FROM entries WHERE type = 'Gider'")
        total_expense = cursor.fetchone()[0] or 0
        
        # Bakiye
        balance = total_income - total_expense
        
        # Etiketleri güncelle
        self.totalIncomeLbl.setText(f"{total_income:,.2f} ₺")
        self.totalExpenseLbl.setText(f"{total_expense:,.2f} ₺")
        self.balanceLbl.setText(f"{balance:,.2f} ₺")
        
        # Bakiye rengini ayarla
        if balance > 0:
            self.balanceLbl.setStyleSheet("color: #10B981; font-weight: bold;")
        elif balance < 0:
            self.balanceLbl.setStyleSheet("color: #EF4444; font-weight: bold;")
        else:
            self.balanceLbl.setStyleSheet("color: #6B7280; font-weight: bold;")

    def apply_styles(self):
        """Stil uygula"""
        style = """
        QMainWindow {
            background-color: #FFFFFF;
            color: #111111;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #E5E7EB;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            color: #374151;
        }
        
        QLabel {
            color: #111111;
            font-weight: 500;
        }
        
        QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox {
            border: 1px solid #C9D1D9;
            border-radius: 6px;
            padding: 8px 12px;
            background-color: #FFFFFF;
            color: #111111;
            min-height: 20px;
        }
        
        QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QDoubleSpinBox:focus {
            border: 2px solid #6366F1;
            outline: none;
        }
        
        QLineEdit::placeholder {
            color: #6B7280;
        }
        
        QPushButton {
            border: 1px solid #C9D1D9;
            border-radius: 6px;
            padding: 8px 16px;
            min-width: 80px;
            font-weight: 500;
        }
        
        QPushButton#saveBtn {
            background-color: #10B981;
            color: #FFFFFF;
            border: 1px solid #10B981;
        }
        
        QPushButton#saveBtn:hover {
            background-color: #059669;
        }
        
        QPushButton#clearBtn, QPushButton#deleteBtn, QPushButton#exportBtn {
            background-color: #E5E7EB;
            color: #111111;
        }
        
        QPushButton#todayBtn, QPushButton#yesterdayBtn {
            background-color: #3B82F6;
            color: #FFFFFF;
            border: 1px solid #3B82F6;
            padding: 6px 8px;
            min-width: 50px;
            font-size: 12px;
        }
        
        QPushButton#todayBtn:hover, QPushButton#yesterdayBtn:hover {
            background-color: #2563EB;
        }
        
        QPushButton#filterBtn {
            background-color: #8B5CF6;
            color: #FFFFFF;
            border: 1px solid #8B5CF6;
            min-width: 70px;
        }
        
        QPushButton#filterBtn:hover {
            background-color: #7C3AED;
        }
        
        QPushButton#clearFilterBtn {
            background-color: #6B7280;
            color: #FFFFFF;
            border: 1px solid #6B7280;
            min-width: 60px;
        }
        
        QPushButton#clearFilterBtn:hover {
            background-color: #4B5563;
        }
        
        QPushButton:hover {
            background-color: #F3F4F6;
        }
        
        QTableWidget {
            border: 1px solid #E5E7EB;
            border-radius: 6px;
            gridline-color: #E5E7EB;
            background-color: #FFFFFF;
            alternate-background-color: #F9FAFB;
        }
        
        QTableWidget::item {
            padding: 8px;
            border: none;
        }
        
        QTableWidget::item:selected {
            background-color: #3B82F6;
            color: #FFFFFF;
        }
        
        QHeaderView::section {
            background-color: #F3F4F6;
            color: #111111;
            font-weight: bold;
            border: 1px solid #E5E7EB;
            padding: 8px;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 20px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #6B7280;
        }
        
        QDateEdit::drop-down {
            border: none;
            width: 20px;
        }
        
        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
            width: 16px;
            border: none;
        }
        """
        
        self.setStyleSheet(style)

    def closeEvent(self, event):
        """Uygulama kapatılırken timer'ı durdur ve veritabanı bağlantısını kapat"""
        if hasattr(self, 'title_timer'):
            self.title_timer.stop()
        self.conn.close()
        event.accept()


if __name__ == "__main__":
    # Yüksek DPI desteği (QApplication'dan önce ayarlanmalı)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    
    # Uygulama ikonunu ayarla (taskbar için)
    try:
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        if os.path.exists(logo_path):
            app_icon = QIcon(logo_path)
            app.setWindowIcon(app_icon)
    except Exception as e:
        print("Uygulama ikonu ayarlanırken hata:", str(e))
    
    # Fusion stili
    app.setStyle("Fusion")
    
    # Ana pencereyi oluştur ve göster
    window = IncomeExpenseWidget()
    window.show()
    
    sys.exit(app.exec_())
