# 📌 Workflow Orchestration, Kestra & ETL Pipelines Quiz - Solutions

## 1️⃣ Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size (i.e., the output file `yellow_tripdata_2020-12.csv` of the extract task)?
✅ **Answer:** `128.3 MB`

---

## 2️⃣ What is the rendered value of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04` during execution?
✅ **Answer:** `green_tripdata_2020-04.csv`

**📌 Explanation:**  
The template follows the pattern:  

```bash
{{inputs.taxi}}tripdata{{inputs.year}}-{{inputs.month}}.csv
```
When substituting the values:  
`green_tripdata_2020-04.csv`

## 3️⃣ How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?
✅ **Answer:** `24,648,499`
![number of rows in bigquery](images/2020_yellow.png)



---

## 4️⃣ How many rows are there for the Green Taxi data for all CSV files in the year 2020?
✅ **Answer:** `1,734,051`

![number of rows in bigquery](images/2020_green.png)

---

## 5️⃣ How many rows are there for the Yellow Taxi data for the March 2021 CSV file?
✅ **Answer:** `1,925,152`

![number of rows in bigquery](images/2020_green.png)

---

## 6️⃣ How would you configure the timezone to New York in a Schedule trigger?
✅ **Answer:** `Add a timezone property set to America/New_York in the Schedule trigger configuration`

