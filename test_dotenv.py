try:
    import python_dotenv
    print(f'? python-dotenv安装成功，版本：{python_dotenv.__version__}')
except ImportError as e:
    print(f'? python-dotenv安装失败：{e}')
