create database zhaobiao; 
use zhaobiao;
create table if not exists zhaobiao_data(
  url varchar(30),采购项目名称 varchar(30),
  爬取时间 datetime,
  品目 varchar(20),
  采购单位 varchar(30),
  行政区域 varchar(10),
  公告时间 varchar(20),
  获取招标文件时间 varchar(20),
  招标文件售价 varchar(15),
  获取招标文件地点 varchar(30),
  开标时间 varchar(20),
  开标地点 varchar(30),
  预算金额 varchar(15),
  项目联系人 varchar(10),
  项目联系电话 varchar(20), 
  采购单位地址 varchar(30),
  采购单位联系方式 varchar(20),
  代理机构名称 varchar(20),
  代理机构地址 varchar(30),
  代理机构联系方式 varchar(15),
  PRIMARY KEY(采购项目名称,爬取时间)
)ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 



