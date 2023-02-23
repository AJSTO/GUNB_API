## 👨‍💻 Built with
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" /> <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white"/> <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" /> <img src="https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white" /> 
<img src="https://d1tlzifd8jdoy4.cloudfront.net/wp-content/uploads/2020/09/gcp-eyecatch-cloud-run_1200x630.png" width="100" height="27,5" />
<img src="https://www.scitylana.com/wp-content/uploads/2019/01/Hello-BigQuery.png" width="100" height="27,5" />

##  🗺️Descripction about project

In this project, I focused on implementing an API that allows communication with the bigquery database created in my [GUNB_building_permissions](https://github.com/AJSTO/GUNB_building_permissions) project, which contains information from the [GUNB](https://wyszukiwarka.gunb.gov.pl/pobranie.html) (Main Building Supervision Office) website in the form of aggregates collecting information on building permits issued in the last: 1 month, 2 months and 3 months months, divided by building category and type of building permission. Aggregates are collected for territorial units: voivodships, poviats and registration units.

## 🚪Endpoints
- @api.get("/") - homepage of GUNB API
- @api.get("/info") - endpoint created  to get all available unit id (voivodships, poviats and registration units)
- @api.get("/aggregates/{unit_id}") -endpoint created to get aggregates for given unit id (mandatory) and month (optional - if you dont pass value you will receive aggregates for the current month
## 🌲 Project tree
```bash
├── Dockerfile # Docker file to build container
├── README.md # Description about project
├── credentials.json # Your google cloud JSON key to authenticate access to cloud services in the project
├── .env # enviromental variables
├── home.html # HTML file for homepage
├── main.py # Python scrip with FastAPI
└── requirements.txt # All needed requirements to run container properly
```

## 🔑 Setup 
To run properly this project you should change variables in .env-sample file and rename it to .env:
```bash
# BIGQUERY INFO ABOUT MY PROJECT, DATASET AND TABLE
PROJECT_ID=your_project_id
DATASET_NAME=your_dataset_name
TABLE_AGG=your_aggregates_table_name
TABLE_UNIT_INFO=your_unit_info_table_name
JSON_KEY_BQ=your_json_key_filename
```
## ⚙️Deploying FastAPI on Cloudrun
Check github repo: [FastAPI-on-Google-Cloud-Run](https://github.com/sekR4/FastAPI-on-Google-Cloud-Run)

## ⏩ Demo version
[GUNB-API](https://gunb-api-4zobymftpq-lm.a.run.app)
![IMG_API](https://i.ibb.co/Nnjx3cw/Zrzut-ekranu-2023-02-21-o-12-04-11.png)


To get into Swagger UI click on the API home page: [API Documentation](https://gunb-api-4zobymftpq-lm.a.run.app/docs)
![IMG_SWAGGER](https://i.ibb.co/qRk0YSQ/Zrzut-ekranu-2023-02-22-o-20-09-19.png)
