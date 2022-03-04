# PlayStation Transaction Crawler

Python scripts for crawling PlayStation transactions information.

用来爬虫 PlayStation 交易信息的 Python 脚本。

## What you need? | 你需要什么？

For **API version 2**, the only one string for authorization you need is `authorization` in HTTPS request's header.

For **API version 1**, the only one string for authorization you need is `pdccws_p` in Cookie.

As far as I know, PlayStation accounts in **United States use API version 2**, while those in **Hong Kong SAR use API version 1**.

Whether you are using **API version 2** or **API version 1**, you need to specify the **date & time range** that needs to be used for crawler, including **start date & time** `start_date` and **end date & time** `end_date`. When **end date & time** `end_date` is set to **"None"**, the script will automatically use the **runtime date & time**. Date & time are in **Universal Time Coordinated** or **Greenwich Mean Time**.

对于 **API 版本 2**，您需要的唯一一个用于验证授权的字符串是 HTTPS 请求标头中的 `authorization`。

对于 **API 版本 1**，您需要的唯一一个用于验证授权的字符串是 Cookie 中的 `pdccws_p`。

目前据我所知，**美国区** PlayStation 账号**使用 API 版本 2**，而**香港区使用 API 版本 1**。

无论是使用 **API 版本 2** 还是 **API 版本 1**，都需要指定需要用来爬虫的**日期时间范围**，包括**起始日期时间** `start_date` 和**结束日期时间** `end_date`。**结束日期时间** `end_date` 设置为 **"None"** 则脚本自动使用**运行时的日期时间**。日期时间采用**世界协调时（UTC）**，或者叫**格林威治标准时间（GMT）**。

## How to use? | 如何使用？

Step 1: Get your own `authorization` or `pdccws_p`

Step 2: Copy the file `config.conf.example` and rename it as `config.conf`

Step 3: Set your own `authorization` or `pdccws_p` values in the file `config.conf`

Step 4: Also set `start_date` and `end_date` you wanted, and the `api_version_2` value (**"True" for using API version 2**)

Step 5: Run the script `main.py` and the results, a csv file, will be saved in the directory `csv_files/[DATE_TODAY]` with the filename format as `csv_file_[TIME_NOW]`

第 1 步：获取您自己的 `authorization` 或 `pdccws_p`

第 2 步：复制文件 `config.conf.example` 并将其重命名为 `config.conf`

第 3 步：在文件 `config.conf` 中设置您自己的 `authorization` 或 `pdccws_p` 值

第 4 步：还需设置您想要的 `start_date` 和 `end_date`，以及 `api_version_2` 值（**"True"表示使用 API 版本 2**）

第 5 步：运行脚本 `main.py`，结果，一个 csv 文件将保存在目录 `csv_files/[DATE_TODAY]` 中，文件名格式为 `csv_file_[TIME_NOW]`

## Tested Environments | 测试环境

- macOS Monterey 12.2.1
- Python 3.9.10
- PyCharm 2021.3
