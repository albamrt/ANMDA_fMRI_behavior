
require(dplyr)
require(reticulate)


data <- read.csv("data/behaviour.csv", sep=";")

data$time <- recode(data$session, S1 = 0, S2 = 3, S3 = 6, S4 = 12, S5 = 24) 

# Label data:
label(data$trial) = "Trial number"
label(data$block) = "Block number"
label(data$run) = "Run"
label(data$type) = "Memory or non-memory trial"
label(data$S_Angle) = "Stimulus angle (deg)"
label(data$P_Angle) = "Probe angle (deg)"
label(data$R_Angle) = "Response angle (deg)"
label(data$RT) = "Response time (s)"
label(data$MT) = "MT"
label(data$ts_b) = "Beginning timestamp"
label(data$ts_p) = "Probe timestamp"
label(data$ts_d) = "delay timestamp"
label(data$ts_r) = "Response timestamp"
label(data$ts_m) = "Mask timestamp"
label(data$ts_e) = "End timestamp"
label(data$m_angle) = "m_angle"
label(data$m_clock) = "_clock"
label(data$S_rad) = "Stimulus angle (rad)"
label(data$P_rad) = "Probe angle (rad)"
label(data$R_rad) = "Response angle (rad)"
label(data$prevstim_rad) = "Previous stimulus angle (rad)"
label(data$prevresp_rad) = "Previous response angle (rad)"
label(data$prevprob_rad) = "Previous probe angle(rad)"
label(data$prevmem) = "Previous trial is memory?"
label(data$futurestim_rad) = "Next stimulus angle (rad)"
label(data$futureresp_rad) = "Next response angle (rad)"
label(data$subject) = "Subject"
label(data$session) = "Session"
label(data$group) = 'Group'
label(data$error) = "Error (rad)"
label(data$errorprevstim) = "Previous stim error relative to current stim"
label(data$errorprevresp) = "Previous resp error relative to current stim"
label(data$errorprevprobe) = "Previous probe error relative to current stim"
label(data$diffstim) = "Difference current-previous stim (rad)"
label(data$diffresp) = "Difference current stim-previous resp (rad)"
label(data$difffuture) = "Difference current-next stim (rad)"
label(data$difffutureresp) = "Difference current stim-next resp (rad)"
label(data$diffprevprob) = "Difference current stim-previous probe (rad)"
label(data$time) = "Time"

# Remove variables:
data$m_angle <- NULL
data$m_clock <- NULL

# exclude session 5:
data <- data[data$session != 'S5',]

# time from months to years:
data$time <- data$time/12

# Convert variables to factors:
data$session <- as.factor(data$session)
data$session <- droplevels(data$session)
data$group <- as.factor(data$group)
data$subject <- as.factor(data$subject)

# Relevel factors:
data$group <- relevel(data$group, ref = 'C')

# Keep only memory trials:
data = data[data$type == 1, ]

# time from months to days
# data$time <- data$time*30

# Removing RT>2.8 (as max RT is 3, in these trials they probably needed more time):
data = data[data$RT<2.8,]

# Subjects to remove, having more than 50% outlier trials (abs error>0.7):
outliers <- data %>% 
  group_by(subject, session) %>%
  summarise(outliers = sum(abs(error)>0.7), trials = n(), propout = sum(abs(error)>0.7)/n()) %>%
  filter(propout>0.5)


# Removing outlier subjects:
data = data %>% 
  filter(!(paste(subject, session, sep = '') %in% paste(outliers$subject, outliers$session, sep = '')))

# removing outlier trials 
# data = data[abs(data$error) < 0.7,]

# rename columns
colnames(data)[colnames(data) %in% c('S_Angle', 'P_Angle', 'R_Angle', 'diffstim', 'diffresp', 'difffuture')] <- 
  c('target', 'probe', 'response', 'prevcurr', 'prevrespcurrstim', 'futurcurr')

# select only needed columns:
dat <- data[, c('subject', 'group', 'session', 'time',  'trial',  'block', 'run', 'type', 'error', 'RT',
         'target', 'probe', 'response', 'prevcurr', 'prevrespcurrstim', 'futurcurr')]


write.csv(data, "data/preprocessed.csv", row.names = FALSE)

py_save_object(data, "data/preprocessed.pkl", pickle = "pickle")


