```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'fontSize': '16px'}, 'themeConfig': {'fontFamily': 'arial'}}}%%
graph TD
    A[Client] -->|HTTP Requests| B[CarPool API]
    
    subgraph API Endpoints
        C[Root GET]
        D[List Carpools]
        E[Get Carpool]
        F[Create Carpool]
        G[Update Carpool]
        H[Delete Carpool]
        B --> C
        B --> D
        B --> E
        B --> F
        B --> G
        B --> H
    end

    subgraph Data Model
        I[CarPool]
        J[Properties]
        K[ID]
        L[Driver Name]
        M[Car Model]
        N[Available Seats]
        O[Departure Time]
        P[Departure Location]
        Q[Destination]
        R[Price Per Seat]
        S[Is Active]
        I --> J
        J --> K
        J --> L
        J --> M
        J --> N
        J --> O
        J --> P
        J --> Q
        J --> R
        J --> S
    end

    subgraph In-Memory Storage
        T[CarPool List]
    end

    subgraph Response Codes
        U[Success 200]
        V[Not Found 404]
        W[Validation Error 422]
    end

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style I fill:#dfd,stroke:#333,stroke-width:2px
    style T fill:#fdd,stroke:#333,stroke-width:2px
    style U fill:#9f9,stroke:#333,stroke-width:1px
    style V fill:#f99,stroke:#333,stroke-width:1px
    style W fill:#ff9,stroke:#333,stroke-width:1px
```

# CarPool API Architecture

## Components

1. **Client**
   - Makes HTTP requests to the API
   - Can be a web application, mobile app, or other service

2. **API Endpoints**
   - Root endpoint (`/`): Welcome message
   - List all carpools (`GET /carpools`)
   - Get specific carpool (`GET /carpools/{id}`)
   - Create carpool (`POST /carpools`)
   - Update carpool (`PUT /carpools/{id}`)
   - Delete carpool (`DELETE /carpools/{id}`)

3. **Data Model (CarPool)**
   - Unique identifier (id)
   - Driver information (name, car model)
   - Trip details (seats, departure time, locations)
   - Pricing (price per seat)
   - Status (active/inactive)

4. **Storage**
   - In-memory list of CarPool objects
   - Each operation (CRUD) interacts with this storage

5. **Response Codes**
   - 200: Successful operation
   - 404: Resource not found
   - 422: Validation error (e.g., negative values)

## Data Flow

1. **Create Flow**
   ```
   Client -> POST /carpools -> Validate Data -> Create CarPool -> Store -> Return Created
   ```

2. **Read Flow**
   ```
   Client -> GET /carpools/{id} -> Find CarPool -> Return Data
   ```

3. **Update Flow**
   ```
   Client -> PUT /carpools/{id} -> Validate Data -> Update CarPool -> Store -> Return Updated
   ```

4. **Delete Flow**
   ```
   Client -> DELETE /carpools/{id} -> Find CarPool -> Remove -> Return Success
   ```

## Validation Rules

1. **Required Fields**
   - All fields except `id` are required
   - `id` is auto-generated

2. **Value Constraints**
   - `available_seats` must be > 0
   - `price_per_seat` must be > 0
   - `departure_time` must be a valid datetime

3. **Default Values**
   - `is_active` defaults to `True`
   - `id` is `None` for new carpools 