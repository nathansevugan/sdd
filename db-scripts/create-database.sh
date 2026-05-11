#!/bin/bash
psql -h localhost -U postgres -d postgres -f ./create-database.sql
psql "postgresql://daily_wisdom_user:daily_wisdom_user@localhost:5432/daily_wisdom" -f ./daily-wisdoms.sql 