import { useEffect, useRef } from 'react';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css'; // Terminal CSS uslublari (Juda muhim!)
import { FaTimes, FaTerminal } from 'react-icons/fa';

const LogViewer = ({ container, onClose }) => {
    const terminalRef = useRef(null);
    const ws = useRef(null);

    useEffect(() => {
        // 1. Terminal obyektini yaratish
        const term = new Terminal({
            cursorBlink: true,
            convertEol: true, // \n ni \r\n ga aylantirish
            theme: {
                background: '#0f172a', // Tailwind slate-900
                foreground: '#00ff00', // Hacker Green
                cursor: '#ffffff',
                selectionBackground: '#ffffff33',
            },
            fontFamily: 'Menlo, Monaco, "Courier New", monospace',
            fontSize: 14,
            rows: 24,
        });

        // Addonni ulash
        const fitAddon = new FitAddon();
        term.loadAddon(fitAddon);

        // Terminalni HTML div ichiga chizish
        if (terminalRef.current) {
            term.open(terminalRef.current);
            fitAddon.fit();
        }

        // Boshlang'ich xabar
        term.write(`\x1b[34m[System]\x1b[0m Connecting to logs for container: \x1b[1;37m${container.name}\x1b[0m...\r\n`);

        // 2. WebSocket manzilini aniqlash
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        // Backend manzili localhost:8000 da
        const wsUrl = `${protocol}//localhost:8000/ws/containers/${container.id}/logs/`;

        // 3. Ulanish
        ws.current = new WebSocket(wsUrl);

        ws.current.onopen = () => {
            term.write('\r\n\x1b[32m>>> CONNECTION ESTABLISHED <<<\x1b[0m\r\n\r\n');
        };

        ws.current.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (data.log) {
                    term.write(data.log); // Loglarni yozish
                } else if (data.error) {
                    term.write(`\r\n\x1b[31m[Error] ${data.error}\x1b[0m\r\n`);
                }
            } catch (e) {
                console.error("Parse error:", e);
            }
        };

        ws.current.onclose = () => {
            term.write('\r\n\x1b[31m>>> CONNECTION CLOSED <<<\x1b[0m\r\n');
        };

        ws.current.onerror = (err) => {
            term.write('\r\n\x1b[31m[System] WebSocket Error occurred.\x1b[0m\r\n');
            console.error("WS Error:", err);
        };

        // 4. Tozalash (ComponentUnmount)
        return () => {
            if (ws.current) {
                ws.current.close();
            }
            term.dispose();
        };
    }, [container]); // container o'zgarsa qayta ishga tushadi

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
            <div className="w-full max-w-4xl bg-gray-900 rounded-xl shadow-2xl border border-gray-700 overflow-hidden flex flex-col h-[500px]">
                {/* Header */}
                <div className="flex justify-between items-center px-4 py-3 bg-gray-800 border-b border-gray-700">
                    <div className="flex items-center gap-2 text-gray-200">
                        <FaTerminal className="text-blue-400" />
                        <span className="font-mono text-sm font-bold">{container.name}</span>
                        <span className="text-xs px-2 py-0.5 rounded bg-gray-700 text-gray-400">{container.image}</span>
                    </div>
                    <button 
                        onClick={onClose}
                        className="p-1 hover:bg-gray-700 rounded text-gray-400 hover:text-white transition-colors"
                    >
                        <FaTimes size={18} />
                    </button>
                </div>

                {/* Terminal Body */}
                <div className="flex-1 p-2 bg-[#0f172a] overflow-hidden relative">
                    <div ref={terminalRef} className="w-full h-full" />
                </div>
            </div>
        </div>
    );
};

export default LogViewer;

