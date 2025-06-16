# Factory Inventory Flask App

This project is a simple inventory management system for factory intranet using Flask and SQL Server.

## Setup

1. Create a `.env` file based on `.env.example` and configure SQL Server credentials.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Seed database with default data:
   ```bash
   python seed.py
   ```
4. Run application:
   ```bash
   python run.py
   ```

## Testing

Run unit tests with pytest:
```bash
pytest
```
