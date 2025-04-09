# Modular ETL Framework

## About
This framework is designed for Extract - Transform - Load (ETL) operations, allowing you to process data from multiple source systems and load it into HDFS (Hadoop Distributed File System).

## Architecture
![image](https://github.com/hnphien/etl_framework/assets/51280965/919c348c-64d0-43ad-8cef-70ad950ee75c)

### Extract flowchart
![image](https://github.com/hnphien/etl_framework/assets/51280965/1acace15-8ea9-470d-804f-fff13dd5c7e3)

### Transform flowchart
![image](https://github.com/hnphien/etl_framework/assets/51280965/b6b6a10c-b8e1-4ca9-b394-6e6cba632488)


## Project Tree
├── src

│ ├── config

│ ├── extract

│ ├── transform

│ ├── load

│ └── db_interaction

├── logs

├── tests

├── data

├── docs

├── output

├── .gitignore

├── config.ini

├── etl_db.db

├── main.py

├── requirements.txt

└── README.md


### Descriptions
- **src**: Main source code directory.
  - **config**: Configuration files for the ETL process.
  - **extract**: Code for extracting data from source systems.
  - **transform**: Code for transforming the extracted data.
  - **load**: Code for loading the transformed data into HDFS.
  - **db_interaction**: Code for interacting with databases if needed.
- **logs**: Directory for storing log files generated during ETL process.
- **tests**: Directory for unit tests and testing-related files.
- **data**: Storage for input or intermediate data.
- **docs**: Documentation related to the ETL framework.
- **output**: Directory for final output files or data.
- **.gitignore**: File specifying excluded files/directories from version control.
- **config.ini**: Configuration file for connection details, API keys, etc.
- **etl_db.db**: Local database file if used.
- **main.py**: Main entry point for the ETL framework.
- **requirements.txt**: List of required Python packages.
- **README.md**: Main project documentation in Markdown.

## Features
This ETL framework includes the following core features:
- **Extract**: Fetch data from various source systems.
- **Transform**: Clean, process, and transform the extracted data.
- **Load**: Load the transformed data into HDFS.

## Tech Stack
The framework utilizes the following technologies:
- Programming Language: Python
- ETL Libraries/Frameworks: (Specify if applicable)
- Database System: (Specify if applicable)
- HDFS Setup: (Specify if applicable)

## Installation
Follow these steps to set up the ETL framework:
1. Clone this repository: `git clone <repository_url>`
2. Navigate to the project directory: `cd ETL_Framework`
3. Install required packages: `pip install -r requirements.txt`
4. Configure settings in `config.ini` as needed.

## How to Use
Perform ETL operations using the following steps:
1. Navigate to the project directory: `cd ETL_Framework`
2. Run the ETL process: `python main.py`
3. Monitor the logs in the `logs` directory for progress and issues.
4. Find the final output in the `output` directory.

For more detailed information, refer to the [documentation](./docs) provided.

---

Feel free to customize and expand this Markdown template to provide comprehensive information about your ETL framework.
