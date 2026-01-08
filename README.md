# LaunchSentiment: Wikipedia Pageviews Analytics Pipeline 

## 🎯 Project Overview <br>
LaunchSentiment is a stock market prediction tool that leverages Wikipedia pageview data to perform sentiment analysis.
It hypothesizes that an increase in a company's Wikipedia page views indicates positive sentiment and potential stock price increase, while a decrease suggests waning interest and potential stock price decline. <br>

This pipeline tracks the Wikipedia pageviews for five major tech companies:
* Apple
* Amazon
* Facebook (Meta)
* Google
* Microsoft

## ✨ Features
* Automated Data Ingestion: Downloads hourly Wikipedia pageview dump (50MB+ compressed file)
* Efficient Processing: Extracts and filters millions of records for target companies
* Data Storage: Loads processed data into a PostgreSQL database with optimized indexing
* Analytics: Identifies companies with the highest pageviews
* Email Notifications: Sends success notifications via SMTP
* Error Handling: Robust retry mechanism with configurable delays
* Monitoring: Comprehensive logging for debugging and tracking

## 📁 Project Structure
```
Wikipedia_pageviews/
│
├── wikipedia_pageviews_dag.py          # Main DAG file
│
├── include/
│   ├── analysis/
│   │   ├── create_table.sql            # Database schema
│   │   └── analysis.sql                # Analysis queries
│   │
│   ├── data/
│   │   ├── raw/                        # Downloaded .gz files
│   │   └── processed/                  # Extracted .txt files
│   │
│   ├── download_file.py
│   │
│   ├── extract_file.py
│   │
│   ├── process_and_load.py
│   │
│   └── email_template.html             # Email notification template
│
└──__pycache__
```

### 🔄 DAG Tasks
![Tasks](wikipedia_pageviews-graph.png)

| **Task**          | **Description**                       |
|-------------------|---------------------------------------|
| create_table      | Creates PostgreSQL table with indexes |
| download          | Downloads gzipped pageview file       |
| extract           | Extracts gzip to text file            |
| load              | Filters and loads data to PostgreSQL  |
| analyze_data      | Runs SQL query to find top company    |
| send_notifcations | Sends success notification email      |

## 📈 Sample Output
After a successful pipeline run:
![Email to admin after a successful run](success_mail.png)


## 📚 Data Source Documentation
* **Wikipedia Pageviews:** https://dumps.wikimedia.org/other/pageviews/
* **Data Structure:** https://wikitech.wikimedia.org/wiki/Analytics/Data_Lake/Traffic/Pageviews
* **Technical Details:** https://meta.wikimedia.org/wiki/Research:Page_view

## ⚙️ Tools
* Apache Airflow
* Python
* SQL

-----------------

***Built by Ufuoma with ❤️ using Apache Airflow***

