NMDAEvents <- read.csv("data/NMDAEvents.csv", sep = ";")
NMDAEvents <- NMDAEvents %>%
  select(record_id, redcap_event_name, n_visit, testing, birthdate, gender)
NMDAEvents$session <- paste0('S', substr(NMDAEvents$redcap_event_name, 8, 8))
NMDAEvents$testingDate <- as.POSIXct(NMDAEvents$testing, format = "%Y-%m-%d")

Visit0 <- NMDAEvents %>%
  group_by(record_id) %>%
  filter(!is.na(testingDate)) %>%
  filter(testingDate == min(testingDate)) %>%
  select(record_id, testingDate) %>%
  rename(V0 = testingDate)

NMDAEvents_all <- merge(NMDAEvents, Visit0, by = 'record_id', all.x = TRUE)
require(lubridate)
NMDAEvents_all$time <- interval(NMDAEvents_all$V0, NMDAEvents_all$testingDate) %/% months(1)
NMDAEvents_all <- NMDAEvents_all %>%
  rename(subject = record_id)

beh <- read.csv("data/behaviour.csv", sep = ";")

data <- merge(beh, NMDAEvents_all, by = c('subject', 'session'), all.x = TRUE, all.y = FALSE)

data[,c('subject', 'session', 'time')]

save(data, file = 'data.RData')
