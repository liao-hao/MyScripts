import pymysql
import pandas as pd


def get_mysql_connection():
    host = input("请输入MySQL地址: ")
    port = input("请输入MySQL端口: ")
    user = input("请输入MySQL用户名: ")
    password = input("请输入MySQL密码: ")

    try:
        # 连接MySQL
        connection = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            charset='utf8mb4'
        )
        print("成功连接到MySQL数据库！")
        return connection
    except pymysql.MySQLError as e:
        print(f"连接失败: {e}")
        return None


def choose_database(connection):
    # 获取所有数据库
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES")
    databases = [db[0] for db in cursor.fetchall()]

    print("可用的数据库:")
    for i, db in enumerate(databases):
        print(f"{i + 1}. {db}")

    choice = int(input("请选择数据库的编号: ")) - 1
    if 0 <= choice < len(databases):
        return databases[choice]
    else:
        print("无效的选择")
        return None


def export_tables_to_excel(connection, database):
    cursor = connection.cursor()
    cursor.execute(f"USE `{database}`")

    # 获取所有表
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]

    # 创建Excel工作簿
    with pd.ExcelWriter(f"{database}_export.xlsx", engine='openpyxl') as writer:
        for table in tables:
            # 将每个表的数据导出到一个DataFrame
            query = f"SELECT * FROM {table}"
            df = pd.read_sql(query, connection)
            # 控制 Sheet 名称长度，防止超过 31 字符
            sheet_name = table[:31]
            # 将DataFrame写入到Excel的Sheet
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"已导出表 {table}")
            # 获取当前工作表
            worksheet = writer.sheets[sheet_name]

            # 自动调整列宽度
            for column_cells in worksheet.columns:
                max_length = max(len(str(cell.value)) if cell.value is not None else 0 for cell in column_cells)
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column_cells[0].column_letter].width = adjusted_width

    print(f"所有表已成功导出到 {database}_export.xlsx")


def main():
    connection = get_mysql_connection()
    if connection:
        database = choose_database(connection)
        if database:
            export_tables_to_excel(connection, database)
        connection.close()


if __name__ == "__main__":
    main()
