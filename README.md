# jobs-data-mining

This repository is part of a comprehensive project on analyzing the demand in the data science job market. It focuses on processing raw data collected using the [Jobs Advertisement Scrapper](https://github.com/a-anurag1024/li_jobs_collector). The processed data will be utilized to create visual analytics and insights, which will be presented through an interactive [dashboard](https://github.com/a-anurag1024/jobs-analytics-dashboard)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Future Directions](#future-directions)
- [License](#license)


## Introduction

The Jobs Data Mining Project aims to assist job seekers, recruiters, and market analysts in understanding the current job market landscape. By extracting data from job postings, the project identifies trends, in-demand skills, and other valuable insights.

At present, the focus is on gaining a deeper understanding of which skill clusters are most in demand across different seniority levels, employment types, job functions, and industries.


## Features

- **Extract Top Skills From Job Description**: Using Llama-3.1
- **Cluster the Top Skills**: Using sentence-transformer, Dimentionality Reduction and K-means Clustering.


## Installation

To get started with the project, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/a-anurag1024/jobs-data-mining.git
cd jobs-data-mining
pip install -e .
```

The Repository depends and builds on top of the MySQL Database created in the [Jobs Advertisement Scrapper](https://github.com/a-anurag1024/li_jobs_collector). So, the docker container for the MySQL-DB built in that project needs to be up for this repository to work.


## Usage

All the Runable scripts are kept at ```./scripts```. 

1. **Top Skills Extraction**: Run the top skills extractor script to obtain the top ten skills required from job postings.
    ```bash
    python scripts/extract_data.py
    ```
2. **Creating Top Skills Embedding**: To create clusters, we need to create the sentence embeddings of the top skills collected. To create the embeddings,
    ```bash
    python scripts/create_top_skills_emb.py
    ```
3. **Skills Clustering**: Script for clustering the top skills embeddings that has been extracted from step-2 and tagging of the clusters and creating word-clouds for the skills in those clusters. The wordclouds are stored at ```./mount/top_skills_wordclouds``` by default.
    ```bash
    python scripts/create_skills_clusters.py
    ```


## Future Directions

This is just a surface level analysis of the job posts dataset that has been collected (till now). To get more in-depth analytics, the following can be done:

1. In addition to identifying the top skills required, we can enhance specificity and detail by extracting information on the top tech stacks and tools needed for each job. Furthermore, we can analyze the educational qualifications and experience requirements for these roles.
2. Currently, the dataset does not include company names associated with each job posting. To enrich this information, we can establish a pipeline that uses Google Search, Glassdoor, or similar platforms, along with LLM, to gather company details such as company size, industry, work culture, and reviews.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
