@echo off

uvicorn src.main:app --port 80 --host 0.0.0.0 --reload