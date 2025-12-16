import { useEffect, useState, useRef } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { FaTimes, FaChartArea } from 'react-icons/fa';

const StatsModal = ({ container, onClose }) => {
    const [data, setData] = useState([]);
    const ws = useRef(null);

    useEffect(() => {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//localhost:8000/ws/containers/${container.id}/stats/`;
        
        ws.current = new WebSocket(wsUrl);

        ws.current.onmessage = (event) => {
            const stat = JSON.parse(event.data);
            
            // Grafik uchun vaqt belgisini qo'shamiz
            const now = new Date().toLocaleTimeString();
            
            setData(prev => {
                const newData = [...prev, { time: now, ...stat }];
                // Faqat oxirgi 20 ta nuqtani saqlaymiz (grafik to'lib ketmasligi uchun)
                return newData.slice(-20);
            });
        };

        return () => {
            if (ws.current) ws.current.close();
        };
    }, [container]);

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
            <div className="w-full max-w-4xl bg-gray-900 rounded-xl shadow-2xl border border-gray-700 p-6">
                
                {/* Header */}
                <div className="flex justify-between items-center mb-6">
                    <div className="flex items-center gap-3">
                        <FaChartArea className="text-purple-400 text-2xl" />
                        <div>
                            <h2 className="text-xl font-bold text-white">Monitoring: {container.name}</h2>
                            <p className="text-sm text-gray-400">Real-time CPU & Memory Usage</p>
                        </div>
                    </div>
                    <button onClick={onClose} className="text-gray-400 hover:text-white"><FaTimes size={24} /></button>
                </div>

                {/* Grafiklar */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 h-64">
                    
                    {/* CPU Chart */}
                    <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
                        <h3 className="text-sm font-bold text-gray-300 mb-2">CPU Usage (%)</h3>
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={data}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                                <XAxis dataKey="time" hide />
                                <YAxis domain={[0, 100]} stroke="#9ca3af" />
                                <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} />
                                <Area type="monotone" dataKey="cpu" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.3} isAnimationActive={false} />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>

                    {/* Memory Chart */}
                    <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
                        <h3 className="text-sm font-bold text-gray-300 mb-2">Memory Usage (MB)</h3>
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={data}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                                <XAxis dataKey="time" hide />
                                <YAxis stroke="#9ca3af" />
                                <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} />
                                <Area type="monotone" dataKey="memory" stroke="#10b981" fill="#10b981" fillOpacity={0.3} isAnimationActive={false} />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>

                </div>
            </div>
        </div>
    );
};

export default StatsModal;

