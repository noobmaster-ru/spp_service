project_dir := .

.PHONY: reformat
reformat: ## Reformat code
	ruff format $(project_dir)
	ruff check $(project_dir) --fix

# выполняет запросы и сохраняет per-cabinet json в data/results/
parse:
	python main.py parse

# объединит results -> data/merged_results.json
merge:
	python main.py merge

# создаст data/df_filtered.csv
analyze:
	python main.py analyze

# запустит CLI для запроса spp по nm_id
find-spp:
	python main.py find-spp

# всё
all:
	python main.py parse
	python main.py merge
	python main.py analyze
	python main.py find-spp

# считать спп по часам и сохранять в df_filtered
spp-hour:
	python main.py parse
	python main.py merge
	python main.py analyze