import { useState } from 'react';
import api from './api';
import { useNavigate } from 'react-router-dom';
import toast, { Toaster } from 'react-hot-toast';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            // Backendga so'rov
            const response = await api.post('/api/token/', { username, password });
            
            // Tokenlarni saqlash
            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);
            
            toast.success("Muvaffaqiyatli kirdingiz!");
            
            // Dashboardga yo'naltirish (hozircha yo'q, lekin qo'shamiz)
            setTimeout(() => navigate('/dashboard'), 1000);
            
        } catch (error) {
            toast.error("Login yoki parol xato!");
            console.error(error);
        }
    };

    return (
        <div className="flex items-center justify-center h-screen bg-gray-900">
            <Toaster />
            <div className="w-full max-w-md p-8 space-y-6 bg-gray-800 rounded-lg shadow-lg">
                <h2 className="text-3xl font-bold text-center text-white">DevOps Dashboard</h2>
                <form onSubmit={handleLogin} className="space-y-4">
                    <div>
                        <label className="block text-gray-300">Username</label>
                        <input 
                            type="text" 
                            className="w-full px-4 py-2 mt-2 bg-gray-700 text-white rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                    </div>
                    <div>
                        <label className="block text-gray-300">Password</label>
                        <input 
                            type="password" 
                            className="w-full px-4 py-2 mt-2 bg-gray-700 text-white rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    <button type="submit" className="w-full py-2 font-bold text-white bg-blue-600 rounded hover:bg-blue-500">
                        KIRISH
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Login;