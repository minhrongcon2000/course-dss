# course-dss

## Dependecies

- uvicorn
- FastAPI
- networkx
- numpy
- pandas
- streamlit

## Usage

1. Init MySQL database
2. Add data to database using `DSS_course.sql`
3. Change database config in `server/utils.py` under `ServerConfig` class

4. Create two terminal. One cd to `server` and execute `uvicorn api:app --reload`. One cd to `client` and execute `streamlit run main.py`

5. Enjoy the result

## Basic functionalities

- Take the whole transcript as an input and suggest new subject to learn based on that

## TODO

Deploy it to gh-page (maybe if we have time)
