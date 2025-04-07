from setuptools import setup

setup(name='vvm_lib',
      version='3.3.0',
      description='my frequently used functions',
      packages=[
          'vvm_lib',
          "vvm_lib.db",
      ],
      package_dir={
          "vvm_lib": "vvm_lib",
          "vvm_lib.db": "vvm_lib/db",
      },
      author_email='v.vazhinskiy@yandex.ru',
      author="vvazhinskiy",
      url="https://github.com/VazhikVM/vvm_lib",
      zip_safe=False,
      install_requires=[
          "pandas", 'gspread', 'google-auth-oauthlib', 'google-auth', 'xlsxwriter'
          , 'oauth2client', 'psycopg2-binary', 'mysql-connector-python',  "openpyxl",  "requests-ntlm"
          , "clickhouse-connect", 'tzlocal', 'polars', 'hvac'
      ],
      )
