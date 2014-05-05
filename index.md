Boston Marathon Raw Data and Visualizations
==================================================

This repository has two parts:

* all of the data on Boston Marathon finishers available from 2001-2014
* Visualizations of that data

Visualizations
--------------------------------------

* by @tmcw
    * [heatmap of finish times](http://bl.ocks.org/tmcw/11376778/d39142fc73e14097fad33d50e75366d197b6c2a3)
    * [which years did people PR?](http://bl.ocks.org/tmcw/raw/11385055/)
* by me
    * [An interactive map of the states and provinces of the runners](https://billmill.org/bostonmarathon/maps/)
    * [An interactive map of the countries of origin of the runenrs](https://billmill.org/bostonmarathon/maps/world.html)
    * A violin plot of finish times 2001-2014: ![Violin plot of finish times 2001-2014](https://raw.githubusercontent.com/llimllib/bostonmarathon/master/images/times_violin.png)
    * A histogram of finishers, by gender and age: ![histogram of finishers by gender and age](https://pbs.twimg.com/media/BmH86ZHCQAEay54.png:large)

The Data
--------------------------------------

Look in the [results directory](https://github.com/llimllib/bostonmarathon/tree/master/results) for the data.
Do something interesting with it, and make sure you [tell me about it](bill.mill@gmail.com)!

Format
--------------------------------------

There are (unfortunately) two different data formats. 2013 and 2014 have more detailed
timing data, with splits at 10k, 20k, 25k, half, 30k, 35k, and 40k.

Pre-2013, the data has only the finishing time, but adds the person's standing in their
division, gender, and overall.

Caveats
--------------------------------------

* The data includes wheelchair racers but not hand cyclists or other special groups...
if you're interested in that data please submit a pull request!
* The data does not include runners who did not finish. There's nothing I can
do about that, as far as I can tell that data is unavailable from baa.org
* The data is certainly missing a few people, but it ought to contain the large
majority of runners who finished from each year.
* The code is ugly. This is just about grinding the results out!

License
--------------------------------------

MIT License. Use it as you want to, don't feel obligated to give me credit. It's the BAA's
data anyway. (Thanks for organizing, BAA)

Downloading The Data
--------------------------------------

I... already did that for you. Why do you want to do that?

Anyway, if you do, you'll want to run `python multidl.py {year}`

Viewing the notebook
--------------------------------------

1. Install the prerequisites: `pip install < requirements.txt`
2. Start the notebook: `make notebook`
3. Play!
