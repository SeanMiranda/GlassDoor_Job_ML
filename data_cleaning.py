# -*- coding: utf-8 -*-
"""
Created on Sat May 23 16:42:29 2020

@author: seanj
"""

import pandas as pd
from datetime import date


df = pd.read_csv('glassdoor_jobs.csv')

#Salary

df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary' in x.lower() else 0)


df = df[df['Salary Estimate'] != '-1']
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_Kd = salary.apply(lambda x: x.replace('K','').replace('$',''))

min_hr = minus_Kd.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))
df['min_salary'] = min_hr.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = min_hr.apply(lambda x: int(x.split('-')[1]))

df['avg_salary'] = (df.min_salary+df.max_salary)/2


# Company name

df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating']<0 else x['Company Name'][:-3], axis=1)

# State Field

df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])
# print(df.job_state.value_counts())

df['same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis=1)

# Age of the company
df['age'] = df.Founded.apply(lambda x: x if x<1 else int(date.today().year)-x)

# Parsing job description

skill_dict = {'python_yn' : ['python'],
              'R_yn' : ['r studio', 'r-studio'],
              'spark' : ['spark'],
              'aws' : ['aws'],
              'excel' : ['excel'],
              'tableau': ['tableau'],
              'jmp': ['jmp'],
              'power_bi': ['power bi'],
              'sas' : ['sas']
}

for key, val in skill_dict.items():
    df[key] = df['Job Description'].apply(lambda x: 1 if any(ele in x.lower() for ele in val) else 0)
    print(df[key].value_counts())
    
print(df.columns)
df_out = df.drop(['Unnamed: 0'], axis=1)

df_out.to_csv('salary_data_cleaned.csv', index=False)