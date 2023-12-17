FROM postgres

ENV POSTGRES_PASSWORD wirenboard
ENV POSTGRES_DB postgres

COPY db.sql /docker-entrypoint-initdb.d/
