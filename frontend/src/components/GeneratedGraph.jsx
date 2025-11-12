export default function GeneratedChart({ data }) {
    // Limit the dataset to the first 50 entries for performance.
    const filteredData = data.slice(0, 50);
    
    // Prepare data for the ranking metric (e.g., average lap time in milliseconds).
    const processedData = filteredData.map(entry => ({
        name: entry.name,
        averageLapTime: entry.laptime_min * 60000 + entry.laptime_sec * 1000 + entry.laptime_thousandth
    }));

    return (
        <ResponsiveContainer width="100%" height={400}>
            <BarChart data={processedData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="averageLapTime" fill="#82ca9d" />
            </BarChart>
        </ResponsiveContainer>
    );
}