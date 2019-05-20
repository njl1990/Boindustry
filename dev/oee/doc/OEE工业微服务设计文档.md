# 1 功能要求

## 1.1 OEE指标展示

###  1.1.1 单台设备OEE功能

* 可实时显示单台设备的当日OEE曲线

### 1.1.2 性能稼动率

* 可实时显示单台设备的当日性能稼动率

### 1.1.3 时间稼动率

* 可实时显示单台设备的当日性能稼动率

### 1.1.4 良品率

* 可实时显示单台设备的当日性能稼动率

## 1.2 设备清单功能

## 1.3 OEE参数管理

## 1.4 OEE事务填报



# 2 架构设计

# 3 UI设计

# 4 接口设计

## 4.1 OeeInfo

## 4.2 MachineList

##  4.3 OeeConfig

### 4.3.1 Page

#### OeeConfig

* WorkingTime
* StandardTimeList

### 4.3.2 Api

#### UpdateOeeConf

更新/新增OEE配置信息：

> UpdateOeeConf(id,type,value)

#### DeleteOeeConf

删除Oee配置信息

> DeleteOeeConf(id)

### 4.3.3 Service

#### LoadOeeConfList(filter)

#### GetOeeConf(filter)

# 5 数据结构设计

## 5.1 基础数据表 basedata

用于存储从接口直接获取的数据

## 5.2 主功能表 mainrcd

用于缓存计算数据，提供OEE可视化服务的

## 5.3 配置表 conf

用于存储Oee配置信息

| 配置表 |      |      |       |
| ------ | ---- | ---- | ----- |
| 字段   | _id  | type | value |
| 范例   | /    | DT   | 424   |

### 5.3.1 type 数据字典

| name         | 英文名                | type |
| ------------ | --------------------- | ---- |
| 故障时间     | downTime              | DT   |
| 换线时间     | change over time      | COT  |
| 调试时间     | adjust time           | AT   |
| 处理不良时间 | rejects handling time | RHT  |
| 出勤时间     | working time          | WT   |
| 计划停机时间 | Planned down time     | PDT  |
| 标准工时     | standard time         | ST   |

### 5.3.2 标准工时 ST定义

|      | 标准工时        |              |       |
| ---- | --------------- | ------------ | :---: |
| 字段 | MachineName     | ProductName  | Value |
| 范例 | 2000-11-11-3242 | MY5124028177 | 3000  |