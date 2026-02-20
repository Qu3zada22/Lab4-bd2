# Roadmap — Lab 4: MongoDB Charts

Dashboard de ventas de una cafetería construido con datos crudos en CSV,
ingesta via Python + PyMongo, y visualización en MongoDB Charts.

---

## Fase 1 – Infraestructura

- [x] Estructura de módulos Python (`src/`, `scripts/`)
- [x] `docker-compose.yml` con MongoDB local + Mongo Express
- [x] `.env.example` con variables para Docker y Atlas
- [ ] Levantar MongoDB local con Docker (`docker compose up -d`)
- [ ] Copiar `.env.example` → `.env` y configurar valores

## Fase 2 – Ingesta de datos

- [x] `src/models/sale.py` — dataclass del documento
- [x] `src/ingestion/loader.py` — lectura de CSVs
- [x] `src/ingestion/bulk_writer.py` — bulk_write a MongoDB
- [x] `scripts/ingest.py` — entry point con flag `--drop`
- [ ] Probar ingesta local: `python scripts/ingest.py --drop`
- [ ] Verificar datos: `python scripts/verify.py`

## Fase 3 – Validación de agregaciones

- [x] `src/aggregations/queries.py` — pipelines para charts y KPIs
- [ ] Confirmar que las 3 gráficas y 3 KPIs retornan datos coherentes

## Fase 4 – Atlas

- [ ] Crear cluster en MongoDB Atlas
- [ ] Obtener connection string y actualizar `MONGO_URI` en `.env`
- [ ] Re-ejecutar ingesta apuntando a Atlas: `python scripts/ingest.py --drop`
- [ ] Verificar colección en Atlas UI

## Fase 5 – MongoDB Charts

### Gráficas

- [ ] **Gráfica 1** — Ventas por tipo de café *(Bar Chart)*
  - Eje X: `coffee_name` | Eje Y: conteo de ventas
- [ ] **Gráfica 2** — Ingresos por mes *(Line Chart)*
  - Eje X: `year_month` | Eje Y: suma de `money`
- [ ] **Gráfica 3** — Método de pago: Efectivo vs Tarjeta *(Donut Chart)*
  - Segmentos: `cash_type` | Valor: conteo o suma de `money`

### KPIs

- [ ] **KPI 1** — Ingresos Totales (`$sum` de `money`)
- [ ] **KPI 2** — Total de Transacciones (`$count`)
- [ ] **KPI 3** — Ticket Promedio por Venta (`$avg` de `money`)

## Fase 6 – Entrega

- [ ] Revisar nombres de ejes, títulos y estética de los charts
- [ ] Grabar video explicando arquitectura + dashboard
- [ ] Subir scripts documentados al repositorio
- [ ] Entregar antes del **domingo 22 de febrero a las 23:59**
