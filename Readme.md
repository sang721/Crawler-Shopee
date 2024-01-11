# Hướng dẫn

Hãy cài python3 (>= 3.8) trên Windows hoặc trên các nền tảng Linux Os trước.

Windows:
[conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)

Ubuntu: 

```bash
sudo apt update
```

```bash
sudo apt install python3
```


## Cài thư viện

Truy cập vào thư mục Crawler-Shopee rồi chạy câu lệnh sau để cài đặt những thư viện cần dùng. Nên dùng Anaconda Prompt nếu dùng Windows.

```bash
pip install -r requirements.txt
```

## Chạy crawler

```bash
cd shopee

```

```bash
scrapy crawl shopee

```

## Lưu ý

Trong trường hợp bị chặn hãy vào truy cập vào file config.json rồi đặt lại cookies.

## License

[MIT](https://choosealicense.com/licenses/mit/)