# Python (Pandas + Matplotlib + Jinja2)
import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader

# === 解决中文乱码 ===
plt.rcParams["font.sans-serif"] = [
    "PingFang SC",
    "Hiragino Sans GB",
    "Arial Unicode MS",
]
plt.rcParams["axes.unicode_minus"] = False  # 正常显示负号

# 1. 数据分析
df = pd.read_csv("sales_data.csv")
total_sales = df["sales"].sum()
top_products = df.groupby("product")["sales"].sum().nlargest(5)
top_products_df = top_products.reset_index()

# 2. 创建图表
plt.figure()
top_products.plot(kind="bar")
plt.title("销售 Top 5 产品")
plt.savefig("top_products.png")

# 3. 生成 HTML 报告
env = Environment(loader=FileSystemLoader("."))
template = env.get_template("report_template.html")

html_content = template.render(
    total_sales=total_sales, top_products_table=top_products_df.to_html(index=False)
)

with open("report.html", "w") as f:
    f.write(html_content)
