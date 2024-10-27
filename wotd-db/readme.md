# Useful Commands

## Development
```bash
psql -d wotd_db -U admin
psql -d wotd_db -U admin -a -f /docker-entrypoint-initdb.d/init.sql
```

```sql
DROP SCHEMA public CASCADE; CREATE SCHEMA public;
```