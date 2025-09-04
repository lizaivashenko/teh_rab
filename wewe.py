import tkinter as tk
from tkinter import ttk
import psutil
import platform
import time
from threading import Thread
import subprocess
import os

class CPUMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Температура и скорость вентиляторов")
        self.root.geometry("400x250")
        self.root.configure(bg='white')
        self.root.resizable(False, False)
        
        # Стиль для бело-черной темы
        self.setup_styles()
        
        # Переменные для данных
        self.cpu_temp = tk.StringVar(value="Загрузка...")
        self.fan_speed = tk.StringVar(value="Загрузка...")
        
        self.running = True
        self.setup_ui()
        self.start_monitoring()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Настройка цветов
        style.configure('White.TFrame', background='white')
        style.configure('Center.TLabel', 
                       background='white', 
                       foreground='black',
                       font=('Arial', 12, 'bold'),
                       anchor='center')
        
        style.configure('Data.TLabel', 
                       background='white', 
                       foreground='black',
                       font=('Arial', 14, 'bold'),
                       anchor='center')
        
        style.configure('Black.TButton',
                      background='white',
                      foreground='black',
                      bordercolor='black',
                      focuscolor='none',
                      font=('Arial', 10, 'bold'))
        
        # Убираем подсветку кнопки при наведении
        style.map('Black.TButton',
                 background=[('active', 'white')],
                 foreground=[('active', 'black')])

    def setup_ui(self):
        # Главный фрейм
        main_frame = ttk.Frame(self.root, style='White.TFrame', padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Центральный фрейм для данных
        center_frame = ttk.Frame(main_frame, style='White.TFrame')
        center_frame.pack(expand=True, fill=tk.BOTH)
        
        # Температура ЦП - красный цвет
        ttk.Label(center_frame, text="Температура ЦП:", style='Center.TLabel').pack(pady=(20, 5))
        self.cpu_temp_label = ttk.Label(center_frame, textvariable=self.cpu_temp, style='Data.TLabel')
        self.cpu_temp_label.configure(foreground='red')  # Красный цвет для температуры
        self.cpu_temp_label.pack(pady=(0, 20))
        
        # Скорость вентилятора - красный цвет
        ttk.Label(center_frame, text="Скорость вентилятора:", style='Center.TLabel').pack(pady=(0, 5))
        self.fan_speed_label = ttk.Label(center_frame, textvariable=self.fan_speed, style='Data.TLabel')
        self.fan_speed_label.configure(foreground='red')  # Красный цвет для скорости вентилятора
        self.fan_speed_label.pack(pady=(0, 20))
        
        # Кнопка выхода внизу
        exit_button = ttk.Button(main_frame, 
                                text="ВЫХОД", 
                                command=self.exit_app,
                                style='Black.TButton',
                                width=15)
        exit_button.pack(side=tk.BOTTOM, pady=(10, 0))

    def run_command_safe(self, command):
        """Безопасное выполнение команды с обработкой кодировки"""
        try:
            # Устанавливаем правильную кодировку для Windows
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            
            result = subprocess.run(command, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10,
                                  env=env,
                                  encoding='utf-8',
                                  errors='ignore')
            return result
        except Exception as e:
            return None

    def get_cpu_temperature_windows(self):
        """Методы для Windows"""
        try:
            # Метод 1: Через WMI (более надежный)
            try:
                result = self.run_command_safe(['wmic', 'path', 'Win32_PerfFormattedData_Counters_ThermalZoneInformation', 'get', 'Temperature'])
                if result and result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if line.strip().isdigit():
                            temp = int(line.strip())
                            if temp > 0:
                                return temp / 10.0
            except:
                pass
            
            # Метод 2: Через MSAcpi_ThermalZoneTemperature
            try:
                result = self.run_command_safe(['wmic', '/namespace:\\\\root\\wmi', 'path', 'MSAcpi_ThermalZoneTemperature', 'get', 'CurrentTemperature'])
                if result and result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if line.strip().isdigit():
                            temp = int(line.strip())
                            return (temp / 10.0) - 273.15
            except:
                pass
            
            # Метод 3: Через psutil
            try:
                if hasattr(psutil, "sensors_temperatures"):
                    temps = psutil.sensors_temperatures()
                    if temps:
                        for name, entries in temps.items():
                            for entry in entries:
                                if hasattr(entry, 'current') and entry.current:
                                    return entry.current
            except:
                pass
            
            return None
            
        except Exception:
            return None

    def get_cpu_temperature(self):
        """Универсальный метод получения температуры"""
        try:
            system = platform.system()
            
            if system == "Windows":
                temp = self.get_cpu_temperature_windows()
                if temp is not None:
                    return temp
                else:
                    return "N/A"
            else:
                return "N/A"
                
        except Exception as e:
            return f"Ошибка: {str(e)}"

    def get_fan_speed_windows(self):
        """Методы для получения скорости вентилятора в Windows"""
        try:
            # Метод 1: Через WMI
            result = self.run_command_safe(['wmic', 'path', 'Win32_Fan', 'get', 'DesiredSpeed'])
            if result and result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if line.strip().isdigit():
                        return f"{line.strip()} RPM"
            
            # Метод 2: Альтернативный запрос
            result = self.run_command_safe(['wmic', 'path', 'Win32_PerfFormattedData_Counters_ThermalZoneInformation', 'get', 'ActiveCooling'])
            if result and result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if line.strip().isdigit():
                        speed = int(line.strip())
                        if speed > 0:
                            return f"{speed} RPM"
            
            return None
            
        except Exception:
            return None

    def get_fan_speed(self):
        """Упрощенный метод получения скорости вентилятора"""
        try:
            system = platform.system()
            
            if system == "Windows":
                speed = self.get_fan_speed_windows()
                if speed is not None:
                    return speed
                else:
                    return "N/A"
            else:
                return "N/A"
                
        except Exception as e:
            return f"Ошибка: {str(e)}"

    def update_data(self):
        """Обновление данных"""
        while self.running:
            try:
                # Температура CPU
                temp = self.get_cpu_temperature()
                if isinstance(temp, (int, float)):
                    self.cpu_temp.set(f"{temp:.1f} °C")
                else:
                    self.cpu_temp.set(str(temp))
                
                # Скорость вентилятора
                fan_speed = self.get_fan_speed()
                self.fan_speed.set(fan_speed)
                
            except Exception as e:
                error_msg = f"Ошибка: {str(e)}"
                self.cpu_temp.set(error_msg)
            
            time.sleep(3)

    def start_monitoring(self):
        """Запуск мониторинга в отдельном потоке"""
        self.monitor_thread = Thread(target=self.update_data, daemon=True)
        self.monitor_thread.start()

    def exit_app(self):
        """Выход из приложения"""
        self.running = False
        self.root.quit()
        self.root.destroy()

def main():
    # Проверка зависимостей
    try:
        import psutil
        print("psutil установлен")
    except ImportError:
        print("Установите psutil: pip install psutil")
        return
    
    print(f"Система: {platform.system()} {platform.release()}")
    
    root = tk.Tk()
    app = CPUMonitorApp(root)
    
    # Обработка закрытия окна
    def on_closing():
        app.exit_app()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()