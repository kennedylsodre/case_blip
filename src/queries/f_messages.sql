WITH messages as (
  SELECT 
    *
    ,CASE 
      WHEN MessageOriginator = 'Bot' THEN ToIdentity 
      ELSE FromIdentity 
    END AS User
  FROM `carna-belo.carna_belo_bot.Messages` 
) 

,messages_previous as (
SELECT 
  * 
  ,lag(storagedate) over(partition by User,cast(StorageDate as date) ORDER BY MessageSequentialID asc) StorageDatePrevious
  ,lag(MessageOriginator) over(partition by User,cast(StorageDate as date) ORDER BY MessageSequentialID asc) MessageOriginatorPrevious
FROM messages ) 


SELECT 
  *
  ,CAST(StorageDate as Date) DataMessage
  ,EXTRACT(HOUR FROM StorageDate) HoraMensagem
  ,CASE 
    WHEN StorageDatePrevious is not null and MessageOriginator <> MessageOriginatorPrevious 
    THEN TIMESTAMP_DIFF(StorageDate,StorageDatePrevious,minute) 
    ELSE NULL 
  END as TempoEntreMensagens

FROM messages_previous