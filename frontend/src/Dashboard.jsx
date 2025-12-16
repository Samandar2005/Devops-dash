import { useEffect, useState } from 'react';
import api from './api';
import { useNavigate } from 'react-router-dom';
import toast, { Toaster } from 'react-hot-toast';
import { FaPlay, FaStop, FaTrash, FaTerminal, FaSync, FaSignOutAlt } from 'react-icons/fa';

const Dashboard = () => {
    const [containers, setContainers] = useState([]);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    // 1. Konteynerlarni Backenddan yuklash
    const fetchContainers = async () => {
        setLoading(true);
        try {
            const res = await api.get('/api/containers/');
            setContainers(res.data);
        } catch (error) {
            console.error(error);
            if (error.response && error.response.status === 401) {
                toast.error("Sessiya vaqti tugadi. Qaytadan kiring.");
                localStorage.clear();
                navigate('/login');
            } else {
                toast.error("Ma'lumotlarni yuklashda xatolik!");
            }
        } finally {
            setLoading(false);
        }
    };

    // Sahifa ochilishi bilan yuklash
    useEffect(() => {
        fetchContainers();
    }, []);

    // 2. Start / Stop funksiyasi
    const toggleStatus = async (id, currentStatus) => {
        const action = currentStatus === 'running' ? 'stop' : 'start';
        // Loading toast chiqarish
        const toastId = toast.loading(`Konteyner ${action} qilinmoqda...`);

        try {
            await api.post(`/api/containers/${id}/${action}/`);
            toast.success(`Muvaffaqiyatli: ${action}`, { id: toastId });
            fetchContainers(); // Ro'yxatni yangilash
        } catch (error) {
            toast.error("Xatolik yuz berdi!", { id: toastId });
        }
    };

    // 3. O'chirish (Delete) funksiyasi
    const deleteContainer = async (id) => {
        if (!window.confirm("Bu konteynerni o'chirib yuborishga aminmisiz?")) return;
        
        const toastId = toast.loading("O'chirilmoqda...");
        try {
            await api.delete(`/api/containers/${id}/`);
            toast.success("Konteyner o'chirildi", { id: toastId });
            fetchContainers();
        } catch (error) {
            toast.error("O'chirishda xatolik", { id: toastId });
        }
    };

    // 4. Logout funksiyasi
    const handleLogout = () => {
        localStorage.clear();
        navigate('/login');
    };

    return (
        <div className="min-h-screen bg-gray-900 text-gray-100 font-sans">
            <Toaster position="top-right" />
            
            {/* Navbar qismi */}
            <nav className="bg-gray-800 border-b border-gray-700 px-6 py-4 flex justify-between items-center shadow-md">
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-blue-500 animate-pulse"></div>
                    <h1 className="text-2xl font-bold tracking-wide text-white">DevOps<span className="text-blue-500">Dash</span></h1>
                </div>
                
                <div className="flex gap-3">
                     <button 
                        onClick={fetchContainers}
                        disabled={loading}
                        className="flex items-center gap-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-all text-sm font-medium"
                    >
                        <FaSync className={loading ? "animate-spin" : ""} /> Yangilash
                    </button>
                    <button 
                        onClick={handleLogout}
                        className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition-all text-sm font-medium shadow-lg shadow-red-900/20"
                    >
                        <FaSignOutAlt /> Chiqish
                    </button>
                </div>
            </nav>

            {/* Asosiy Kontent */}
            <main className="max-w-7xl mx-auto p-6 mt-6">
                <div className="bg-gray-800 rounded-xl shadow-xl overflow-hidden border border-gray-700">
                    <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr className="bg-gray-750 border-b border-gray-700 text-gray-400 text-xs uppercase tracking-wider">
                                    <th className="p-5 font-semibold">Name</th>
                                    <th className="p-5 font-semibold">Image</th>
                                    <th className="p-5 font-semibold">Status</th>
                                    <th className="p-5 font-semibold">Ports (Int:Ext)</th>
                                    <th className="p-5 font-semibold text-center">Boshqaruv</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-700">
                                {containers.length === 0 && !loading ? (
                                    <tr>
                                        <td colSpan="5" className="p-10 text-center text-gray-500">
                                            <p className="text-lg">Hozircha konteynerlar yo'q 🤷‍♂️</p>
                                            <p className="text-sm mt-2">Swagger orqali yangi konteyner qo'shib ko'ring.</p>
                                        </td>
                                    </tr>
                                ) : (
                                    containers.map((c) => (
                                        <tr key={c.id} className="hover:bg-gray-700/50 transition duration-150">
                                            <td className="p-5 font-medium text-white">{c.name}</td>
                                            <td className="p-5">
                                                <span className="px-2 py-1 bg-blue-900/30 text-blue-400 rounded text-xs font-mono border border-blue-900/50">
                                                    {c.image}
                                                </span>
                                            </td>
                                            <td className="p-5">
                                                <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold ${
                                                    c.status === 'running' ? 'bg-green-900/30 text-green-400 border border-green-900/50' : 
                                                    c.status === 'exited' || c.status === 'stopped' ? 'bg-red-900/30 text-red-400 border border-red-900/50' : 
                                                    'bg-yellow-900/30 text-yellow-400 border border-yellow-900/50'
                                                }`}>
                                                    <span className={`w-1.5 h-1.5 rounded-full ${c.status === 'running' ? 'bg-green-400' : 'bg-current'}`}></span>
                                                    {c.status.toUpperCase()}
                                                </span>
                                            </td>
                                            <td className="p-5 text-gray-400 font-mono text-sm">
                                                {c.container_port} <span className="text-gray-600">→</span> {c.host_port}
                                            </td>
                                            <td className="p-5">
                                                <div className="flex justify-center items-center gap-3">
                                                    {/* Start/Stop */}
                                                    <button 
                                                        onClick={() => toggleStatus(c.id, c.status)}
                                                        className={`p-2 rounded-lg transition-colors shadow-lg ${
                                                            c.status === 'running' 
                                                            ? 'bg-yellow-600/20 text-yellow-500 hover:bg-yellow-600 hover:text-white' 
                                                            : 'bg-green-600/20 text-green-500 hover:bg-green-600 hover:text-white'
                                                        }`}
                                                        title={c.status === 'running' ? "To'xtatish" : "Ishga tushirish"}
                                                    >
                                                        {c.status === 'running' ? <FaStop size={14} /> : <FaPlay size={14} />}
                                                    </button>

                                                    {/* Terminal (Hozircha ishlamaydi, 10-qadamda ulaymiz) */}
                                                    <button 
                                                        className="p-2 bg-gray-700 text-gray-400 rounded-lg hover:bg-gray-600 hover:text-white transition-colors cursor-not-allowed opacity-50"
                                                        title="Terminal (Tez orada)"
                                                    >
                                                        <FaTerminal size={14} />
                                                    </button>

                                                    {/* Delete */}
                                                    <button 
                                                        onClick={() => deleteContainer(c.id)}
                                                        className="p-2 bg-red-600/20 text-red-500 rounded-lg hover:bg-red-600 hover:text-white transition-colors shadow-lg"
                                                        title="O'chirish"
                                                    >
                                                        <FaTrash size={14} />
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default Dashboard;