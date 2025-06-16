# Task 1 – Návrh dátového modelu


## Úvod

Tento dokument sumarizuje riešenie úlohy 1. Jeho cieľom je navrhnúť, implementovať a otestovať dátový model pre e-commerce platformu vrátane analytického star schema.
Obsahuje aj simuláciu vytvorenia celej databázovej štruktúry vrátane generovania testovacích dát, bližšie info pre spustenie a riešenia zadaných úloh nájdete nižšie.

---

# Postup spúšťania Tasku 1 – Návrh a implementácia dátového modelu

Ak chcete spustiť kompletnú simuláciu vytvorenia celej databázovej štruktúry vrátane generovania 
testovacích dát, importu a vytvorenia analytického modelu (star schema), použite skript:

`python run_all_task1.py`

1. **Nastav virtuálne prostredie a nainštaluj závislosti:**

```bash
python -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate     # (Windows)
pip install -r requirements.txt
```

---

## Štruktúra
```
1_data_modeling_ecommerce/
├── faked_ecommerce_data/          # CSV súbory s generovanými dátami
│   ├── categories.csv
│   ├── customers.csv
│   ├── order_items.csv
│   ├── orders.csv
│   ├── products.csv
│   └── transactions.csv
├── build_star_schema.sql          # SQL skript na vytvorenie star schema tabuliek
├── er_diagram.dbml                # textová definícia ER diagramu
├── ER_diagram.png                 # vizuálny ER diagram
├── fake_ecommerce.db              # SQLite databáza s načítanými dátami
├── faker_ecommerce_generator.py   # generátor fake CSV dát
├── generate_fake_ecommerce_db.py  # import CSV do SQLite DB (možno voliteľný)
├── run_all_task1.py               # master skript spúšťajúci všetky kroky v správnom poradí
├── run_build_star_schema.py       # samostatný skript na spustenie star schema SQL
└── sql_schema.sql                 # SQL skript na vytvorenie relačných tabuliek
```
## Komponenty riešenia

## 1. ER diagram

- Definuje základné entity a ich vzťahy: Produkty, Kategórie, Zákazníci, Objednávky, Položky objednávok, Transakcie.  
- Vizualizácia je k dispozícii v `1_data_modeling_ecommerce/ER_diagram.png`.

## 2. Star schema (`build_star_schema.sql` a `run_build_star_schema.py`)

- Skript vytvára analytické dimenzie a faktové tabuľky (star schema) z relačných tabuliek.  
- Slúži pre rýchle a efektívne analytické dotazy.

## 3. Identifikácia

### a) Primárne a cudzie kľúče

| Tabuľka 		 | Primárny kľúč   | Cudzí kľúč 													 |
|----------------|-----------------|-----------------------------------------------------------------|
| categories	 | category_id 	   | parent_category_id -> categories.category_id (sebaodkaz)		 |
| products		 | product_id	   | category_id -> categories.category_id							 |
| customers		 | customer_id	   | -																 |
| orders		 |	order_id	   | customer_id -> orders.order_id , products.product_id			 |
| order_items	 | order_item_id   | order_id -> orders.order_id , product_id -> products.product_id |
| transactions	 | transaction_id  | order_id -> orders.order_id									 |

### b) Normalizácia

- model je normalizovaný do **3. normálnej formy (3NF)**, čo znamená:
	- žiadne opakovanie skupín údajov v tabuľkách (1NF)
	- každý atribút závisí úplne od primárneho kľúča (2NF)
	- žiadne tranzitívne závislosti medzi ne-kľúčovými atribútmi (3NF)
	
- hierarchia kategórií je riešená pomocou sebaodkazu (`parent_category_id`), ktorý eliminuje duplicity

### c) Denormalizácia

| miesto využitia 			 | návrh denormalizácie 																					|
|----------------------------|----------------------------------------------------------------------------------------------------------|
| Produkty a kategórie		 | Duplikovanie názvovv kategórií priamo v tabuľke produktov pre zrýchlenie dotazov bez JOIN-ov				|
| Región a kategórie		 | Zjednodušenie adresných údajov priamo v tabuľkeň objednávok alebo faktovej tabuľke 						|
| Dátumové analýzy			 | Predpočítanie a uloženie dátumových atribútov (rok, mesiac, štvrtok) v dimenziách alebo faktovej tabuľke |
| Súhrnné metriky objednávok | Uloženie celkovej sumy objednávky priamo v tabuľke objednávok 											|


## 4. SQL schéma (`sql_schema.sql`)

- Skript na vytvorenie základných relačných tabuliek so všetkými PK, FK a obmedzeniami.  
- Používa sa na definovanie OLTP modelu pre správu dát.

---

## Zmeny a dôvody

| Pôvodný postup                      			 | Aktualizovaný postup                                					| Dôvod zmeny                                   |
|------------------------------------------------|----------------------------------------------------------------------|-----------------------------------------------|
| Star schema sa vytvára ihneď        			 | Najskôr vytvorenie relačnej schémy, import dát, potom star schema    | Zabezpečiť správny postup a testovateľnosť    |
| Generovanie dát a import nebolo jasne oddelené | Jasné oddelenie generovania, importu a tvorby schém 					| Lepšia organizácia a prehľadnosť              |
| Miešanie SQL skriptov a ich spúšťania 		 | Navrhnutý master skript spúšťajúci všetky kroky v správnom poradí    | Automatizácia a zníženie rizika chýb          |
| Nedostatočná dokumentácia procesu 			 | Pridané vysvetlenie logického workflow a vzťahov  					| Lepšie pochopenie hodnotiteľmi i používateľmi |

---

## Workflow riešenia

```text
1. Vytvorenie základnej relačnej schémy (sql_schema.sql)
2. Generovanie testovacích dát (faker_ecommerce_generator.py)
3. Import dát do DB (generate_fake_ecommerce_db.py)
4. Vytvorenie star schema (build_star_schema.sql cez run_build_star_schema.py)
5. Analytické dotazy a testovanie
