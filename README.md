My names is Lindeci.

You can test my api by "http://159.75.208.85:8080".


install app:

1、init mysql

      yum install mysql-server
      
      yum install mysql
      
      systemctl start mysqld.service
      
      systemctl enable mysqld
      
      systemctl daemon-reload
      

      mysql -u root -p
      use mysql
      ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';
      create user 'root'@'%' identified by 'root';
      grant all privileges on *.* to 'root'@'%';
      create database bit_ly;
      use bit_ly;

      CREATE TABLE `t_short_url` (
        `id` bigint NOT NULL AUTO_INCREMENT,
        `url_long` varchar(256) NOT NULL,
        `url_short` varchar(9) NOT NULL,
        `type` tinyint DEFAULT NULL,
        `general_count` int DEFAULT NULL,
        `click_count` int DEFAULT NULL,
        `share_count` int DEFAULT NULL,
        `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
        `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`),
        KEY `idx_url_long` (`url_long`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
      
      
2、init redis 

      yum install redis
      
      systemctl start redis
      
      systemctl status redis
      
      systemctl enable redis
      
      systemctl restart redis
      


3、install python and fastapi

      yum install python39
      
      pip install redis
      
      pip install mysql.connector
      
      pip install fastapi
      
      pip install uvicorn
      
