# REST API Data Extraction & JSON Processing Assignment

**Author**: Data Analytics Engineering Team  
**Module**: Week 2 REST APIs, JSON Serialization & Data Ingestion  
**Executable Script**: [`api_data_extraction.py`](file:///D:/Admin/Documents/Week2_FinTech_and_Software_Ecosystem_Deliverables/api_data_extraction.py)  
**Output Files**: 
- FX Rates CSV: [`api_extracted_fx_data.csv`](file:///D:/Admin/Documents/Week2_FinTech_and_Software_Ecosystem_Deliverables/api_extracted_fx_data.csv)
- Raw FX JSON: [`api_raw_fx_response.json`](file:///D:/Admin/Documents/Week2_FinTech_and_Software_Ecosystem_Deliverables/api_raw_fx_response.json)
- Mutual Fund NAV CSV: [`api_extracted_mf_data.csv`](file:///D:/Admin/Documents/Week2_FinTech_and_Software_Ecosystem_Deliverables/api_extracted_mf_data.csv)
- Raw MF JSON: [`api_raw_mf_response.json`](file:///D:/Admin/Documents/Week2_FinTech_and_Software_Ecosystem_Deliverables/api_raw_mf_response.json)

---

## 1. What is an API?

An **Application Programming Interface (API)** is a formalized set of rules, protocols, and interface specifications that allow different software systems to communicate and exchange data programmatically over networks.

### REST (Representational State Transfer) Architecture Principles
- **Client-Server Separation**: The user interface (client) and data storage (server) remain strictly decoupled.
- **Statelessness**: Every HTTP request contains all context, authentication tokens, and parameters required for processing; no session state is maintained on the server between requests.
- **Uniform Interface**: Resources are uniquely identified by standard URIs (Uniform Resource Identifiers).

---

## 2. Core HTTP Protocol Mechanics

### A. HTTP Methods
| Method | Operational Role | Idempotent | Common Analytics Use Case |
| :--- | :--- | :---: | :--- |
| **`GET`** | Retrieve / Fetch resource data | **Yes** | Fetching live stock quotes, NAV timeseries, historical FX rates |
| **`POST`** | Submit new data / execute order | No | Placing a buy/sell trade order, submitting user KYC forms |
| **`PUT`** | Update / Replace existing resource | **Yes** | Updating user address or risk tolerance profile |
| **`DELETE`**| Remove resource | **Yes** | Cancelling an open limit order |

### B. Common HTTP Status Codes
- **`200 OK`**: Request succeeded; payload returned.
- **`201 Created`**: Resource created successfully (typical for POST).
- **`400 Bad Request`**: Malformed syntax or missing query parameters.
- **`401 Unauthorized`**: Authentication credentials (API Key / Bearer Token) missing or invalid.
- **`403 Forbidden`**: Authenticated, but user lacks permissions for this resource.
- **`404 Not Found`**: Target URI endpoint does not exist.
- **`429 Too Many Requests`**: Rate limit exceeded; client must throttle requests.
- **`500 Internal Server Error`**: Server encountered an unhandled exception.

---

## 3. JSON (JavaScript Object Notation) Mechanics

JSON is the ubiquitous text-based format for exchanging semi-structured data across modern web APIs.

### Structure Breakdown:
- **Object (`{ ... }`)**: Key-value pairs enclosed in braces (analogous to Python dictionaries).
- **Array (`[ ... ]`)**: Ordered lists of values enclosed in square brackets (analogous to Python lists).
- **Supported Data Types**: String, Number, Boolean (`true`/`false`), Null, Object, Array.

---

## 4. End-to-End Extraction Pipeline Execution

The Python script [`api_data_extraction.py`](file:///D:/Admin/Documents/Week2_FinTech_and_Software_Ecosystem_Deliverables/api_data_extraction.py) executed the following steps:

```mermaid
flowchart LR
    A["Python requests.get()"] -->|Query Params + Headers| B["REST API Endpoint"]
    B -->|200 OK + JSON Payload| C["Raw JSON File (.json)"]
    C -->|pd.json_normalize()| D["Tabular DataFrame"]
    D -->|Add Computed Columns| E["Clean CSV Dataset (.csv)"]
```

### Script Execution Summary:
1. **Foreign Exchange API**:
   - Endpoint: `https://api.frankfurter.app/latest?from=USD`
   - Retrieved rates for **29 global currencies** relative to the USD.
   - Parsed nested dictionary `rates` into tabular rows with computed inverse rates (`inverse_rate_usd`) and UTC timestamps.
2. **Mutual Fund Timeseries API**:
   - Endpoint: `https://api.mfapi.in/mf/120503`
   - Retrieved **3,404 historical trading day records** for Axis ELSS Tax Saver Fund.
   - Converted string NAVs to numeric floats, parsed dates to ISO format, and saved to CSV.
