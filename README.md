# LG ThinQ OpenAPI (Smart Solution API)
<p style="text-align:center"><img src="Resource/thinq_logo.png" width="150"></p>

Prepare
---
1. Issue ThinQ API Personal Access Token<br>
   How to? [LG ThinQ(씽큐) 플랫폼 API 공개 및 OpenAPI 사용해보기 (스마트솔루션 API)](https://yogyui.tistory.com/entry/LG-ThinQ%EC%94%BD%ED%81%90-%ED%94%8C%EB%9E%AB%ED%8F%BC-API-%EA%B3%B5%EA%B0%9C-%EB%B0%8F-%EC%84%9C%EB%B9%84%EC%8A%A4-%EC%82%AC%EC%9A%A9)
2. Clone repository
    ```shell
    $ git clone https://github.com/YOGYUI/py_thinq_openapi_tester.git
    ```
3. Install python virtual environments
    ```shell
    $ cd py_thinq_openapi_tester
    # create python virtual environment
    $ python3 -m venv ./venv
    # activate virtual environment
    $ source ./venv/bin/activate
    # install prerequisite packages
    $ python3 -m pip install -r requirements.txt
    ```

Run Application
---
```shell
$ cd py_thinq_openapi_tester
$ source ./venv/bin/activate
$ python3 main.py
```
