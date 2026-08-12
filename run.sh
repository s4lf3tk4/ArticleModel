#!/bin/bash
cd "$(dirname "$0")" || exit
echo "Запуск ArticleModel чата..."
if [ -d "venv" ]; then
    . venv/Scripts/activate
    python main.py
else
    echo "Отсутствует виртуальное окружение"
    cmd /c pause
fi
echo ""
cmd /c pause
