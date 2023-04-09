import flo

if __name__ == "__main__":
    chart = flo.ChartData()
    print(chart.name)
    print(chart.date)
    for entry in chart:
        print(entry.json())
