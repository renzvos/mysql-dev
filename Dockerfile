FROM oraclelinux:8

ARG MYSQL_SERVER_PACKAGE=mysql-community-server-minimal-8.0.29
ARG MYSQL_SHELL_PACKAGE=mysql-shell-8.0.29

# Setup repositories for minimal packages (all versions)
RUN rpm -U https://repo.mysql.com/mysql-community-minimal-release-el8.rpm \
  && rpm -U https://repo.mysql.com/mysql80-community-release-el8.rpm

RUN dnf install -y microdnf && \
    rm -rf /var/cache/dnf

# Install server and shell 8.0
RUN microdnf update && echo "[main]" > /etc/dnf/dnf.conf \
  && microdnf install -y $MYSQL_SHELL_PACKAGE \
  && microdnf install -y --disablerepo=ol8_appstream \
   --enablerepo=mysql80-server-minimal $MYSQL_SERVER_PACKAGE \
  && microdnf clean all \
  && mkdir /docker-entrypoint-initdb.d

RUN dnf -y module disable python36 && \
    dnf -y module enable python38 && \
    dnf -y install python38 python38-pip python38-setuptools python38-wheel && \
    rm -rf /var/cache/dnf

COPY build build
RUN build/prepare-image.sh && rm -f build/prepare-image.sh
ENV MYSQL_UNIX_PORT /var/lib/mysql/mysql.sock

RUN pip3 install requests
RUN pip3 install six
RUN pip3 install mysql-connector-python
#RUN dnf -y install nano


COPY automation automation
RUN chmod u+x automation/backup.py
RUN ln -s automation/backup.py backup
RUN chmod u+x automation/scripts/showram.sh
RUN ln -s automation/scripts/showram.sh showram

ENTRYPOINT ["python3","automation/start.py"]
HEALTHCHECK CMD /automation/company_startup/healthcheck.sh
EXPOSE 3306 33060 33061
CMD ["mysqld"]
