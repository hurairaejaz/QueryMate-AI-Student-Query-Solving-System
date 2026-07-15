"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Mail, ArrowLeft, Send, Sparkles } from "lucide-react"; // Note: Needs 'lucide-react'

export default function ForgotPasswordPage() {
  const router = useRouter();

  const [identifier, setIdentifier] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setMessage("");
    setError("");

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/auth/forgot-password`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ identifier: identifier.trim() }),
        }
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Something went wrong");
      }

      setMessage(data.message || "OTP sent successfully");

      setTimeout(() => {
        router.push(
          `/reset-password?identifier=${encodeURIComponent(identifier.trim())}`
        );
      }, 1500);
    } catch (err) {
      setError(err.message || "Request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        
        {/* Back Button */}
        <button 
          onClick={() => router.push("/login")}
          className="group flex items-center text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors mb-6 ml-2"
        >
          <ArrowLeft size={18} className="mr-2 group-hover:-translate-x-1 transition-transform" />
          Back to Login
        </button>

        <div className="bg-white/80 backdrop-blur-md shadow-2xl rounded-3xl p-8 border border-white">
          {/* Header Section */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-14 h-14 bg-blue-100 text-blue-600 rounded-2xl mb-4">
              <Sparkles size={28} />
            </div>
            <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">
              Forgot Password?
            </h1>
            <p className="text-gray-500 mt-2 text-sm leading-relaxed">
              No worries! Enter your details below and we will send you a recovery OTP.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2 ml-1">
                Account Identifier
              </label>
              <div className="relative">
                <span className="absolute inset-y-0 left-0 pl-4 flex items-center text-gray-400">
                  <Mail size={18} />
                </span>
                <input
                  type="text"
                  placeholder="Email"
                  value={identifier}
                  onChange={(e) => setIdentifier(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all tracking-widest font-mono text-gray-900 font-semibold"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-4 rounded-2xl font-bold shadow-lg shadow-blue-200 transition-all active:scale-[0.98] disabled:opacity-70 flex justify-center items-center gap-2"
              disabled={loading}
            >
              {loading ? (
                <>
                  <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Sending...
                </>
              ) : (
                <>
                  <Send size={18} />
                  Send OTP
                </>
              )}
            </button>
          </form>

          {/* Success Notification */}
          {message && (
            <div className="mt-6 flex items-start gap-3 text-sm text-green-700 bg-green-50 border border-green-100 rounded-2xl p-4 animate-in fade-in slide-in-from-bottom-2">
              <div className="mt-0.5 h-2 w-2 bg-green-500 rounded-full shrink-0" />
              <p>{message}</p>
            </div>
          )}

          {/* Error Notification */}
          {error && (
            <div className="mt-6 flex items-start gap-3 text-sm text-red-700 bg-red-50 border border-red-100 rounded-2xl p-4 animate-in fade-in slide-in-from-bottom-2">
              <div className="mt-0.5 h-2 w-2 bg-red-500 rounded-full shrink-0" />
              <p>{error}</p>
            </div>
          )}
        </div>

        {/* Footer Info */}
        <div className="mt-8 text-center text-xs text-gray-400 uppercase tracking-widest font-semibold">
          QueryMate Security Protocol
        </div>
      </div>
    </div>
  );
}