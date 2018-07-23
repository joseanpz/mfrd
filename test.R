# Title     : TODO
# Objective : TODO
# Created by: BRM08931
# Created on: 20/07/2018
###### MODELO DETECCIÃN DE FRAUDES

library(Hmisc)

library(readr)
library(stats)

# Se genera un dataframe a partir de una nueva observaciÃ³n

BANDERA_ <- 1

NEW_OBS <- as.numeric(t(c(FOLIO = '00000001',FOLIOBURO = '00000001',FECHABURO = '01/01/2018',
                             CONSULTAS_U02M_SBCBR = 16, MOP_MAXIMO_U24M_SERVSGRALES = 8,
                             PCT_DIR_JALGTO = 1, PCT_APERTURAS_U18M = 0.28571429,
                             PCT_APERTURAS_ANT_REGBC = 0,
                             PCT_CTAS_BANCARIAS = 0.2857143, PCT_CTAS_SERVS_GRALES = 0.28571429,
                             PROM_LIMCRE_MAXCRE_SERVSGRALES = 339000, PCT_ALERTAS_JUICIOS = 0,
                             UNIVERSO_11 = BANDERA_)))


# La tabla JAT_FRAUDES contiene el Universo de construcciÃ³n del modelo

JAT_FRAUDES <- read_csv("JAT_FRAUDES.csv")

y<-JAT_FRAUDES[JAT_FRAUDES$UNIVERSO_11==1|JAT_FRAUDES$UNIVERSO_11==2,]

# Se adjunta el nuevo registro
JAT_FRAUDES <- rbind(JAT_FRAUDES,NEW_OBS)

JAT_FRAUDES$CONSULTAS_U02M_SBCBR[JAT_FRAUDES$CONSULTAS_U02M_SBCBR==-1] <- NA
JAT_FRAUDES$PCT_DIR_JALGTO[JAT_FRAUDES$PCT_DIR_JALGTO==-1] <- NA
JAT_FRAUDES$PCT_APERTURAS_U18M[JAT_FRAUDES$PCT_APERTURAS_U18M==-1] <- NA
JAT_FRAUDES$PCT_APERTURAS_ANT_REGBC[JAT_FRAUDES$PCT_APERTURAS_ANT_REGBC==-1] <- NA
JAT_FRAUDES$PCT_CTAS_BANCARIAS[JAT_FRAUDES$PCT_CTAS_BANCARIAS==-1] <- NA
JAT_FRAUDES$PCT_CTAS_SERVS_GRALES[JAT_FRAUDES$PCT_CTAS_SERVS_GRALES==-1] <- NA
JAT_FRAUDES$PROM_LIMCRE_MAXCRE_SERVSGRALES[JAT_FRAUDES$PROM_LIMCRE_MAXCRE_SERVSGRALES==-1] <- NA
JAT_FRAUDES$PCT_ALERTAS_JUICIOS[JAT_FRAUDES$PCT_ALERTAS_JUICIOS==-1] <- NA
JAT_FRAUDES$UNIVERSO_11[JAT_FRAUDES$UNIVERSO_11==-1] <- NA

# Se imputan los vacÃ­os (NA)
JAT_FRAUDES <- apply(JAT_FRAUDES[,4:(ncol(JAT_FRAUDES))],2,impute,fun=median)

# Se identifica el Universo de fraude
JAT_FRAUDES[JAT_FRAUDES[,ncol(JAT_FRAUDES)]==2] <- 1

# Se normalizan las variables
JAT_FRAUDES <- cbind(scale(JAT_FRAUDES[,1:ncol(JAT_FRAUDES)-1]),JAT_FRAUDES[,ncol(JAT_FRAUDES)])

# Se obtiene un modelo de regresiÃ³n lineal mÃºltiple
mod <- lm(JAT_FRAUDES[,ncol(JAT_FRAUDES)] ~ .,data = as.data.frame(JAT_FRAUDES))

# Se calcula la distancia de Cook
cooksd <- cooks.distance(mod)

# Se clasifica el nuevo registro
POSIBLE_FRAUDE <- cooksd[length(cooksd)] > 0.000032891

