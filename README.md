# BSC Pair Radar

Минимальный каркас проекта для отслеживания события `PairCreated` в PancakeSwap V2 Factory на BNB Smart Chain.

## Структура
```
bsc_pair_radar/
├── src/
│   ├── main.py
│   ├── listener.py
│   ├── filters.py
│   └── utils.py
├── requirements.txt
└── README.md
```

## Запуск
1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Убедитесь, что в `src/main.py` корректно указан `BSC_WSS_URL`.
3. Запустите скрипт:
   ```bash
   python -m src.main
   ```

При появлении новой пары с ликвидностью ≥ 1000 USD информация выводится в консоль.
