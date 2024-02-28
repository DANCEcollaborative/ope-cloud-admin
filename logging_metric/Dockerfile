FROM mysql:latest
EXPOSE 3306

ENV MYSQL_ROOT_PASSWORD=CloudCC@100
ENV MYSQL_DATABASE=employees

# RUN microdnf install -y procps-ng

RUN pip3 install requests watchdog

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
RUN export PATH=$PATH:/usr/bin/pip3:/usr/local/bin/docker-entrypoint.sh

COPY log_monitor_talk_to_activity_server.py /
COPY dump.sql /docker-entrypoint-initdb.d/

CMD ["mysqld"]
