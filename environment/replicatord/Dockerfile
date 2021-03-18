FROM centos:7

RUN yum -y install git ncurses-devel cmake gcc-c++ boost boost-devel wget unzip nano bzip2 mysql-devel mysql-lib

##
## Install mysql57 client, devel packages
##
RUN yum localinstall -y https://dev.mysql.com/get/mysql80-community-release-el7-1.noarch.rpm \
    && yum --disablerepo=mysql80-community --enablerepo=mysql57-community install -y \
        mysql-community-client \
        mysql-community-devel


RUN git clone https://github.com/tarantool/mysql-tarantool-replication.git mysql_tarantool-replication
COPY replicatord.yml mysql_tarantool-replication/replicatord.yml


RUN cd mysql_tarantool-replication \
    && git submodule update --init --recursive


RUN yum -y install g++ make
RUN cd mysql_tarantool-replication \
    && cmake . \
    && make
