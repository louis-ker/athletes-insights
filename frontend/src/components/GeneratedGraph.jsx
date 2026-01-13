export default function GeneratedChart({ data }) {
    // In the context of measurable effects and future trends, it's likely we want
    // to compare the consistency of lap times between different countries 
    // or categories of racers. So we'll create a boxplot using these columns.
  
    const transformedData = data.map(item => ({
        countryCategory: `${item.country} (${item.category})`,
        laptime: item.laptime_min * 60000 + item.laptime_sec * 1000 + item.laptime_thousandth
    }));

    const countriesCategories = [...new Set(transformedData.map(item => item.countryCategory))];

    const dataForBoxPlot = countriesCategories.map(cc => {
      const times = transformedData.filter(d => d.countryCategory === cc).map(d => d.laptime);
      times.sort((a, b) => a - b);
      const min = Math.min(...times);
      const max = Math.max(...times);
      const median = times[Math.floor(times.length / 2)];
      const q1 = times[Math.floor(times.length / 4)];
      const q3 = times[Math.floor((3 * times.length) / 4)];
      return { countryCategory: cc, min, max, median, q1, q3 };
    });

    return (
        <ResponsiveContainer width="100%" height={400}>
            <ComposedChart layout="vertical" data={dataForBoxPlot} margin={{ top: 20, right: 30, bottom: 20, left: 100 }}>
                <XAxis type="number" />
                <YAxis type="category" dataKey="countryCategory" />
                <Tooltip />
                {dataForBoxPlot.map((entry, index) => (
                    <React.Fragment key={`whisker-${index}`}>
                        <Line type="monotone" dataKey="min" data={dataForBoxPlot} stroke="#000" strokeWidth={1} dot={false}/>
                        <Line type="monotone" dataKey="max" data={dataForBoxPlot} stroke="#000" strokeWidth={1} dot={false}/>
                        <Bar dataKey="q3" fill="#413ea0" />
                        <Bar dataKey="median" fill="#ff7300" />
                        <Bar dataKey="q1" fill="#8884d8" />
                    </React.Fragment>
                ))}
            </ComposedChart>
        </ResponsiveContainer>
    );
}