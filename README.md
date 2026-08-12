<font size="3"><b>

<div align = 'center'>

# ArticleModel


### Описание работы


ArticleModel представляет собой граф, который использует 3 ReAct агентов для написания доклада

`
  агент questioner - формально реакт агент без инструментов: анализирует текст и задает по нему уточняющие вопросы;
`

`
  агент reseracher - рекат агент, который в интернете ищет подходящие по теме ссылки и выдает информацию
`

`
  агент writer - рекат агент, который систематизирует получаенную информацию и выдает красивый файл с докладом
`

### Быстрый старт
<div align = 'left'>

1) Клонирвоать репозиторий git clone https://github.com/s4lf3tk4/ArticleModel.git

2) Установить окружение: `python -m venv venv`

3) Установить зависимости `pip install -r requirements.txt` 

4) Создаь файл .env с данными 
   
5) Запуск run.sh
   
</div>

### Структура проекта 

<div align = 'left'>

    ArticleModel/
    │
    ├── main.py # Точка входа: запуск оркестратора
    │  
    ├── core/ # Ядро: настройки и состояние
    │ ├── init.py # Экспорт WORKDIR, MAX_SYMBOLS, MAX_ITERATIONS, OrchestraState
    │ ├── settings.py # Pydantic-настройки (переменные окружения, defaults)
    │ └── state.py # Определение OrchestraState (TypedDict)
    │
    ├── agents/ # Создание ReAct-агентов
    │ ├── init.py # Экспорт researcher, questioner, writer
    │ └── agents.py # create_researcher(), create_questioner(), create_writer()
    │
    ├── nodes/ # Узлы графа
    │ ├── init.py # Экспорт узлов
    │ └── nodes.py # node_research, inf_analyzer_node, node_write
    │
    ├── graph/ # Построение графа LangGraph
    │ ├── init.py # Экспорт готового графа
    │ └── graph.py # StateGraph, conditional_edges, компиляция
    │
    ├── tools/ # Инструменты для агентов
    │ ├── init.py # Экспорт web_search, save_report
    │ └── tools.py # web_search() – DuckDuckGo, save_report() – запись файла
    │
    ├── utils/ # Вспомогательные функции (опционально)
    │ └── helpers.py # Общие утилиты (например, форматирование, логирование)
    │
    ├── .env # Переменные окружения (опционально)
    ├── requirements.txt # Зависимости проекта
    └── README.md # Описание проекта, инструкция по запуску

</div>



</div>

</b>
