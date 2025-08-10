# suppliers_stock_service

в директории надо иметь файлы 
```
WB - выбор ниши - 05.08.2025 (2).csv
wb_tokens.csv
```

```
Данные сохраняются в папку data
```

```
make parse - парсит данные с апи и с сайта(цену спп + вб кошелёк) и создает для каждого кабинета свой json с данными wb_wallet_price_i.json

make merge - сливает все спаршенные данные в один большой json: data/merged_results.json

make analyze - очищает пандосом данные от 0 и "Нет в наличии", считает спп и сохраняет в data/df_filtered.csv

make find-spp - находить по nm_id категорию через парсинг сайта вб и выдает все категории с avg_price и spp в датасете df_filtered.csv 


make all - запускает всё
```
