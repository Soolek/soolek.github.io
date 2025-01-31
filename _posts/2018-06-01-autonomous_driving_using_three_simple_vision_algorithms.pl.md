---
layout: post
title:  "Autonomiczne prowadzenie przy pomocy trzech prostych algorytmów wizyjnych"
date:   2018-06-01 17:00
public: true
categories: developer
lang: pl
---

Celem tego wpisu jest zaznajomienie czytelnika z trzema prostymi algorytmami wizyjnymi dzięki którym można uzyskać prosty algorytm autonomicznego prowadzenia.

Autonomiczne prowadzenie jest bardzo skomplikowanym tematem. Aby poprowadzić samochód autonomicznie, duże sieci neuronowe, uczenie maszynowe oraz dużo inżynierii musi zostać użyte. Prymitywny algorytm autonomicznego prowadzenia może jednak zostać stworzony przy pomocy trzech prostych algorytmów wizyjnych, przedstawionych w tym wpisie. Efektywność tego algorytmu jest niska, ale jako że nie wymaga dodatkowej wiedzy ze sztucznej inteligencji, jest to bardzo dobry punkt początkowy do dalszych badań.

Celem tego algorytmu jest kierowanie wzdłuż drogi oraz kontrola prędkości odpowiednio do zakrętów. Aby zobaczyć algorytm w akcji, środowisko do jego przetestowania będzie potrzebne. Ponieważ testowanie w prawdziwym świecie jest drogie, skomplikowane i najprawdopodobniej nielegalne - wirtualne środowisko będzie użyte. Wybór jest bardzo duży: [Carla](http://carla.org/), [AirSim](https://github.com/Microsoft/AirSim), albo dowolna inna gra samochodowa ze wspaciem dla programistów, np. [GTAV](https://www.rockstargames.com/V/) wraz z [ScriptHook](http://www.dev-c.com/gtav/scripthookv/) albo [Live for speed](https://www.lfs.net/).

Ponieważ celem tego wpisu jest skupienie się na autonomicznym prowadzeniu, oczywiste części implementacji są pominięte (Pobieranie widoku oraz danych z symulatora jak i przesyłanie sterowania). Przykładowa implementacja znajduje się tutaj: [AutoCruise](https://github.com/Soolek/AutoCruise/tree/master/AutoCruise).

Uproszczony algorytm prowadzenia używa trzy algorytmy wizyjne korzystające z siebie po kolei: Perspektywa, Sobel i Przesuwane okno.

## Perspektywa

Pierwszym użytym algorytmem wizyjnym jest Perspektywa. Tworzy on widok z góry samochodu na podstawie widoku z oczu kierowcy. Dzięki temu przekształceniu jest znacznie łatwiej znaleźć równoległe granice drogi niż gdyby zbiegały one do jednego punktu.

Transformacja perspektywy jest transformacją w trzech wymiarach, w ten sposób że dolna część obrazu będzie oddalona a górna przybliżona.

![](/assets/images/posts/autonomous_driving_using_three_simple_vision_algorithms/perspective.gif)

Taka transformacja może zostać stworzona manualnie, albo przy pomocy funkcji [FindHomography()](https://docs.opencv.org/3.4.1/d9/dab/tutorial_homography.html) z biblioteki opencv. Przy zastosowaniu drugiego podejścia, dolna część obrazu zostanie ściśnięta aby skontrować widok perspektywiczny projekcji świata trójwymiarowego na dwuwymiarowy ekran:

![](/assets/images/posts/autonomous_driving_using_three_simple_vision_algorithms/perspective1.jpg)
![](/assets/images/posts/autonomous_driving_using_three_simple_vision_algorithms/perspective2.jpg)

Posiadając macierz przekształcenia, nowa pozycja każdego piksela z obrazu źródłowego może zostać obliczona:

![](/assets/images/posts/autonomous_driving_using_three_simple_vision_algorithms/perspective_matrix1.jpg)
![](/assets/images/posts/autonomous_driving_using_three_simple_vision_algorithms/perspective_matrix2.jpg)

...alternatywnie można użyć funkcji [WarpPerspective()](https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html) aby uzyskać przekształcony obraz

## Sobel

Obraz przekształcony perspektywą jest przekazywany do następnego algorytmu wykrywającego krawędzie: Sobel. Jego zadaniem jest zaznaczenie krawędzi obrazu które powinny być "interesujące i ważne" dla algorytmu sterowania. Sobel zaznacza krawędzie obrazu które się odznaczają w osi X w porównaniu do tła.

W celu przybliżenia jego działania, uwaga będzie skupiona na małym wycinku obrazu, gdzie widoczny jest pas oddzielający pas drogowy od pobocza. Obraz jest czarnobiały i reprezentowany na 8 bitach (w przedziale od 0 do 255).

![](/assets/images/posts/autonomous_driving_using_three_simple_vision_algorithms/sobel1.png)

Na zaznaczonym wycinku widać jak wartości rosną z 119 do 149 z lewej do prawej. Algorytm Sobel zamienia obraz źródłowy poprzez porównywanie każdego piksela do jego prawego sąsiada. Wynik tego porównania jest zapisywany ponownie na obrazie. Ponieważ porównanie może być ujemne jak i dodatnie, do wyniku dodawane jest 128 (odpowiednik idealnie szarego koloru) dzięki czemu porównanie pozytywne będzie widoczne jako jasny piksel, a negatywne jako ciemny.

![](/assets/images/posts/autonomous_driving_using_three_simple_vision_algorithms/sobel2.png)

W celu zwiększenia efektywności algorytmu Sobel, dodatkowy parametr został użyty: kernel. Definiuje on długość boku kwadratu użytego do obliczenia wartości sąsiadujących pikseli podczas porównywania zestawu pikseli do sąsiadujących pikseli. Dzięki takiej operacji obraz wyjściowy zawiera mniej szumu a więcej krawędzi które się odznaczają.

![](/assets/images/posts/autonomous_driving_using_three_simple_vision_algorithms/sobel3.png)

## Przesuwane okno

Ostatnim użytym algorytmem wizyjnym jest Przesuwane okno. Jego zadaniem jest śledzenie krawędzi obrazu, które są najprawdopodobniej krawędziami jezdni. Ten algorytm jest całkiem odporny na zaszumione obrazy, ale mniej dokładny - wystarczająco jednak efektywny do zastosowania w prostym algorytmie autonomicznego prowadzenia.

Pierwszym krokiem w algorytmie Przesuwanego okna jest ustawienie okna poszukiwań (o konfigurowalnej wielkości) w miejscu gdzie krawędź drogi powinna być obecna: Przedni róg auta. Następnie okno poszukiwań jest przesuwane ku górze obrazu po najbardziej odznaczającej się krawędzi. Za każdym razem jak okno jest przesunięte ku górze (o jego wysokość), nowa pozycja w poziomie jest obliczona przy użyciu średniej ważonej wartościami pikseli: Im więcej pikseli (o większej wartości) jest znalezionych na danej pozycji poziomej w oknie poszukiwań, tym bardziej nowa pozycja okna poszukiwań będzie bliżej tej pozycji (w osi X). Te kroki są powtarzane aż okno poszukiwań wyjdzie poza granice obrazu.

![](/assets/images/posts/autonomous_driving_using_three_simple_vision_algorithms/sliding_window.gif)

Po tym, jak lewa oraz prawa strona Przesuwanego okna dojdzie do końca granicy obrazu, dwie ścieżki reprezentujące krawędzie drogi zostały stworzone.

## Algorytm prowadzenia

Wraz z wyznaczeniem (prawdopodobnych) krawędzi drogi, prymitywny algorytm kierowania jest użyty: Utrzymuj około 50km/h wraz z zwalnianiem propocjonalnie do skrętu zakrętów oraz steruj tak aby utrzymać auto pomiędzy krawędziami jezdni. Kierowanie pomiędzy krawędziami jezdni to nie tylko utrzymywanie auta pomiędzy nimi ale także utrzymywanie jego równolegle do krawędzi. Stosunek tych dwóch zachowań wymaga dużo eksperymentów jeśli jest dokonywane manualnie. Aby uzyskać jak najwięcej z tego podejścia, uczenie maszynowe powinno zostać użyte z wykorzystaniem nagranych danych prowadzenia manualnego. W ten sposób algorytm autonomicznego prowadzenia powinień być w stanie kopiować zachowanie nagranego manualnego prowadzenia, ale ten temat zostanie przedstawiony w przyszłym wpisie bloga.

Ostatecznie, całość przedstawia się następująco:

[![](/assets/images/posts/autonomous_driving_using_three_simple_vision_algorithms/yt_link.jpg)](https://youtu.be/jKJhDTwFSVY?t=37)