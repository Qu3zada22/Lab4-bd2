# Lab 4 — MongoDB Charts

**CC3089 Base de Datos 2 | UVG | Semestre I 2026**

Dashboard de ventas de una cafetería: ingesta de CSVs a MongoDB via Python +
PyMongo (bulk_write), y visualización con MongoDB Charts.

---

## Estructura

```
lab4/
├── data/                        # CSVs con datos de ventas
│   ├── index_1.csv
│   └── index_2.csv
├── docs/
│   ├── instrucciones.md
│   ├── roadmap.md               # Estado y checklist del proyecto
│   └── todos.md                 # Charts y KPIs del dashboard
├── scripts/
│   ├── ingest.py                # CSV → MongoDB (entry point)
│   └── verify.py                # Valida datos con agregaciones
├── src/
│   ├── config/settings.py       # Variables de entorno
│   ├── models/sale.py           # Dataclass documento Sale
│   ├── ingestion/
│   │   ├── loader.py            # Lee CSVs → lista de Sale
│   │   └── bulk_writer.py       # bulk_write a MongoDB
│   └── aggregations/queries.py  # Pipelines para charts y KPIs
├── docker-compose.yml           # MongoDB local + Mongo Express
├── pyproject.toml               # Config uv
└── requirements.txt             # Para venv
```

---

## Cómo correr

### 1. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env si es necesario
```

### 2. Levantar MongoDB local

```bash
docker compose up -d
```

Mongo Express disponible en `http://localhost:8081`.

### 3. Instalar dependencias

**Con uv:**
```bash
uv sync
```

**Con venv:**
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Ingestar datos

**Con uv:**
```bash
uv run scripts/ingest.py --drop
```

**Con venv:**
```bash
python scripts/ingest.py --drop
```

### 5. Verificar datos

```bash
uv run scripts/verify.py
# o
python scripts/verify.py
```

---

## Cambiar a Atlas

1. Detener Docker: `docker compose down`
2. Editar `.env` → reemplazar `MONGO_URI` con la connection string de Atlas
3. Re-ejecutar la ingesta: `python scripts/ingest.py --drop`

---

## Dashboard

Ver [`docs/roadmap.md`](docs/roadmap.md) para el estado actual del proyecto.

| Tipo | Nombre |
|------|--------|
| Bar Chart | Ventas por tipo de café |
| Line Chart | Ingresos por mes |
| Donut Chart | Método de pago: Efectivo vs Tarjeta |
| KPI | Ingresos Totales |
| KPI | Total de Transacciones |
| KPI | Ticket Promedio por Venta |
