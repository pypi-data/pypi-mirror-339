# RadarChart
A Python library for creating customizable radar charts (spider plots).

## How to use it

**Step 1**: Import the `radarplot` library.

```py
import radarchart
```

**Step 2**: Prepare the dataframe.

```py
df = radarchart.example_dataframe()
df
```

![example-df](https://github.com/user-attachments/assets/71fff230-e6b9-453a-8ab0-ea4ed634bfc1)

**Step 3**: Plot the chart.

```py
radarchart.plot(df, norm_max=True)
```

![example-plot](https://github.com/user-attachments/assets/32ff7a41-f1c7-47ec-9927-087bf0dba818)
