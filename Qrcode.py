import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import qrcode
from PIL import Image, ImageTk
import os


class ModernQRGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.qr_image_path = None
        
    def setup_window(self):
        self.root.title("現代化 QR 碼生成器")
        self.root.geometry("600x700")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(False, False)
        
        # 設置窗口圖標（可選）
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
    
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 配置按鈕樣式
        self.style.configure(
            "Modern.TButton",
            font=("Microsoft YaHei", 12, "bold"),
            borderwidth=0,
            focuscolor='none',
            padding=(20, 10)
        )
        
        self.style.map(
            "Modern.TButton",
            background=[
                ('active', '#4a90e2'),
                ('pressed', '#357abd'),
                ('!active', '#5dade2')
            ],
            foreground=[('active', 'white'), ('!active', 'white')],
            relief=[('pressed', 'flat'), ('!pressed', 'flat')]
        )
        
        # 配置輸入框樣式
        self.style.configure(
            "Modern.TEntry",
            font=("Microsoft YaHei", 12),
            borderwidth=2,
            relief="solid",
            focuscolor='#5dade2'
        )
        
        # 配置標籤樣式
        self.style.configure(
            "Title.TLabel",
            font=("Microsoft YaHei", 24, "bold"),
            background="#1a1a2e",
            foreground="#ffffff"
        )
        
        self.style.configure(
            "Subtitle.TLabel",
            font=("Microsoft YaHei", 12),
            background="#1a1a2e",
            foreground="#b0b0b0"
        )
        
        self.style.configure(
            "Result.TLabel",
            font=("Microsoft YaHei", 11),
            background="#1a1a2e",
            foreground="#2ecc71"
        )
    
    def create_widgets(self):
        # 主標題區域
        title_frame = tk.Frame(self.root, bg="#1a1a2e")
        title_frame.pack(pady=(30, 20))
        
        title_label = ttk.Label(title_frame, text="QR 碼生成器", style="Title.TLabel")
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="輸入文字或URL，生成精美的QR碼", style="Subtitle.TLabel")
        subtitle_label.pack(pady=(5, 0))
        
        # 輸入區域
        input_frame = tk.Frame(self.root, bg="#1a1a2e")
        input_frame.pack(pady=20, padx=40, fill="x")
        
        # URL輸入標籤
        url_label = ttk.Label(input_frame, text="請輸入文字或URL：", style="Subtitle.TLabel")
        url_label.pack(anchor="w", pady=(0, 5))
        
        # URL輸入框
        self.entry_url = ttk.Entry(input_frame, font=("Microsoft YaHei", 12), style="Modern.TEntry")
        self.entry_url.pack(fill="x", ipady=8)
        self.entry_url.bind('<Return>', lambda event: self.generate_qrcode())
        
        # 按鈕區域
        button_frame = tk.Frame(self.root, bg="#1a1a2e")
        button_frame.pack(pady=30)
        
        # 生成按鈕
        self.button_generate = ttk.Button(
            button_frame, 
            text="🔄 生成 QR 碼", 
            command=self.generate_qrcode, 
            style="Modern.TButton"
        )
        self.button_generate.pack(side="left", padx=10)
        
        # 保存按鈕
        self.button_save = ttk.Button(
            button_frame, 
            text="💾 保存圖片", 
            command=self.save_qrcode, 
            style="Modern.TButton",
            state="disabled"
        )
        self.button_save.pack(side="left", padx=10)
        
        # QR碼顯示區域
        qr_frame = tk.Frame(self.root, bg="#2c2c54", relief="solid", bd=2)
        qr_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # QR碼標籤
        self.qr_label = tk.Label(qr_frame, bg="#2c2c54", text="QR碼將顯示在這裡", 
                                fg="#888888", font=("Microsoft YaHei", 14))
        self.qr_label.pack(expand=True, fill="both", padx=20, pady=20)
        
        # 結果提示區域
        result_frame = tk.Frame(self.root, bg="#1a1a2e")
        result_frame.pack(pady=10)
        
        self.label_result = ttk.Label(result_frame, text="", style="Result.TLabel")
        self.label_result.pack()
        
        # 底部信息
        footer_frame = tk.Frame(self.root, bg="#1a1a2e")
        footer_frame.pack(side="bottom", pady=10)
        
        footer_label = ttk.Label(footer_frame, text="按 Enter 鍵快速生成 | 支持中文、英文、數字、URL", 
                               style="Subtitle.TLabel")
        footer_label.pack()
    
    def generate_qrcode(self):
        url = self.entry_url.get().strip()
        if not url:
            messagebox.showerror("錯誤", "請輸入有效的文字或URL。")
            return
        
        try:
            # 更新按鈕狀態
            self.button_generate.config(text="⏳ 生成中...")
            self.root.update()
            
            # 生成QR碼
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=8,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            
            # 創建QR碼圖片
            qr_image = qr.make_image(fill_color="#1a1a2e", back_color="white")
            
            # 調整圖片大小以適應顯示區域
            display_size = (300, 300)
            qr_image = qr_image.resize(display_size, Image.Resampling.LANCZOS)
            
            # 保存圖片
            self.qr_image_path = "qrcode_temp.png"
            qr_image.save(self.qr_image_path)
            
            # 顯示QR碼
            qr_image_tk = ImageTk.PhotoImage(qr_image)
            self.qr_label.config(image=qr_image_tk, text="")
            self.qr_label.image = qr_image_tk
            
            # 更新結果標籤
            self.label_result.config(text="✅ QR碼生成成功！點擊'保存圖片'按鈕可保存到本地")
            
            # 啟用保存按鈕
            self.button_save.config(state="normal")
            
        except Exception as e:
            messagebox.showerror("錯誤", f"生成QR碼時發生錯誤：{str(e)}")
            self.label_result.config(text="❌ 生成失敗，請重試")
        
        finally:
            # 恢復按鈕狀態
            self.button_generate.config(text="🔄 生成 QR 碼")
    
    def save_qrcode(self):
        if not self.qr_image_path or not os.path.exists(self.qr_image_path):
            messagebox.showerror("錯誤", "沒有可保存的QR碼圖片")
            return
        
        try:
            # 打開文件保存對話框
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG 圖片", "*.png"),
                    ("JPEG 圖片", "*.jpg"),
                    ("所有文件", "*.*")
                ],
                title="保存QR碼圖片"
            )
            
            if file_path:
                # 重新生成高質量的QR碼用於保存
                url = self.entry_url.get().strip()
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=10,
                    border=4,
                )
                qr.add_data(url)
                qr.make(fit=True)
                
                qr_image = qr.make_image(fill_color="#1a1a2e", back_color="white")
                qr_image.save(file_path)
                
                self.label_result.config(text=f"💾 QR碼已保存到：{os.path.basename(file_path)}")
                messagebox.showinfo("成功", f"QR碼已成功保存到：\n{file_path}")
                
        except Exception as e:
            messagebox.showerror("錯誤", f"保存文件時發生錯誤：{str(e)}")
    
    def run(self):
        # 清理臨時文件
        def on_closing():
            if self.qr_image_path and os.path.exists(self.qr_image_path):
                try:
                    os.remove(self.qr_image_path)
                except:
                    pass
            self.root.destroy()
        
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.mainloop()


if __name__ == "__main__":
    app = ModernQRGenerator()
    app.run()