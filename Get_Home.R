# Array delle coordinate
coordinate_array <- c(
  "45.66929172527679, 12.233426768912489", "45.66260512799594, 12.246697241930748",
  "45.68607814398785, 12.215461991142554", "45.657778449205416, 12.127068226584814",
  "45.558967724574174, 12.320753438216423", "45.566000427113735, 12.307793868908176",
  "45.71155082066824, 12.215926468914267", "45.59458135872523, 12.32250239774578",
  "45.77534680191902, 12.274016897753388", "45.69830387968747, 12.290299219117456",
  "45.676486608892716, 12.280540182403483", "45.60371706232694, 12.233733813091922",
  "45.63863299365098, 12.295233184256949", "45.66838422477975, 12.24262959774891",
  "45.66231704641649, 12.247224997748642", "45.66330594079054, 12.23240199774864",
  "45.690497610158815, 12.126027868913356", "45.64542279163172, 12.308196870766551",
  "45.66654923848084, 12.163182097748772"
)



# Carica i dati in un dataframe (assumi che il file CSV sia già caricato in 'dati')
dati <- read.csv(text = '
,Zona,IndirizzoPrincipale,NumeroPersone,Orario,Coordinate,Nomi,Partenza
0,"treviso porta santi quaranta ","via fortunato venanzio n8 ",2,03:00:00,"45.66929172527679, 12.233426768912489","Fiore Cicchetti 3516551788","https://maps.app.goo.gl/Kv8MqqoPXDckotyS9"
1,"Piazza Giustinian Recanati, Treviso","Piazza Giustinian Recanati, Treviso",8,03:00:00,"45.66260512799594, 12.246697241930748","Marco Carrieri 3402619456","Villa Navagero, Rovarè."
2,"Santa bona ","Via bezzecca 61",1,03:00:00,"45.68607814398785, 12.215461991142554","Caterina Antoniazzi 3931761761","Villa navagero erizzo rovarè "
3,"Via Bomben,7/A, Morgano(Tv)","Via Bomben,7/A, Morgano(Tv)",2,03:15:00,"45.657778449205416, 12.127068226584814","Alessandro Zanini 3921317559","XXX ROVARE"
4,"Marcon (VE)","Via Giacomo Matteotti 39, Marcon ",6,03:30:00,"45.558967724574174, 12.320753438216423","Filippo Giummolè 3921255224","XXX ROVARE"
5,"Marcon","Via Sant’ Antonio civ.5 Marcon (VE)",5,03:30:00,"45.566000427113735, 12.307793868908176","Pellizzon Eleonora 3500947201","San Biagio di Callalta"
6,"Ponzano","Via Giuseppe Garibaldi 10",8,03:45:00,"45.71155082066824, 12.215926468914267","Vincenzo Bocchetti 3284555567","starline (villani?)"
7,"Casale Sul Sile ","Via Re Ashoka 90",2,04:00:00,"45.59458135872523, 12.32250239774578","Olivia Schiavon 3923764006","XXX ROVARE"
8,"Spresiano ","Via fornasette 19 ",2,04:00:00,"45.77534680191902, 12.274016897753388","Dejan Chinellato 3296594056","Villa di Rovaré"
9,"Pezzan di CARBONERA","Via Cal di Breda 29 ",2,04:30:00,"45.69830387968747, 12.290299219117456","Matilde Rigato 3296145728","XXX ROVARE"
10,"Carbonera ","Via brigata Marche 165, Carbonera ",5,04:30:00,"45.676486608892716, 12.280540182403483","Marta Artuso 3926598156","XXX ROVARE"
11,"Preganziol","Viale Roma Preganziol ",5,04:30:00,"45.60371706232694, 12.233733813091922","Nicola Colesso 351 565 5140","XXX ROVARE"
12,"Casier (Tv)","Vicolo Peschierette 1 Casier",4,04:30:00,"45.63863299365098, 12.295233184256949","Leonardo Sartor 3396488028","Radika Club"
13,"Treviso","Piazza Tommasini 4",2,04:30:00,"45.66838422477975, 12.24262959774891","Ottavia Camilla Carobba +39 3932288444","Festa Villana"
14,"Treviso, Piazza Giustiniani","Via Pietro di Dante 1",2,04:45:00,"45.66231704641649, 12.247224997748642","Andrea Farinati 3469467690","Villa Navagero, Rovarè."
15,"treviso ","Via Giuseppe verdi ",2,05:00:00,"45.66330594079054, 12.23240199774864","Kristel Muharremi 3923279203","Villani"
16,"Padernello","via Bassano,12 , Padernello ",3,05:00:00,"45.690497610158815, 12.126027868913356","Beatrice Pavanello 3471264195","San Biagio di Callalta (Martino Morandin)"
17,"Silea","Via Fratelli Bandiera, 2",3,05:30:00,"45.64542279163172, 12.308196870766551","Tommaso De Rossi 3920190621","XXX ROVARE"
18,"paese","via arturo toscanini, 2/b, Paese",1,05:30:00,"45.66654923848084, 12.163182097748772","Alessandro Lucato 3924959795","starline group (villani?)"
', header = TRUE)

# Separare le coordinate in latitudine e longitudine
coordinate <- do.call(rbind, strsplit(as.character(dati$Coordinate), ", "))
lat <- as.numeric(coordinate[, 1])
long <- as.numeric(coordinate[, 2])

# Aggiungere etichette con il numero di persone
text(long, lat, labels = paste(dati$NumeroPersone), pos = 4, cex = 0.8, col = "red")

# Separare le coordinate in due colonne (latitudine e longitudine)
coordinate_matrix <- do.call(rbind, strsplit(coordinate_array, ", "))
coordinate_matrix <- apply(coordinate_matrix, 2, as.numeric)

# Definizione delle coordinate delle feste
feste <- data.frame(
  nome = c("Morandin", "Festa Martini (Istrana)", "Villani", "Perchè no? (Istrana)", "TREVISO"),
  latitudine = c(45.70111, 45.65617075144528, 45.68808383977507, 45.67915872772207, 45.66686821190888),
  longitudine = c(12.36806, 12.094269383482416, 12.362454539306622, 12.077284342329024, 12.242633810934722),
  colore = c("orange2", "blue", "green3", "magenta3", 'brown')
)

feste[c(2, 3), ] <- feste[c(3, 2), ]

# Calcolo dei limiti degli assi per includere tutto
x_lim <- range(c(coordinate_matrix[, 2], feste$longitudine))  # Limiti per la longitudine
y_lim <- range(c(coordinate_matrix[, 1], feste$latitudine))   # Limiti per la latitudine

# Plot delle coordinate (punti delle destinazioni)
plot(coordinate_matrix[, 2], coordinate_matrix[, 1], pch = 19, cex = 1,
     xlab = "Longitudine", ylab = "Latitudine", main = "Distribuzione delle Coordinate e Feste",
     xlim = x_lim, ylim = y_lim)

# Aggiungere i punti delle feste al grafico
points(feste$longitudine, feste$latitudine, col = feste$colore, cex = 3.5, pch = '*')

# Aggiungere i nomi delle feste a sinistra dei punti
text(feste$longitudine[1:2], feste$latitudine[1:2], labels = feste$nome[1:2], 
     pos = 2, cex = 0.8, col = feste$colore[1:2])

# Numero di persone per punto 
text(long, lat, labels = paste(dati$NumeroPersone), pos = 4, cex = 0.8)

# Aggiungere i nomi delle feste (3 e 4) alla destra dei punti
text(feste$longitudine[3:4], feste$latitudine[3:4], labels = feste$nome[3:4], 
     pos = 4, cex = 0.8, col = feste$colore[3:4])

# TREVISO
text(feste$longitudine[5], feste$latitudine[5], labels = feste$nome[5], 
     pos = 4, cex = 0.8, col = feste$colore[5])



#### CLUSTERING 

# Librerie necessarie
if (!require(ggplot2)) install.packages("ggplot2")
if (!require(deldir)) install.packages("deldir")

# Dati di esempio
set.seed(42)
n_points <- 100
coordinate <- data.frame(
  x = runif(n_points, min = 0, max = 100),
  y = runif(n_points, min = 0, max = 100)
)

# Centroidi iniziali (4 centroidi principali)
centroids <- data.frame(
  x = c(20, 80, 50, 50),
  y = c(20, 20, 80, 50)
)

# Step 1: Assegnare i punti ai centroidi principali
library(deldir)
assignments <- apply(as.matrix(coordinate), 1, function(point) {
  which.min(rowSums((t(as.matrix(centroids)) - point)^2))
})

# Step 2: Suddividere i cluster con sufficiente densità in cluster aggiuntivi
to_split <- c(3, 4) # Indici dei centroidi da suddividere
new_clusters <- list()

for (i in to_split) {
  points_in_cluster <- coordinate[assignments == i, ]
  
  # Controllo se il cluster contiene punti
  if (nrow(points_in_cluster) >= 2) { 
    kmeans_result <- kmeans(points_in_cluster, centers = 2, nstart = 25)
    new_clusters[[i]] <- data.frame(points_in_cluster, cluster = kmeans_result$cluster + (i * 10))
  } else if (nrow(points_in_cluster) > 0) { # Gestione cluster con 1 punto
    new_clusters[[i]] <- data.frame(points_in_cluster, cluster = i)
  }
}

# Step 3: Unire i cluster divisi e quelli rimasti invariati
final_clusters <- coordinate[assignments %in% setdiff(1:4, to_split), ]
final_clusters$cluster <- assignments[assignments %in% setdiff(1:4, to_split)]

# Aggiungi solo i cluster non vuoti
for (i in names(new_clusters)) {
  if (!is.null(new_clusters[[i]]) && nrow(new_clusters[[i]]) > 0) {
    final_clusters <- rbind(final_clusters, new_clusters[[i]])
  }
}

# Step 4: Visualizzazione
ggplot() +
  geom_point(data = final_clusters, aes(x = x, y = y, color = as.factor(cluster))) +
  geom_point(data = centroids, aes(x = x, y = y), color = "black", size = 4, shape = 4) +
  labs(title = "Clustering con 6 Cluster derivati da 4 Centroidi", color = "Cluster") +
  theme_minimal()




