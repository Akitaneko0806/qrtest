# -*- coding: utf-8 -*-
from app import create_app

# WSGIサーバーが使用するエントリーポイント
application = create_app()

if __name__ == '__main__':
    # ローカル開発用
    application.run(debug=False, host='0.0.0.0', port=5001)