export default function GeneratedChart({ data }) {
  const processLapTime = (row) => {
    return row.laptime_min * 60000 + row.laptime_sec * 1000 + row.laptime_thousandth;
  };

  // Step 1: Calculate average lap times per racer
  const lapTimesByName = data.reduce((acc, curr) => {
    const lapTime = processLapTime(curr);
    if (!acc[curr.name]) {
      acc[curr.name] = { totalLapTime: 0, count: 0 };
    }
    acc[curr.name].totalLapTime += lapTime;
    acc[curr.name].count += 1;
    return acc;
  }, {});

  const averagedLapTimes = Object.entries(lapTimesByName).map(([name, { totalLapTime, count }]) => ({
    name,
    averageLapTime: totalLapTime / count,
  }));

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={averagedLapTimes}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="averageLapTime" fill="#8884d8" />
      </BarChart>
    </ResponsiveContainer>
  );
}