# Analysis of distribution of clicks from center of click location

## Recording mouse clicks
Run `record_clicks.py` to generate the sample of clicks. The first click records the center of the clicking region. The second click is the leftmost edge, third is the right most. Fourth click is the bottom, and the fifth click is the top of the region. Subsequent clicks are used to create the distribution. Then record points and then right click to save and exit.

## Analyse mouse clicks
Run `analyise_clicks.py` to calculate distribution parameters and display the following chart

## Distribution of clicks
![](image.png)
I have a bias of clicking high and to the left, so this will be included the interaction component

```
x mean: -9.981818181818182, x std: 8.404524558703558
y mean: 6.572727272727272, y std: 7.741809855241263
```