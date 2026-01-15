export default function GeneratedChart({ data }) {
  // If the question is regarding the top 10 athletes based on their achievements and legacy, no specific chart is requested.
  // However, an alternative approach to show performance can be inferred based on the data structure.
  // For this exercise, let's assume we're required to report a bar chart comparing their fastest lap times
  
  // We first calculate the full lap time in seconds for each racer
  const calculatedLapTimes = data.map((entry) => ({
    ...entry,
    fullLapTime: entry.laptime_min * 60 + entry.laptime_sec + entry.laptime_thousandth / 1000,
  }));

  // Sort the racers based on their full lap time in ascending order, which means faster times will be first
  const sortedLapTimes = calculatedLapTimes.sort((a, b) => a.fullLapTime - b.fullLapTime);

  // We'll only take the first 10 for visual clarity
  const top10Racers = sortedLapTimes.slice(0, 10);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={top10Racers}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis label={{ value: 'Lap Time (s)', angle: -90, position: 'insideLeft' }} />
        <Tooltip />
        <Legend />
        <Bar dataKey="fullLapTime" fill="#8884d8" />
      </BarChart>
    </ResponsiveContainer>
  );
}