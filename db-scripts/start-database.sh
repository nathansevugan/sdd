#!/bin/bash
docker pull postgres
docker run --name daily-wisdom -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres
