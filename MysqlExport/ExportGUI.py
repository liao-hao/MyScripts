import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pandas as pd
from sqlalchemy import create_engine
import threading

# 创建主窗口
root = tk.Tk()
root.title("MySQL 数据导出工具")
root.geometry("600x300")

# 创建数据库连接参数输入框
tk.Label(root, text="主机:").grid(row=0, column=0, padx=10, pady=5)
host_entry = tk.Entry(root, width=25)
host_entry.insert(0, "127.0.0.1:3296")  # 设置默认主机地址
host_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="用户名:").grid(row=1, column=0, padx=10, pady=5)
user_entry = tk.Entry(root, width=25)
user_entry.insert(0, "root")  # 设置默认用户名
user_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="密码:").grid(row=2, column=0, padx=10, pady=5)
password_entry = tk.Entry(root, width=25, show="*")
password_entry.insert(0, "password")  # 设置默认密码
password_entry.grid(row=2, column=1, padx=10, pady=5)

# 创建选择数据库的下拉框
tk.Label(root, text="选择数据库:").grid(row=4, column=0, padx=10, pady=5)
database_combobox = ttk.Combobox(root, width=22)
database_combobox.grid(row=4, column=1, padx=10, pady=5)
database_combobox.grid_remove()  # 初始时隐藏下拉框


# 创建日志输出框
log_output = scrolledtext.ScrolledText(root, width=40, height=12, state='disabled')
log_output.grid(row=0, column=2, rowspan=5, padx=10, pady=5)


def log_message(message):
    """将日志信息添加到输出框中"""
    log_output.configure(state='normal')
    log_output.insert(tk.END, message + '\n')
    log_output.see(tk.END)  # 自动滚动到最后一行
    log_output.configure(state='disabled')


def fetch_databases():
    """连接数据库并获取数据库列表"""
    try:
        log_message("正在加载数据库列表...")
        engine = create_engine(f"mysql+pymysql://{user_entry.get()}:{password_entry.get()}@{host_entry.get()}")
        databases = pd.read_sql("SHOW DATABASES", engine)
        database_combobox['values'] = databases['Database'].tolist()
        database_combobox.grid()  # 成功后显示下拉框
        log_message("数据库列表加载成功！")
        # messagebox.showinfo("成功", "数据库列表加载成功！")
    except Exception as e:
        log_message(f"加载数据库列表失败: {e}")
        messagebox.showerror("错误", f"无法加载数据库列表: {e}")


def export_all_tables():
    """导出所选数据库的所有表"""
    selected_db = database_combobox.get()
    if not selected_db:
        messagebox.showwarning("警告", "请先选择一个数据库")
        return

    def run_export():
        try:
            log_message(f"正在导出数据库 {selected_db} 的所有表...")
            engine = create_engine(
                f"mysql+pymysql://{user_entry.get()}:{password_entry.get()}@{host_entry.get()}/{selected_db}")
            connection = engine.connect()

            # 获取所有表名
            tables = pd.read_sql("SHOW TABLES", connection)
            table_names = tables[tables.columns[0]].tolist()

            # 创建 Excel 工作簿
            with pd.ExcelWriter(f"{selected_db}_export.xlsx", engine='openpyxl') as writer:
                for table in table_names:
                    # 将每个表的数据导出到一个 DataFrame
                    df = pd.read_sql(f"SELECT * FROM {table}", connection)

                    # 控制 Sheet 名称长度，防止超过 31 字符
                    sheet_name = table[:31]

                    # 将 DataFrame 写入到 Excel 的 Sheet
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    log_message(f"已导出表 {table}")

                    # 获取当前工作表并自动调整列宽度
                    worksheet = writer.sheets[sheet_name]
                    for column_cells in worksheet.columns:
                        max_length = max(len(str(cell.value)) if cell.value is not None else 0 for cell in column_cells)
                        adjusted_width = (max_length + 2)
                        worksheet.column_dimensions[column_cells[0].column_letter].width = adjusted_width

            log_message(f"所有表已成功导出到 {selected_db}_export.xlsx")
            messagebox.showinfo("成功", f"所有表已成功导出到 {selected_db}_export.xlsx")
        except Exception as e:
            log_message(f"导出失败: {e}")
            messagebox.showerror("错误", f"导出失败: {e}")
        finally:
            connection.close()

    # 创建并启动新线程
    export_thread = threading.Thread(target=run_export)
    export_thread.start()


# 创建按钮
tk.Button(root, text="加载数据库", command=fetch_databases).grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(root, text="导出所有表", command=export_all_tables).grid(row=5, column=0, columnspan=2, pady=10)

# 运行主循环
root.mainloop()