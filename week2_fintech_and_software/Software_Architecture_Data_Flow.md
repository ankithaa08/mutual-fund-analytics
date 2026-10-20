# Software Architecture & Data Flow in FinTech Platforms

**Author**: Data Analytics Engineering Team  
**Module**: Week 2 Software Development Ecosystem & Data Pipelines  
**Deliverable**: Software Architecture Diagram & Technical Guide  

---

## 1. End-to-End Data Flow Architecture

The diagram below illustrates how an event initiated by a retail trader on a mobile app or web browser flows through the backend microservices, persists in operational transactional databases (OLTP), streams into data pipelines, and materializes into business analytics dashboards (OLAP):

```mermaid
flowchart TD
    %% Client Layer
    subgraph Client_Layer ["1. Client / Frontend Layer"]
        User["Retail Investor / User"]
        Web["Web Application (React / Next.js)"]
        Mobile["Mobile App (Flutter / React Native)"]
        User -->|Clicks 'Buy 100 Shares of TCS'| Web
        User -->|Places Order via App| Mobile
    end

    %% Security & Gateway
    subgraph Gateway_Layer ["2. API Gateway & Security"]
        APIGW["API Gateway (Kong / AWS API Gateway)"]
        Auth["Auth Service (OAuth 2.0 / JWT Verification)"]
        RateLimiter["Rate Limiter & WAF"]
        Web -->|HTTPS POST /api/v1/orders| APIGW
        Mobile -->|HTTPS POST /api/v1/orders| APIGW
        APIGW <--> Auth
        APIGW <--> RateLimiter
    end

    %% Backend Services
    subgraph Backend_Layer ["3. Backend Microservices (OLTP)"]
        OrderService["Order Management Service (Go / Java)"]
        RiskEngine["Risk & Margin Engine"]
        ExchangeRouter["Exchange Fix Gateway (NSE/BSE)"]
        OLTP_DB[("Transactional Database (PostgreSQL / Aurora OLTP)")]

        APIGW -->|Authorized Payload| OrderService
        OrderService <-->|Check Funds & Limits| RiskEngine
        OrderService -->|Execute Order| ExchangeRouter
        OrderService -->|Commit Order State| OLTP_DB
    end

    %% Data Pipeline & Streaming
    subgraph Pipeline_Layer ["4. Data Pipeline & Ingestion (ETL / ELT)"]
        CDC["Change Data Capture (Debezium)"]
        Kafka["Event Stream (Apache Kafka)"]
        ETL["Batch / Stream Transformation (dbt / Spark / Airflow)"]
        
        OLTP_DB -->|WAL Logs| CDC
        CDC -->|Real-time Order Events| Kafka
        Kafka -->|Raw Event Stream| ETL
    end

    %% Analytics & Data Warehouse
    subgraph Analytics_Layer ["5. Data Warehouse & Storage (OLAP)"]
        DWH[("Cloud Data Warehouse (Snowflake / BigQuery / ClickHouse)")]
        DataLake[("Object Storage / S3 (Parquet)")]
        
        ETL -->|Curated Dimensional Models| DWH
        ETL -->|Cold Raw Storage| DataLake
    end

    %% BI & Consumption
    subgraph Consumption_Layer ["6. Business Intelligence & Decision Support"]
        BI["Analytics Dashboard (Power BI / Metabase / Tableau)"]
        Executive["Executive Management (Revenue & AUM Monitoring)"]
        DataAnalyst["Data Analyst (Risk, Churn, Funnel Analytics)"]
        
        DWH -->|SQL Direct Query / Import| BI
        BI --> Executive
        BI --> DataAnalyst
    end

    classDef client fill:#E1F5FE,stroke:#03A9F4,stroke-width:2px;
    classDef backend fill:#E8F5E9,stroke:#4CAF50,stroke-width:2px;
    classDef data fill:#FFF3E0,stroke:#FF9800,stroke-width:2px;
    classDef bi fill:#F3E5F5,stroke:#9C27B0,stroke-width:2px;

    class User,Web,Mobile client;
    class APIGW,Auth,OrderService,RiskEngine,ExchangeRouter,OLTP_DB backend;
    class CDC,Kafka,ETL,DWH,DataLake data;
    class BI,Executive,DataAnalyst bi;
```

---

## 2. Sequence Diagram: Step-by-Step Execution Journey

```mermaid
sequenceDiagram
    autonumber
    actor User as Retail Trader
    participant FE as Frontend (Web/App)
    participant GW as API Gateway
    participant BE as Backend Order Service
    participant DB as OLTP Database (Postgres)
    participant K as Kafka / CDC Pipeline
    participant DWH as Data Warehouse (ClickHouse/Snowflake)
    actor DA as Data Analyst (Power BI)

    User->>FE: Clicks "Confirm Buy Order"
    FE->>GW: POST /api/v1/orders (Bearer JWT Token)
    GW->>GW: Validate JWT & Rate Limits
    GW->>BE: Route Order Payload
    BE->>BE: Validate Margin & Risk Rules
    BE->>DB: INSERT INTO orders (status = 'EXECUTED')
    DB-->>BE: Commit Confirmation (tx_id = 98412)
    BE-->>FE: Return 201 Created (Order Success)
    FE-->>User: Display Green Success Screen

    Note over DB,K: Asynchronous Data Pipeline Begins
    DB->>K: Debezium captures CDC WAL Event
    K->>DWH: Stream transformed facts to fact_orders
    DWH->>DA: Power BI visual refreshes metrics (AUM, Volume, Margin)
```

---

## 3. Core Software Engineering Concepts Explained

### 1. Frontend vs. Backend
- **Frontend (Client-Side)**: The visual, interactive user interface rendered on the user's device (built using React.js, Next.js, Flutter, or Swift). It captures user gestures, performs initial form validation, and renders UI state.
- **Backend (Server-Side)**: The hidden computational engine running in secure cloud environments (built using Python/FastAPI, Go, Java, or Node.js). It enforces core business logic, verifies authentication, calculates trade margins, and interfaces with databases.

### 2. Client–Server Architecture
The architectural paradigm where the **Client** initiates structured requests over the network via standard protocols (HTTP/HTTPS, WebSockets) and the **Server** processes those requests and returns responses (JSON/HTML). This ensures strong security, as secret database keys never touch user devices.

### 3. Authentication & Security
- **OAuth 2.0 & JWT (JSON Web Tokens)**: When a user logs in, the authentication server signs a tamper-proof JWT token. Every subsequent request sends this token in the `Authorization: Bearer <token>` header, verifying identity without repeated password lookups.
- **API Gateway**: Acts as the single entry point, handling SSL termination, DDoS protection, rate limiting, and request routing across internal microservices.

### 4. Databases: OLTP vs. OLAP
| Dimension | OLTP (Online Transaction Processing) | OLAP (Online Analytical Processing) |
| :--- | :--- | :--- |
| **Primary Goal** | High-speed, atomic CRUD operations | Complex aggregations, rollups, and reporting |
| **Typical Systems** | PostgreSQL, MySQL, Amazon Aurora | Snowflake, Google BigQuery, ClickHouse, DuckDB |
| **Data Storage** | Row-oriented (optimal for single-record writes) | Column-oriented (optimal for scanning billions of rows) |
| **Schema Design** | Highly Normalized (3NF to prevent duplicates) | Denormalized (Star / Snowflake Schemas) |
| **FinTech Use Case** | Recording an instantaneous trade execution | Calculating 3-year rolling Sharpe ratios across 10M trades |

### 5. Data Pipelines: Change Data Capture (CDC) & ETL
To prevent analytics queries from slowing down live trading operations, data is continuously synced from OLTP to OLAP:
- **Change Data Capture (CDC)**: Tools like Debezium monitor database transaction write-ahead logs (WAL) and publish change events to **Apache Kafka**.
- **ELT / dbt (Data Build Tool)**: Ingests raw events into the data warehouse and executes scheduled SQL transformations to populate dimensional analytical models.

### 6. Logging, Telemetry & Error Handling
- **Structured Logging**: Services write events in JSON format containing `trace_id`, `user_id`, `timestamp`, and `log_level` (`INFO`, `WARN`, `ERROR`).
- **Telemetry Tools**: Sentry captures unhandled frontend and backend exceptions; the ELK Stack (Elasticsearch, Logstash, Kibana) enables centralized log analytics.

### 7. Software Development Lifecycle (SDLC)
Modern software and data engineering follow Agile SDLC stages:
1. **Requirements & Product Design**: User stories and technical specifications.
2. **Architecture & Schema Design**: Modeling database entities and API contracts.
3. **Implementation**: Writing clean, modular code with automated unit tests.
4. **CI/CD (Continuous Integration / Continuous Deployment)**: GitHub Actions automatically runs tests, linters, and deploys builds to cloud staging environments.
5. **Production Monitoring**: Real-time observability tracking error rates, latency (p99), and pipeline uptime.
