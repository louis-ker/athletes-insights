export default function GeneratedChart({ data }) {
    // Preprocess data to ensure we handle a maximum of 50 rows and numeric conversions
    const processedData = data.slice(0, 50).map(item => ({
        name: item.name,
        laptime: parseFloat(item.laptime_min) * 60 + parseFloat(item.laptime_sec) + parseFloat(item.laptime_thousandth) / 1000,
        date: item.date
    }));

    return (
        <ResponsiveContainer width="100%" height={400}>
            <BarChart data={processedData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="laptime" fill="#8884d8" />
            </BarChart>
        </ResponsiveContainer>
    );
}