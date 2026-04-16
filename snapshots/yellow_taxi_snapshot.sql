{% snapshot yellow_taxi_snapshot %} # this file defines a snapshot. 

{{
  config(
    target_schema='snapshots', #This tells dbt where to store the snapshot table. 
    unique_key='trip_id',
    strategy='check',
    check_cols=[
      'VendorID',
      'tpep_dropoff_datetime',
      'passenger_count',
      'trip_distance',
      'RatecodeID',
      'PULocationID',
      'DOLocationID',
      'payment_type',
      'fare_amount',
      'tip_amount'
    ]
  )
}}
# to_hex(...) converts the hash into a readable hexadecimal string
select
    to_hex(md5(concat(
        cast(VendorID as string),
        '|',
        cast(tpep_dropoff_datetime as string),
        '|',
        cast(passenger_count as string),
        '|',
        cast(trip_distance as string),
        '|',
        cast(RatecodeID as string),
        '|',
        cast(PULocationID as string),
        '|',
        cast(DOLocationID as string)
    ))) as trip_id,
    VendorID,
    tpep_dropoff_datetime,
    passenger_count,
    trip_distance,
    RatecodeID,
    store_and_fwd_flag,
    PULocationID,
    DOLocationID,
    payment_type,
    fare_amount,
    extra,
    mta_tax,
    tip_amount
from {{ source('raw_data', 'yellow_tripdata_partitioned') }}

{% endsnapshot %}