"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

      // Send JSON body with email and password (NOT form data)
      const response = await fetch(`${API_URL}/api/v1/users/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",  // Changed from form-urlencoded
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Login failed");
      }

      const data = await response.json();

      // Store token and username in localStorage
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("username", email.split("@")[0]); // Store username from email

      // Redirect to home page
      router.push("/");
    } catch (err: any) {
      setError(err.message || "An error occurred during login");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <div className="w-full max-w-md p-8 space-y-6 bg-gray-800 rounded-lg shadow-xl">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-3xl font-bold text-white mb-2">IntelliAgent</h1>
          <p className="text-gray-400">Sign in to your account</p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="p-3 bg-red-900 border border-red-700 rounded-md">
            <p className="text-red-200 text-sm">{error}</p>
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
              Email Address
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="mohit@example.com"
              className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="••••••••"
              className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-800"
          >
            {isLoading ? "Signing in..." : "Log In"}
          </button>
        </form>

        {/* Helper Text */}
        <div className="text-center text-sm text-gray-400">
          <p>Use your existing credentials</p>
          <p className="mt-1 text-gray-500">Default: mohit@example.com</p>
        </div>

        {/* Back to Home Link */}
        <div className="text-center">
          <button
            onClick={() => router.push("/")}
            className="text-blue-400 hover:text-blue-300 text-sm transition-colors"
          >
            ← Back to Home
          </button>
        </div>
      </div>
    </div>
  );
}
