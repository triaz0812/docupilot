---
title: "Cloudera on Cloud Preview Features: Documentation"
source_url: https://docs.cloudera.com/cdp-public-cloud-preview-features/cloud/index.html
---

Cloudera on Cloud Preview Features: Documentation




Homepagecloud



# Cloudera on Cloud Preview Features

* Cloudera on cloud Release Notes
* Cloudera on cloud Release Summaries
* Cloudera on cloud Patterns
* Cloudera on cloud Preview Features

The information provided on these pages outlines features currently available in preview.
Access to preview features is provided upon request for customers for trial and evaluation.
The components are provided âas isâ, without warranty or support, and Cloudera assumes no liability for their use.
Customers should use preview features at their own risk.

To enable a preview feature in your Cloudera account, contact your account team.

## Cloudera Data Engineering

Using JVM debugger with Apache Spark jobs
:   published: 2022-11-23;
    modified: 2022-11-23  
    Learn how to connect a JVM debugger remotely to Spark jobs (driver/executor).

## Cloudera Data Hub

Schedule-based Autoscaling for Cloudera Data Hub Clusters Using Impala
:   published: 2023-11-09;
    modified: 2024-12-04  
    Schedule-based autoscaling for Cloudera Data Hub clusters using Impala is a feature that scales the number of nodes in an executor host group up or down based upon a schedule that you define.

## Cloudera Data Warehouse

User quotas in admission control
:   published: 2025-04-23;
    modified: 2025-04-23  
    Learn how User Quotas in Impala Admission Control optimize resource management and ensure fair query distribution for seamless operation.

Running queries on system tables
:   published: 2025-04-23;
    modified: 2025-04-23  
    Learn about Impala's new "only coordinators" request pool lets system table queries bypass executor queues, reducing delays caused by admission control. Benefit from faster query execution for system tables, improving efficiency and responsiveness.

Hue File Browser
:   published: 2025-04-23;
    modified: 2025-04-23  
    The Hue File Browser is a web-based interface designed to provide seamless interaction with multiple file systems. With enhanced usability and functionality, the File Browser improves data management within the file system, offering a streamlined experience.

Using Hive Data Connectors to support External Data Sources
:   published: 2023-11-20;
    modified: 2023-11-20  
    Learn how you can achieve SQL query federation by using Hive data connectors to map databases present in external data sources to a local Hive Metastore.

Reserving nodes for auto-scaling
:   published: 2022-07-26;
    modified: 2022-07-26  
    Learn how to accelerate Virtual Warehouse startup and autoscaling by configuring buffer nodes to keep compute instances on standby, ready to join new or autoscaled clusters.

Using the Impala AI Function
:   published: 2024-07-26;
    modified: 2024-07-26  
    Learn how you can use Impala's ai\_generate\_text function to access Large Language Models in SQL queries. This function enables you to input a prompt, retrieve the response, and include it in results.

Using Impala to query external JDBC data sources
:   published: 2024-07-26;
    modified: 2024-07-26  
    Learn how you can use external JDBC tables to connect Impala to a database, such as MySQL, PostgreSQL, or another Impala cluster and read the data in the remote tables.

Impala Workload Management
:   published: 2024-07-26;
    modified: 2024-07-30  
    Learn how to use the Impala query logging capability in Cloudera Data Warehouse to archive essential query profile data into dedicated database tables, enabling consolidated reporting on previously executed queries.

## Governance

Integrating CDP Data Catalog with AWS Glue Data Catalog
:   published: 2021-08-09;
    modified: 2021-12-08  
    While using AWS Glue in Data Catalog, you will be able to experience a complete snapshot metadata view, along with other visible attributes that can power your data governance capabilities.

Navigating to tables and databases in Hue using Data Catalog
:   published: 2021-08-07;
    modified: 2021-08-07  
    The integration between Data Catalog and Cloudera Data Warehouse service provides a direct web link to the Hue instance from the Data Catalog web UI, making it easy to navigate across services.

Support for CDP Private Cloud Base clusters in Data Catalog
:   published: 2022-02-24;
    modified: 2022-04-06  
    Data Catalog now supports discovering and profiling assets that reside in Cloudera Private Cloud Base clusters.

Supporting High Availability for Profiler services
:   published: 2021-08-07;
    modified: 2021-08-07  
    The Data Catalog profiler services is now supported by enabling the High Availability feature.

Transitioning Profiler Manager Service into SDX
:   published: 2022-02-24;
    modified: 2022-02-24  
    The Profiler Manager Service is moved to the SDX infrastructure.

## Cloudera AI

Using Job Retry
:   published: 2025-08-25;
    modified: 2025-09-04  
    The Job Retry feature enables automatic retries of jobs based on their terminal execution.

Private Cluster Support
:   published: 2022-01-06;
    modified: 2023-07-17  
    Private Clusters provide a simple way to create a secure cluster, where the API server and the workloads themselves only rely on private IP addresses that are not accessible from the internet.

CMK Encryption on AWS
:   published: 2021-08-10;
    modified: 2022-08-10  
    Cloudera Machine Learning on AWS is now able to use a Customer Master Key to encrypt data.

Retry Workspace Installation
:   published: 2023-04-26;
    modified: 2023-04-26  
    When Workspace Provisioning experiences a problem, it is easy to restart the provisioning process from the point where it stopped.

## Cloudera Management Console

Root Disk Vertical Scaling
:   published: 2025-05-05;
    modified: 2025-05-05  
    You can manually add more storage capacity on the root disks attached to the Cloudera environment, Data Lake, or Cloudera Data Hub instances.

Configuring SELinux for Cloudera environments
:   published: 2025-02-07;
    modified: 2025-02-07  
    You can choose the SELinux mode for your Cloudera environment based on your security requirements.

Rebuilding FreeIPA
:   published: 2025-01-25;
    modified: 2025-01-25  
    You can rebuild FreeIPA in case all the instances are lost or the LDAP database is damaged beyond repair.

Enabling Secure Boot Option for GCP
:   published: 2025-01-30;
    modified: 2025-01-30  
    VMs on GCP are created without the Secure Boot option enabled by default. You can request to have the Secure Boot option for subsequently provisioned VMs.

Deploying Cloudera in multiple GCP availability zones
:   published: 2025-01-22;
    modified: 2025-02-25  
    You can optionally choose to deploy Data Lake, FreeIPA, and Cloudera Data Hub clusters across multiple availability zones (multi-AZ). With multi-AZ support, newly created GCP environments, enterprise Data Lakes and Cloudera Data Hub clusters using HA templates can be deployed across multiple availability zones of the selected GCP region. This provides fault tolerance during the extreme event of an availability zone outage.

Horizontal scaling for the Data Lake
:   published: 2024-03-22;
    modified: 2024-12-04  
    An enterprise Data Lake can be scaled horizontally, meaning that you can add additional instances to dedicated host groups for some services.

Disk Vertical Scaling â Disk Type Change and Resizing in Azure
:   published: 2023-12-12;
    modified: 2024-12-04  
    The standard magnetic storage disks attached to Data Lake and Data Hub clusters can be changed or resized without downtime.

GCS Fine-Grained Access Control
:   published: 2023-06-29;
    modified: 2025-02-25  
    Register a GCP environment with Ranger Authorization Service enabled to allow Google Cloud Storage users to use fine-grained access policies and audit capabilities available in Apache Ranger.

Disabling S3Guard in an Existing Cloudera Environment
:   published: 2022-10-05;
    modified: 2024-12-04  
    You may need to disable S3Guard when upgrading your Data Lakes or Cloudera Data Hub clusters. Use the Beta CDP CLI to disable S3Guard in an existing Cloudera environment.

Azure VM Encryption at Host
:   published: 2022-06-06;
    modified: 2024-12-04  
    You can optionally enable encryption at host for Data Lake, FreeIPA, and Cloudera Data Hub clusters. Currently, you need to enable it individually for each Virtual Machine on Azure Portal.

New UI for adding a Cloudera Base on premises cluster
:   published: 2022-03-29;
    modified: 2024-12-04  
    Register a Cloudera Base on premises cluster as a classic cluster using Cloudera Manager and Knox endpoints so that you can use this cluster in Cloudera Replication Manager and Cloudera Data Catalog services.

## Cloudera Replication Manager

Snapshot Policies in Replication Manager
:   published: 2022-02-25;
    modified: 2022-02-25  
    You can create HDFS and HBase snapshot policies in Replication Manager to schedule taking snapshots of snapshottable HDFS directories and HBase tables at regular intervals. An HDFS directory is snapshottable after it has been enabled for snapshots, or because a parent directory is enabled for snapshots in Cloudera Manager.

## Cloudera Operational Database

AWS Graviton instances in Cloudera Operational Database
:   published: 2024-12-11;
    modified: 2025-01-20  
    Learn how to create AWS Graviton-based Cloudera Operational Database clusters.

HBase Time-based Data Tiering using Persistent BucketCache
:   published: 2024-10-01;
    modified: 2024-10-09  
    Learn how you can configure time-based priority caching for HBase, and also define a specific time range for cache eviction policy.

Fast autoscaling in Cloudera operational database
:   published: 2025-01-15;
    modified: 2025-01-15  
    Learn how to enable and configure fast autoscaling in the Cloudera Operational Database.

Rolling Upgrade in Cloudera Operational Database
:   published: 2025-01-15;
    modified: 2025-01-15  
    Learn how to perform a rolling and a non-rolling Cloudera Runtime and operating system upgrade for your existing Cloudera Operational Database.

Monitoring Metrics in the Cloudera Operational Database with Grafana
:   published: 2025-01-16;
    modified: 2025-01-16  
    Learn how to enable the Grafana URL for your COD database so that you can visualize the COD metrics using the Grafana dashboard.

Scaling Cloudera Operational Database Instances vertically
:   published: 2025-01-16;
    modified: 2025-01-16  
    Learn how to scale up a Cloudera Operational Database Instance vertically.

Custom table coprocessors in Cloudera Operational Database
:   published: 2025-01-16;
    modified: 2025-01-16  
    Learn how to use custom table coprocessors in Cloudera Operational Database

![cloudera_short_logo.png](https://docs.cloudera.com/common/img/cloudera_short_logo.png)

![cloudera.png](https://docs.cloudera.com/common/img/cloudera.png)
