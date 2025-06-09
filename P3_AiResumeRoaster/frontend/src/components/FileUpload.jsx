import { useState, useRef, useEffect } from 'react';
import { uploadFile, getFileById } from '../api/fileApi';
import { v4 as uuidv4 } from 'uuid';

export default function ChatBotUI() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const addMessage = (from, content, type = 'text') => {
    const message = { id: uuidv4(), from, content, type };
    setMessages((prev) => [...prev, message]);
    return message.id;
  };

  const updateMessage = (id, newContent) => {
    setMessages((prev) =>
      prev.map((msg) => (msg.id === id ? { ...msg, content: newContent } : msg))
    );
  };

  const cleanResult = (text) =>
    text.replace(/\*{2,}/g, '').replace(/\n{3,}/g, '\n\n');

  const trackParsing = async (fileId, statusId) => {
    updateMessage(statusId, '🔄 Parsing your resume...');

    for (let i = 0; i < 30; i++) {
      const data = await getFileById(fileId);
      console.log('Parsing check:', data);

      if (data.status === 'Processed!' && data.result) {
        updateMessage(statusId, '✅ Parsing complete!');
        addBotMessage(`🔥 Roast Result:\n\n${cleanResult(data.result)}`);
        return;
      }

      await new Promise((res) => setTimeout(res, 2000));
    }

    updateMessage(statusId, '⚠️ Parsing timed out. Please try again later.');
  };

  const addBotMessage = (content, type = 'text') => addMessage('bot', content, type);
  const addUserMessage = (content, type = 'text') => addMessage('user', content, type);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.type !== 'application/pdf') {
      addBotMessage('❌ Only PDF files are allowed.');
      return;
    }

    addUserMessage(`📎 ${file.name}`, 'file');
    setIsProcessing(true);

    try {
      const { file_id } = await uploadFile(file);
      addBotMessage(`✅ Resume uploaded. File ID: ${file_id}`);
      const statusId = addBotMessage('🔄 Parsing your resume...');
      await trackParsing(file_id, statusId);
    } catch (err) {
      addBotMessage(`❌ Upload failed: ${err.message}`);
    }

    setIsProcessing(false);
  };

  const handleGetById = async () => {
    if (!input.trim()) return;

    addUserMessage(input);
    setIsProcessing(true);

    try {
      const statusId = addBotMessage('🔄 Parsing your resume...');
      await trackParsing(input.trim(), statusId);
    } catch {
      addBotMessage('❌ Could not retrieve result. Check the File ID and try again.');
    }

    setInput('');
    setIsProcessing(false);
  };

  return (
    <div className="bg-zinc-900 text-white h-screen w-screen flex flex-col">
      {/* Header */}
      <header className="bg-zinc-800 p-5 text-2xl font-bold border-b border-zinc-700">
        AI Resume Roaster
      </header>

      {/* Chat Area */}
      <main className="flex-1 overflow-auto p-6 space-y-6">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.from === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className="flex items-end max-w-[80%] gap-2">
              {msg.from === 'bot' && (
                <img
                  src="https://api.dicebear.com/7.x/bottts/svg?seed=bot"
                  alt="bot"
                  className="w-8 h-8 rounded-full"
                />
              )}
              <div
                className={`p-4 text-sm md:text-base rounded-xl whitespace-pre-wrap leading-relaxed ${
                  msg.from === 'user'
                    ? 'bg-blue-600 text-white rounded-br-none shadow-lg'
                    : 'bg-zinc-700 text-white rounded-bl-none shadow-md'
                }`}
              >
                {msg.type === 'file' ? <strong>{msg.content}</strong> : msg.content}
              </div>
              {msg.from === 'user' && (
                <img
                  src="https://api.dicebear.com/7.x/personas/svg?seed=user"
                  alt="you"
                  className="w-8 h-8 rounded-full"
                />
              )}
            </div>
          </div>
        ))}
        <div ref={chatEndRef} />
      </main>

      {/* Input Panel */}
      <footer className="p-4 bg-zinc-800 border-t border-zinc-700 flex flex-col gap-3 md:flex-row md:items-center">
        {/* File Upload */}
        <label className={`w-full md:w-auto ${isProcessing ? 'opacity-40 pointer-events-none' : ''}`}>
          <input
            type="file"
            accept="application/pdf"
            onChange={handleFileUpload}
            className="hidden"
          />
          <div className="bg-blue-700 hover:bg-blue-800 text-white text-center py-2 px-4 rounded cursor-pointer transition">
            Upload Resume PDF
          </div>
        </label>

        {/* ID Search */}
        <div className="flex-1 flex gap-2 mt-2 md:mt-0">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isProcessing}
            placeholder="Search roast by File ID"
            className="flex-1 bg-zinc-700 text-white border border-zinc-600 px-3 py-2 rounded placeholder:text-zinc-400"
          />
          <button
            onClick={handleGetById}
            disabled={isProcessing}
            className={`px-4 py-2 rounded text-white transition ${
              isProcessing ? 'bg-zinc-600 cursor-not-allowed' : 'bg-green-600 hover:bg-green-700'
            }`}
          >
            Search
          </button>
        </div>
      </footer>
    </div>
  );
}
