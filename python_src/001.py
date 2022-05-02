import os

try:
    import pandas
except:
    str00 = 'pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple'
    os.system(str00)
    import pandas

# pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple