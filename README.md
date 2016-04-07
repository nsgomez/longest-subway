# :train: longest-subway

A Python port of the JavaScript implementation used by WNYC to find the longest possible
continuous subway ride, using only free transfers and without repeating sections of track.
WNYC's challenge and results can be found [here](http://www.wnyc.org/story/search-longest-subway-ride/).
The original implementation can be found [here](http://project.wnyc.org/longest-subway/js/project.js).

## Running longest-subway

longest-subway will run entirely on stock Python and has been tested on an implementation of Python
2.7.10 — no dependencies, no kitchen sink! Since this program is a long-running graph traversal,
Pypy is recommended for better performance.

## Caveats

* WNYC's dataset has not been updated since July 2015 and therefore will not contain 34 St – Hudson
Yards or the upcoming 2nd Ave subway.
* Some terminals can be omitted due to being outclassed by another branch. For instance, Ozone Park
could be removed from calculations since the branches to the Rockaways would always supersede it
in length.
* The Staten Island Railway could be included due to a free transfer between it and the subway, but
WNYC omits it. It could plausibly be added to the dataset though.

## Full rules
From WNYC:
> * You can visit the same station as many times as you want.
> * You can make any station-to-station transfer that's marked as a free transfer on the subway map.
> * You can only ride each segment of the subway map once. A segment is basically anything that looks
> like one segment on the map. If any two lines go between station A and station B, and they don't diverge
> in between, that's one segment.
> * Once you've ridden a segment, you can't backtrack in the opposite direction. If you take the R north from
> Bay Ridge - 95 St, you can't take it back south.
> * Once you've taken the local, you can't take the express, and vice versa. If you take the E from 14 St to
> 34 St - Penn Station, you can't take the A between them later.
> * If there's more than one line, but they run side-by-side on the map, that's still one segment. The E, F,
> M and R between Jackson Heights and Forest Hills are one segment together. The B and Q from Prospect Park to
> Brighton Beach are one segment together.
> * We're choosing to ignore the existence of the West 8 St - NY Aquarium and Sutphin Blvd - Archer Av stations
> for simplicity's sake.
> * We assume that every standard line is running in its entirety, including the shuttles.
> * The AirTrain isn't a subway line. Don't be ridiculous.