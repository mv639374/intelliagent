"use client";

import { useState, useRef, useEffect } from "react";

interface Message {
  role: "user" | "ai";
  content: string;
}

export function ChatStream() {
  const [history, setHistory] = useState<Message[]>([]);
  const [query, setQuery] = useState("");
  const [streamingResponse, setStreamingResponse] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [currentNode, setCurrentNode] = useState<string | null>(null);
  const [username, setUsername] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [history, streamingResponse]);

  // Check if user is logged in on component mount
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    const storedUsername = localStorage.getItem("username");
    if (token && storedUsername) {
      setUsername(storedUsername);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("username");
    setUsername(null);
    window.location.href = "/login";
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query || isStreaming) return;

    const token = localStorage.getItem("access_token");
    if (!token) {
      alert("Please login first");
      window.location.href = "/login";
      return;
    }

    setIsStreaming(true);
    setCurrentNode(null);
    setStreamingResponse("");
    setHistory((prev) => [...prev, { role: "user", content: query }]);

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
      
      // Generate a valid UUID for project_id
      const projectId = "00000000-0000-0000-0000-000000000000"; // Default UUID
      
      const response = await fetch(`${API_URL}/api/v1/chat/stream`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          query: query,
          project_id: projectId,  // Valid UUID format
          top_k: 10,
          rerank: false,
        }),
      });

      if (response.status === 401 || response.status === 403) {
        alert("Session expired. Please login again.");
        handleLogout();
        return;
      }

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Stream error:", errorText);
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      if (!response.body) return;

      const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
      let fullResponse = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const lines = value.split("\n\n").filter(Boolean);

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const jsonStr = line.substring(6);
            try {
              const event = JSON.parse(jsonStr);

              if (event.event === "on_chat_model_stream") {
                const token = event.data?.token || "";
                fullResponse += token;
                setStreamingResponse((prev) => prev + token);
              } else if (event.event === "on_chain_start") {
                setCurrentNode(event.data?.node || null);
              }
            } catch (error) {
              console.error("Failed to parse SSE event:", jsonStr, error);
            }
          }
        }
      }

      setHistory((prev) => [...prev, { role: "ai", content: fullResponse }]);
    } catch (error) {
      console.error("Streaming failed:", error);
      setHistory((prev) => [
        ...prev,
        { role: "ai", content: "Sorry, I encountered an error. Please try again." },
      ]);
    } finally {
      setIsStreaming(false);
      setCurrentNode(null);
      setStreamingResponse("");
      setQuery("");
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-white">
      {/* Header with Login/Logout Button */}
      <div className="flex justify-between items-center p-4 bg-gray-800 border-b border-gray-700">
        <h1 className="text-2xl font-bold">IntelliAgent Chat</h1>
        {username ? (
          <div className="flex items-center gap-4">
            <span className="text-green-400">👤 {username}</span>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-md text-sm"
            >
              Logout
            </button>
          </div>
        ) : (
          <button
            onClick={() => (window.location.href = "/login")}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-md text-sm"
          >
            Login
          </button>
        )}
      </div>

      {/* Chat History */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {history.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-3xl p-4 rounded-lg ${
                msg.role === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-700 text-gray-100"
              }`}
            >
              <div className="font-semibold mb-1">
                {msg.role === "user" ? "You" : "AI"}
              </div>
              <div className="whitespace-pre-wrap">{msg.content}</div>
            </div>
          </div>
        ))}

        {/* Streaming Response */}
        {streamingResponse && (
          <div className="flex justify-start">
            <div className="max-w-3xl p-4 rounded-lg bg-gray-700 text-gray-100">
              <div className="font-semibold mb-1">AI (streaming...)</div>
              <div className="whitespace-pre-wrap">{streamingResponse}</div>
            </div>
          </div>
        )}

        {/* Current Node Indicator */}
        {isStreaming && currentNode && (
          <div className="flex justify-center">
            <div className="px-4 py-2 bg-purple-600 rounded-full text-sm">
              ⚙️ Current Step: {currentNode}
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <form
        onSubmit={handleSubmit}
        className="p-4 bg-gray-800 border-t border-gray-700"
      >
        <div className="flex gap-2 max-w-4xl mx-auto">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question..."
            className="flex-grow bg-gray-700 text-white rounded-md p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isStreaming}
          />
          <button
            type="submit"
            disabled={isStreaming || !query}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-md font-semibold transition-colors"
          >
            {isStreaming ? "Sending..." : "Send"}
          </button>
        </div>
      </form>
    </div>
  );
}
