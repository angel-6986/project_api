import { useState, useEffect } from 'react'

function App() {
  const [sensorData, setSensorData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch data from your live Render API
    //Added fetch logic to reusable function
    const fetchSensorData = () => {
      fetch("https://project-api-am.onrender.com/api/v1/sensors/data")
        .then(response => response.json())
        .then(data => {
          // Pull array of records
          let records = [];
          if(data && Array.isArray(data.data)) {
            records = data.data;
          } else if( Array.isArray(data) ) {
            records = data;
          }

          //Sort by timestamp, newest first, then grab top 12
          const sortedData = records.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
          const top12Data = sortedData.slice(0, 12);

          setSensorData(top12Data);
          setLoading(false);
        })
        .catch(error => console.error("Error fetching data:", error));
    };

    fetchSensorData();

    // poll every 5 seconds for new data
    const interval = setInterval(fetchSensorData, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8 font-sans">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-blue-400 border-b border-gray-700 pb-4">
          IoT Sensor Dashboard
        </h1>
        
        {loading ? (
          <p className="text-gray-400 animate-pulse text-lg">Loading secure data from cloud...</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {sensorData.map((reading) => (
              <div 
                key={reading.id} 
                className="bg-gray-800 p-6 rounded-xl shadow-lg border border-gray-700 hover:border-blue-500 transition-colors"
              >
                <h2 className="text-xl font-semibold mb-2 text-gray-300">
                  {reading.sensor_id}
                </h2>
                
                {/* Changes color if temperature goes above 30 degrees! */}
                <div className={`text-5xl font-bold mb-4 ${reading.temperature > 30 ? 'text-red-400' : 'text-emerald-400'}`}>
                  {reading.temperature}°C
                </div>
                
                <div className="flex justify-between text-xs text-gray-500 mt-4 pt-4 border-t border-gray-700">
                  <span className="uppercase tracking-wider">Status: {reading.status}</span>
                  <span>{new Date(reading.timestamp).toLocaleTimeString()}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default App