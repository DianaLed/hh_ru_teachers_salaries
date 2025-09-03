#!/bin/sh
curl -s "https://api.hh.ru/vacancies?per_page=20&text=teacher&area=66&search_field=name&professional_role=132" \
| jq > ../data/raw/nnTeacher.json
curl -s "https://api.hh.ru/vacancies?per_page=99&text=teacher&area=1&search_field=name&professional_role=132" \
| jq > ../data/raw/moTeacher.json
