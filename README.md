# VideoSynopsis
- zauważyć, znaleźć klatki, w których był ruch
temporal spatial activity/intensity - globals()
-opencv/dlib do sledzenia ruchu

googlescholar
- pokazuje cytowane artykuły

Generalnie OK, ale parę uwag. Ważne jest, żeby ruch nie nakładał się na siebie.
Czyli musi Pan wyszukać fragmenty, które mają ruch w innych przestrzennych 
obszarach sekwencji wizyjnej. 
Oczywiście może być ich więcej niż 2, 
choć zapewne trudno będzie znajdywać dużo fragmentów, żeby były rozłączne przestrzennie.

Nie musi Pan wyrównywać fragmentów. 
Po prostu, kiedy "wchodzi" nowy fragment, to dorzuca Pan +1 do mianownika przy dzieleniu. 
I robi -1, jak fragment się kończy.

Oczywiście trzeba mieć przede wszystkim "maszynkę" do eksperymentowana 
i próbować jeszcze innych koncepcji, od razu oglądając efekty.

Nie wygląda to najgorzej, niemniej ewidentnie mamy problem z nakładaniem się obiektów. 
Dodatkowo proponowałbym przeprowadzenie testów na trochę dłuższych sekwencjach.
